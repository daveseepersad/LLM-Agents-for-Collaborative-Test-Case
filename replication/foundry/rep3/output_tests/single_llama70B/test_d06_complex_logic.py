import pytest
from data.input_code.d06_complex_logic import Warehouse, DiscountEngine, OrderProcessor, InventoryError, PaymentError, FraudDetectedError, UserValidationError
from unittest.mock import patch, MagicMock
from datetime import datetime
import re

@pytest.fixture
def warehouse():
    return Warehouse({"item1": 10, "item2": 20})

@pytest.fixture
def order_processor(warehouse):
    return OrderProcessor(warehouse)

def test_warehouse_check_stock(warehouse):
    assert warehouse.check_stock("item1", 5) == True
    with pytest.raises(InventoryError):
        warehouse.check_stock("item3", 5)

def test_warehouse_lock_item(warehouse):
    warehouse.lock_item("item1", 5)
    assert warehouse._locked_stock["item1"] == 5

def test_warehouse_release_item(warehouse):
    warehouse.lock_item("item1", 5)
    warehouse.release_item("item1", 5)
    assert "item1" not in warehouse._locked_stock



def test_order_processor_validate_user(order_processor):
    with pytest.raises(UserValidationError):
        order_processor.validate_user("invalid-email", 18)
    with pytest.raises(UserValidationError):
        order_processor.validate_user("test@test.com", 17)
    with pytest.raises(UserValidationError):
        order_processor.validate_user("test@test.com", 101)

def test_order_processor_process_order_success(order_processor):
    user_data = {"email": "test@test.com", "age": 18, "tier": "GOLD", "payment_method": "CC"}
    items = [{"id": "item1", "qty": 5, "price": 10.0}]
    result = order_processor.process_order("order1", user_data, items)
    assert result["status"] == "success"

def test_order_processor_process_order_out_of_stock(order_processor):
    user_data = {"email": "test@test.com", "age": 18, "tier": "GOLD", "payment_method": "CC"}
    items = [{"id": "item1", "qty": 15, "price": 10.0}]
    result = order_processor.process_order("order1", user_data, items)
    assert result["status"] == "failed"

def test_order_processor_process_order_invalid_promo_code(order_processor):
    user_data = {"email": "test@test.com", "age": 18, "tier": "GOLD", "payment_method": "CC"}
    items = [{"id": "item1", "qty": 5, "price": 10.0}]
    result = order_processor.process_order("order1", user_data, items, "invalid-promo-code")
    assert result["status"] == "error"




@patch("re.match")
def test_discount_engine_calculate_discount_promo_code_regex(mock_match):
    mock_match.return_value = None
    with pytest.raises(ValueError):
        DiscountEngine.calculate_discount(100.0, "GOLD", "ABC-123")

