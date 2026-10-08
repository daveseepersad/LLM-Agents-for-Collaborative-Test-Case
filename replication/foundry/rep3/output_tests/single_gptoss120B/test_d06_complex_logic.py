import pytest
import re
from datetime import datetime, timedelta

from data.input_code.d06_complex_logic import (
    Warehouse,
    DiscountEngine,
    OrderProcessor,
    InventoryError,
    PaymentError,
    FraudDetectedError,
    UserValidationError,
)


def test_warehouse_basic_operations():
    wh = Warehouse({"item1": 5, "item2": 10})
    # check stock exists
    assert wh.check_stock("item1", 3) is True
    # lock some items
    wh.lock_item("item1", 3)
    assert wh.check_stock("item1", 3) is False  # only 2 left
    # release part of the lock
    wh.release_item("item1", 2)
    assert wh.check_stock("item1", 3) is True  # now 4 available
    # release remaining lock should delete entry
    wh.release_item("item1", 2)
    assert "item1" not in wh._locked_stock

    # missing item raises
    with pytest.raises(InventoryError):
        wh.check_stock("missing", 1)

    # insufficient stock raises on lock
    with pytest.raises(InventoryError):
        wh.lock_item("item2", 20)




def test_order_processor_user_validation():
    wh = Warehouse({"a": 1})
    proc = OrderProcessor(wh)

    # Invalid email
    with pytest.raises(UserValidationError):
        proc.validate_user("invalid-email", 30)

    # Underage
    with pytest.raises(UserValidationError):
        proc.validate_user("test@example.com", 17)

    # Over 100
    with pytest.raises(UserValidationError):
        proc.validate_user("test@example.com", 101)


def test_process_order_success_basic():
    wh = Warehouse({"item1": 10})
    proc = OrderProcessor(wh)

    order = proc.process_order(
        order_id="ORD1",
        user_data={"email": "user@example.com", "age": 30},
        items=[{"id": "item1", "qty": 2, "price": 10.0}],
    )
    assert order["status"] == "success"
    assert order["original_price"] == 20.0
    assert order["discount_applied"] == 0.0
    assert order["final_total"] == round(20.0 * 1.22, 2)
    assert order["items_count"] == 1






def test_process_order_invalid_promo_returns_error():
    wh = Warehouse({"item1": 5})
    proc = OrderProcessor(wh)

    result = proc.process_order(
        order_id="ORD4",
        user_data={"email": "user@example.com", "age": 30},
        items=[{"id": "item1", "qty": 1, "price": 10.0}],
        promo_code="BAD-CODE",
    )
    assert result["status"] == "error"
    assert "Promo Error" in result["reason"]


def test_process_order_inventory_failure_rollback():
    wh = Warehouse({"item1": 1, "item2": 5})
    proc = OrderProcessor(wh)

    result = proc.process_order(
        order_id="ORD5",
        user_data={"email": "user@example.com", "age": 30},
        items=[
            {"id": "item1", "qty": 1, "price": 10.0},
            {"id": "item2", "qty": 10, "price": 5.0},  # exceeds stock
        ],
    )
    assert result["status"] == "failed"
    assert "Out of stock" in result["reason"]
    # Ensure first lock was released
    assert wh._locked_stock == {}


def test_process_order_paypal_fraud(monkeypatch):
    wh = Warehouse({"item1": 10})
    proc = OrderProcessor(wh)
    # Set tax_rate to 0 to make final amount equal to total
    proc.tax_rate = 0.0

    # total price exactly 666.66, no discount
    result = None
    with pytest.raises(FraudDetectedError):
        proc.process_order(
            order_id="ORD6",
            user_data={
                "email": "user@example.com",
                "age": 30,
                "payment_method": "PAYPAL",
            },
            items=[{"id": "item1", "qty": 1, "price": 666.66}],
        )


def test_process_order_crypto_min_amount():
    wh = Warehouse({"item1": 10})
    proc = OrderProcessor(wh)

    # total 40, after tax 48.8 (<50) should raise PaymentError
    with pytest.raises(PaymentError):
        proc.process_order(
            order_id="ORD7",
            user_data={
                "email": "user@example.com",
                "age": 30,
                "payment_method": "CRYPTO",
            },
            items=[{"id": "item1", "qty": 1, "price": 40.0}],
        )