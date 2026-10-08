import pytest
from data.input_code.d06_complex_logic import *
import data.input_code.d06_complex_logic as d06

# 1) Warehouse tests
def test_warehouse_check_stock_not_found():
    w = Warehouse({"A1": 10})
    with pytest.raises(InventoryError):
        w.check_stock("B2", 1)

def test_warehouse_lock_item_insufficient():
    w = Warehouse({"A1": 5})
    with pytest.raises(InventoryError):
        w.lock_item("A1", 10)

def test_warehouse_release_item_deletes_lock():
    w = Warehouse({"A1": 5})
    w._locked_stock = {"A1": 5}
    w.release_item("A1", 5)
    assert "A1" not in w._locked_stock

# Helpers for DiscountEngine tests to mock current hour
def _patch_datetime_to_hour(monkeypatch, hour):
    class FakeDateTime:
        @classmethod
        def now(cls):
            class T: pass
            t = T(); t.hour = hour; return t
    monkeypatch.setattr(d06, 'datetime', FakeDateTime)

# 2) DiscountEngine tests
def test_discount_night_gold(monkeypatch):
    _patch_datetime_to_hour(monkeypatch, 2)
    result = DiscountEngine.calculate_discount(200.0, "GOLD", None)
    assert result == pytest.approx(0.15)

def test_discount_platinum_high(monkeypatch):
    _patch_datetime_to_hour(monkeypatch, 14)
    result = DiscountEngine.calculate_discount(1500.0, "PLATINUM", None)
    assert result == 0.25

def test_discount_promo_valid(monkeypatch):
    _patch_datetime_to_hour(monkeypatch, 12)
    result = DiscountEngine.calculate_discount(300.0, "STANDARD", "ABC-123")
    assert result == 0.10

def test_discount_promo_super(monkeypatch):
    _patch_datetime_to_hour(monkeypatch, 9)
    result = DiscountEngine.calculate_discount(800.0, "GOLD", "XYZ-999")
    assert result == 400.0

def test_discount_promo_invalid(monkeypatch):
    _patch_datetime_to_hour(monkeypatch, 1)
    with pytest.raises(ValueError):
        DiscountEngine.calculate_discount(100.0, "STANDARD", "bad_code")

# 3) OrderProcessor tests (validate_user)
@pytest.mark.parametrize("email,age", [
    ("invalid-email", 30),
    ("test@example.com", 16),
    ("elder@example.com", 101),
])
def test_validate_user_raises(email, age):
    w = Warehouse({})
    op = OrderProcessor(w)
    with pytest.raises(UserValidationError):
        op.validate_user(email, age)

# 4) OrderProcessor.process_order tests
def test_orderprocessor_process_order_success(monkeypatch):
    # Patch discount to deterministic 0.40
    monkeypatch.setattr(d06.DiscountEngine, 'calculate_discount', staticmethod(lambda total_price, user_tier, promo_code=None: 0.40))
    # Patch time to night hour 3
    class FakeDateTime:
        @classmethod
        def now(cls):
            class T: pass
            t = T(); t.hour = 3; return t
    monkeypatch.setattr(d06, 'datetime', FakeDateTime)

    warehouse = Warehouse({"A1": 10, "B2": 5})
    op = OrderProcessor(warehouse)
    order = op.process_order(
        "ORD123",
        user_data={
            "email": "user@example.com",
            "age": 35,
            "tier": "PLATINUM",
            "payment_method": "CC"
        },
        items=[
            {"id": "A1", "qty": 2, "price": 600.0},
            {"id": "B2", "qty": 1, "price": 200.0}
        ],
        promo_code="ABC-123"
    )
    assert order["status"] == "success"
    assert order["order_id"] == "ORD123"
    assert order["original_price"] == 1400.0
    assert order["discount_applied"] == 0.40
    assert abs(order["final_total"] - 1024.8) < 1e-6
    assert order["items_count"] == 2

def test_orderprocessor_process_order_inventory_fail():
    warehouse = Warehouse({"A1": 1})
    op = OrderProcessor(warehouse)
    result = op.process_order(
        "ORD124",
        user_data={
            "email": "buyer@example.com",
            "age": 28,
            "tier": "STANDARD",
            "payment_method": "CC"
        },
        items=[
            {"id": "A1", "qty": 2, "price": 50.0}
        ],
        promo_code=None
    )
    assert result == {"status": "failed", "reason": "Out of stock: Insufficient stock for A1"}

def test_orderprocessor_process_order_promo_error():
    warehouse = Warehouse({"A1": 5})
    op = OrderProcessor(warehouse)
    result = op.process_order(
        "ORD125",
        user_data={
            "email": "shopper@example.com",
            "age": 45,
            "tier": "GOLD",
            "payment_method": "CC"
        },
        items=[
            {"id": "A1", "qty": 1, "price": 100.0}
        ],
        promo_code="WRONG-12"
    )
    assert result == {"status": "error", "reason": "Promo Error: Invalid promo code format"}

def test_orderprocessor_process_order_paypal_fraud(monkeypatch):
    warehouse = Warehouse({"A1": 10})
    op = OrderProcessor(warehouse)
    class FakeDateTime:
        @classmethod
        def now(cls):
            class T: pass
            t = T(); t.hour = 10; return t
    monkeypatch.setattr(d06, 'datetime', FakeDateTime)
    with pytest.raises(FraudDetectedError):
        op.process_order(
            "ORD126",
            user_data={
                "email": "fraud@example.com",
                "age": 30,
                "tier": "STANDARD",
                "payment_method": "PAYPAL"
            },
            items=[
                {"id": "A1", "qty": 1, "price": 546.44}
            ],
            promo_code=None
        )

def test_orderprocessor_process_order_crypto_min(monkeypatch):
    warehouse = Warehouse({"A1": 5})
    op = OrderProcessor(warehouse)
    class FakeDateTime:
        @classmethod
        def now(cls):
            class T: pass
            t = T(); t.hour = 11; return t
    monkeypatch.setattr(d06, 'datetime', FakeDateTime)
    with pytest.raises(PaymentError):
        op.process_order(
            "ORD127",
            user_data={
                "email": "crypto@example.com",
                "age": 27,
                "tier": "STANDARD",
                "payment_method": "CRYPTO"
            },
            items=[
                {"id": "A1", "qty": 1, "price": 40.0}
            ],
            promo_code=None
        )

def test_orderprocessor_process_order_negative_qty():
    warehouse = Warehouse({"A1": 5})
    op = OrderProcessor(warehouse)
    with pytest.raises(ValueError):
        op.process_order(
            "ORD128",
            user_data={
                "email": "return@example.com",
                "age": 30,
                "tier": "STANDARD",
                "payment_method": "CC"
            },
            items=[
                {"id": "A1", "qty": -1, "price": 0.0}
            ],
            promo_code=None
        )

def test_warehouse_check_stock_positive():
    w = Warehouse({"A1": 5})
    result = w.check_stock("A1", 3)
    assert result == True

def test_warehouse_lock_item_success():
    w = Warehouse({"A1": 10})
    w.lock_item("A1", 4)
    assert w._locked_stock == {"A1": 4}

def test_warehouse_release_item_no_lock():
    w = Warehouse({"A1": 5})
    w.release_item("A1", 2)
    assert w._locked_stock == {}

def _patch_datetime_to_hour(monkeypatch, hour):
    class FakeDateTime:
        @classmethod
        def now(cls):
            class T: pass
            t = T(); t.hour = hour; return t
    monkeypatch.setattr(d06, 'datetime', FakeDateTime)

def test_discount_no_discount(monkeypatch):
    _patch_datetime_to_hour(monkeypatch, 10)
    result = DiscountEngine.calculate_discount(100.0, "STANDARD", None)
    assert result == 0.0

def test_discount_platinum_no_extra(monkeypatch):
    _patch_datetime_to_hour(monkeypatch, 12)
    result = DiscountEngine.calculate_discount(800.0, "PLATINUM", None)
    assert result == 0.20

def test_discount_cap_reached(monkeypatch):
    _patch_datetime_to_hour(monkeypatch, 2)
    result = DiscountEngine.calculate_discount(1500.0, "PLATINUM", "ABC-123")
    assert result == 0.40

def test_validate_user_success():
    w = Warehouse({})
    op = OrderProcessor(w)
    op.validate_user("valid.user@example.com", 30)

def test_orderprocessor_paypal_nonfraud(monkeypatch):
    _patch_datetime_to_hour(monkeypatch, 10)
    warehouse = Warehouse({"A1": 5})
    op = OrderProcessor(warehouse)
    result = op.process_order(
        "ORD200",
        user_data={
            "email": "buyer@example.com",
            "age": 35,
            "tier": "STANDARD",
            "payment_method": "PAYPAL"
        },
        items=[
            {"id": "A1", "qty": 1, "price": 100.0}
        ],
        promo_code=None
    )
    assert result["status"] == "success"
    assert result["order_id"] == "ORD200"
    assert result["original_price"] == 100.0
    assert "discount_applied" in result
    assert result["items_count"] == 1

def test_orderprocessor_crypto_min_ok(monkeypatch):
    _patch_datetime_to_hour(monkeypatch, 11)
    warehouse = Warehouse({"A1": 5})
    op = OrderProcessor(warehouse)
    result = op.process_order(
        "ORD201",
        user_data={
            "email": "crypto.user@example.com",
            "age": 28,
            "tier": "STANDARD",
            "payment_method": "CRYPTO"
        },
        items=[
            {"id": "A1", "qty": 1, "price": 60.0}
        ],
        promo_code=None
    )
    assert result["status"] == "success"
    assert result["order_id"] == "ORD201"
    assert result["original_price"] == 60.0
    assert "discount_applied" in result
    assert result["items_count"] == 1

def test_orderprocessor_inventory_partial_fail(monkeypatch):
    _patch_datetime_to_hour(monkeypatch, 9)
    warehouse = Warehouse({"A1": 5, "B2": 1})
    op = OrderProcessor(warehouse)
    result = op.process_order(
        "ORD202",
        user_data={
            "email": "shopper@example.com",
            "age": 40,
            "tier": "STANDARD",
            "payment_method": "CC"
        },
        items=[
            {"id": "A1", "qty": 3, "price": 20.0},
            {"id": "B2", "qty": 2, "price": 15.0}
        ],
        promo_code=None
    )
    assert result == {"status": "failed", "reason": "Out of stock: Insufficient stock for B2"}
    assert warehouse._locked_stock == {}

def test_orderprocessor_promo_super_discount(monkeypatch):
    _patch_datetime_to_hour(monkeypatch, 14)
    warehouse = Warehouse({"A1": 5})
    op = OrderProcessor(warehouse)
    result = op.process_order(
        "ORD203",
        user_data={
            "email": "super@example.com",
            "age": 45,
            "tier": "STANDARD",
            "payment_method": "CC"
        },
        items=[
            {"id": "A1", "qty": 2, "price": 100.0}
        ],
        promo_code="XYZ-999"
    )
    assert result["status"] == "success"
    assert result["order_id"] == "ORD203"
    assert result["original_price"] == 200.0
    assert result["discount_applied"] == 100.0
    assert "final_total" in result
    assert result["items_count"] == 1