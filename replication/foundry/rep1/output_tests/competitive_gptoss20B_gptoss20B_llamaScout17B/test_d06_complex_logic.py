import pytest
from data.input_code.d06_complex_logic import *

@pytest.fixture
def warehouse():
    return Warehouse({"itemA": 10, "item1": 5, "tiny": 1, "out_of_stock": 0})

def test_Warehouse_check_stock_ok(warehouse):
    assert warehouse.check_stock("itemA", 2) == True

def test_Warehouse_check_stock_not_found(warehouse):
    with pytest.raises(InventoryError):
        warehouse.check_stock("unknown", 1)

def test_Warehouse_lock_item_insufficient(warehouse):
    with pytest.raises(InventoryError):
        warehouse.lock_item("itemA", 50)

def test_Warehouse_release_item(warehouse):
    warehouse.lock_item("itemA", 1)
    warehouse.release_item("itemA", 1)
    assert "itemA" not in warehouse._locked_stock

@pytest.mark.parametrize('total_amount, user_tier, promo_code, mock_datetime_hour, expected', [
    (1500.0, "PLATINUM", None, 2, 0.25),
    (800.0, "GOLD", "ABC-999", 14, 400.0),
    (500.0, "PLATINUM", "DEF-123", 14, 0.30),
    (100.0, "STANDARD", "invalid", 14, "ValueError")
])
def test_DiscountEngine_calculate_discount(monkeypatch, total_amount, user_tier, promo_code, mock_datetime_hour, expected):
    monkeypatch.setattr('datetime.datetime', lambda: datetime(2023, 1, 1, mock_datetime_hour, 0, 0))
    if isinstance(expected, str) and expected.endswith('Error'):
        with pytest.raises(eval(expected)):
            DiscountEngine.calculate_discount(total_amount, user_tier, promo_code)
    else:
        result = DiscountEngine.calculate_discount(total_amount, user_tier, promo_code)
        if isinstance(expected, (int, float)):
            assert result == pytest.approx(expected)
        else:
            assert result == expected

@pytest.mark.parametrize('order_id, user_data, items, promo_code, expected', [
    ("ORD123", {"email": "test@example.com", "age": 25, "tier": "STANDARD", "payment_method": "CC"}, [{"id": "item1", "qty": 2, "price": 5.0}], None, {"status": "success", "order_id": "ORD123", "original_price": 10.0, "discount_applied": 0.0, "final_total": 12.2, "items_count": 1}),
    ("ORD124", {"email": "test@example.com", "age": 30, "tier": "STANDARD"}, [{"id": "out_of_stock", "qty": 2, "price": 10.0}], None, {"status": "failed", "reason": "Out of stock: Insufficient stock for out_of_stock"}),
    ("ORD125", {"email": "test@example.com", "age": 30}, [{"id": "item1", "qty": 1, "price": 1.0}], "bad", {"status": "error", "reason": "Promo Error: Invalid promo code format"}),
    ("ORD126", {"email": "user@example.com", "age": 28, "payment_method": "CRYPTO"}, [{"id": "tiny", "qty": 1, "price": 0.01}], None, "PaymentError")
])
def test_OrderProcessor_process_order(warehouse, order_id, user_data, items, promo_code, expected):
    processor = OrderProcessor(warehouse)
    if isinstance(expected, str) and expected.endswith('Error'):
        with pytest.raises(eval(expected)):
            processor.process_order(order_id, user_data, items, promo_code)
    else:
        assert processor.process_order(order_id, user_data, items, promo_code) == expected

@pytest.mark.parametrize('email, age, expected', [
    ("bad-email", 20, "UserValidationError"),
    ("valid@example.com", 16, "UserValidationError")
])
def test_OrderProcessor_validate_user(email, age, expected):
    processor = OrderProcessor(Warehouse({}))
    with pytest.raises(eval(expected)):
        processor.validate_user(email, age)

def test_Warehouse_lock_item_unknown_item():
    w = Warehouse({"existing": 5})
    with pytest.raises(InventoryError):
        w.lock_item("unknown_item", 1)

def test_OrderProcessor_validate_user_age_101():
    processor = OrderProcessor(Warehouse({}))
    with pytest.raises(UserValidationError):
        processor.validate_user("valid@example.com", 101)

def test_OrderProcessor_process_order_negative_free():
    w = Warehouse({"item1": 10})
    processor = OrderProcessor(w)
    order_id = "ORD_NEG_FREE"
    user_data = {"email": "test@example.com", "age": 25, "payment_method": "CC"}
    items = [{"id": "item1", "qty": -1, "price": 0.0}]
    with pytest.raises(ValueError):
        processor.process_order(order_id, user_data, items, None)

def test_OrderProcessor_process_order_paypal_fraud(monkeypatch):
    w = Warehouse({"item1": 5})
    processor = OrderProcessor(w)
    monkeypatch.setattr('datetime.datetime', lambda: datetime(2023, 1, 1, 14, 0, 0))
    order_id = "ORD_PAYPAL_FRAUD"
    user_data = {"email": "buyer@example.com", "age": 30, "payment_method": "PAYPAL"}
    items = [{"id": "item1", "qty": 1, "price": 546.44262295}]
    with pytest.raises(FraudDetectedError):
        processor.process_order(order_id, user_data, items, None)

@pytest.mark.parametrize('total_amount, user_tier, promo_code, mock_datetime_hour, expected', [
    (3000.0, "GOLD", None, 3, 0.10),
    (1500.0, "PLATINUM", "ABC-123", 2, 0.35),
    (500.0, "GOLD", None, 9, 0.10),
])
def test_DiscountEngine_calculate_discount_new_cases(monkeypatch, total_amount, user_tier, promo_code, mock_datetime_hour, expected):
    monkeypatch.setattr('datetime.datetime', lambda: datetime(2023, 1, 1, mock_datetime_hour, 0, 0))
    result = DiscountEngine.calculate_discount(total_amount, user_tier, promo_code)
    assert result == pytest.approx(expected)

def test_DiscountEngine_calculate_discount_promo_999_platinum():
    total_amount = 1500.0
    user_tier = "PLATINUM"
    promo_code = "QWE-999"
    result = DiscountEngine.calculate_discount(total_amount, user_tier, promo_code)
    assert result == pytest.approx(750.0)