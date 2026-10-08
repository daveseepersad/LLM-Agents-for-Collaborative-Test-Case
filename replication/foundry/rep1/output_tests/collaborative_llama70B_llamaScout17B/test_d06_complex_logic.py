import pytest
from data.input_code.d06_complex_logic import *
from unittest.mock import patch
from datetime import datetime

@pytest.mark.parametrize('item_id, quantity, initial_stock, expected', [
    ('item1', 1, {'item1': 10}, True),
    ('item2', 1, {'item1': 10}, 'InventoryError')
])
def test_Warehouse_check_stock(item_id, quantity, initial_stock, expected):
    warehouse = Warehouse(initial_stock)
    if isinstance(expected, bool):
        assert warehouse.check_stock(item_id, quantity) == expected
    else:
        with pytest.raises(eval(expected)):
            warehouse.check_stock(item_id, quantity)

@pytest.mark.parametrize('item_id, quantity, initial_stock, expected', [
    ('item1', 1, {'item1': 10}, None),
    ('item1', 11, {'item1': 10}, 'InventoryError')
])
def test_Warehouse_lock_item(item_id, quantity, initial_stock, expected):
    warehouse = Warehouse(initial_stock)
    if expected is None:
        warehouse.lock_item(item_id, quantity)
    else:
        with pytest.raises(eval(expected)):
            warehouse.lock_item(item_id, quantity)

@pytest.mark.parametrize('total_amount, user_tier, promo_code, expected_discount', [
    (100.0, 'GOLD', None, 0.15),  
    (100.0, 'GOLD', 'ABC-123', 0.25),  
    (100.0, 'GOLD', 'invalid', 'ValueError'),
    (1500.0, 'PLATINUM', None, 0.3),  
    (1500.0, 'PLATINUM', 'XYZ-999', 750.0),  
])
@patch('data.input_code.d06_complex_logic.datetime')
def test_DiscountEngine_calculate_discount(mock_datetime, total_amount, user_tier, promo_code, expected_discount):
    mock_datetime.now.return_value = datetime(2023, 1, 1, 2, 0, 0)  
    if isinstance(expected_discount, float):
        assert round(DiscountEngine.calculate_discount(total_amount, user_tier, promo_code), 2) == round(expected_discount, 2)
    else:
        with pytest.raises(eval(expected_discount)):
            DiscountEngine.calculate_discount(total_amount, user_tier, promo_code)

@pytest.mark.parametrize('email, age, expected', [
    ('test@example.com', 25, None),
    ('invalid', 25, 'UserValidationError'),
    ('test@example.com', 17, 'UserValidationError')
])
def test_OrderProcessor_validate_user(email, age, expected):
    order_processor = OrderProcessor(Warehouse({}))
    if expected is None:
        order_processor.validate_user(email, age)
    else:
        with pytest.raises(eval(expected)):
            order_processor.validate_user(email, age)

@pytest.mark.parametrize('order_id, user_data, items, promo_code, expected', [
    ('order1', {'email': 'test@example.com', 'age': 25, 'tier': 'GOLD'}, [{'id': 'item1', 'qty': 1, 'price': 100.0}], None, {'status': 'success', 'order_id': 'order1', 'original_price': 100.0, 'discount_applied': 0.15, 'final_total': 103.7, 'items_count': 1}),
    ('order1', {'email': 'test@example.com', 'age': 25, 'tier': 'GOLD'}, [{'id': 'item1', 'qty': 11, 'price': 100.0}], None, {'status': 'failed', 'reason': 'Out of stock: Insufficient stock for item1'}),
    ('order1', {'email': 'test@example.com', 'age': 25, 'tier': 'GOLD'}, [{'id': 'item1', 'qty': 1, 'price': 100.0}], 'invalid', {'status': 'error', 'reason': 'Promo Error: Invalid promo code format'}),
    ('order1', {'email': 'test@example.com', 'age': 25, 'tier': 'GOLD', 'payment_method': 'PAYPAL'}, [{'id': 'item1', 'qty': 1, 'price': 666.66}], None, {'status': 'success', 'order_id': 'order1', 'original_price': 666.66, 'discount_applied': 0.15, 'final_total': 691.33, 'items_count': 1}), 
    ('order1', {'email': 'test@example.com', 'age': 25, 'tier': 'GOLD', 'payment_method': 'CRYPTO'}, [{'id': 'item1', 'qty': 1, 'price': 40.0}], None, 'PaymentError')
])
@patch('data.input_code.d06_complex_logic.datetime')
def test_OrderProcessor_process_order(mock_datetime, order_id, user_data, items, promo_code, expected):
    mock_datetime.now.return_value = datetime(2023, 1, 1, 2, 0, 0)  
    warehouse = Warehouse({'item1': 10})
    order_processor = OrderProcessor(warehouse)
    if isinstance(expected, dict):
        if expected['status'] == 'success':
            result = order_processor.process_order(order_id, user_data, items, promo_code)
            assert result['status'] == expected['status']
            assert result['order_id'] == expected['order_id']
            assert round(result['original_price'], 2) == round(expected['original_price'], 2)
            assert round(result['discount_applied'], 2) == round(expected['discount_applied'], 2)
            assert round(result['final_total'], 2) == round(expected['final_total'], 2)
            assert result['items_count'] == expected['items_count']
        else:
            result = order_processor.process_order(order_id, user_data, items, promo_code)
            assert result == expected
    else:
        with pytest.raises(eval(expected)):
            order_processor.process_order(order_id, user_data, items, promo_code)

import pytest
from data.input_code.d06_complex_logic import *
from unittest.mock import patch
from datetime import datetime


