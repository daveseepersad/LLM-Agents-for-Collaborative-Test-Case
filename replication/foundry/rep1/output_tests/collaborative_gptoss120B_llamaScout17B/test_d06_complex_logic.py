import pytest
from data.input_code.d06_complex_logic import *
import datetime

@pytest.mark.parametrize('initial_stock, item_id, quantity, expected', [
    ({"A1": 5}, "B2", 1, 'InventoryError'),
    ({"A1": 5}, "A1", 6, False),
    ({"A1": 10}, "A1", 4, True)
])
def test_Warehouse_check_stock(initial_stock, item_id, quantity, expected):
    warehouse = Warehouse(initial_stock)
    if expected == 'InventoryError':
        with pytest.raises(InventoryError):
            warehouse.check_stock(item_id, quantity)
    else:
        assert warehouse.check_stock(item_id, quantity) == expected


@pytest.mark.parametrize('email, age, expected', [
    ("bademail@", 30, 'UserValidationError'),
    ("test@example.com", 16, 'UserValidationError'),
    ("senior@example.com", 101, 'UserValidationError'),
    ("test@example.com", 30, None)
])
def test_OrderProcessor_validate_user(email, age, expected):
    order_processor = OrderProcessor(Warehouse({}))
    if expected == 'UserValidationError':
        with pytest.raises(UserValidationError):
            order_processor.validate_user(email, age)
    else:
        assert order_processor.validate_user(email, age) is expected

