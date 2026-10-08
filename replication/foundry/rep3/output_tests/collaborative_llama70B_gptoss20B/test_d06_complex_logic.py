import pytest
from data.input_code.d06_complex_logic import *
from data.input_code.d06_complex_logic import Warehouse as _Warehouse  # alias for potential clarity

# Helpers to control DiscountEngine time-based behavior
def _patch_discount_time(monkeypatch, hour: int):
    class DummyNow:
        pass
    def _make_now():
        n = DummyNow()
        n.hour = hour
        return n
    class FakeDateTime:
        @staticmethod
        def now():
            return _make_now()
    monkeypatch.setattr('data.input_code.d06_complex_logic.datetime', FakeDateTime, raising=False)

# 1) Warehouse tests (T1_OK, T2_ERR)
def test_warehouse_check_stock_ok():
    w = Warehouse({"item1": 10})
    assert w.check_stock("item1", 5) is True

def test_warehouse_check_stock_item_not_found():
    w = Warehouse({"item1": 10})
    with pytest.raises(InventoryError):
        w.check_stock("item2", 1)

# 2) Warehouse lock_item tests (T3_OK, T4_ERR)
def test_warehouse_lock_item_ok():
    w = Warehouse({"item1": 10})
    w.lock_item("item1", 5)
    assert w._locked_stock.get("item1", 0) == 5

def test_warehouse_lock_item_insufficient_stock():
    w = Warehouse({"item1": 10})
    with pytest.raises(InventoryError):
        w.lock_item("item1", 15)

# 3) DiscountEngine tests (T5_OK, T6_OK, T7_OK, T8_ERR, T9_OK)
def test_discount_gold_no_night(monkeypatch):
    _patch_discount_time(monkeypatch, hour=12)  # not in night window
    assert DiscountEngine.calculate_discount(100.0, "GOLD") == 0.10

def test_discount_platinum_no_night(monkeypatch):
    _patch_discount_time(monkeypatch, hour=12)  # not in night window
    assert DiscountEngine.calculate_discount(100.0, "PLATINUM") == 0.20

def test_discount_platinum_with_night(monkeypatch):
    _patch_discount_time(monkeypatch, hour=2)  # night window
    # 0.05 night + 0.20 Platinum = 0.25 (no promo)
    assert DiscountEngine.calculate_discount(1000.0, "PLATINUM") == 0.25

def test_discount_invalid_promo_format_raises(monkeypatch):
    _patch_discount_time(monkeypatch, hour=12)  # safe hour
    with pytest.raises(ValueError):
        DiscountEngine.calculate_discount(100.0, "PLATINUM", promo_code="ABC-1234")

def test_discount_platinum_with_valid_promo_and_night(monkeypatch):
    _patch_discount_time(monkeypatch, hour=2)  # night window
    # 0.05 night + 0.20 Platinum + 0.10 promo = 0.35
    assert DiscountEngine.calculate_discount(100.0, "PLATINUM", promo_code="ABC-123") == 0.35

# 4) OrderProcessor.validate_user tests (T10_OK, T11_ERR, T12_ERR)
def test_order_validate_user_ok():
    op = OrderProcessor(Warehouse({"item1": 10}))
    # Should not raise
    assert op.validate_user("test@example.com", 25) is None

def test_order_validate_user_invalid_email():
    op = OrderProcessor(Warehouse({"item1": 10}))
    with pytest.raises(UserValidationError):
        op.validate_user("invalid_email", 25)

def test_order_validate_user_underage():
    op = OrderProcessor(Warehouse({"item1": 10}))
    with pytest.raises(UserValidationError):
        op.validate_user("test@example.com", 15)

# 5) OrderProcessor.process_order tests (T14 and T15 analogs)
def test_order_process_out_of_stock_item_not_found():
    # Warehouse empty, item not present -> should fail with InventoryError path
    w = Warehouse({})
    op = OrderProcessor(w)
    order_id = "order1"
    user_data = {"email": "test@example.com", "age": 25, "tier": "GOLD"}
    items = [{"id": "item1", "qty": 1, "price": 10.0}]
    result = op.process_order(order_id, user_data, items)
    assert result["status"] == "failed"
    assert "Out of stock" in result["reason"]

def test_order_process_promo_format_error():
    w = Warehouse({"item1": 5})
    op = OrderProcessor(w)
    order_id = "order1"
    user_data = {"email": "test@example.com", "age": 25, "tier": "GOLD"}
    items = [{"id": "item1", "qty": 5, "price": 10.0}]
    # Use a bad promo format to trigger promo error path
    result = op.process_order(order_id, user_data, items, promo_code="ABC-12")  # invalid format
    assert result["status"] == "error"
    assert "Promo Error" in result["reason"]

import pytest
from data.input_code.d06_complex_logic import *

# 1) NIGHTOWL discount when STANDARD and night hour
def test_discount_nightowl_standard(monkeypatch):
    class DummyNow:
        pass
    def _make_now():
        n = DummyNow()
        n.hour = 2  # night window
        return n
    class FakeDateTime:
        @staticmethod
        def now():
            return _make_now()
    monkeypatch.setattr('data.input_code.d06_complex_logic.datetime', FakeDateTime, raising=False)
    assert DiscountEngine.calculate_discount(100.0, "STANDARD") == 0.05

# 2) Platinum over 1000 should yield 0.25 discount (night not required)
def test_discount_platinum_over_1000(monkeypatch):
    class DummyNow:
        pass
    def _make_now():
        n = DummyNow()
        n.hour = 12  # non-night window
        return n
    class FakeDateTime:
        @staticmethod
        def now():
            return _make_now()
    monkeypatch.setattr('data.input_code.d06_complex_logic.datetime', FakeDateTime, raising=False)
    assert DiscountEngine.calculate_discount(1001.0, "PLATINUM") == 0.25

# 3) Promo code 999 should return 50% regardless of other discounts
def test_discount_promo_code_999(monkeypatch):
    class DummyNow:
        pass
    def _make_now():
        n = DummyNow()
        n.hour = 12  # any hour
        return n
    class FakeDateTime:
        @staticmethod
        def now():
            return _make_now()
    monkeypatch.setattr('data.input_code.d06_complex_logic.datetime', FakeDateTime, raising=False)
    assert DiscountEngine.calculate_discount(100.0, "STANDARD", promo_code="ABC-999") == 50.0

# 4) OrderProcessor.validate_user over 100 should raise
def test_order_validate_user_over_100():
    op = OrderProcessor(Warehouse({"item1": 10}))
    with pytest.raises(UserValidationError):
        op.validate_user("test@example.com", 101)

# 5) PayPal evil number should trigger FraudDetectedError
def test_order_process_paypal_evil_number(monkeypatch):
    w = Warehouse({"item1": 5})
    op = OrderProcessor(w)
    order_id = "order1"
    user_data = {"email": "test@example.com", "age": 25, "tier": "GOLD", "payment_method": "PAYPAL"}
    items = [{"id": "item1", "qty": 1, "price": 546.44}]
    # Force discount to 0 to hit exact rounding edge case
    def _fake_discount(total_amount, tier, promo_code=None):
        return 0.0
    monkeypatch.setattr('data.input_code.d06_complex_logic.DiscountEngine.calculate_discount', _fake_discount)
    with pytest.raises(FraudDetectedError):
        op.process_order(order_id, user_data, items)

# 6) Crypto under 50 should raise PaymentError
def test_order_process_crypto_under_50(monkeypatch):
    w = Warehouse({"item1": 5})
    op = OrderProcessor(w)
    order_id = "order1"
    user_data = {"email": "test@example.com", "age": 25, "tier": "GOLD", "payment_method": "CRYPTO"}
    items = [{"id": "item1", "qty": 1, "price": 0.0}]
    def _fake_discount(total_amount, tier, promo_code=None):
        return 0.0
    monkeypatch.setattr('data.input_code.d06_complex_logic.DiscountEngine.calculate_discount', _fake_discount)
    with pytest.raises(PaymentError):
        op.process_order(order_id, user_data, items)

# 7) Returning free item should raise ValueError
def test_order_process_return_free_item():
    w = Warehouse({"item1": 10})
    op = OrderProcessor(w)
    order_id = "order1"
    user_data = {"email": "test@example.com", "age": 25, "tier": "GOLD"}
    items = [{"id": "item1", "qty": -1, "price": 0.0}]
    with pytest.raises(ValueError):
        op.process_order(order_id, user_data, items)

# 8) Warehouse.release_item when not locked should be a no-op (not raising)
def test_warehouse_release_item_not_locked_noop():
    w = Warehouse({"item1": 10})
    w.release_item("item1", 5)
    assert w._locked_stock.get("item1", 0) == 0

# 9) Warehouse.release_item when locked should decrease lock amount
def test_warehouse_release_item_locked_reduces_lock():
    w = Warehouse({"item1": 10})
    w.lock_item("item1", 5)
    w.release_item("item1", 5)
    assert w._locked_stock.get("item1", 0) == 0