import pytest
from data.input_code.d06_complex_logic import *

@pytest.mark.parametrize('total_amount, user_tier, promo_code, mock_hour, expected', [
    (500, "GOLD", None, 12, 0.10),
    (1500, "PLATINUM", "ABC-999", 2, 750.0),
    (200, "STANDARD", "ABC-999", 12, 100.0),
    (100, "STANDARD", "abc-123", 12, 'ValueError'),
    (100, "STANDARD", None, 3, 0.0)
])
def test_DiscountEngine_calculate_discount(monkeypatch, total_amount, user_tier, promo_code, mock_hour, expected):
    monkeypatch.setattr('datetime.datetime', lambda: datetime(2024, 1, 1, mock_hour))
    if isinstance(expected, str) and expected == 'ValueError':
        with pytest.raises(ValueError):
            DiscountEngine.calculate_discount(total_amount, user_tier, promo_code)
    else:
        assert DiscountEngine.calculate_discount(total_amount, user_tier, promo_code) == expected

@pytest.mark.parametrize('order_id, user_data, items, promo_code, warehouse_initial_stock, mock_hour, expected', [
    ("ORD1", {"email": "user@example.com", "age": 30, "tier": "STANDARD"}, [{"id": "A", "qty": 2, "price": 10}, {"id": "B", "qty": 1, "price": 20}], None, {"A": 5, "B": 5}, 12, {"status": "success", "order_id": "ORD1", "original_price": 40, "discount_applied": 0, "final_total": 48.8, "items_count": 2}),
    ("ORD2", {"email": "u@example.com", "age": 25, "tier": "STANDARD"}, [{"id": "X", "qty": 1, "price": 10}], None, {"X": 0}, 12, {"status": "failed", "reason": "Out of stock: Insufficient stock for X"}),
    ("ORD3", {"email": "user@example.com", "age": 28, "tier": "STANDARD"}, [{"id": "A", "qty": 1, "price": 10}], "bad", {"A": 5}, 12, {"status": "error", "reason": "Promo Error: Invalid promo code format"}),
    ("ORD4", {"email": "test@example.com", "age": 30, "tier": "GOLD", "payment_method": "CRYPTO"}, [{"id": "A", "qty": 2, "price": 10}], None, {"A": 5}, 12, 'PaymentError')
])
def test_OrderProcessor_process_order(monkeypatch, order_id, user_data, items, promo_code, warehouse_initial_stock, mock_hour, expected):
    monkeypatch.setattr('datetime.datetime', lambda: datetime(2024, 1, 1, mock_hour))
    warehouse = Warehouse(warehouse_initial_stock)
    processor = OrderProcessor(warehouse)
    if isinstance(expected, str) and expected == 'PaymentError':
        with pytest.raises(PaymentError):
            processor.process_order(order_id, user_data, items, promo_code)
    else:
        result = processor.process_order(order_id, user_data, items, promo_code)
        assert result == expected

@pytest.mark.parametrize('email, age, expected', [
    ("bademail", 25, 'UserValidationError'),
    ("ok@example.com", 16, 'UserValidationError')
])
def test_OrderProcessor_validate_user(email, age, expected):
    processor = OrderProcessor(Warehouse({}))
    if isinstance(expected, str) and expected == 'UserValidationError':
        with pytest.raises(UserValidationError):
            processor.validate_user(email, age)
    else:
        processor.validate_user(email, age)

@pytest.mark.parametrize('order_id, user_data, items, promo_code, warehouse_initial_stock, mock_hour, expected', [
    ("ORD_PAYPAL", {"email": "fraud@example.com", "age": 30, "tier": "STANDARD", "payment_method": "PAYPAL"}, [{"id": "Z", "qty": 1, "price": 546.44}], None, {"Z": 5}, 12, 'FraudDetectedError'),
])
def test_OrderProcessor_process_order_paypal_fraud(monkeypatch, order_id, user_data, items, promo_code, warehouse_initial_stock, mock_hour, expected):
    monkeypatch.setattr('datetime.datetime', lambda: datetime(2024, 1, 1, mock_hour))
    warehouse = Warehouse(warehouse_initial_stock)
    processor = OrderProcessor(warehouse)
    if isinstance(expected, str) and expected == 'FraudDetectedError':
        with pytest.raises(FraudDetectedError):
            processor.process_order(order_id, user_data, items, promo_code)
    else:
        result = processor.process_order(order_id, user_data, items, promo_code)
        assert result == expected

@pytest.mark.parametrize('email, age, expected', [
    ("ok@example.com", 101, 'UserValidationError'),
])
def test_OrderProcessor_validate_user_over100(email, age, expected):
    processor = OrderProcessor(Warehouse({}))
    if isinstance(expected, str) and expected == 'UserValidationError':
        with pytest.raises(UserValidationError):
            processor.validate_user(email, age)
    else:
        processor.validate_user(email, age)

@pytest.mark.parametrize('order_id, user_data, items, promo_code, warehouse_initial_stock, mock_hour, expected', [
    ("ORD_NEG", {"email": "ok@example.com", "age": 30, "tier": "STANDARD"}, [{"id": "N", "qty": -1, "price": 0.0}], None, {"N": 5}, 12, 'ValueError'),
])
def test_OrderProcessor_process_order_neg_qty_zero_price(monkeypatch, order_id, user_data, items, promo_code, warehouse_initial_stock, mock_hour, expected):
    monkeypatch.setattr('datetime.datetime', lambda: datetime(2024, 1, 1, mock_hour))
    warehouse = Warehouse(warehouse_initial_stock)
    processor = OrderProcessor(warehouse)
    if isinstance(expected, str) and expected == 'ValueError':
        with pytest.raises(ValueError):
            processor.process_order(order_id, user_data, items, promo_code)
    else:
        result = processor.process_order(order_id, user_data, items, promo_code)
        assert result == expected

import pytest
from data.input_code.d06_complex_logic import *

def test_Warehouse_check_stock_missing_item():
    warehouse = Warehouse({"A": 5})
    with pytest.raises(InventoryError):
        warehouse.check_stock("UNKNOWN", 1)

@pytest.mark.parametrize('order_id, user_data, items, promo_code, warehouse_initial_stock, mock_hour, expected', [
    ("ORD_ROLLBACK", {"email": "user@example.com", "age": 30, "tier": "STANDARD"}, [{"id": "A", "qty": 1, "price": 5}, {"id": "B", "qty": 1, "price": 5}], None, {"A": 5, "B": 0}, 12, {"status": "failed", "reason": "Out of stock: Insufficient stock for B"}),
])
def test_OrderProcessor_process_order_rollback(monkeypatch, order_id, user_data, items, promo_code, warehouse_initial_stock, mock_hour, expected):
    monkeypatch.setattr('datetime.datetime', lambda: datetime(2024, 1, 1, mock_hour))
    warehouse = Warehouse(warehouse_initial_stock)
    processor = OrderProcessor(warehouse)
    result = processor.process_order(order_id, user_data, items, promo_code)
    assert result == expected

