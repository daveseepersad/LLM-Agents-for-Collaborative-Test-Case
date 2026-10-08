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
    ('item2', 5, {'item1': 10}, 'InventoryError')
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
    (100, 'STANDARD', None, 0.0),
    (100, 'GOLD', None, 0.10),
    (100, 'PLATINUM', None, 0.20),
    (1001, 'PLATINUM', None, 0.25),
    (100, 'STANDARD', 'ABC-123', 0.10),
    (100, 'STANDARD', 'ABC-999', 50.0),
    (100, 'STANDARD', 'invalid', 'ValueError')
])
def test_calculate_discount(total_amount, user_tier, promo_code, expected):
    if expected == 'ValueError':
        with pytest.raises(eval(expected)):
            DiscountEngine.calculate_discount(total_amount, user_tier, promo_code)
    else:
        assert DiscountEngine.calculate_discount(total_amount, user_tier, promo_code) == expected


@patch('datetime.datetime')
def test_calculate_discount_time_outside_discount_hours(mock_datetime):
    mock_datetime.now.return_value.hour = 12
    assert DiscountEngine.calculate_discount(100, 'STANDARD') == 0.0


# Additional test for test_calculate_discount_time
@patch('datetime.datetime')
def test_calculate_discount_time_outside_discount_hours(mock_datetime):
    mock_datetime.now.return_value.hour = 12
    assert DiscountEngine.calculate_discount(100, 'STANDARD') == 0.0