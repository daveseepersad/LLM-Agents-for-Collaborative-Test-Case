import pytest
from data.input_code.d06_complex_logic import *

# Helper to patch datetime.now() behavior inside the module
import data.input_code.d06_complex_logic as logic_mod

class _FakeDateTime:
    class _Obj:
        hour = 12  # default non-hour-discount time
    @staticmethod
    def now():
        return _FakeDateTime._Obj()

# T1_VALID_USER and T2/T3/T4 tests for validate_user
def test_validate_user_valid():
    wh = Warehouse({})
    op = OrderProcessor(wh)
    assert op.validate_user("test@example.com", 25) is None

@pytest.mark.parametrize("email, age", [
    ("invalid", 25),     # invalid email format
    ("test@example.com", 17),  # under 18
    ("test@example.com", 101), # over 100
])
def test_validate_user_invalid(email, age):
    wh = Warehouse({})
    op = OrderProcessor(wh)
    with pytest.raises(UserValidationError):
        op.validate_user(email, age)

# T5_T6_T7: Warehouse.check_stock behavior
def test_check_stock_ok_and_fail(monkeypatch):
    wh = Warehouse({"item1": 10})
    assert wh.check_stock("item1", 5) is True
    assert wh.check_stock("item1", 15) is False

def test_check_stock_missing_item():
    wh = Warehouse({"item1": 10})
    with pytest.raises(InventoryError):
        wh.check_stock("nonexistent", 1)

# T8_T9: Warehouse.lock_item behavior
def test_lock_item_ok_and_check_stock_after_lock():
    wh = Warehouse({"item1": 10})
    wh.lock_item("item1", 5)
    # After locking 5, 6 items requested should fail, 5 should pass
    assert wh.check_stock("item1", 6) is False
    assert wh.check_stock("item1", 5) is True

def test_lock_item_fail():
    wh = Warehouse({"item1": 10})
    with pytest.raises(InventoryError):
        wh.lock_item("item1", 15)

# T10_T16: DiscountEngine.calculate_discount with controlled time (hour outside discount window)
def _patch_hour(monkeypatch, hour_value):
    class FakeDateTime:
        class Obj:
            hour = hour_value
        @staticmethod
        def now():
            return FakeDateTime.Obj()
    monkeypatch.setattr(logic_mod, "datetime", FakeDateTime)

@pytest.mark.parametrize("total_amount, user_tier, promo_code, expected", [
    (100, "STANDARD", None, 0.0),
    (100, "GOLD", None, 0.10),
    (100, "PLATINUM", None, 0.20),
    (1001, "PLATINUM", None, 0.25),
    (100, "STANDARD", "ABC-123", 0.10),
    (100, "STANDARD", "ABC-999", 50.0),  # super promo code path
])
def test_discount_engine_calculate_discount(monkeypatch, total_amount, user_tier, promo_code, expected):
    _patch_hour(monkeypatch, 12)  # ensure non-hour-discount path
    result = logic_mod.DiscountEngine.calculate_discount(total_amount, user_tier, promo_code)
    assert result == expected

@pytest.mark.parametrize("total_amount, user_tier, promo_code", [
    (100, "STANDARD", "invalid"),
])
def test_discount_engine_invalid_promo(monkeypatch, total_amount, user_tier, promo_code):
    _patch_hour(monkeypatch, 12)
    with pytest.raises(ValueError):
        logic_mod.DiscountEngine.calculate_discount(total_amount, user_tier, promo_code)

# T17_T18_T19_T20_T21: Order processing scenarios
def test_process_order_success(monkeypatch):
    wh = Warehouse({"item1": 10})
    op = OrderProcessor(wh)

    # Patch discount to be 0 to simplify expected values
    monkeypatch.setattr(logic_mod, "DiscountEngine", logic_mod.DiscountEngine)  # ensure class reference available
    def _zero_discount(total_amount, tier, promo=None):
        return 0.0
    monkeypatch.setattr(logic_mod, "DiscountEngine", logic_mod.DiscountEngine)
    monkeypatch.setattr(logic_mod.DiscountEngine, "calculate_discount", staticmethod(_zero_discount))

    input_data = {
        "order_id": "1",
        "user_data": {"email": "test@example.com", "age": 25, "tier": "STANDARD"},
        "items": [{"id": "item1", "qty": 1, "price": 10.0}],
    }

    result = op.process_order(**input_data)
    expected = {
        "status": "success",
        "order_id": "1",
        "original_price": 10.0,
        "discount_applied": 0.0,
        "final_total": 12.2,
        "items_count": 1
    }
    assert result == expected

def test_process_order_stock_fail(monkeypatch):
    wh = Warehouse({"item1": 10})
    op = OrderProcessor(wh)

    # No discount
    monkeypatch.setattr(logic_mod, "DiscountEngine", logic_mod.DiscountEngine)
    monkeypatch.setattr(logic_mod.DiscountEngine, "calculate_discount", staticmethod(lambda t, tier, promo=None: 0.0))

    input_data = {
        "order_id": "1",
        "user_data": {"email": "test@example.com", "age": 25, "tier": "STANDARD"},
        "items": [{"id": "item1", "qty": 15, "price": 10.0}],
    }

    result = op.process_order(**input_data)
    assert result == {"status": "failed", "reason": "Out of stock: Insufficient stock for item1"}

def test_process_order_invalid_promo(monkeypatch):
    wh = Warehouse({"item1": 10})
    op = OrderProcessor(wh)

    # Do not patch discount to test real promo invalid path
    input_data = {
        "order_id": "1",
        "user_data": {"email": "test@example.com", "age": 25, "tier": "STANDARD"},
        "items": [{"id": "item1", "qty": 1, "price": 10.0}],
        "promo_code": "invalid"
    }

    result = op.process_order(**input_data)
    assert result == {"status": "error", "reason": "Promo Error: Invalid promo code format"}

def test_process_order_paypal_fraud(monkeypatch):
    # This test ensures the FraudDetectedError is raised when the final amount after tax matches 666.66
    wh = Warehouse({"item1": 10})
    op = OrderProcessor(wh)

    input_data = {
        "order_id": "1",
        "user_data": {"email": "test@example.com", "age": 25, "tier": "STANDARD", "payment_method": "PAYPAL"},
        "items": [{"id": "item1", "qty": 1, "price": 546.44}],
    }

    with pytest.raises(FraudDetectedError):
        op.process_order(**input_data)

def test_process_order_crypto_min_amount(monkeypatch):
    wh = Warehouse({"item1": 10})
    op = OrderProcessor(wh)

    input_data = {
        "order_id": "1",
        "user_data": {"email": "test@example.com", "age": 25, "tier": "STANDARD", "payment_method": "CRYPTO"},
        "items": [{"id": "item1", "qty": 1, "price": 10.0}],
    }

    with pytest.raises(PaymentError):
        op.process_order(**input_data)