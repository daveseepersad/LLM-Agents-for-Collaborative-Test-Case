import pytest
from data.input_code.d06_complex_logic import *

def test_module_imports():
    import importlib
    mod = importlib.import_module("data.input_code.d06_complex_logic")
    assert mod is not None

import pytest
from data.input_code.d06_complex_logic import *

def test_warehouse_check_stock_success():
    w = Warehouse({"A1": 5})
    assert w.check_stock("A1", 3) is True

def test_warehouse_check_stock_not_found():
    w = Warehouse({"A1": 5})
    with pytest.raises(InventoryError):
        w.check_stock("UNKNOWN", 1)

def test_warehouse_lock_and_release():
    w = Warehouse({"B2": 5})
    w.lock_item("B2", 4)
    assert w.check_stock("B2", 1) is True
    w.release_item("B2", 4)
    assert w.check_stock("B2", 5) is True

def test_discount_night_gold_promo(monkeypatch):
    class FakeDateTime:
        @classmethod
        def now(cls):
            class T:
                hour = 2
            return T()
    monkeypatch.setattr("data.input_code.d06_complex_logic.datetime", FakeDateTime)
    discount = DiscountEngine.calculate_discount(200.0, "GOLD", "ABC-123")
    assert discount == 0.25

def test_discount_platinum_super():
    discount = DiscountEngine.calculate_discount(1500.0, "PLATINUM", "XYZ-999")
    assert discount == 750.0

def test_discount_invalid_promo_raises():
    with pytest.raises(ValueError):
        DiscountEngine.calculate_discount(100.0, "STANDARD", "bad_code")

def test_validate_user_invalid_email():
    w = Warehouse({"X": 1})
    op = OrderProcessor(w)
    with pytest.raises(UserValidationError):
        op.validate_user("invalid_email@", 30)

def test_validate_user_underage():
    w = Warehouse({"X": 1})
    op = OrderProcessor(w)
    with pytest.raises(UserValidationError):
        op.validate_user("test@example.com", 16)

def test_validate_user_overage():
    w = Warehouse({"X": 1})
    op = OrderProcessor(w)
    with pytest.raises(UserValidationError):
        op.validate_user("senior@example.com", 101)

def test_process_order_success():
    w = Warehouse({"C3": 2})
    op = OrderProcessor(w)
    res = op.process_order(
        "ORD123",
        {"email": "user@test.com", "age": 30, "tier": "STANDARD", "payment_method": "CC"},
        [{"id": "C3", "qty": 2, "price": 50.0}],
        promo_code=None
    )
    expected = {
        "status": "success",
        "order_id": "ORD123",
        "original_price": 100.0,
        "discount_applied": 0.0,
        "final_total": 122.0,
        "items_count": 1
    }
    assert res == expected

def test_process_order_inventory_fail():
    w = Warehouse({"D4": 5})
    op = OrderProcessor(w)
    res = op.process_order(
        "ORD124",
        {"email": "buyer@test.com", "age": 25, "tier": "STANDARD", "payment_method": "CC"},
        [{"id": "D4", "qty": 10, "price": 20.0}],
        promo_code=None
    )
    assert res == {
        "status": "failed",
        "reason": "Out of stock: Insufficient stock for D4"
    }

def test_process_order_promo_error():
    w = Warehouse({"E5": 5})
    op = OrderProcessor(w)
    res = op.process_order(
        "ORD125",
        {"email": "shopper@test.com", "age": 40, "tier": "STANDARD", "payment_method": "CC"},
        [{"id": "E5", "qty": 1, "price": 30.0}],
        "WRONG-12"
    )
    assert res == {
        "status": "error",
        "reason": "Promo Error: Invalid promo code format"
    }

def test_process_order_paypal_fraud():
    w = Warehouse({"F6": 1})
    op = OrderProcessor(w)
    with pytest.raises(FraudDetectedError):
        op.process_order(
            "ORD126",
            {"email": "fraud@test.com", "age": 35, "tier": "STANDARD", "payment_method": "PAYPAL"},
            [{"id": "F6", "qty": 1, "price": 546.44}],
            None
        )

def test_process_order_crypto_error():
    w = Warehouse({"G7": 2})
    op = OrderProcessor(w)
    with pytest.raises(PaymentError):
        op.process_order(
            "ORD127",
            {"email": "crypto@test.com", "age": 28, "tier": "STANDARD", "payment_method": "CRYPTO"},
            [{"id": "G7", "qty": 1, "price": 40.0}],
            None
        )

def test_process_order_return_free_item():
    w = Warehouse({"H8": 2})
    op = OrderProcessor(w)
    with pytest.raises(ValueError):
        op.process_order(
            "ORD128",
            {"email": "return@test.com", "age": 45, "tier": "STANDARD", "payment_method": "CC"},
            [{"id": "H8", "qty": -1, "price": 0.0}],
            None
        )