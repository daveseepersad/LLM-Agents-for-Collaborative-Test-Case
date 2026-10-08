import pytest
from data.input_code.d06_complex_logic import *
import data.input_code.d06_complex_logic as logic

class FakeDateTime12:
    @classmethod
    def now(cls):
        class D: pass
        d = D()
        d.hour = 12
        return d

class FakeDateTime2:
    @classmethod
    def now(cls):
        class D: pass
        d = D()
        d.hour = 2
        return d

def test_T1_OK_stock_check():
    w = Warehouse({"item1": 10})
    assert w.check_stock("item1", 1) is True

def test_T2_ERR_stock_check_raises():
    w = Warehouse({"item1": 10})
    with pytest.raises(InventoryError):
        w.check_stock("item2", 1)

def test_T3_OK_lock_item():
    w = Warehouse({"item1": 10})
    w.lock_item("item1", 1)
    # No exception means success

def test_T4_ERR_lock_item_raises():
    w = Warehouse({"item1": 10})
    with pytest.raises(InventoryError):
        w.lock_item("item1", 11)

def test_T5_OK_discount_gold(monkeypatch):
    monkeypatch.setattr(logic, "datetime", FakeDateTime12)
    assert DiscountEngine.calculate_discount(100.0, "GOLD") == 0.1

def test_T6_OK_discount_platinum(monkeypatch):
    monkeypatch.setattr(logic, "datetime", FakeDateTime12)
    assert DiscountEngine.calculate_discount(100.0, "PLATINUM") == 0.2

def test_T7_OK_discount_platinum_high_amount(monkeypatch):
    monkeypatch.setattr(logic, "datetime", FakeDateTime2)
    assert DiscountEngine.calculate_discount(1000.0, "PLATINUM") == 0.25

def test_T8_OK_discount_with_promo_code(monkeypatch):
    monkeypatch.setattr(logic, "datetime", FakeDateTime12)
    assert DiscountEngine.calculate_discount(100.0, "GOLD", "ABC-123") == 0.2

def test_T9_ERR_invalid_promo_code(monkeypatch):
    monkeypatch.setattr(logic, "datetime", FakeDateTime12)
    with pytest.raises(ValueError):
        DiscountEngine.calculate_discount(100.0, "GOLD", "invalid")

def test_T10_validate_user_ok():
    w = Warehouse({"item1": 5})
    o = OrderProcessor(w)
    # Expect None when valid
    assert o.validate_user("test@example.com", 25) is None

def test_T11_validate_user_invalid_email():
    w = Warehouse({"item1": 5})
    o = OrderProcessor(w)
    with pytest.raises(UserValidationError):
        o.validate_user("invalid", 25)

def test_T12_validate_user_age():
    w = Warehouse({"item1": 5})
    o = OrderProcessor(w)
    with pytest.raises(UserValidationError):
        o.validate_user("test@example.com", 17)

def test_T13_process_order_happy_path(monkeypatch):
    monkeypatch.setattr(logic, "datetime", FakeDateTime12)
    w = Warehouse({"item1": 10})
    op = OrderProcessor(w)
    user_data = {"email": "test@example.com", "age": 25, "tier": "GOLD"}
    items = [{"id": "item1", "qty": 1, "price": 100.0}]
    res = op.process_order("order1", user_data, items)
    assert res == {
        "status": "success",
        "order_id": "order1",
        "original_price": 100.0,
        "discount_applied": 0.1,
        "final_total": 109.8,
        "items_count": 1
    }

def test_T14_out_of_stock():
    w = Warehouse({"item1": 10})
    op = OrderProcessor(w)
    user_data = {"email": "test@example.com", "age": 25, "tier": "GOLD"}
    items = [{"id": "item1", "qty": 11, "price": 100.0}]
    res = op.process_order("order1", user_data, items)
    assert res == {"status": "failed", "reason": "Out of stock: Insufficient stock for item1"}

def test_T15_promo_error(monkeypatch):
    monkeypatch.setattr(logic, "datetime", FakeDateTime12)
    w = Warehouse({"item1": 10})
    op = OrderProcessor(w)
    user_data = {"email": "test@example.com", "age": 25, "tier": "GOLD"}
    items = [{"id": "item1", "qty": 1, "price": 100.0}]
    res = op.process_order("order1", user_data, items, promo_code="invalid")
    assert res == {"status": "error", "reason": "Promo Error: Invalid promo code format"}

def test_T16_fraud_detected(monkeypatch):
    # Patch discount to 0 to isolate amount
    monkeypatch.setattr(logic, "datetime", FakeDateTime12)
    monkeypatch.setattr(DiscountEngine, "calculate_discount", staticmethod(lambda total_amount, user_tier, promo_code=None: 0.0))
    w = Warehouse({"item1": 10})
    op = OrderProcessor(w)
    user_data = {"email": "test@example.com", "age": 25, "tier": "GOLD", "payment_method": "PAYPAL"}
    items = [{"id": "item1", "qty": 1, "price": 546.44}]
    with pytest.raises(FraudDetectedError):
        op.process_order("order1", user_data, items)

def test_T17_payment_error_crypto():
    w = Warehouse({"item1": 10})
    op = OrderProcessor(w)
    user_data = {"email": "test@example.com", "age": 25, "tier": "STANDARD", "payment_method": "CRYPTO"}
    items = [{"id": "item1", "qty": 1, "price": 10.0}]
    with pytest.raises(PaymentError):
        op.process_order("order1", user_data, items)

def test_T_MISSING_1_night_owl_discount(monkeypatch):
    # Night hour discount should apply
    monkeypatch.setattr(logic, "datetime", FakeDateTime2)
    assert DiscountEngine.calculate_discount(100.0, "STANDARD") == 0.05

def test_T_MISSING_2_promo_999(monkeypatch):
    # Promo code ABC-999 should trigger 50% off immediately
    monkeypatch.setattr(logic, "datetime", FakeDateTime12)
    assert DiscountEngine.calculate_discount(100.0, "STANDARD", "ABC-999") == 50.0

def test_T_MISSING_3_validate_user_age_over_100():
    w = Warehouse({"item1": 5})
    o = OrderProcessor(w)
    with pytest.raises(UserValidationError) as exc:
        o.validate_user("test@example.com", 101)
    assert "Age verification required for 100+" in str(exc.value)

def test_T_MISSING_4_process_order_negative_qty_raises():
    w = Warehouse({"item1": 10})
    op = OrderProcessor(w)
    user_data = {"email": "test@example.com", "age": 25}
    items = [{"id": "item1", "qty": -1, "price": 0.0}]
    with pytest.raises(ValueError) as exc:
        op.process_order("order1", user_data, items)
    assert "Cannot return free items" in str(exc.value)

def test_T_MISSING_5_max_discount_cap(monkeypatch):
    monkeypatch.setattr(logic, "datetime", FakeDateTime12)
    # PLATINUM with promo ABC-123 should cap at 0.3 due to floating point addition
    assert round(DiscountEngine.calculate_discount(100.0, "PLATINUM", "ABC-123"), 2) == 0.30

def test_T_MISSING_6_process_order_cc(monkeypatch):
    monkeypatch.setattr(logic, "datetime", FakeDateTime12)  # deterministic timing
    w = Warehouse({"item1": 10})
    op = OrderProcessor(w)
    user_data = {"email": "test@example.com", "age": 25, "payment_method": "CC"}
    items = [{"id": "item1", "qty": 1, "price": 100.0}]
    res = op.process_order("order1", user_data, items)
    assert res == {
        "status": "success",
        "order_id": "order1",
        "original_price": 100.0,
        "discount_applied": 0.0,
        "final_total": 122.0,
        "items_count": 1
    }

def test_T_MISSING_7_release_item():
    w = Warehouse({"item1": 10})
    w.lock_item("item1", 1)
    w.release_item("item1", 1)
    assert w.check_stock("item1", 1) is True

def test_T_MISSING_8_locked_stock():
    w = Warehouse({"item1": 1})
    assert w.check_stock("item1", 1) is True

def test_T_MISSING_9_locked_stock_insufficient():
    w = Warehouse({"item1": 10})
    assert w.check_stock("item1", 11) is False

def test_T_MISSING_10_check_stock_zero_quantity():
    w = Warehouse({"item1": 5})
    assert w.check_stock("item1", 0) is True

def test_T_MISSING_11_lock_item_zero_quantity():
    w = Warehouse({"item1": 5})
    w.lock_item("item1", 0)
    # No exception means success

def test_T_MISSING_12_release_item_zero_quantity():
    w = Warehouse({"item1": 5})
    w.release_item("item1", 0)
    # No exception means success

def test_T_MISSING_13_discount_engine_negative_total_amount(monkeypatch):
    monkeypatch.setattr(logic, "datetime", FakeDateTime12)
    assert DiscountEngine.calculate_discount(-100.0, "STANDARD") == 0.0

def test_T_MISSING_14_process_order_empty_items(monkeypatch):
    monkeypatch.setattr(logic, "datetime", FakeDateTime12)
    w = Warehouse({"item1": 10})
    op = OrderProcessor(w)
    user_data = {"email": "test@example.com", "age": 25}
    items = []
    res = op.process_order("order1", user_data, items)
    assert res == {
        "status": "success",
        "order_id": "order1",
        "original_price": 0.0,
        "discount_applied": 0.0,
        "final_total": 0.0,
        "items_count": 0
    }

def test_T_MISSING_15_process_order_null_user_data():
    w = Warehouse({"item1": 5})
    op = OrderProcessor(w)
    user_data = None
    items = [{"id": "item1", "qty": 1, "price": 100.0}]
    with pytest.raises(AttributeError):
        op.process_order("order1", user_data, items)

def test_T_MISSING_16_process_order_null_items():
    w = Warehouse({"item1": 5})
    op = OrderProcessor(w)
    user_data = {"email": "test@example.com", "age": 25}
    items = None
    with pytest.raises(TypeError):
        op.process_order("order1", user_data, items)

def test_T_NEW_1():
    w = Warehouse({"item1": 5})
    w.lock_item("item1", 1)
    assert w.check_stock("item1", 0) is True

def test_T_NEW_2(monkeypatch):
    monkeypatch.setattr(logic, "datetime", FakeDateTime12)
    assert DiscountEngine.calculate_discount(100.0, "GOLD", "ABC-123") == 0.2


def test_T_NEW_4():
    w = Warehouse({"item1": 5})
    o = OrderProcessor(w)
    assert o.validate_user("test+special@example.com", 25) is None

def test_T_NEW_5(monkeypatch):
    monkeypatch.setattr(logic, "datetime", FakeDateTime12)
    w = Warehouse({"item1": 10})
    op = OrderProcessor(w)
    user_data = {"email": "test@example.com", "age": 25, "payment_method": "CC"}
    items = [{"id": "item1", "qty": 1, "price": 1001.0}]
    res = op.process_order("order1", user_data, items)
    assert res == {
        "status": "success",
        "order_id": "order1",
        "original_price": 1001.0,
        "discount_applied": 0.0,
        "final_total": round(1001.0 * 1.22, 2),
        "items_count": 1
    }

def test_T_NEW_6(monkeypatch):
    monkeypatch.setattr(logic, "datetime", FakeDateTime12)
    assert DiscountEngine.calculate_discount(-100.0, "STANDARD", "ABC-123") == 0.1

def test_T_NEW_7(monkeypatch):
    monkeypatch.setattr(logic, "datetime", FakeDateTime12)
    w = Warehouse({"item1": 10})
    op = OrderProcessor(w)
    user_data = {"email": "test@example.com", "age": 25, "tier": "PLATINUM"}
    items = [{"id": "item1", "qty": 1, "price": 1001.0}]
    res = op.process_order("order1", user_data, items)
    expected_final_total = round(1001.0 * (1 - 0.25) * 1.22, 2)
    assert res == {
        "status": "success",
        "order_id": "order1",
        "original_price": 1001.0,
        "discount_applied": 0.25,
        "final_total": expected_final_total,
        "items_count": 1
    }