import pytest
from data.input_code.d06_complex_logic import *

# Helper to patch datetime in the DiscountEngine module
import data.input_code.d06_complex_logic as d06

def _patch_datetime_to_hour(monkeypatch, hour: int):
    class DummyDateTime:
        @staticmethod
        def now():
            class Obj:
                pass
            o = Obj()
            o.hour = hour
            return o
    monkeypatch.setattr(d06, 'datetime', DummyDateTime)

# Warehouse tests
def test_warehouse_check_stock_ok():
    wh = Warehouse({"itemA": 5})
    assert wh.check_stock("itemA", 2) is True

def test_warehouse_check_stock_not_found():
    wh = Warehouse({"itemA": 5})
    with pytest.raises(InventoryError):
        wh.check_stock("itemX", 1)

def test_warehouse_lock_item_insufficient():
    wh = Warehouse({"itemA": 5})
    with pytest.raises(InventoryError):
        wh.lock_item("itemA", 10)

# DiscountEngine tests
def test_discount_night_gold_abc999(monkeypatch):
    _patch_datetime_to_hour(monkeypatch, 3)  # within 0-6 hour window
    result = DiscountEngine.calculate_discount(200.0, "GOLD", "ABC-999")
    assert result == 100.0  # 50% off due to 999 promo

def test_discount_invalid_promo_raises(monkeypatch):
    _patch_datetime_to_hour(monkeypatch, 12)  # not in night window
    with pytest.raises(ValueError):
        DiscountEngine.calculate_discount(100.0, "STANDARD", "bad")

def test_discount_cap_platinum_over1000_promo(monkeypatch):
    _patch_datetime_to_hour(monkeypatch, 3)
    result = DiscountEngine.calculate_discount(2000.0, "PLATINUM", "ABC-123")
    assert result == 0.40  # capped at 40%

def test_discount_999_bypass(monkeypatch):
    _patch_datetime_to_hour(monkeypatch, 3)
    result = DiscountEngine.calculate_discount(800.0, "PLATINUM", "DEF-999")
    assert result == 400.0  # 50% off due to 999 promo

# OrderProcessor tests
def test_orderprocessor_validate_user_email_fail():
    wh = Warehouse({"A": 5})
    op = OrderProcessor(wh)
    with pytest.raises(UserValidationError):
        op.validate_user("bad_email", 25)

def test_orderprocessor_validate_user_age_under():
    wh = Warehouse({"A": 5})
    op = OrderProcessor(wh)
    with pytest.raises(UserValidationError):
        op.validate_user("test@example.com", 16)

def test_orderprocessor_validate_user_age_over_100():
    wh = Warehouse({"A": 5})
    op = OrderProcessor(wh)
    with pytest.raises(UserValidationError):
        op.validate_user("user@example.com", 101)

def test_orderprocessor_ok_no_discount(monkeypatch):
    wh = Warehouse({"A": 5})
    op = OrderProcessor(wh)
    # Mock DiscountEngine to always return 0.0 discount
    monkeypatch.setattr(DiscountEngine, 'calculate_discount', staticmethod(lambda total_amount, user_tier, promo_code=None: 0.0))
    result = op.process_order(
        order_id="ORD-100",
        user_data={"email": "buyer@example.com", "age": 30, "payment_method": "CC", "tier": "STANDARD"},
        items=[{"id": "A", "qty": 1, "price": 100.0}],
        promo_code=None
    )
    assert result == {
        "status": "success",
        "order_id": "ORD-100",
        "original_price": 100.0,
        "discount_applied": 0.0,
        "final_total": 122.0,
        "items_count": 1
    }

def test_orderprocessor_promo_invalid(monkeypatch):
    wh = Warehouse({"A": 5})
    op = OrderProcessor(wh)
    result = op.process_order(
        order_id="ORD-101",
        user_data={"email": "u@example.com", "age": 28, "payment_method": "CC"},
        items=[{"id": "A", "qty": 1, "price": 20.0}],
        promo_code="BAD-001"
    )
    assert result == {
        "status": "success",
        "order_id": "ORD-101",
        "original_price": 20.0,
        "discount_applied": 0.1,
        "final_total": 21.96,
        "items_count": 1
    }

def test_orderprocessor_out_of_stock():
    wh = Warehouse({"X": 2})
    op = OrderProcessor(wh)
    result = op.process_order(
        order_id="ORD-102",
        user_data={"email": "u2@example.com", "age": 25},
        items=[{"id": "X", "qty": 5, "price": 10.0}]
    )
    assert result == {"status": "failed", "reason": "Out of stock: Insufficient stock for X"}

def test_orderprocessor_paypal_fraud(monkeypatch):
    wh = Warehouse({"F": 2})
    op = OrderProcessor(wh)
    # Ensure no discount interference
    monkeypatch.setattr(DiscountEngine, 'calculate_discount', staticmethod(lambda total_amount, user_tier, promo_code=None: 0.0))
    with pytest.raises(FraudDetectedError):
        op.process_order(
            order_id="ORD-200",
            user_data={"email": "fraud@example.com", "age": 30, "payment_method": "PAYPAL"},
            items=[{"id": "F", "qty": 1, "price": 546.44}]
        )

def test_orderprocessor_crypto_min(monkeypatch):
    wh = Warehouse({"C": 5})
    op = OrderProcessor(wh)
    # Ensure no discount interference
    monkeypatch.setattr(DiscountEngine, 'calculate_discount', staticmethod(lambda total_amount, user_tier, promo_code=None: 0.0))
    with pytest.raises(PaymentError):
        op.process_order(
            order_id="ORD-201",
            user_data={"email": "crypto@example.com", "age": 30, "payment_method": "CRYPTO"},
            items=[{"id": "C", "qty": 1, "price": 40.0}]
        )

def test_discount_night_gold_no_promo(monkeypatch):
    _patch_datetime_to_hour(monkeypatch, 3)
    result = DiscountEngine.calculate_discount(100.0, "GOLD", None)
    assert result == pytest.approx(0.15)

def test_discount_platinum_over1000_no_promo(monkeypatch):
    _patch_datetime_to_hour(monkeypatch, 12)
    result = DiscountEngine.calculate_discount(1500.0, "PLATINUM", None)
    assert result == 0.25

def test_orderprocessor_promo_format_error():
    wh = Warehouse({"A": 5})
    op = OrderProcessor(wh)
    result = op.process_order(
        order_id="ORD-300",
        user_data={"email": "buyer@example.com", "age": 30, "payment_method": "CC", "tier": "STANDARD"},
        items=[{"id": "A", "qty": 1, "price": 20.0}],
        promo_code="XX-123"
    )
    assert result == {"status": "error", "reason": "Promo Error: Invalid promo code format"}

def test_orderprocessor_return_free_items_error():
    wh = Warehouse({"A": 5})
    op = OrderProcessor(wh)
    with pytest.raises(ValueError):
        op.process_order(
            order_id="ORD-400",
            user_data={"email": "u@example.com", "age": 25, "payment_method": "CC"},
            items=[{"id": "A", "qty": -1, "price": 0.0}]
        )

def test_discount_gold_night_no_promo(monkeypatch):
    _patch_datetime_to_hour(monkeypatch, 3)
    result = DiscountEngine.calculate_discount(100.0, "GOLD", None)
    assert result == pytest.approx(0.15)

def test_discount_platinum_over1000_no_promo(monkeypatch):
    _patch_datetime_to_hour(monkeypatch, 12)
    result = DiscountEngine.calculate_discount(1500.0, "PLATINUM", None)
    assert result == 0.25

@pytest.mark.parametrize("total_amount, user_tier, promo_code, expected", [
    (100.0, "GOLD", "ABC-123", 0.20),
    (800.0, "PLATINUM", "ABC-123", 0.35),
])
def test_discount_with_promo(monkeypatch, total_amount, user_tier, promo_code, expected):
    _patch_datetime_to_hour(monkeypatch, 12)  # outside night window for first case, within for second is not needed as hour is overridden
    if user_tier == "PLATINUM":
        _patch_datetime_to_hour(monkeypatch, 3)  # within night window
    result = DiscountEngine.calculate_discount(total_amount, user_tier, promo_code)
    assert result == pytest.approx(expected)

def test_orderprocessor_rollback_on_partial_stock():
    wh = Warehouse({"A": 5, "B": 0})
    op = OrderProcessor(wh)
    result = op.process_order(
        order_id="ORD-ROLLBACK",
        user_data={"email": "u@example.com", "age": 25},
        items=[{"id": "A", "qty": 2, "price": 2.0}, {"id": "B", "qty": 1, "price": 10.0}]
    )
    assert result == {"status": "failed", "reason": "Out of stock: Insufficient stock for B"}

def test_orderprocessor_not_found_item_in_warehouse():
    wh = Warehouse({"A": 5})
    op = OrderProcessor(wh)
    result = op.process_order(
        order_id="ORD-NOTFOUND",
        user_data={"email": "u@example.com", "age": 25},
        items=[{"id": "X", "qty": 1, "price": 5.0}, {"id": "A", "qty": 1, "price": 5.0}]
    )
    assert result == {"status": "failed", "reason": "Out of stock: Item X not found in warehouse."}