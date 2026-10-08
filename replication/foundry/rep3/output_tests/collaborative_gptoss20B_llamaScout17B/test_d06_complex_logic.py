import pytest
from data.input_code.d06_complex_logic import *
from unittest.mock import patch
from datetime import datetime


@pytest.mark.parametrize('order_id, user_data, items, promo_code, expected', [
    ("ORD-4", {"email": "user@example.com", "age": 30}, [{"id": "missing", "qty": 1, "price": 10.0}], None, {"status": "failed", "reason": "Out of stock: Item missing not found in warehouse."}),
    ("ORD-6", {"email": "user@example.com", "age": 30, "payment_method": "PAYPAL"}, [{"id": "A", "qty": 1, "price": 5.0}, {"id": "B", "qty": 1, "price": 10.0}], None, {
      "status": "success",
      "order_id": "ORD-6",
      "original_price": 15.0,
      "discount_applied": 0.0,
      "final_total": 18.3,
      "items_count": 2
    }),
    ("ORD-7", {"email": "user@example.com", "age": 30, "payment_method": "CRYPTO"}, [{"id": "C", "qty": 1, "price": 15.0}], None, {"status": "failed", "reason": "Out of stock: Item C not found in warehouse."}),
    ("ORD-8", {"email": "user@example.com", "age": 30}, [{"id": "A", "qty": 1, "price": 10.0}], "BADPROMO", {"status": "error", "reason": "Promo Error: Invalid promo code format"})
])
@patch('datetime.datetime')
def test_OrderProcessor_process_order(mock_datetime, order_id, user_data, items, promo_code, expected):
    mock_datetime.now.return_value = datetime(2024, 1, 1, 12, 0, 0)
    warehouse = Warehouse({"A": 10, "B": 10})  
    processor = OrderProcessor(warehouse)
    if isinstance(expected, str) and expected.endswith('Error'):
        with pytest.raises(eval(expected)):
            processor.process_order(order_id, user_data, items, promo_code)
    else:
        result = processor.process_order(order_id, user_data, items, promo_code)
        assert result == expected

@pytest.mark.parametrize('email, age, expected', [
    ("bad-email", 16, 'UserValidationError')
])
def test_OrderProcessor_validate_user(email, age, expected):
    processor = OrderProcessor(Warehouse({}))
    if isinstance(expected, str) and expected.endswith('Error'):
        with pytest.raises(eval(expected)):
            processor.validate_user(email, age)
    else:
        assert processor.validate_user(email, age) == expected

@pytest.mark.parametrize('initial_stock, item_id, quantity, expected', [
    ({"A": 5}, "A", 6, False)  # Corrected expected value
])
def test_Warehouse_check_stock(initial_stock, item_id, quantity, expected):
    warehouse = Warehouse(initial_stock)
    if isinstance(expected, str) and expected.endswith('Error'):
        with pytest.raises(eval(expected)):
            warehouse.check_stock(item_id, quantity)
    else:
        assert warehouse.check_stock(item_id, quantity) == expected

@pytest.mark.parametrize('email, age, expected', [
    ("user@example.com", 17, 'UserValidationError')
])
def test_OrderProcessor_validate_user(email, age, expected):
    processor = OrderProcessor(Warehouse({}))
    if isinstance(expected, str) and expected.endswith('Error'):
        with pytest.raises(eval(expected)):
            processor.validate_user(email, age)
    else:
        assert processor.validate_user(email, age) == expected

@patch('datetime.datetime')
def test_OrderProcessor_process_order_neg_qty_price_zero(mock_datetime):
    mock_datetime.now.return_value = datetime(2024, 1, 1, 12, 0, 0)
    warehouse = Warehouse({"A": 10})
    processor = OrderProcessor(warehouse)
    with pytest.raises(ValueError):
        processor.process_order("ORD-NEG", {"email": "user@example.com", "age": 25}, [{"id": "A", "qty": -1, "price": 0.0}], None)