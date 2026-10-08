import pytest
from data.input_code.d06_complex_logic import *
from unittest.mock import patch
from datetime import datetime

@pytest.mark.parametrize('initial_stock, item_id, quantity, expected', [
    ({"A": 5}, "B", 1, InventoryError),
    ({"A": 10}, "A", 5, True),
    ({"A": 0}, "A", 1, False)
])
def test_Warehouse_check_stock(initial_stock, item_id, quantity, expected):
    warehouse = Warehouse(initial_stock)
    if isinstance(expected, type) and issubclass(expected, Exception):
        with pytest.raises(expected):
            warehouse.check_stock(item_id, quantity)
    else:
        assert warehouse.check_stock(item_id, quantity) == expected

@pytest.mark.parametrize('initial_stock, item_id, quantity, expected', [
    ({"A": 3}, "A", 5, InventoryError),
    ({"A": 10}, "A", 3, None),
    ({"A": 0}, "A", 1, InventoryError)
])
def test_Warehouse_lock_item(initial_stock, item_id, quantity, expected):
    warehouse = Warehouse(initial_stock)
    if isinstance(expected, type) and issubclass(expected, Exception):
        with pytest.raises(expected):
            warehouse.lock_item(item_id, quantity)
    else:
        warehouse.lock_item(item_id, quantity)

@pytest.mark.parametrize('total_amount, user_tier, promo_code, expected', [
    (50.0, "STANDARD", "abc", ValueError),
    (100.0, "STANDARD", "ABC-999", 0.5),
    (1500.0, "PLATINUM", None, 0.25),
    (100.0, "GOLD", None, 0.1),
    (100.0, "STANDARD", None, 0.05),  
    (50.0, "STANDARD", "ABC-123", 0.15),
    (1000.0, "PLATINUM", "ABC-123", 0.3)
])
def test_DiscountEngine_calculate_discount(mocker, total_amount, user_tier, promo_code, expected):
    if promo_code is None and expected == 0.05:  
        mocker.patch('datetime.datetime.now', return_value=datetime(2023, 1, 1, 2, 0, 0))
    if isinstance(expected, type) and issubclass(expected, Exception):
        with pytest.raises(expected):
            DiscountEngine.calculate_discount(total_amount, user_tier, promo_code)
    else:
        assert round(DiscountEngine.calculate_discount(total_amount, user_tier, promo_code), 2) == expected

@pytest.mark.parametrize('email, age, expected', [
    ("bademail", 25, UserValidationError),
    ("test@example.com", 17, UserValidationError),
    ("test@example.com", 101, UserValidationError),
    ("test@example.com", 25, None)
])
def test_OrderProcessor_validate_user(email, age, expected):
    order_processor = OrderProcessor(Warehouse({}))
    if isinstance(expected, type) and issubclass(expected, Exception):
        with pytest.raises(expected):
            order_processor.validate_user(email, age)
    else:
        order_processor.validate_user(email, age)

@pytest.mark.parametrize('order_id, warehouse_stock, items, user_data, promo_code, expected', [
    ("ORD-1", {"X": 5}, [{"id": "X", "qty": 1, "price": 10.0}], {"email": "buyer@example.com", "age": 30, "tier": "STANDARD"}, None, 
     {'status': 'success', 'order_id': 'ORD-1', 'original_price': 10.0, 'discount_applied': 0.05, 'final_total': round(10.0 * (1 - 0.05) * 1.22, 2), 'items_count': 1}),
    ("ORD-2", {"X": 1}, [{"id": "X", "qty": 2, "price": 5.0}], {"email": "buyer@example.com", "age": 25, "tier": "STANDARD"}, None, 
     {'status': 'failed', 'reason': 'Out of stock: Insufficient stock for X'}),
    ("ORD-3", {"Y": 5}, [{"id": "Y", "qty": 1, "price": 20.0}], {"email": "buyer@example.com", "age": 28, "tier": "STANDARD"}, "BAD", 
     {'status': 'error', 'reason': 'Promo Error: Invalid promo code format'}),
    ("ORD-4", {"Z": 10}, [{"id": "Z", "qty": 1, "price": 10.0}], {"email": "buyer@example.com", "age": 29, "payment_method": "CRYPTO", "tier": "STANDARD"}, None, 
     {'status': 'success', 'order_id': 'ORD-4', 'original_price': 10.0, 'discount_applied': 0.05, 'final_total': round(10.0 * (1 - 0.05) * 1.22, 2), 'items_count': 1}), 
    ("ORD-5", {"W": 100}, [{"id": "W", "qty": 1, "price": 666.66}], {"email": "buyer@example.com", "age": 35, "payment_method": "PAYPAL", "tier": "STANDARD"}, None, 
     FraudDetectedError)
])
def test_OrderProcessor_process_order(mocker, order_id, warehouse_stock, items, user_data, promo_code, expected):
    mocker.patch('datetime.datetime.now', return_value=datetime(2023, 1, 1, 2, 0, 0))  
    warehouse = Warehouse(warehouse_stock)
    order_processor = OrderProcessor(warehouse)
    if isinstance(expected, type) and issubclass(expected, Exception):
        with pytest.raises(expected):
            order_processor.process_order(order_id, user_data, items, promo_code)
    else:
        result = order_processor.process_order(order_id, user_data, items, promo_code)
        assert result == expected