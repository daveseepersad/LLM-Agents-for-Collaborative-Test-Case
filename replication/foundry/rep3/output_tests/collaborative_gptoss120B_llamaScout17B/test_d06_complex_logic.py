import pytest
from data.input_code.d06_complex_logic import *

@pytest.mark.parametrize('initial_stock, item_id, quantity, expected', [
    ({"itemA": 10}, "itemA", 5, True),
    ({"itemA": 10}, "itemA", 15, False),
])
def test_Warehouse_check_stock_success(initial_stock, item_id, quantity, expected):
    warehouse = Warehouse(initial_stock)
    assert warehouse.check_stock(item_id, quantity) == expected

def test_Warehouse_check_stock_not_found():
    warehouse = Warehouse({"itemA": 10})
    with pytest.raises(InventoryError):
        warehouse.check_stock("itemX", 1)

@pytest.mark.parametrize('initial_stock, item_id, quantity', [
    ({"itemB": 3}, "itemB", 5),
])
def test_Warehouse_lock_item_insufficient(initial_stock, item_id, quantity):
    warehouse = Warehouse(initial_stock)
    with pytest.raises(InventoryError):
        warehouse.lock_item(item_id, quantity)


@pytest.mark.parametrize('total_amount, user_tier, promo_code, mock_datetime_hour, expected', [
    (200.0, "GOLD", None, 2, 0.15),
    (1500.0, "PLATINUM", None, 12, 0.25),
    (800.0, "PLATINUM", None, 15, 0.20),
    (500.0, "GOLD", "ABC-123", 1, 0.25),
    (1000.0, "STANDARD", "XYZ-999", 10, 0.5),
    (100.0, "STANDARD", "BAD-CODE", 10, 'ValueError'),
])
def test_DiscountEngine_calculate_discount(mocker, total_amount, user_tier, promo_code, mock_datetime_hour, expected):
    mocker.patch('datetime.datetime.now', return_value=datetime(mock_datetime_hour, 1, 1))
    if isinstance(expected, str):
        with pytest.raises(eval(expected)):
            DiscountEngine.calculate_discount(total_amount, user_tier, promo_code)
    else:
        assert DiscountEngine.calculate_discount(total_amount, user_tier, promo_code) == expected

def test_DiscountEngine_calculate_discount_invalid_promo():
    with pytest.raises(ValueError):
        DiscountEngine.calculate_discount(100.0, "STANDARD", "bad_code")

@pytest.mark.parametrize('email, age, expected', [
    ("invalid_email", 30, "UserValidationError"),
    ("test@example.com", 16, "UserValidationError"),
    ("senior@example.com", 101, "UserValidationError"),
    ("test@example.com", 30, None),
])
def test_OrderProcessor_validate_user(email, age, expected):
    order_processor = OrderProcessor(Warehouse({}))
    if expected is None:
        order_processor.validate_user(email, age)
    else:
        with pytest.raises(eval(expected)):
            order_processor.validate_user(email, age)

@pytest.mark.parametrize('order_id, user_data, items, promo_code, warehouse_initial_stock, mock_datetime_hour, expected', [
    ("ORD001", {"email": "buyer@example.com", "age": 35, "tier": "STANDARD", "payment_method": "CC"}, [{"id": "item1", "qty": 2, "price": 50.0}, {"id": "item2", "qty": 1, "price": 30.0}], None, {"item1": 5, "item2": 3}, 14, {"status": "success", "order_id": "ORD001", "original_price": 130.0, "discount_applied": 0.0, "final_total": 158.6, "items_count": 2}),
    ("ORD002", {"email": "buyer2@example.com", "age": 40, "tier": "GOLD", "payment_method": "CC"}, [{"id": "itemX", "qty": 1, "price": 20.0}], None, {"itemX": 0}, 10, {"status": "failed", "reason": "Out of stock: Item itemX not found in warehouse."}),
    ("ORD003", {"email": "buyer3@example.com", "age": 28, "tier": "STANDARD", "payment_method": "CC"}, [{"id": "itemZ", "qty": -1, "price": 0.0}], None, {"itemZ": 10}, 9, {"status": "error", "reason": "Promo Error: Cannot return free items"}),
    ("ORD004", {"email": "buyer4@example.com", "age": 45, "tier": "STANDARD", "payment_method": "CC"}, [{"id": "item1", "qty": 1, "price": 100.0}], "BAD-12", {"item1": 5}, 12, {"status": "error", "reason": "Promo Error: Invalid promo code format"}),
    ("ORD005", {"email": "buyer5@example.com", "age": 30, "tier": "GOLD", "payment_method": "CC"}, [{"id": "item1", "qty": 2, "price": 200.0}], "ABC-999", {"item1": 10}, 8, {"status": "success", "order_id": "ORD005", "original_price": 400.0, "discount_applied": 0.5, "final_total": 244.0, "items_count": 1}),
    ("ORD006", {"email": "buyer6@example.com", "age": 27, "tier": "PLATINUM", "payment_method": "CC"}, [{"id": "item1", "qty": 1, "price": 1200.0}], "XYZ-123", {"item1": 5}, 2, {"status": "success", "order_id": "ORD006", "original_price": 1200.0, "discount_applied": 0.3, "final_total": 1024.8, "items_count": 1}),
    ("ORD007", {"email": "buyer7@example.com", "age": 40, "tier": "STANDARD", "payment_method": "PAYPAL"}, [{"id": "item1", "qty": 1, "price": 666.66}], None, {"item1": 2}, 10, {"status": "error", "reason": "Suspicious transaction amount"}),
    ("ORD008", {"email": "buyer8@example.com", "age": 33, "tier": "STANDARD", "payment_method": "CRYPTO"}, [{"id": "item1", "qty": 1, "price": 30.0}], None, {"item1": 5}, 13, {"status": "error", "reason": "Minimum crypto amount not met"}),
])
def test_OrderProcessor_process_order(mocker, order_id, user_data, items, promo_code, warehouse_initial_stock, mock_datetime_hour, expected):
    mocker.patch('datetime.datetime.now', return_value=datetime(mock_datetime_hour, 1, 1))
    warehouse = Warehouse(warehouse_initial_stock)
    order_processor = OrderProcessor(warehouse)
    result = order_processor.process_order(order_id, user_data, items, promo_code)
    assert result == expected