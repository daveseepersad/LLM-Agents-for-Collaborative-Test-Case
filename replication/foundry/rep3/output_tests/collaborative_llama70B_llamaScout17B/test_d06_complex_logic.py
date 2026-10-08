import pytest
from data.input_code.d06_complex_logic import *
from unittest.mock import patch
from datetime import datetime

@pytest.mark.parametrize('initial_stock', [
    ({"item1": 10, "item2": 20})
])
def test_warehouse_init(initial_stock):
    warehouse = Warehouse(initial_stock)
    assert warehouse._stock == initial_stock

@pytest.mark.parametrize('item_id, quantity, expected', [
    ("item1", 5, True),
    ("item3", 5, 'InventoryError')
])
def test_warehouse_check_stock(item_id, quantity, expected):
    warehouse = Warehouse({"item1": 10})
    if expected == 'InventoryError':
        with pytest.raises(InventoryError):
            warehouse.check_stock(item_id, quantity)
    else:
        assert warehouse.check_stock(item_id, quantity) == expected

@pytest.mark.parametrize('item_id, quantity, expected', [
    ("item1", 5, None),
    ("item1", 15, 'InventoryError')
])
def test_warehouse_lock_item(item_id, quantity, expected):
    warehouse = Warehouse({"item1": 10})
    if expected == 'InventoryError':
        with pytest.raises(InventoryError):
            warehouse.lock_item(item_id, quantity)
    else:
        warehouse.lock_item(item_id, quantity)
        assert warehouse._locked_stock[item_id] == quantity

def test_warehouse_release_item():
    warehouse = Warehouse({"item1": 10})
    warehouse.lock_item("item1", 5)
    warehouse.release_item("item1", 5)
    assert "item1" not in warehouse._locked_stock


@pytest.mark.parametrize('email, age, expected', [
    ("test@example.com", 25, None),
    ("invalid", 25, 'UserValidationError'),
    ("test@example.com", 17, 'UserValidationError')
])
def test_order_processor_validate_user(email, age, expected):
    order_processor = OrderProcessor(Warehouse({}))
    if expected == 'UserValidationError':
        with pytest.raises(UserValidationError):
            order_processor.validate_user(email, age)
    else:
        order_processor.validate_user(email, age)

