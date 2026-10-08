import pytest
import importlib

# Import symbols from the module under test
from data.input_code.d06_complex_logic import *

# Load module for monkeypatching datetime behavior
d06 = importlib.import_module('data.input_code.d06_complex_logic')

def patch_time(monkeypatch, hour: int):
    class FakeDateTime:
        @classmethod
        def now(cls):
            class DT:
                pass
            dt = DT()
            dt.hour = hour
            return dt
    monkeypatch.setattr(d06, 'datetime', FakeDateTime, raising=True)

# T1_VALID_USER, T2_INVALID_EMAIL, T3_UNDERAGE_USER, T4_OVERAGE_USER
@pytest.mark.parametrize('email, age, should_raise', [
    ('test@example.com', 25, None),
    ('invalid_email', 25, UserValidationError),
    ('test@example.com', 17, UserValidationError),
    ('test@example.com', 101, UserValidationError),
])
def test_validate_user_plan_variants(email, age, should_raise, monkeypatch):
    w = Warehouse({})
    op = OrderProcessor(w)
    if should_raise:
        with pytest.raises(should_raise):
            op.validate_user(email, age)
    else:
        assert op.validate_user(email, age) is None

# T5_STOCK_CHECK_OK, T6_STOCK_CHECK_FAIL, T7_STOCK_CHECK_MISSING_ITEM
def test_warehouse_check_stock_ok():
    w = Warehouse({"item1": 10})
    assert w.check_stock("item1", 5) is True

def test_warehouse_check_stock_fail():
    w = Warehouse({"item1": 10})
    assert w.check_stock("item1", 15) is False

def test_warehouse_check_stock_missing_item():
    w = Warehouse({"item1": 10})
    with pytest.raises(InventoryError):
        w.check_stock("nonexistent", 1)

# T8_LOCK_ITEM_OK, T9_LOCK_ITEM_FAIL
def test_lock_item_ok():
    w = Warehouse({"item1": 10})
    w.lock_item("item1", 5)
    # If no exception is raised, test passes

def test_lock_item_fail():
    w = Warehouse({"item1": 10})
    with pytest.raises(InventoryError):
        w.lock_item("item1", 15)

# DiscountEngine tests (T10-T16)
def test_discount_standard_zero(monkeypatch):
    patch_time(monkeypatch, hour=12)
    assert DiscountEngine.calculate_discount(100, "STANDARD") == 0.0

def test_discount_gold(monkeypatch):
    patch_time(monkeypatch, hour=12)
    assert DiscountEngine.calculate_discount(100, "GOLD") == 0.10

def test_discount_platinum(monkeypatch):
    patch_time(monkeypatch, hour=12)
    assert DiscountEngine.calculate_discount(100, "PLATINUM") == 0.20

def test_discount_platinum_high_amount(monkeypatch):
    patch_time(monkeypatch, hour=12)
    assert DiscountEngine.calculate_discount(1001, "PLATINUM") == 0.25

def test_discount_promo_valid(monkeypatch):
    patch_time(monkeypatch, hour=12)
    assert DiscountEngine.calculate_discount(100, "STANDARD", "ABC-123") == 0.10

def test_discount_promo_invalid():
    with pytest.raises(ValueError):
        DiscountEngine.calculate_discount(100, "STANDARD", "invalid")

def test_discount_promo_super():
    assert DiscountEngine.calculate_discount(100, "STANDARD", "ABC-999") == 50.0

# T17_PROCESS_ORDER_OK
def test_process_order_ok(monkeypatch):
    # Ensure discount is 0 to have predictable results
    monkeypatch.setattr(DiscountEngine, 'calculate_discount', staticmethod(lambda total_amount, user_tier, promo_code=None: 0.0))
    w = Warehouse({"item1": 10})
    op = OrderProcessor(w)
    result = op.process_order(
        order_id="1",
        user_data={"email": "test@example.com", "age": 25, "tier": "STANDARD"},
        items=[{"id": "item1", "qty": 1, "price": 10.0}]
    )
    assert isinstance(result, dict)
    assert result.get("status") == "success"
    assert result.get("order_id") == "1"
    assert result.get("original_price") == 10.0
    assert result.get("items_count") == 1

# T18_PROCESS_ORDER_INVENTORY_ERROR
def test_process_order_inventory_error(monkeypatch):
    monkeypatch.setattr(DiscountEngine, 'calculate_discount', staticmethod(lambda total_amount, user_tier, promo_code=None: 0.0))
    w = Warehouse({"item1": 10})
    op = OrderProcessor(w)
    res = op.process_order(
        order_id="1",
        user_data={"email": "test@example.com", "age": 25, "tier": "STANDARD"},
        items=[{"id": "item1", "qty": 15, "price": 10.0}]
    )
    assert res["status"] == "failed"
    assert "Out of stock" in res["reason"]

# T19_PROCESS_ORDER_INVALID_PROMO
def test_process_order_invalid_promo(monkeypatch):
    def raise_value(total_amount, user_tier, promo_code=None):
        raise ValueError("Invalid promo code format")
    monkeypatch.setattr(DiscountEngine, 'calculate_discount', staticmethod(raise_value))
    w = Warehouse({"item1": 10})
    op = OrderProcessor(w)
    res = op.process_order(
        order_id="1",
        user_data={"email": "test@example.com", "age": 25, "tier": "STANDARD"},
        items=[{"id": "item1", "qty": 1, "price": 10.0}],
        promo_code="invalid"
    )
    assert res["status"] == "error"
    assert "Promo Error" in res["reason"]

# T21_PROCESS_ORDER_CRYPTO_MIN_AMOUNT
def test_process_order_crypto_min_amount(monkeypatch):
    monkeypatch.setattr(DiscountEngine, 'calculate_discount', staticmethod(lambda total_amount, user_tier, promo_code=None: 0.0))
    w = Warehouse({"item1": 10})
    op = OrderProcessor(w)
    with pytest.raises(PaymentError):
        op.process_order(
            order_id="1",
            user_data={"email": "test@example.com", "age": 25, "tier": "STANDARD", "payment_method": "CRYPTO"},
            items=[{"id": "item1", "qty": 1, "price": 10.0}]
        )

import pytest
import importlib

from data.input_code.d06_complex_logic import *

d06 = importlib.import_module('data.input_code.d06_complex_logic')

def _set_fake_time(monkeypatch, hour: int):
    class FakeDateTime:
        @classmethod
        def now(cls):
            class DT:
                pass
            dt = DT()
            dt.hour = hour
            return dt
    monkeypatch.setattr(d06, 'datetime', FakeDateTime, raising=True)


# T_MISSING_NIGHT_DISCOUNT
def test_missing_night_discount(monkeypatch):
    _set_fake_time(monkeypatch, hour=2)
    assert DiscountEngine.calculate_discount(100.0, "STANDARD") == 0.05


# T_MISSING_MAX_DISCOUNT_CAP
def test_discount_cap_maximum(monkeypatch):
    _set_fake_time(monkeypatch, hour=2)
    assert DiscountEngine.calculate_discount(1000.0, "PLATINUM", "ABC-123") == 0.35


# T_MISSING_PAYPAL_EDGE_CASE
def test_process_order_paypal_edge_case(monkeypatch):
    _set_fake_time(monkeypatch, hour=12)
    w = Warehouse({"item1": 5})
    op = OrderProcessor(w)
    with pytest.raises(FraudDetectedError):
        op.process_order(
            order_id="1",
            user_data={"email": "test@example.com", "age": 25, "tier": "STANDARD", "payment_method": "PAYPAL"},
            items=[{"id": "item1", "qty": 1, "price": 546.44}]
        )


# T_MISSING_CRYPTO_PAYMENT_OK
def test_process_order_crypto_ok(monkeypatch):
    _set_fake_time(monkeypatch, hour=12)
    monkeypatch.setattr(DiscountEngine, 'calculate_discount', staticmethod(lambda total_amount, user_tier, promo_code=None: 0.0))
    w = Warehouse({"item1": 20})
    op = OrderProcessor(w)
    res = op.process_order(
        order_id="1",
        user_data={"email": "test@example.com", "age": 25, "tier": "STANDARD", "payment_method": "CRYPTO"},
        items=[{"id": "item1", "qty": 10, "price": 5.0}]
    )
    assert isinstance(res, dict)
    assert res.get("status") == "success"


# T_MISSING_RETURN_FREE_ITEMS_ERROR
def test_process_order_return_free_items_error(monkeypatch):
    w = Warehouse({"item1": 10})
    op = OrderProcessor(w)
    with pytest.raises(ValueError):
        op.process_order(
            order_id="1",
            user_data={"email": "test@example.com", "age": 25, "tier": "STANDARD"},
            items=[{"id": "item1", "qty": -1, "price": 0.0}],
            promo_code=None
        )