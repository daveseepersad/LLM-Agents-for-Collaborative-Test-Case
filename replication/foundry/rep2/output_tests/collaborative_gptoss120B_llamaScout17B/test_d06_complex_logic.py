import pytest
from data.input_code.d06_complex_logic import *
from datetime import datetime


def test_Warehouse_check_stock_not_found():
    warehouse = Warehouse({'A1': 10})
    with pytest.raises(InventoryError):
        warehouse.check_stock('B2', 1)

@pytest.mark.parametrize('item_id, quantity, initial_stock, expected_locked_stock', [
    ('A1', 3, {'A1': 10}, {'A1': 3})
])
def test_Warehouse_lock_item_success(item_id, quantity, initial_stock, expected_locked_stock):
    warehouse = Warehouse(initial_stock)
    warehouse.lock_item(item_id, quantity)
    assert warehouse._locked_stock == expected_locked_stock

def test_Warehouse_lock_item_insufficient():
    warehouse = Warehouse({'A1': 5})
    with pytest.raises(InventoryError):
        warehouse.lock_item('A1', 7)


@pytest.mark.parametrize('email, age, expected', [
    ('invalid_email', 30, 'UserValidationError'),
    ('test@example.com', 16, 'UserValidationError'),
    ('old@example.com', 101, 'UserValidationError'),
    ('test@example.com', 30, None)  # Valid case
])
def test_OrderProcessor_validate_user(email, age, expected):
    order_processor = OrderProcessor(Warehouse({}))
    if expected is None:
        order_processor.validate_user(email, age)  # Should not raise
    else:
        with pytest.raises(UserValidationError):
            order_processor.validate_user(email, age)

