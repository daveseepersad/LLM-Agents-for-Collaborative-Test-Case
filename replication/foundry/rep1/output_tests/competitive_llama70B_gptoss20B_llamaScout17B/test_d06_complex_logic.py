import pytest
from data.input_code.d06_complex_logic import *

# Tests for Warehouse stock management

def test_check_stock_ok():
    w = Warehouse({"item1": 10})
    assert w.check_stock("item1", 1) is True

def test_check_stock_item_not_found():
    w = Warehouse({"item1": 10})
    with pytest.raises(InventoryError):
        w.check_stock("item2", 1)

def test_lock_item_ok():
    w = Warehouse({"item1": 10})
    w.lock_item("item1", 1)
    assert w.check_stock("item1", 1) is True  # still enough stock remains

def test_lock_item_insufficient_stock():
    w = Warehouse({"item1": 10})
    with pytest.raises(InventoryError):
        w.lock_item("item1", 11)

def test_release_item_ok():
    w = Warehouse({"item1": 10})
    w.lock_item("item1", 1)
    w.release_item("item1", 1)
    assert w.check_stock("item1", 1) is True


# Helper classes to control datetime for DiscountEngine tests

class FakeDateTimeNoNight:
    @classmethod
    def now(cls):
        class M:
            hour = 14
        return M()

class FakeDateTimeNight:
    @classmethod
    def now(cls):
        class M:
            hour = 2
        return M()


# Tests for DiscountEngine
def test_discount_gold_no_night(monkeypatch):
    monkeypatch.setattr('data.input_code.d06_complex_logic.datetime', FakeDateTimeNoNight)
    assert DiscountEngine.calculate_discount(100.0, "GOLD") == 0.10

def test_discount_platinum_no_night(monkeypatch):
    monkeypatch.setattr('data.input_code.d06_complex_logic.datetime', FakeDateTimeNoNight)
    assert DiscountEngine.calculate_discount(100.0, "PLATINUM") == 0.20

def test_discount_platinum_with_night(monkeypatch):
    monkeypatch.setattr('data.input_code.d06_complex_logic.datetime', FakeDateTimeNight)
    assert DiscountEngine.calculate_discount(1000.0, "PLATINUM") == 0.25

def test_discount_invalid_promo_raises(monkeypatch):
    monkeypatch.setattr('data.input_code.d06_complex_logic.datetime', FakeDateTimeNoNight)
    with pytest.raises(ValueError):
        DiscountEngine.calculate_discount(100.0, "PLATINUM", promo_code="InvalidCode")

def test_discount_valid_promo(monkeypatch):
    monkeypatch.setattr('data.input_code.d06_complex_logic.datetime', FakeDateTimeNoNight)
    assert DiscountEngine.calculate_discount(100.0, "PLATINUM", promo_code="ABC-123") == pytest.approx(0.30)


# Tests for OrderProcessor and end-to-end flow

def test_validate_user_ok():
    w = Warehouse({"item1": 5})
    op = OrderProcessor(w)
    assert op.validate_user("test@example.com", 25) is None

def test_validate_user_invalid_email():
    w = Warehouse({"item1": 5})
    op = OrderProcessor(w)
    with pytest.raises(UserValidationError):
        op.validate_user("invalid_email", 25)

def test_validate_user_underage():
    w = Warehouse({"item1": 5})
    op = OrderProcessor(w)
    with pytest.raises(UserValidationError):
        op.validate_user("test@example.com", 17)


def test_process_order_success(monkeypatch):
    w = Warehouse({"item1": 10})
    op = OrderProcessor(w)
    # Freeze discount to a deterministic value
    monkeypatch.setattr(DiscountEngine, 'calculate_discount', staticmethod(lambda total_amount, user_tier, promo_code=None: 0.1))
    result = op.process_order(
        order_id="order1",
        user_data={"email": "test@example.com", "age": 25, "tier": "GOLD"},
        items=[{"id": "item1", "qty": 1, "price": 100.0}]
    )
    assert result["status"] == "success"
    assert result["order_id"] == "order1"
    assert result["original_price"] == 100.0
    assert result["discount_applied"] == 0.1
    assert result["items_count"] == 1
    assert pytest.approx(result["final_total"], 0.001) == 109.8  # 100 * 0.9 * 1.22
    

def test_process_order_promo_error(monkeypatch):
    w = Warehouse({"item1": 10})
    op = OrderProcessor(w)
    # Do not patch discount; invalid promo code should trigger ValueError inside DiscountEngine
    result = op.process_order(
        order_id="order2",
        user_data={"email": "test@example.com", "age": 25, "tier": "GOLD"},
        items=[{"id": "item1", "qty": 1, "price": 100.0}],
        promo_code="InvalidCode"
    )
    assert result["status"] == "error"
    assert "Promo Error" in result["reason"]

def test_missing_discount_nightowl(monkeypatch):
    # Night discount should apply when hour is between 0 and 6
    monkeypatch.setattr('data.input_code.d06_complex_logic.datetime', FakeDateTimeNight)
    assert DiscountEngine.calculate_discount(100.0, "STANDARD") == pytest.approx(0.05)

def test_missing_discount_platinum_high_amount(monkeypatch):
    # Platinum with high amount should include additional 0.05 discount when not night
    monkeypatch.setattr('data.input_code.d06_complex_logic.datetime', FakeDateTimeNoNight)
    assert DiscountEngine.calculate_discount(1001.0, "PLATINUM") == pytest.approx(0.25)

def test_missing_discount_promo_999(monkeypatch):
    # Promo code ABC-999 should trigger 50% discount regardless of other factors
    monkeypatch.setattr('data.input_code.d06_complex_logic.datetime', FakeDateTimeNoNight)
    assert DiscountEngine.calculate_discount(100.0, "STANDARD", promo_code="ABC-999") == pytest.approx(50.0)

def test_missing_validate_user_over_100():
    w = Warehouse({"item1": 5})
    op = OrderProcessor(w)
    with pytest.raises(UserValidationError):
        op.validate_user("test@example.com", 101)

def test_missing_process_order_division_by_zero():
    w = Warehouse({"item1": 5})
    op = OrderProcessor(w)
    with pytest.raises(ValueError):
        op.process_order(
            order_id="order1",
            user_data={"email": "test@example.com", "age": 25},
            items=[{"id": "item1", "qty": -1, "price": 0.0}]
        )

def test_missing_process_order_fraud_detected(monkeypatch):
    w = Warehouse({"item1": 1})
    op = OrderProcessor(w)
    monkeypatch.setattr(
        DiscountEngine,
        'calculate_discount',
        staticmethod(lambda total_amount, user_tier, promo_code=None: max(min(1 - 666.66/(total_amount*1.22), 0.40), 0.0))
    )
    with pytest.raises(FraudDetectedError):
        op.process_order(
            order_id="order1",
            user_data={"email": "test@example.com", "age": 25, "payment_method": "PAYPAL"},
            items=[{"id": "item1", "qty": 1, "price": 666.66}]
        )

def test_missing_process_order_min_crypto_amount(monkeypatch):
    w = Warehouse({"item1": 10})
    op = OrderProcessor(w)
    monkeypatch.setattr(DiscountEngine, 'calculate_discount', staticmethod(lambda total_amount, user_tier, promo_code=None: 0.40))
    with pytest.raises(PaymentError):
        op.process_order(
            order_id="order1",
            user_data={"email": "test@example.com", "age": 25, "payment_method": "CRYPTO"},
            items=[{"id": "item1", "qty": 1, "price": 49.99}]
        )

def test_release_item_zero_no_error():
    w = Warehouse({"item1": 5})
    # Should not raise any exception for releasing zero quantity
    w.release_item("item1", 0)


def test_lock_item_zero_no_error():
    w = Warehouse({"item1": 5})
    # Should not raise any exception for locking zero quantity
    w.lock_item("item1", 0)


def test_discount_no_discount(monkeypatch):
    import pytest

    class FakeDateTimeNoNight:
        @classmethod
        def now(cls):
            class M:
                hour = 14
            return M()

    monkeypatch.setattr('data.input_code.d06_complex_logic.datetime', FakeDateTimeNoNight)
    assert DiscountEngine.calculate_discount(100.0, "STANDARD") == pytest.approx(0.0)

def test_negative_price_process_order(monkeypatch):
    # Ensure deterministic non-night behavior
    monkeypatch.setattr('data.input_code.d06_complex_logic.datetime', FakeDateTimeNoNight)
    w = Warehouse({"item1": 5})
    op = OrderProcessor(w)
    result = op.process_order(
        order_id="order1",
        user_data={"email": "test@example.com", "age": 25},
        items=[{"id": "item1", "qty": 1, "price": -100.0}]
    )
    assert result["status"] == "success"
    assert result["final_total"] == pytest.approx(-122.0)


def test_zero_quantity_price_process_order(monkeypatch):
    # Ensure deterministic non-night behavior
    monkeypatch.setattr('data.input_code.d06_complex_logic.datetime', FakeDateTimeNoNight)
    w = Warehouse({"item1": 5})
    op = OrderProcessor(w)
    result = op.process_order(
        order_id="order1",
        user_data={"email": "test@example.com", "age": 25},
        items=[{"id": "item1", "qty": 0, "price": 100.0}]
    )
    assert result["status"] == "success"
    assert result["original_price"] == 0.0
    assert result["final_total"] == pytest.approx(0.0)


def test_high_quantity_inventory_error():
    w = Warehouse({"item1": 5})
    op = OrderProcessor(w)
    result = op.process_order(
        order_id="order1",
        user_data={"email": "test@example.com", "age": 25},
        items=[{"id": "item1", "qty": 1000000, "price": 10.0}]
    )
    assert result["status"] == "failed"
    assert "Out of stock" in result["reason"]


def test_invalid_tier_discount():
    assert DiscountEngine.calculate_discount(100.0, "INVALID_TIER") == pytest.approx(0.0)


def test_promo_code_valid_standard_no_tier(monkeypatch):
    monkeypatch.setattr('data.input_code.d06_complex_logic.datetime', FakeDateTimeNoNight)
    assert DiscountEngine.calculate_discount(100.0, "STANDARD", promo_code="ABC-123") == pytest.approx(0.1)


def test_unsupported_payment_method_no_error():
    w = Warehouse({"item1": 5})
    op = OrderProcessor(w)
    result = op.process_order(
        order_id="order1",
        user_data={"email": "test@example.com", "age": 25, "payment_method": "UNSUPPORTED_METHOD"},
        items=[{"id": "item1", "qty": 1, "price": 100.0}]
    )
    assert result["status"] == "success"