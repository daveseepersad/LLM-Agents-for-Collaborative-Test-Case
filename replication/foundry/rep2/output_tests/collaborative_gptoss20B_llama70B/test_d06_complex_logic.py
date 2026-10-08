import pytest
from data.input_code.d06_complex_logic import *
from datetime import datetime
from unittest.mock import patch, MagicMock

@pytest.mark.parametrize('total_amount, user_tier, promo_code, expected', [
    (900.0, "PLATINUM", "ABC-123", 0.30),
    (100.0, "STANDARD", "ABC-999", 50.0)
])
def test_discount_engine_success(total_amount, user_tier, promo_code, expected):
    assert round(DiscountEngine.calculate_discount(total_amount, user_tier, promo_code), 2) == round(expected, 2)

def test_discount_engine_error():
    with pytest.raises(ValueError):
        DiscountEngine.calculate_discount(100.0, "STANDARD", "BADPROMO")


@pytest.mark.parametrize('initial_stock, item_id, quantity, expected', [
    ({"A": 5}, "A", 3, True),
    ({"A": 1}, "A", 2, False)
])
def test_warehouse_check_stock(initial_stock, item_id, quantity, expected):
    warehouse = Warehouse(initial_stock)
    assert warehouse.check_stock(item_id, quantity) == expected

def test_warehouse_lock_item():
    warehouse = Warehouse({"A": 5})
    warehouse.lock_item("A", 3)
    assert warehouse._locked_stock["A"] == 3

def test_warehouse_release_item():
    warehouse = Warehouse({"A": 5})
    warehouse.lock_item("A", 3)
    warehouse.release_item("A", 3)
    assert "A" not in warehouse._locked_stock


def test_order_processor_error():
    with pytest.raises(ValueError):
        warehouse = Warehouse({"X": 10})
        order_processor = OrderProcessor(warehouse)
        order_processor.process_order("ORD3", {"email": "edge@example.com", "age": 30}, [{"id": "F", "qty": -1, "price": 0.0}], None)

def test_order_processor_paypal_fraud():
    with pytest.raises(FraudDetectedError):
        warehouse = Warehouse({"F": 10})
        order_processor = OrderProcessor(warehouse)
        order_processor.process_order("ORD4", {"email": "fraud@example.com", "age": 28, "payment_method": "PAYPAL"}, [{"id": "F", "qty": 1, "price": 546.44}], None)

def test_order_processor_crypto_minimum():
    with pytest.raises(PaymentError):
        warehouse = Warehouse({"C": 10})
        order_processor = OrderProcessor(warehouse)
        order_processor.process_order("ORD5", {"email": "crypto@example.com", "age": 30, "payment_method": "CRYPTO"}, [{"id": "C", "qty": 1, "price": 40.0}], None)

def test_order_processor_out_of_stock():
    warehouse = Warehouse({"Y": 1})
    order_processor = OrderProcessor(warehouse)
    result = order_processor.process_order("ORD6", {"email": "inventory@example.com", "age": 30}, [{"id": "Y", "qty": 2, "price": 5.0}], None)
    assert result["status"] == "failed"
    assert "Out of stock" in result["reason"]


def test_discount_engine_success_abc_999():
    assert DiscountEngine.calculate_discount(100.0, "STANDARD", "ABC-999") == 50.0