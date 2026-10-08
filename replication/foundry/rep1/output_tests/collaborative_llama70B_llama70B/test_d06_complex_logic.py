import pytest
from data.input_code.d06_complex_logic import Warehouse, DiscountEngine, OrderProcessor, InventoryError, PaymentError, FraudDetectedError, UserValidationError

@pytest.mark.parametrize('item_id, quantity, initial_stock, expected', [
    ('item1', 1, {'item1': 10}, True),
])
def test_warehouse_check_stock_success(item_id, quantity, initial_stock, expected):
    warehouse = Warehouse(initial_stock)
    assert warehouse.check_stock(item_id, quantity) == expected

def test_warehouse_check_stock_error():
    warehouse = Warehouse({'item1': 10})
    with pytest.raises(InventoryError):
        warehouse.check_stock('item2', 1)

@pytest.mark.parametrize('item_id, quantity, initial_stock, expected', [
    ('item1', 1, {'item1': 10}, None),
])
def test_warehouse_lock_item_success(item_id, quantity, initial_stock, expected):
    warehouse = Warehouse(initial_stock)
    assert warehouse.lock_item(item_id, quantity) == expected

def test_warehouse_lock_item_error():
    warehouse = Warehouse({'item1': 10})
    with pytest.raises(InventoryError):
        warehouse.lock_item('item1', 11)

@pytest.mark.parametrize('total_amount, user_tier, promo_code, expected', [
    (100.0, 'GOLD', None, 0.1),
])
def test_discount_engine_calculate_discount_success(total_amount, user_tier, promo_code, expected):
    assert DiscountEngine.calculate_discount(total_amount, user_tier, promo_code) == expected

def test_discount_engine_calculate_discount_error():
    with pytest.raises(ValueError):
        DiscountEngine.calculate_discount(100.0, 'GOLD', 'ABC-12345')

@pytest.mark.parametrize('email, age, expected', [
    ('test@example.com', 25, None),
])
def test_order_processor_validate_user_success(email, age, expected):
    order_processor = OrderProcessor(Warehouse({}))
    assert order_processor.validate_user(email, age) == expected

def test_order_processor_validate_user_error():
    order_processor = OrderProcessor(Warehouse({}))
    with pytest.raises(UserValidationError):
        order_processor.validate_user('invalid_email', 25)

@pytest.mark.parametrize('order_id, user_data, items, promo_code, expected', [
    ('order1', {'email': 'test@example.com', 'age': 25, 'tier': 'GOLD'}, [{'id': 'item1', 'qty': 1, 'price': 10.0}], None, 
     {'status': 'success', 'order_id': 'order1', 'original_price': 10.0, 'discount_applied': 0.1, 'final_total': 10.98, 'items_count': 1}),
])
def test_order_processor_process_order_success(order_id, user_data, items, promo_code, expected):
    warehouse = Warehouse({'item1': 10})
    order_processor = OrderProcessor(warehouse)
    assert order_processor.process_order(order_id, user_data, items, promo_code) == expected

def test_order_processor_process_order_error():
    warehouse = Warehouse({'item1': 1})
    order_processor = OrderProcessor(warehouse)
    result = order_processor.process_order('order1', {'email': 'test@example.com', 'age': 25, 'tier': 'GOLD'}, [{'id': 'item1', 'qty': 2, 'price': 10.0}])
    assert result['status'] == 'failed'
    assert 'Out of stock' in result['reason']


def test_order_processor_process_order_payment_error_crypto():
    warehouse = Warehouse({'item1': 10})
    order_processor = OrderProcessor(warehouse)
    with pytest.raises(PaymentError):
        order_processor.process_order('order1', {'email': 'test@example.com', 'age': 25, 'tier': 'GOLD', 'payment_method': 'CRYPTO'}, [{'id': 'item1', 'qty': 1, 'price': 10.0}])