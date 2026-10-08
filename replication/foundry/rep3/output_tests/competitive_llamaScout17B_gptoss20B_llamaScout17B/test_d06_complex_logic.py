import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime
from data.input_code.d06_complex_logic import *

@pytest.mark.parametrize("email, age, expected", [
    ("test@example.com", 18, None),
    ("invalid_email", 18, UserValidationError),
    ("test@example.com", 17, UserValidationError),
    ("test@example.com", 101, UserValidationError),
])
def test_validate_user(email, age, expected):
    order_processor = OrderProcessor(Warehouse({}))
    if expected is None:
        order_processor.validate_user(email, age)
    else:
        with pytest.raises(expected):
            order_processor.validate_user(email, age)

def test_calculate_discount():
    # Test discount calculation logic
    assert DiscountEngine.calculate_discount(100, "STANDARD") == min(0.0 + (datetime.now().hour < 6 and 0.05 or 0.0), 0.40)
    assert DiscountEngine.calculate_discount(100, "GOLD") == min(0.10 + (datetime.now().hour < 6 and 0.05 or 0.0), 0.40)
    assert DiscountEngine.calculate_discount(1001, "PLATINUM") == min(0.20 + 0.05 + (datetime.now().hour < 6 and 0.05 or 0.0), 0.40)
    with pytest.raises(ValueError):
        DiscountEngine.calculate_discount(100, "STANDARD", "invalid_promo")


def test_process_order_stock_failure():
    warehouse = Warehouse({"item1": 10})
    order_processor = OrderProcessor(warehouse)
    user_data = {"email": "test@example.com", "age": 30, "tier": "STANDARD"}
    items = [{"id": "item1", "qty": 11, "price": 10.0}]  # Quantity exceeds stock
    result = order_processor.process_order("order1", user_data, items)
    assert result["status"] == "failed"
    assert "Out of stock" in result["reason"]

def test_process_order_invalid_promo_code():
    warehouse = Warehouse({"item1": 10})
    order_processor = OrderProcessor(warehouse)
    user_data = {"email": "test@example.com", "age": 30, "tier": "STANDARD"}
    items = [{"id": "item1", "qty": 1, "price": 10.0}]
    result = order_processor.process_order("order1", user_data, items, "invalid_promo")
    assert result["status"] == "error"
    assert "Promo Error" in result["reason"]

@patch('data.input_code.d06_complex_logic.datetime')
def test_process_order_success(mock_datetime):
    mock_datetime.now.return_value = datetime(2023, 1, 1, 12, 0, 0)
    warehouse = Warehouse({"item1": 10})
    order_processor = OrderProcessor(warehouse)
    user_data = {"email": "test@example.com", "age": 30, "tier": "GOLD", "payment_method": "CC"}
    items = [{"id": "item1", "qty": 1, "price": 100.0}]
    result = order_processor.process_order("order1", user_data, items)
    assert result["status"] == "success"
    assert result["original_price"] == 100.0
    assert round(result["discount_applied"], 2) == 0.10  # GOLD tier discount
    assert result["final_total"] > 0

@patch('data.input_code.d06_complex_logic.datetime')
def test_process_order_payment_failure(mock_datetime):
    mock_datetime.now.return_value = datetime(2023, 1, 1, 12, 0, 0)
    warehouse = Warehouse({"item1": 10})
    order_processor = OrderProcessor(warehouse)
    user_data = {"email": "test@example.com", "age": 30, "tier": "STANDARD", "payment_method": "PAYPAL"}
    items = [{"id": "item1", "qty": 1, "price": 546.44}]  # Adjusted price to trigger FraudDetectedError (ROUND(1.22*546.44) == 666.66)
    with pytest.raises(FraudDetectedError):
        order_processor.process_order("order1", user_data, items)

def test_process_order_crypto_payment_failure():
    warehouse = Warehouse({"item1": 10})
    order_processor = OrderProcessor(warehouse)
    user_data = {"email": "test@example.com", "age": 30, "tier": "STANDARD", "payment_method": "CRYPTO"}
    items = [{"id": "item1", "qty": 1, "price": 10.0}]  # Below minimum crypto amount
    with pytest.raises(PaymentError):
        order_processor.process_order("order1", user_data, items)

@patch('data.input_code.d06_complex_logic.datetime')
def test_calculate_discount_night_hour(mock_datetime):
    mock_datetime.now.return_value = datetime(2023, 1, 1, 4, 0, 0)  # Night hour
    total_amount = 100.0
    user_tier = "STANDARD"
    discount = DiscountEngine.calculate_discount(total_amount, user_tier)
    assert discount == 0.05

@patch('data.input_code.d06_complex_logic.datetime')
def test_calculate_discount_platinum_tier(mock_datetime):
    mock_datetime.now.return_value = datetime(2023, 1, 1, 12, 0, 0)
    total_amount = 100.0
    user_tier = "PLATINUM"
    discount = DiscountEngine.calculate_discount(total_amount, user_tier)
    assert discount == 0.20

def test_process_order_division_by_zero():
    warehouse = Warehouse({"item1": 10})
    order_processor = OrderProcessor(warehouse)
    user_data = {"email": "test@example.com", "age": 30}
    items = [{"id": "item1", "qty": -1, "price": 0.0}]
    with pytest.raises(ValueError):
        order_processor.process_order("order1", user_data, items)

@patch('data.input_code.d06_complex_logic.datetime')
def test_process_order_crypto_payment_success(mock_datetime):
    mock_datetime.now.return_value = datetime(2023, 1, 1, 12, 0, 0)
    warehouse = Warehouse({"item1": 10})
    order_processor = OrderProcessor(warehouse)
    user_data = {"email": "test@example.com", "age": 30, "payment_method": "CRYPTO"}
    items = [{"id": "item1", "qty": 1, "price": 50.0}]
    result = order_processor.process_order("order1", user_data, items)
    assert result["status"] == "success"

def test_warehouse_release_item_zero_quantity():
    warehouse = Warehouse({"item1": 10})
    warehouse.lock_item("item1", 5)
    warehouse.release_item("item1", 0)
    assert "item1" in warehouse._locked_stock
    assert warehouse._locked_stock["item1"] == 5

@patch('data.input_code.d06_complex_logic.datetime')
def test_process_order_invalid_payment_method(mock_datetime):
    mock_datetime.now.return_value = datetime(2023, 1, 1, 12, 0, 0)
    warehouse = Warehouse({"item1": 10})
    order_processor = OrderProcessor(warehouse)
    user_data = {"email": "test@example.com", "age": 30, "payment_method": "INVALID"}
    items = [{"id": "item1", "qty": 1, "price": 10.0}]
    result = order_processor.process_order("order1", user_data, items)
    assert result["status"] == "success"

def test_missing_warehouse_item_not_found():
    warehouse = Warehouse({})
    with pytest.raises(InventoryError):
        warehouse.check_stock("nonexistent_item", 1)

def test_missing_warehouse_lock_item_not_found():
    warehouse = Warehouse({})
    with pytest.raises(InventoryError):
        warehouse.lock_item("nonexistent_item", 1)

def test_release_item_not_found_no_exception():
    warehouse = Warehouse({})
    # Should not raise an exception when releasing an item that was never locked
    warehouse.release_item("nonexistent_item", 1)

@patch('data.input_code.d06_complex_logic.datetime')
def test_discount_engine_night_gold_tier(mock_datetime):
    mock_datetime.now.return_value = datetime(2023, 1, 1, 3, 0, 0)
    discount = DiscountEngine.calculate_discount(100.0, "GOLD")
    assert round(discount, 2) == 0.15

def test_order_processor_missing_user_data():
    warehouse = Warehouse({"item1": 10})
    order_processor = OrderProcessor(warehouse)
    input_data = {"order_id": "order1", "user_data": {}, "items": [{"id": "item1", "qty": 1, "price": 10.0}]}
    with pytest.raises(UserValidationError):
        order_processor.process_order(input_data["order_id"], input_data["user_data"], input_data["items"])

def test_order_processor_empty_items_list():
    warehouse = Warehouse({"item1": 10})
    order_processor = OrderProcessor(warehouse)
    user_data = {"email": "test@example.com", "age": 30}
    items = []
    result = order_processor.process_order("order1", user_data, items)
    assert result["status"] == "success"
    assert result["items_count"] == 0
    assert result["original_price"] == 0.0

@patch('data.input_code.d06_complex_logic.datetime')
def test_order_processor_paypal_success(mock_datetime):
    mock_datetime.now.return_value = datetime(2023, 1, 1, 12, 0, 0)
    warehouse = Warehouse({"item1": 10})
    order_processor = OrderProcessor(warehouse)
    user_data = {"email": "test@example.com", "age": 30, "payment_method": "PAYPAL"}
    items = [{"id": "item1", "qty": 1, "price": 100.0}]
    result = order_processor.process_order("order1", user_data, items)
    assert result["status"] == "success"

@patch('data.input_code.d06_complex_logic.datetime')
def test_order_processor_crypto_min_amount(mock_datetime):
    mock_datetime.now.return_value = datetime(2023, 1, 1, 12, 0, 0)
    warehouse = Warehouse({"item1": 10})
    order_processor = OrderProcessor(warehouse)
    user_data = {"email": "test@example.com", "age": 30, "payment_method": "CRYPTO"}
    items = [{"id": "item1", "qty": 1, "price": 50.0}]
    result = order_processor.process_order("order1", user_data, items)
    assert result["status"] == "success"