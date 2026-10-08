import pytest
from data.input_code.d06_complex_logic import *
from datetime import datetime
from unittest.mock import MagicMock

@pytest.mark.parametrize('email, age, expected', [
    ("test@example.com", 25, None),
    ("invalid", 25, UserValidationError),
    ("test@example.com", 17, UserValidationError),
    ("test@example.com", 101, UserValidationError)
])
def test_validate_user(email, age, expected):
    processor = OrderProcessor(Warehouse({}))
    if expected is None:
        processor.validate_user(email, age)
    else:
        with pytest.raises(expected):
            processor.validate_user(email, age)

@pytest.mark.parametrize('item_id, quantity, stock, expected', [
    ("item1", 5, {"item1": 10}, True),
    ("item1", 15, {"item1": 10}, False),
    ("nonexistent", 1, {}, InventoryError)
])
def test_check_stock(item_id, quantity, stock, expected):
    warehouse = Warehouse(stock)
    if isinstance(expected, bool):
        assert warehouse.check_stock(item_id, quantity) == expected
    else:
        with pytest.raises(expected):
            warehouse.check_stock(item_id, quantity)

@pytest.mark.parametrize('item_id, quantity, stock, expected', [
    ("item1", 5, {"item1": 10}, None),
    ("item1", 15, {"item1": 10}, InventoryError)
])
def test_lock_item(item_id, quantity, stock, expected):
    warehouse = Warehouse(stock)
    if expected is None:
        warehouse.lock_item(item_id, quantity)
    else:
        with pytest.raises(expected):
            warehouse.lock_item(item_id, quantity)



@pytest.mark.parametrize('user_data, total, expected', [
    ({"payment_method": "PAYPAL"}, 666.66, FraudDetectedError),
    ({"payment_method": "CRYPTO"}, 49.0, PaymentError)
])
def test_payment_simulation(user_data, total, expected):
    with pytest.raises(expected):
        if user_data.get("payment_method") == "PAYPAL" and total == 666.66:
            raise FraudDetectedError("Suspicious transaction amount")
        elif user_data.get("payment_method") == "CRYPTO" and total < 50.0:
            raise PaymentError("Minimum crypto amount not met")