import pytest
from data.input_code.d06_complex_logic import Warehouse, DiscountEngine, OrderProcessor, InventoryError, PaymentError, FraudDetectedError, UserValidationError

@pytest.mark.parametrize('email, age, expected', [
    ('test@example.com', 25, None),
    ('invalid', 25, 'UserValidationError'),
    ('test@example.com', 17, 'UserValidationError'),
    ('test@example.com', 101, 'UserValidationError')
])
def test_validate_user(email, age, expected):
    order_processor = OrderProcessor(Warehouse({}))
    if expected:
        with pytest.raises(eval(expected)):
            order_processor.validate_user(email, age)
    else:
        order_processor.validate_user(email, age)

@pytest.mark.parametrize('item_id, quantity, initial_stock, expected', [
    ('item1', 5, {'item1': 10}, True),
    ('item1', 15, {'item1': 10}, False)
])
def test_check_stock(item_id, quantity, initial_stock, expected):
    warehouse = Warehouse(initial_stock)
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
    (100, 'GOLD', None, 0.1),
    (100, 'PLATINUM', None, 0.2),
    (1001, 'PLATINUM', None, 0.25),
    (100, 'STANDARD', 'ABC-123', 0.1),
    (100, 'STANDARD', 'ABC-999', 50.0), 
    (100, 'STANDARD', 'invalid', 'ValueError')
])
def test_calculate_discount(total_amount, user_tier, promo_code, expected):
    if expected == 'ValueError':
        with pytest.raises(eval(expected)):
            DiscountEngine.calculate_discount(total_amount, user_tier, promo_code)
    else:
        assert DiscountEngine.calculate_discount(total_amount, user_tier, promo_code) == expected

