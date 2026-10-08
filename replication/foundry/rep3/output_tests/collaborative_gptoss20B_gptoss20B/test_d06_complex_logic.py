import pytest
from data.input_code.d06_complex_logic import *

# Warehouse tests
def test_Warehouse_check_stock_exists():
    w = Warehouse({"itemA": 5})
    assert w.check_stock("itemA", 5) is True

def test_Warehouse_check_stock_missing_item():
    w = Warehouse({"itemA": 1})
    with pytest.raises(InventoryError):
        w.check_stock("itemB", 1)

# DiscountEngine tests (deterministic by patching datetime)
class FakeDateTimeHour12:
    @staticmethod
    def now():
        class FakeNow:
            hour = 12
        return FakeNow()

def test_DiscountEngine_GOLD_no_promo(monkeypatch):
    monkeypatch.setattr('data.input_code.d06_complex_logic.datetime', FakeDateTimeHour12)
    assert DiscountEngine.calculate_discount(100.0, "GOLD", None) == 0.10

def test_DiscountEngine_PLATINUM_over_1000(monkeypatch):
    monkeypatch.setattr('data.input_code.d06_complex_logic.datetime', FakeDateTimeHour12)
    assert DiscountEngine.calculate_discount(1500.0, "PLATINUM", None) == 0.25

def test_DiscountEngine_PROMO_999():
    # Should return 50% off immediately, regardless of other discounts
    assert DiscountEngine.calculate_discount(200.0, "STANDARD", "ABC-999") == 100.0

def test_DiscountEngine_PROMO_VALID_NOT_999(monkeypatch):
    monkeypatch.setattr('data.input_code.d06_complex_logic.datetime', FakeDateTimeHour12)
    assert DiscountEngine.calculate_discount(200.0, "STANDARD", "ABC-123") == 0.10

def test_DiscountEngine_PROMO_INVALID():
    with pytest.raises(ValueError):
        DiscountEngine.calculate_discount(200.0, "STANDARD", "bad")

# OrderProcessor tests
def test_OrderProcessor_validate_user_invalid_email():
    w = Warehouse({"item": 1})
    op = OrderProcessor(w)
    with pytest.raises(UserValidationError):
        op.validate_user("not-an-email", 25)

def test_OrderProcessor_validate_user_underage():
    w = Warehouse({"item": 1})
    op = OrderProcessor(w)
    with pytest.raises(UserValidationError):
        op.validate_user("user@example.com", 16)

def test_OrderProcessor_validate_user_over_100():
    w = Warehouse({"item": 1})
    op = OrderProcessor(w)
    with pytest.raises(UserValidationError):
        op.validate_user("user@example.com", 101)

def test_OrderProcessor_happy_path():
    w = Warehouse({"item1": 5})
    op = OrderProcessor(w)
    result = op.process_order(
        order_id="ORD1",
        user_data={"email": "buyer@example.com", "age": 30},
        items=[{"id": "item1", "qty": 2, "price": 21.0}],
        promo_code=None
    )
    assert result == {
        "status": "success",
        "order_id": "ORD1",
        "original_price": 42.0,
        "discount_applied": 0.0,
        "final_total": 51.24,
        "items_count": 1
    }

def test_OrderProcessor_out_of_stock():
    w = Warehouse({"missing_item": 0})
    op = OrderProcessor(w)
    result = op.process_order(
        order_id="ORD2",
        user_data={"email": "buyer@example.com", "age": 28},
        items=[{"id": "missing_item", "qty": 1, "price": 10.0}],
        promo_code=None
    )
    assert result == {"status": "failed", "reason": "Out of stock: Insufficient stock for missing_item"}

def test_OrderProcessor_promo_invalid_in_order():
    w = Warehouse({"item1": 5})
    op = OrderProcessor(w)
    result = op.process_order(
        order_id="ORD3",
        user_data={"email": "buyer@example.com", "age": 25},
        items=[{"id": "item1", "qty": 1, "price": 50.0}],
        promo_code="badpromo"
    )
    assert result == {"status": "error", "reason": "Promo Error: Invalid promo code format"}

def test_OrderProcessor_crypto_min_amount():
    w = Warehouse({"item2": 5})
    op = OrderProcessor(w)
    with pytest.raises(PaymentError):
        op.process_order(
            order_id="ORD5",
            user_data={"email": "buyer@example.com", "age": 30, "payment_method": "CRYPTO"},
            items=[{"id": "item2", "qty": 1, "price": 10.0}],
            promo_code=None
        )

import pytest
from data.input_code.d06_complex_logic import *

class FakeDateTimeHour3:
    @staticmethod
    def now():
        class FakeNow:
            hour = 3
        return FakeNow()

def test_DiscountEngine_NIGHT_STANDARD(monkeypatch):
    monkeypatch.setattr('data.input_code.d06_complex_logic.datetime', FakeDateTimeHour3)
    assert DiscountEngine.calculate_discount(100.0, "STANDARD", None) == 0.05

def test_OrderProcessor_partial_rollback():
    w = Warehouse({"itemA": 2, "itemB": 0})
    op = OrderProcessor(w)
    result = op.process_order(
        order_id="ORD_ROLLBACK",
        user_data={"email": "buyer@example.com", "age": 30},
        items=[{"id": "itemA", "qty": 2, "price": 50.0}, {"id": "itemB", "qty": 1, "price": 60.0}],
        promo_code=None
    )
    assert result == {"status": "failed", "reason": "Out of stock: Insufficient stock for itemB"}

def test_OrderProcessor_paypal_fraud(monkeypatch):
    monkeypatch.setattr('data.input_code.d06_complex_logic.datetime', FakeDateTimeHour12)
    w = Warehouse({"itemF": 1})
    op = OrderProcessor(w)
    with pytest.raises(FraudDetectedError):
        op.process_order(
            order_id="ORD_PAYPAL_FRAUD",
            user_data={"email": "buyer@example.com", "age": 30, "payment_method": "PAYPAL"},
            items=[{"id": "itemF", "qty": 1, "price": 546.44}],
            promo_code=None
        )