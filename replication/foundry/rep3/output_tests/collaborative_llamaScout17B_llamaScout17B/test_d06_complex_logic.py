import pytest
from data.input_code.d06_complex_logic import *
from unittest.mock import Mock

@pytest.mark.parametrize('email, age, expected', [
    ("test@example.com", 25, None),
    ("invalid", 25, UserValidationError),
    ("test@example.com", 17, UserValidationError),
    ("test@example.com", 101, UserValidationError)
])
def test_validate_user(email, age, expected):
    processor = OrderProcessor(Warehouse({}))
    if expected is None:
        processor.validate_user(email, age)
    else:
        with pytest.raises(expected):
            processor.validate_user(email, age)

@pytest.mark.parametrize('item_id, quantity, initial_stock, expected', [
    ("item1", 5, {"item1": 10}, True),
    ("item1", 15, {"item1": 10}, False),
    ("nonexistent", 1, {"item1": 10}, InventoryError)
])
def test_check_stock(item_id, quantity, initial_stock, expected):
    warehouse = Warehouse(initial_stock)
    if isinstance(expected, bool):
        assert warehouse.check_stock(item_id, quantity) == expected
    else:
        with pytest.raises(expected):
            warehouse.check_stock(item_id, quantity)

@pytest.mark.parametrize('item_id, quantity, initial_stock, expected', [
    ("item1", 5, {"item1": 10}, None),
    ("item1", 15, {"item1": 10}, InventoryError)
])
def test_lock_item(item_id, quantity, initial_stock, expected):
    warehouse = Warehouse(initial_stock)
    if expected is None:
        warehouse.lock_item(item_id, quantity)
    else:
        with pytest.raises(expected):
            warehouse.lock_item(item_id, quantity)

@pytest.mark.parametrize('total_amount, user_tier, promo_code, expected', [
    (100.0, "STANDARD", None, 0.0),
    (100.0, "GOLD", None, 0.10),
    (100.0, "PLATINUM", None, 0.20),
    (1001.0, "PLATINUM", None, 0.25),
    (100.0, "STANDARD", "ABC-123", 0.10),
    (100.0, "STANDARD", "invalid", ValueError),
    (100.0, "STANDARD", "ABC-999", 0.50) 
])
def test_calculate_discount(total_amount, user_tier, promo_code, expected, mocker):
    mocker.patch('datetime.datetime.now', return_value=mocker.Mock(hour=12))
    if isinstance(expected, float):
        if promo_code == "ABC-999":
            assert DiscountEngine.calculate_discount(total_amount, user_tier, promo_code) == total_amount * expected
        else:
            assert DiscountEngine.calculate_discount(total_amount, user_tier, promo_code) == expected
    else:
        with pytest.raises(expected):
            DiscountEngine.calculate_discount(total_amount, user_tier, promo_code)

@pytest.mark.parametrize('order_id, user_data, items, promo_code, initial_stock, expected', [
    ("1", {"email": "test@example.com", "age": 25, "tier": "STANDARD"}, [{"id": "item1", "qty": 1, "price": 10.0}], None, {"item1": 10}, 
     {"status": "success", "order_id": "1", "original_price": 10.0, "discount_applied": 0.0, "final_total": round(10.0 * 1.22, 2), "items_count": 1}),
    ("1", {"email": "test@example.com", "age": 25, "tier": "STANDARD"}, [{"id": "item1", "qty": 15, "price": 10.0}], None, {"item1": 10}, 
     {"status": "failed", "reason": "Out of stock: Insufficient stock for item1"}),
    ("1", {"email": "test@example.com", "age": 25, "tier": "STANDARD"}, [{"id": "item1", "qty": 1, "price": 10.0}], "invalid", {"item1": 10}, 
     {"status": "error", "reason": "Promo Error: Invalid promo code format"}),
    ("1", {"email": "test@example.com", "age": 25, "tier": "STANDARD", "payment_method": "PAYPAL"}, [{"id": "item1", "qty": 1, "price": 666.66}], None, {"item1": 10}, FraudDetectedError),
    ("1", {"email": "test@example.com", "age": 25, "tier": "STANDARD", "payment_method": "CRYPTO"}, [{"id": "item1", "qty": 1, "price": 10.0}], None, {"item1": 10}, PaymentError),
    ("1", {"email": "test@example.com", "age": 25, "tier": "STANDARD", "payment_method": "PAYPAL"}, [{"id": "item1", "qty": 1, "price": 545.17}], None, {"item1": 10}, 
     {"status": "success", "order_id": "1", "original_price": 545.17, "discount_applied": 0.0, "final_total": round(545.17 * 1.22, 2), "items_count": 1})
])
def test_process_order(order_id, user_data, items, promo_code, initial_stock, expected, mocker):
    mocker.patch('datetime.datetime.now', return_value=mocker.Mock(hour=12))
    warehouse = Warehouse(initial_stock)
    processor = OrderProcessor(warehouse)
    if isinstance(expected, dict):
        result = processor.process_order(order_id, user_data, items, promo_code)
        assert result == expected  
    else:
        with pytest.raises(expected):
            processor.process_order(order_id, user_data, items, promo_code)