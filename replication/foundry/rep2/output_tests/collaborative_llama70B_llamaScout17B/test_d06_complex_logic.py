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

@pytest.mark.parametrize('total_amount, user_tier, promo_code, expected', [
    (100.0, 'GOLD', None, 0.1), 
    (100.0, 'GOLD', 'ABC-123', 0.2), 
    (100.0, 'GOLD', 'invalid', 'ValueError') 
])
@patch('data.input_code.d06_complex_logic.datetime')
def test_DiscountEngine_calculate_discount(mock_datetime, total_amount, user_tier, promo_code, expected):
    mock_datetime.now.return_value = datetime(2023, 1, 1, 12, 0, 0) 
    if isinstance(expected, float):
        assert round(DiscountEngine.calculate_discount(total_amount, user_tier, promo_code), 2) == round(expected, 2)
    else:
        with pytest.raises(eval(expected)):
            DiscountEngine.calculate_discount(total_amount, user_tier, promo_code)

@pytest.mark.parametrize('email, age, expected', [
    ('test@example.com', 25, None),
    ('invalid', 25, 'UserValidationError')
])
def test_OrderProcessor_validate_user(email, age, expected):
    order_processor = OrderProcessor(Warehouse({}))
    if expected is None:
        order_processor.validate_user(email, age)
    else:
        with pytest.raises(eval(expected)):
            order_processor.validate_user(email, age)

@pytest.mark.parametrize('order_id, user_data, items, promo_code, expected', [
    ('order1', {'email': 'test@example.com', 'age': 25, 'tier': 'GOLD'}, [{'id': 'item1', 'qty': 1, 'price': 100.0}], None, {'status': 'success', 'order_id': 'order1', 'original_price': 100.0, 'discount_applied': 0.1, 'final_total': 109.8, 'items_count': 1}), 
    ('order1', {'email': 'test@example.com', 'age': 25, 'tier': 'GOLD'}, [{'id': 'item1', 'qty': 11, 'price': 100.0}], None, {'status': 'failed', 'reason': 'Out of stock: Insufficient stock for item1'}),
    ('order1', {'email': 'test@example.com', 'age': 25, 'tier': 'GOLD'}, [{'id': 'item1', 'qty': 1, 'price': 100.0}], 'invalid', {'status': 'error', 'reason': 'Promo Error: Invalid promo code format'}),
    ('order1', {'email': 'test@example.com', 'age': 25, 'tier': 'GOLD', 'payment_method': 'PAYPAL'}, [{'id': 'item1', 'qty': 1, 'price': 599.0}], None, {'status': 'success', 'order_id': 'order1', 'original_price': 599.0, 'discount_applied': 0.1, 'final_total': 657.7, 'items_count': 1}), 
    ('order1', {'email': 'test@example.com', 'age': 25, 'tier': 'GOLD', 'payment_method': 'CRYPTO'}, [{'id': 'item1', 'qty': 1, 'price': 60.0}], None, {'status': 'success', 'order_id': 'order1', 'original_price': 60.0, 'discount_applied': 0.1, 'final_total': 65.88, 'items_count': 1}) 
])
@patch('data.input_code.d06_complex_logic.datetime')
def test_OrderProcessor_process_order(mock_datetime, order_id, user_data, items, promo_code, expected):
    mock_datetime.now.return_value = datetime(2023, 1, 1, 12, 0, 0) 
    warehouse = Warehouse({'item1': 10})
    order_processor = OrderProcessor(warehouse)
    if isinstance(expected, dict):
        result = order_processor.process_order(order_id, user_data, items, promo_code)
        assert result == expected
    else:
        with pytest.raises(eval(expected)):
            order_processor.process_order(order_id, user_data, items, promo_code)

@patch('data.input_code.d06_complex_logic.datetime')
def test_DiscountEngine_calculate_discount_PLATINUM_OVER_1000(mock_datetime):
    mock_datetime.now.return_value = datetime(2023, 1, 1, 12, 0, 0)
    total_amount = 1000.01
    user_tier = "PLATINUM"
    promo_code = None
    expected = 0.25  
    assert round(DiscountEngine.calculate_discount(total_amount, user_tier, promo_code), 2) == round(expected, 2)

@patch('data.input_code.d06_complex_logic.datetime')
def test_DiscountEngine_calculate_discount_promo_code_999(mock_datetime):
    mock_datetime.now.return_value = datetime(2023, 1, 1, 12, 0, 0)
    total_amount = 100.0
    user_tier = "GOLD"
    promo_code = "ABC-999"
    expected = total_amount * 0.5
    assert DiscountEngine.calculate_discount(total_amount, user_tier, promo_code) == expected


@patch('data.input_code.d06_complex_logic.datetime')
def test_OrderProcessor_process_order_PaymentError_CRYPTO(mock_datetime):
    mock_datetime.now.return_value = datetime(2023, 1, 1, 12, 0, 0)
    order_id = "order1"
    user_data = {"email": "test@example.com", "age": 25, "tier": "GOLD", "payment_method": "CRYPTO"}
    items = [{"id": "item1", "qty": 1, "price": 40.0}]
    promo_code = None
    warehouse = Warehouse({'item1': 10})
    order_processor = OrderProcessor(warehouse)
    with pytest.raises(PaymentError):
        order_processor.process_order(order_id, user_data, items, promo_code)

def test_OrderProcessor_validate_user_over_100():
    order_processor = OrderProcessor(Warehouse({}))
    email = "test@example.com"
    age = 101
    with pytest.raises(UserValidationError):
        order_processor.validate_user(email, age)

def test_Warehouse_release_item():
    warehouse = Warehouse({'item1': 10})
    warehouse.lock_item('item1', 1)
    warehouse.release_item('item1', 1)
    assert 'item1' not in warehouse._locked_stock

@patch('data.input_code.d06_complex_logic.datetime')
def test_DiscountEngine_calculate_discount_NightOwl(mock_datetime):
    mock_datetime.now.return_value = datetime(2023, 1, 1, 4, 0, 0)  
    total_amount = 100.0
    user_tier = "GOLD"
    promo_code = None
    expected = 0.05 + 0.10
    assert round(DiscountEngine.calculate_discount(total_amount, user_tier, promo_code), 2) == round(expected, 2)

import pytest
from data.input_code.d06_complex_logic import *
from unittest.mock import patch
from datetime import datetime

@pytest.mark.parametrize('order_id, user_data, items, promo_code, expected', [
    ('order1', {'email': 'test@example.com', 'age': 25, 'tier': 'GOLD'}, [{'id': 'item1', 'qty': -1, 'price': 0.0}], None, 'ValueError')
])
@patch('data.input_code.d06_complex_logic.datetime')
def test_OrderProcessor_process_order_division_by_zero(mock_datetime, order_id, user_data, items, promo_code, expected):
    mock_datetime.now.return_value = datetime(2023, 1, 1, 12, 0, 0) 
    warehouse = Warehouse({'item1': 10})
    order_processor = OrderProcessor(warehouse)
    with pytest.raises(eval(expected)):
        order_processor.process_order(order_id, user_data, items, promo_code)

@pytest.mark.parametrize('email, age, expected', [
    ('test@example.com', 17, 'UserValidationError')
])
def test_OrderProcessor_validate_user_under_18(email, age, expected):
    order_processor = OrderProcessor(Warehouse({}))
    with pytest.raises(eval(expected)):
        order_processor.validate_user(email, age)


@pytest.mark.parametrize('order_id, user_data, items, promo_code, expected', [
    ('order1', {'email': 'test@example.com', 'age': 25, 'tier': 'GOLD', 'payment_method': 'CRYPTO'}, [{'id': 'item1', 'qty': 1, 'price': 60.0}], None, {'status': 'success'})
])
@patch('data.input_code.d06_complex_logic.datetime')
def test_OrderProcessor_process_order_crypto_over_50(mock_datetime, order_id, user_data, items, promo_code, expected):
    mock_datetime.now.return_value = datetime(2023, 1, 1, 12, 0, 0) 
    warehouse = Warehouse({'item1': 10})
    order_processor = OrderProcessor(warehouse)
    result = order_processor.process_order(order_id, user_data, items, promo_code)
    assert result['status'] == expected['status']

@pytest.mark.parametrize('item_id, quantity, initial_stock, expected', [
    ('item1', 1, {'item1': 10}, True),
    ('item1', 1, {'item1': 1, 'locked': {'item1': 1}}, False)
])
def test_Warehouse_check_stock_locked_item(item_id, quantity, initial_stock, expected):
    warehouse = Warehouse(initial_stock)
    if 'locked' in initial_stock:
        warehouse._locked_stock = initial_stock['locked']
    assert warehouse.check_stock(item_id, quantity) == expected

def test_Warehouse_release_item_not_locked():
    warehouse = Warehouse({'item1': 10})
    warehouse.release_item('item1', 1)
    assert 'item1' not in warehouse._locked_stock

@pytest.mark.parametrize('total_amount, user_tier, promo_code, expected', [
    (100.0, 'GOLD', 'invalid-format', 'ValueError')
])
@patch('data.input_code.d06_complex_logic.datetime')
def test_DiscountEngine_calculate_discount_promo_code_invalid_format(mock_datetime, total_amount, user_tier, promo_code, expected):
    mock_datetime.now.return_value = datetime(2023, 1, 1, 12, 0, 0) 
    with pytest.raises(eval(expected)):
        DiscountEngine.calculate_discount(total_amount, user_tier, promo_code)

