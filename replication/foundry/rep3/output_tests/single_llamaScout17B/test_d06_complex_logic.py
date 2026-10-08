import pytest
from datetime import datetime
from unittest.mock import patch, MagicMock
from data.input_code.d06_complex_logic import Warehouse, DiscountEngine, OrderProcessor, InventoryError, PaymentError, FraudDetectedError, UserValidationError

def test_warehouse_check_stock():
    warehouse = Warehouse({"item1": 10})
    assert warehouse.check_stock("item1", 5) == True
    assert warehouse.check_stock("item1", 15) == False
    with pytest.raises(InventoryError):
        warehouse.check_stock("item2", 1)



def test_order_processor_validate_user():
    order_processor = OrderProcessor(Warehouse({}))
    order_processor.validate_user("test@example.com", 18)
    with pytest.raises(UserValidationError):
        order_processor.validate_user("invalid", 18)
    with pytest.raises(UserValidationError):
        order_processor.validate_user("test@example.com", 17)
    with pytest.raises(UserValidationError):
        order_processor.validate_user("test@example.com", 101)

def test_order_processor_process_order():
    warehouse = Warehouse({"item1": 10})
    order_processor = OrderProcessor(warehouse)
    user_data = {"email": "test@example.com", "age": 18, "tier": "STANDARD"}
    items = [{"id": "item1", "qty": 5, "price": 10.0}]
    result = order_processor.process_order("order1", user_data, items)
    assert result["status"] == "success"

def test_order_processor_process_order_out_of_stock():
    warehouse = Warehouse({"item1": 0})
    order_processor = OrderProcessor(warehouse)
    user_data = {"email": "test@example.com", "age": 18, "tier": "STANDARD"}
    items = [{"id": "item1", "qty": 5, "price": 10.0}]
    result = order_processor.process_order("order1", user_data, items)
    assert result["status"] == "failed"

def test_order_processor_process_order_invalid_promo_code():
    warehouse = Warehouse({"item1": 10})
    order_processor = OrderProcessor(warehouse)
    user_data = {"email": "test@example.com", "age": 18, "tier": "STANDARD"}
    items = [{"id": "item1", "qty": 5, "price": 10.0}]
    result = order_processor.process_order("order1", user_data, items, "invalid")
    assert result["status"] == "error"


def test_order_processor_process_order_crypto_payment_error():
    warehouse = Warehouse({"item1": 10})
    order_processor = OrderProcessor(warehouse)
    user_data = {"email": "test@example.com", "age": 18, "tier": "STANDARD", "payment_method": "CRYPTO"}
    items = [{"id": "item1", "qty": 1, "price": 10.0}]  # total < 50 after discount and tax
    with pytest.raises(PaymentError):
        order_processor.process_order("order1", user_data, items)

def test_order_processor_process_order_return_free_items():
    warehouse = Warehouse({"item1": 10})
    order_processor = OrderProcessor(warehouse)
    user_data = {"email": "test@example.com", "age": 18, "tier": "STANDARD"}
    items = [{"id": "item1", "qty": -1, "price": 0.0}]
    with pytest.raises(ValueError):
        order_processor.process_order("order1", user_data, items)