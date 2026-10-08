import pytest
from data.input_code.d06_complex_logic import *
import data.input_code.d06_complex_logic as logic  # for monkeypatching datetime

# Helper to mock datetime.now().hour without modifying production code structure
def _make_fake_datetime(hour):
    class _FakeNow:
        def __init__(self):
            self.hour = hour
    class _FakeDateTime:
        @classmethod
        def now(cls):
            return _FakeNow()
    return _FakeDateTime

# Warehouse tests
def test_W1_CHECKSTOCK_OK():
    w = Warehouse({"itemA": 5})
    assert w.check_stock("itemA", 2) is True

def test_W2_CHECKSTOCK_ITEM_NOT_FOUND():
    w = Warehouse({"itemA": 5})
    with pytest.raises(InventoryError):
        w.check_stock("itemX", 1)

def test_W3_LOCKITEM_INSUFFICIENT():
    w = Warehouse({"itemA": 5})
    with pytest.raises(InventoryError):
        w.lock_item("itemA", 999)

def test_W4_LOCKITEM_SUCCESS():
    w = Warehouse({"itemA": 5})
    # Should not raise any exception
    w.lock_item("itemA", 1)


# DiscountEngine tests (control time to ensure deterministic behavior)
def test_D1_PROMO_ENDS_999(monkeypatch):
    # Patch time to a hour that would otherwise cause a night discount, but promo code 999 overrides
    monkeypatch.setattr(logic, "datetime", _make_fake_datetime(2))
    assert DiscountEngine.calculate_discount(100.0, "STANDARD", "ABC-999") == 50.0

def test_D2_INVALID_PROMO_FORMAT(monkeypatch):
    monkeypatch.setattr(logic, "datetime", _make_fake_datetime(12))
    with pytest.raises(ValueError):
        DiscountEngine.calculate_discount(100.0, "STANDARD", "BAD")

def test_D3_DISCOUNT_GOLD(monkeypatch):
    # Time outside night window to ensure only GOLD discount applies
    monkeypatch.setattr(logic, "datetime", _make_fake_datetime(12))
    assert DiscountEngine.calculate_discount(100.0, "GOLD", None) == pytest.approx(0.10)

def test_D4_DISCOUNT_PLATINUM_OVER1000(monkeypatch):
    monkeypatch.setattr(logic, "datetime", _make_fake_datetime(12))
    assert DiscountEngine.calculate_discount(1200.0, "PLATINUM", None) == pytest.approx(0.25)


# OrderProcessor tests
def test_O1_ORDER_BASIC_SUCCESS(monkeypatch):
    monkeypatch.setattr(logic, "datetime", _make_fake_datetime(12))
    w = Warehouse({"sku1": 5})
    op = OrderProcessor(w)
    order = {
        "order_id": "ORD-001",
        "user_data": {"email": "user@example.com", "age": 25},
        "items": [{"id": "sku1", "qty": 2, "price": 10.0}],
        "promo_code": None
    }
    expected = {
        "status": "success",
        "order_id": "ORD-001",
        "original_price": 20.0,
        "discount_applied": 0.0,
        "final_total": 24.4,
        "items_count": 1
    }
    assert op.process_order(**order) == expected


def test_O2_ORDER_OUT_OF_STOCK(monkeypatch):
    monkeypatch.setattr(logic, "datetime", _make_fake_datetime(12))
    w = Warehouse({"sku1": 5})
    op = OrderProcessor(w)
    order = {
        "order_id": "ORD-002",
        "user_data": {"email": "user@example.com", "age": 25},
        "items": [{"id": "missing", "qty": 1, "price": 10.0}],
        "promo_code": None
    }
    res = op.process_order(**order)
    assert res == {"status": "failed", "reason": "Out of stock: Item missing not found in warehouse."}


def test_O3_ORDER_INVALID_EMAIL(monkeypatch):
    monkeypatch.setattr(logic, "datetime", _make_fake_datetime(12))
    w = Warehouse({"sku1": 5})
    op = OrderProcessor(w)
    order = {
        "order_id": "ORD-003",
        "user_data": {"email": "invalid-email", "age": 30},
        "items": [{"id": "sku1", "qty": 1, "price": 10.0}],
        "promo_code": None
    }
    with pytest.raises(UserValidationError):
        op.process_order(**order)


def test_O4_ORDER_AGE_OVER_100(monkeypatch):
    monkeypatch.setattr(logic, "datetime", _make_fake_datetime(12))
    w = Warehouse({"sku1": 5})
    op = OrderProcessor(w)
    order = {
        "order_id": "ORD-004",
        "user_data": {"email": "user@example.com", "age": 101},
        "items": [{"id": "sku1", "qty": 1, "price": 10.0}],
        "promo_code": None
    }
    with pytest.raises(UserValidationError):
        op.process_order(**order)


def test_O5_ORDER_PROMO_INVALID_FORMAT(monkeypatch):
    monkeypatch.setattr(logic, "datetime", _make_fake_datetime(12))
    w = Warehouse({"sku1": 5})
    op = OrderProcessor(w)
    order = {
        "order_id": "ORD-005",
        "user_data": {"email": "user@example.com", "age": 25},
        "items": [{"id": "sku1", "qty": 1, "price": 10.0}],
        "promo_code": "BAD"
    }
    res = op.process_order(**order)
    assert res == {"status": "error", "reason": "Promo Error: Invalid promo code format"}


def test_O6_ORDER_PROMO_999(monkeypatch):
    monkeypatch.setattr(logic, "datetime", _make_fake_datetime(12))
    w = Warehouse({"sku1": 5})
    op = OrderProcessor(w)
    order = {
        "order_id": "ORD-006",
        "user_data": {"email": "user@example.com", "age": 25},
        "items": [{"id": "sku1", "qty": 1, "price": 100.0}],
        "promo_code": "ABC-999"
    }
    expected = {
        "status": "success",
        "order_id": "ORD-006",
        "original_price": 100.0,
        "discount_applied": 50.0,
        "final_total": -5978.0,
        "items_count": 1
    }
    assert op.process_order(**order) == expected


def test_O7_ORDER_PLATINUM_OVER1000(monkeypatch):
    monkeypatch.setattr(logic, "datetime", _make_fake_datetime(12))
    w = Warehouse({"p_item": 5})
    op = OrderProcessor(w)
    order = {
        "order_id": "ORD-007",
        "user_data": {"email": "user@example.com", "age": 30, "tier": "PLATINUM"},
        "items": [{"id": "p_item", "qty": 1, "price": 1200.0}],
        "promo_code": None
    }
    expected = {
        "status": "success",
        "order_id": "ORD-007",
        "original_price": 1200.0,
        "discount_applied": 0.25,
        "final_total": 1098.0,
        "items_count": 1
    }
    assert op.process_order(**order) == expected


def test_O8_ORDER_CRYPTO_MINIMUM_NOT_MET(monkeypatch):
    monkeypatch.setattr(logic, "datetime", _make_fake_datetime(12))
    w = Warehouse({"c_item": 5})
    op = OrderProcessor(w)
    order = {
        "order_id": "ORD-008",
        "user_data": {"email": "user@example.com", "age": 30, "payment_method": "CRYPTO"},
        "items": [{"id": "c_item", "qty": 1, "price": 40.0}],
        "promo_code": None
    }
    with pytest.raises(PaymentError):
        op.process_order(**order)

import pytest
from data.input_code.d06_complex_logic import *
import data.input_code.d06_complex_logic as logic  # for monkeypatching datetime

def test_T_MISSING_D5_GOLD_NIGHT(monkeypatch):
    # Night hour to ensure night discount is applied along with GOLD tier
    monkeypatch.setattr(logic, "datetime", _make_fake_datetime(2))
    assert DiscountEngine.calculate_discount(100.0, "GOLD", None) == pytest.approx(0.15)

def test_T_MISSING_D6_PROMO_VALID_NO_999(monkeypatch):
    # Non-night hour, valid promo code that does not end with 999
    monkeypatch.setattr(logic, "datetime", _make_fake_datetime(12))
    assert DiscountEngine.calculate_discount(100.0, "STANDARD", "DEF-123") == pytest.approx(0.10)

def test_T_MISSING_O9_ROLLBACK_PARTIAL_STOCK():
    w = Warehouse({"sku1": 5})
    op = OrderProcessor(w)
    order = {
        "order_id": "ORD-009",
        "user_data": {"email": "user@example.com", "age": 25},
        "items": [{"id": "sku1", "qty": 2, "price": 10.0}, {"id": "missing", "qty": 1, "price": 5.0}],
        "promo_code": None
    }
    res = op.process_order(**order)
    assert res == {"status": "failed", "reason": "Out of stock: Item missing not found in warehouse."}

import pytest
from data.input_code.d06_complex_logic import *

@pytest.mark.parametrize("total_amount, user_tier, promo_code, expected", [
    (150.0, "STANDARD", "ABC-999", 75.0),
    (1200.0, "PLATINUM", "XYZ-999", 600.0),
])
def test_T_MISSING_D5_PROMO_999_SIMPLE(total_amount, user_tier, promo_code, expected):
    assert DiscountEngine.calculate_discount(total_amount, user_tier, promo_code) == expected

import pytest
from data.input_code.d06_complex_logic import *
import data.input_code.d06_complex_logic as logic  # for monkeypatching datetime

def test_T_MISSING_PP_FRAUD(monkeypatch):
    # Patch time to a deterministic hour where no night discount applies
    monkeypatch.setattr(logic, "datetime", _make_fake_datetime(12))
    w = Warehouse({"sku_fraud": 5})
    op = OrderProcessor(w)
    order = {
        "order_id": "ORD-010",
        "user_data": {"email": "user@example.com", "age": 25, "payment_method": "PAYPAL"},
        "items": [{"id": "sku_fraud", "qty": 1, "price": 546.44}],
        "promo_code": None
    }
    with pytest.raises(FraudDetectedError):
        op.process_order(**order)


def test_T_MISSING_PP_PAYPAL_OK(monkeypatch):
    monkeypatch.setattr(logic, "datetime", _make_fake_datetime(12))
    w = Warehouse({"sku_ok": 5})
    op = OrderProcessor(w)
    order = {
        "order_id": "ORD-011",
        "user_data": {"email": "user@example.com", "age": 25, "payment_method": "PAYPAL"},
        "items": [{"id": "sku_ok", "qty": 1, "price": 100.0}],
        "promo_code": None
    }
    expected = {
        "status": "success",
        "order_id": "ORD-011",
        "original_price": 100.0,
        "discount_applied": 0.0,
        "final_total": 122.0,
        "items_count": 1
    }
    assert op.process_order(**order) == expected


def test_T_MISSING_CRYPTO_SUCCESS(monkeypatch):
    monkeypatch.setattr(logic, "datetime", _make_fake_datetime(12))
    w = Warehouse({"cr_item": 5})
    op = OrderProcessor(w)
    order = {
        "order_id": "ORD-012",
        "user_data": {"email": "user@example.com", "age": 25, "payment_method": "CRYPTO"},
        "items": [{"id": "cr_item", "qty": 1, "price": 60.0}],
        "promo_code": None
    }
    expected = {
        "status": "success",
        "order_id": "ORD-012",
        "original_price": 60.0,
        "discount_applied": 0.0,
        "final_total": 73.2,
        "items_count": 1
    }
    assert op.process_order(**order) == expected


def test_T_MISSING_FREEITEMS_RAISES(monkeypatch):
    monkeypatch.setattr(logic, "datetime", _make_fake_datetime(12))
    w = Warehouse({"sku_free": 5})
    op = OrderProcessor(w)
    order = {
        "order_id": "ORD-013",
        "user_data": {"email": "user@example.com", "age": 25},
        "items": [{"id": "sku_free", "qty": -1, "price": 0.0}],
        "promo_code": None
    }
    with pytest.raises(ValueError):
        op.process_order(**order)