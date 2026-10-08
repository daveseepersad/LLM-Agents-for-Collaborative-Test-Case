import pytest
from datetime import datetime
from data.input_code.d06_complex_logic import (
    Warehouse,
    DiscountEngine,
    OrderProcessor,
    InventoryError,
    PaymentError,
    FraudDetectedError,
    UserValidationError,
)

# Mocking datetime for DiscountEngine tests
from unittest.mock import patch

# Test cases for Warehouse class
def test_check_stock():
    warehouse = Warehouse({"item1": 10})
    assert warehouse.check_stock("item1", 5) is True
    assert warehouse.check_stock("item1", 15) is False
    with pytest.raises(InventoryError):
        warehouse.check_stock("item2", 1)

def test_lock_item():
    warehouse = Warehouse({"item1": 10})
    warehouse.lock_item("item1", 5)
    assert warehouse._locked_stock["item1"] == 5
    with pytest.raises(InventoryError):
        warehouse.lock_item("item1", 6)

def test_release_item():
    warehouse = Warehouse({"item1": 10})
    warehouse.lock_item("item1", 5)
    warehouse.release_item("item1", 5)
    assert "item1" not in warehouse._locked_stock

# Test cases for DiscountEngine class

def test_calculate_discount_tier():
    discount = DiscountEngine.calculate_discount(100.0, "GOLD")
    assert discount == 0.10
    discount = DiscountEngine.calculate_discount(1000.0, "PLATINUM")
    assert discount == 0.20
    discount = DiscountEngine.calculate_discount(1500.0, "PLATINUM")
    assert discount == 0.25


def test_calculate_discount_invalid_promo_code():
    with pytest.raises(ValueError):
        DiscountEngine.calculate_discount(100.0, "GOLD", "INVALID")

# Test cases for OrderProcessor class
def test_validate_user():
    processor = OrderProcessor(Warehouse({}))
    processor.validate_user("test@test.com", 25)
    with pytest.raises(UserValidationError):
        processor.validate_user("invalid-email", 25)
    with pytest.raises(UserValidationError):
        processor.validate_user("test@test.com", 17)
    with pytest.raises(UserValidationError):
        processor.validate_user("test@test.com", 101)

def test_process_order_success():
    warehouse = Warehouse({"item1": 10})
    processor = OrderProcessor(warehouse)
    user_data = {"email": "test@test.com", "age": 25, "tier": "GOLD", "payment_method": "CC"}
    items = [{"id": "item1", "qty": 5, "price": 10.0}]
    result = processor.process_order("order1", user_data, items)
    assert result["status"] == "success"

def test_process_order_insufficient_stock():
    warehouse = Warehouse({"item1": 2})
    processor = OrderProcessor(warehouse)
    user_data = {"email": "test@test.com", "age": 25, "tier": "GOLD", "payment_method": "CC"}
    items = [{"id": "item1", "qty": 5, "price": 10.0}]
    result = processor.process_order("order1", user_data, items)
    assert result["status"] == "failed"

def test_process_order_invalid_promo_code():
    warehouse = Warehouse({"item1": 10})
    processor = OrderProcessor(warehouse)
    user_data = {"email": "test@test.com", "age": 25, "tier": "GOLD", "payment_method": "CC"}
    items = [{"id": "item1", "qty": 5, "price": 10.0}]
    result = processor.process_order("order1", user_data, items, "INVALID")
    assert result["status"] == "error"


def test_process_order_crypto_minimum():
    warehouse = Warehouse({"item1": 10})
    processor = OrderProcessor(warehouse)
    user_data = {"email": "test@test.com", "age": 25, "tier": "GOLD", "payment_method": "CRYPTO"}
    items = [{"id": "item1", "qty": 1, "price": 10.0}]
    with pytest.raises(PaymentError):
        processor.process_order("order1", user_data, items)