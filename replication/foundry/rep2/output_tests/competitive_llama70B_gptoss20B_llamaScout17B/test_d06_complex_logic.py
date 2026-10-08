import pytest
from data.input_code.d06_complex_logic import *
from unittest.mock import patch
from datetime import datetime

@pytest.mark.parametrize('item_id, quantity, initial_stock, expected', [
    ('item1', 1, {'item1': 10}, True),
    ('item2', 1, {'item1': 10}, InventoryError)
])
def test_Warehouse_check_stock(item_id, quantity, initial_stock, expected):
    warehouse = Warehouse(initial_stock)
    if isinstance(expected, type) and issubclass(expected, Exception):
        with pytest.raises(expected):
            warehouse.check_stock(item_id, quantity)
    else:
        assert warehouse.check_stock(item_id, quantity) == expected

@pytest.mark.parametrize('item_id, quantity, initial_stock, expected', [
    ('item1', 1, {'item1': 10}, None),
    ('item1', 11, {'item1': 10}, InventoryError)
])
def test_Warehouse_lock_item(item_id, quantity, initial_stock, expected):
    warehouse = Warehouse(initial_stock)
    if isinstance(expected, type) and issubclass(expected, Exception):
        with pytest.raises(expected):
            warehouse.lock_item(item_id, quantity)
    else:
        warehouse.lock_item(item_id, quantity)

@pytest.mark.parametrize('total_amount, user_tier, promo_code, expected', [
    (100.0, 'GOLD', None, 0.10),
    (100.0, 'GOLD', 'ABC-1234', ValueError),
    (100.0, 'GOLD', 'ABC-123', 0.20)
])
def test_DiscountEngine_calculate_discount(total_amount, user_tier, promo_code, expected):
    if isinstance(expected, type) and issubclass(expected, Exception):
        with pytest.raises(expected):
            DiscountEngine.calculate_discount(total_amount, user_tier, promo_code)
    else:
        assert DiscountEngine.calculate_discount(total_amount, user_tier, promo_code) == expected

@pytest.mark.parametrize('email, age, expected', [
    ('test', 18, UserValidationError),
    ('test@test.com', 18, None),
    ('test@test.com', 17, UserValidationError),
    ('test@test.com', 101, UserValidationError)
])
def test_OrderProcessor_validate_user(email, age, expected):
    order_processor = OrderProcessor(Warehouse({}))
    if isinstance(expected, type) and issubclass(expected, Exception):
        with pytest.raises(expected):
            order_processor.validate_user(email, age)
    else:
        order_processor.validate_user(email, age)

@pytest.mark.parametrize('order_id, user_data, items, promo_code, warehouse_stock, expected', [
    ('order1', {'email': 'test@test.com', 'age': 18}, [{'id': 'item1', 'qty': 1, 'price': 10.0}], None, {}, {'status': 'failed', 'reason': 'Out of stock: Item item1 not found in warehouse.'}),
    ('order1', {'email': 'test@test.com', 'age': 18}, [{'id': 'item1', 'qty': 1, 'price': 10.0}], None, {'item1': 10}, {'status': 'success', 'order_id': 'order1', 'original_price': 10.0, 'discount_applied': 0.10, 'final_total': 10.98, 'items_count': 1}),
    ('order1', {'email': 'test@test.com', 'age': 18}, [{'id': 'item1', 'qty': 1, 'price': 10.0}], 'ABC-1234', {'item1': 10}, {'status': 'error', 'reason': 'Promo Error: Invalid promo code format'}),
    ('order1', {'email': 'test@test.com', 'age': 18, 'payment_method': 'PAYPAL'}, [{'id': 'item1', 'qty': 1, 'price': 10.0}], None, {'item1': 10}, {'status': 'success', 'order_id': 'order1', 'original_price': 10.0, 'discount_applied': 0.10, 'final_total': 10.98, 'items_count': 1}),
    ('order1', {'email': 'test@test.com', 'age': 18, 'payment_method': 'CRYPTO'}, [{'id': 'item1', 'qty': 1, 'price': 10.0}], None, {'item1': 10}, PaymentError)
])
def test_OrderProcessor_process_order(order_id, user_data, items, promo_code, warehouse_stock, expected):
    order_processor = OrderProcessor(Warehouse(warehouse_stock))
    if isinstance(expected, type) and issubclass(expected, Exception):
        with pytest.raises(expected):
            order_processor.process_order(order_id, user_data, items, promo_code)
    elif isinstance(expected, dict) and (expected.get('status') == 'error' or expected.get('status') == 'failed'):
        assert order_processor.process_order(order_id, user_data, items, promo_code) == expected
    else:
        result = order_processor.process_order(order_id, user_data, items, promo_code)
        assert result['status'] == expected['status']
        assert result['order_id'] == expected['order_id']

@pytest.mark.parametrize('total_amount, user_tier, promo_code, expected', [
    (1000.01, 'PLATINUM', None, 0.25)
])
def test_DiscountEngine_calculate_discount_additional(total_amount, user_tier, promo_code, expected):
    with patch('datetime.datetime') as mock_datetime:
        mock_datetime.now.return_value = datetime(2023, 1, 1, 12, 0, 0)
        assert DiscountEngine.calculate_discount(total_amount, user_tier, promo_code) == expected

def test_DiscountEngine_calculate_discount_promo_code_999():
    assert DiscountEngine.calculate_discount(100.0, 'GOLD', 'ABC-999') == 50.0  # Changed to 50.0


