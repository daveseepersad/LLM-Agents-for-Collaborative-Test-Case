import pytest
from data.input_code.d06_complex_logic import *
from datetime import datetime

@pytest.mark.parametrize('email, age, expected', [
    ("test@example.com", 25, None),
    ("invalid", 25, UserValidationError),
    ("test@example.com", 17, UserValidationError),
    ("test@example.com", 101, UserValidationError)
])
def test_validate_user(email, age, expected):
    order_processor = OrderProcessor(Warehouse({}))
    if expected is None:
        order_processor.validate_user(email, age)
    else:
        with pytest.raises(expected):
            order_processor.validate_user(email, age)

@pytest.mark.parametrize('initial_stock, item_id, quantity, expected', [
    ({"item1": 10}, "item1", 5, True),
    ({"item1": 10}, "item2", 5, InventoryError)
])
def test_check_stock(initial_stock, item_id, quantity, expected):
    warehouse = Warehouse(initial_stock)
    if expected is True:
        assert warehouse.check_stock(item_id, quantity) == expected
    else:
        with pytest.raises(expected):
            warehouse.check_stock(item_id, quantity)

@pytest.mark.parametrize('initial_stock, item_id, quantity, expected', [
    ({"item1": 10}, "item1", 5, None),
    ({"item1": 10}, "item1", 15, InventoryError)
])
def test_lock_item(initial_stock, item_id, quantity, expected):
    warehouse = Warehouse(initial_stock)
    if expected is None:
        warehouse.lock_item(item_id, quantity)
    else:
        with pytest.raises(expected):
            warehouse.lock_item(item_id, quantity)


