import pytest
from data.input_code.d06_complex_logic import *
from unittest.mock import patch, MagicMock
from datetime import datetime

@pytest.mark.parametrize('email, age, expected', [
    ('test@example.com', 25, None),
    ('invalid', 25, 'UserValidationError'),
    ('test@example.com', 17, 'UserValidationError'),
    ('test@example.com', 101, 'UserValidationError')
])
def test_validate_user(email, age, expected):
    if expected:
        with pytest.raises(eval(expected)):
            OrderProcessor(Warehouse({})).validate_user(email, age)
    else:
        OrderProcessor(Warehouse({})).validate_user(email, age)

@pytest.mark.parametrize('item_id, quantity, initial_stock, expected', [
    ('item1', 5, {'item1': 10}, True),
    ('item1', 15, {'item1': 10}, False),
    ('nonexistent', 1, {'item1': 10}, 'InventoryError')
])
def test_check_stock(item_id, quantity, initial_stock, expected):
    warehouse = Warehouse(initial_stock)
    if expected == 'InventoryError':
        with pytest.raises(eval(expected)):
            warehouse.check_stock(item_id, quantity)
    else:
        assert warehouse.check_stock(item_id, quantity) == expected

@pytest.mark.parametrize('item_id, quantity, initial_stock, expected', [
    ('item1', 5, {'item1': 10}, None),
    ('item1', 15, {'item1': 10}, 'InventoryError')
])
def test_lock_item(item_id, quantity, initial_stock, expected):
    warehouse = Warehouse(initial_stock)
    if expected:
        with pytest.raises(eval(expected)):
            warehouse.lock_item(item_id, quantity)
    else:
        warehouse.lock_item(item_id, quantity)

@pytest.mark.parametrize('total_amount, user_tier, promo_code, expected', [
    (100.0, 'STANDARD', None, 0.0),
    (100.0, 'GOLD', None, 0.10),
    (100.0, 'PLATINUM', None, 0.20),
    (1001.0, 'PLATINUM', None, 0.25),
    (100.0, 'STANDARD', 'ABC-123', 0.10),
    (100.0, 'STANDARD', 'ABC-999', 50.0),
    (100.0, 'STANDARD', 'invalid', 'ValueError')
])
def test_calculate_discount(total_amount, user_tier, promo_code, expected):
    if expected == 'ValueError':
        with pytest.raises(eval(expected)):
            DiscountEngine.calculate_discount(total_amount, user_tier, promo_code)
    else:
        assert DiscountEngine.calculate_discount(total_amount, user_tier, promo_code) == expected



def test_discount_engine_promo_code():
    assert DiscountEngine.calculate_discount(100.0, 'STANDARD', 'ABC-123') == 0.10

def test_discount_engine_promo_code_super():
    assert DiscountEngine.calculate_discount(100.0, 'STANDARD', 'ABC-999') == 50.0

def test_discount_engine_promo_code_invalid():
    with pytest.raises(ValueError):
        DiscountEngine.calculate_discount(100.0, 'STANDARD', 'invalid')


def test_order_processor_payment_method_crypto():
    warehouse = Warehouse({'item1': 10})
    order_processor = OrderProcessor(warehouse)
    user_data = {'email': 'test@example.com', 'age': 25, 'tier': 'STANDARD', 'payment_method': 'CRYPTO'}
    items = [{'id': 'item1', 'qty': 1, 'price': 10.0}]
    with pytest.raises(PaymentError):
        order_processor.process_order('ORD1', user_data, items)

# Additional test to cover the case when the current hour is between 0 and 6
