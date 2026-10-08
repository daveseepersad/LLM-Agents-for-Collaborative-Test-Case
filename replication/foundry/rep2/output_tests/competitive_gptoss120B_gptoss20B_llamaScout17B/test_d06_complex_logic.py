import pytest
from data.input_code.d06_complex_logic import *

@pytest.mark.parametrize('total_amount, user_tier, promo_code, mock_datetime_hour, expected', [
    (100.0, "STANDARD", None, 2, 0.0),
])
def test_DiscountEngine_night_discount(monkeypatch, total_amount, user_tier, promo_code, mock_datetime_hour, expected):
    if mock_datetime_hour is not None:
        monkeypatch.setattr('datetime.datetime', lambda *args, **kwargs: datetime(2023, 1, 1, mock_datetime_hour, 0))
    result = DiscountEngine.calculate_discount(total_amount, user_tier, promo_code)
    assert result == expected

@pytest.mark.parametrize('total_amount, user_tier, promo_code, mock_datetime_hour, expected', [
    (2000.0, "PLATINUM", "ABC-123", 1, 0.35),
])
def test_DiscountEngine_cap(monkeypatch, total_amount, user_tier, promo_code, mock_datetime_hour, expected):
    if mock_datetime_hour is not None:
        monkeypatch.setattr('datetime.datetime', lambda *args, **kwargs: datetime(2023, 1, 1, mock_datetime_hour, 0))
    result = DiscountEngine.calculate_discount(total_amount, user_tier, promo_code)
    assert result == expected

# Warehouse tests
@pytest.mark.parametrize('initial_stock, item_id, quantity, expected', [
    ({"itemX": 5}, "itemX", 3, True),
])
def test_Warehouse_check_stock_true(initial_stock, item_id, quantity, expected):
    warehouse = Warehouse(initial_stock)
    assert warehouse.check_stock(item_id, quantity) == expected

@pytest.mark.parametrize('initial_stock, item_id, quantity, expected', [
    ({"itemX": 5}, "itemX", 6, False),
])
def test_Warehouse_check_stock_false(initial_stock, item_id, quantity, expected):
    warehouse = Warehouse(initial_stock)
    assert warehouse.check_stock(item_id, quantity) == expected

@pytest.mark.parametrize('initial_stock, item_id, quantity, expected_locked', [
    ({"itemY": 5}, "itemY", 2, {"itemY": 2}),
])
def test_Warehouse_lock_item(initial_stock, item_id, quantity, expected_locked):
    warehouse = Warehouse(initial_stock)
    warehouse.lock_item(item_id, quantity)
    assert warehouse._locked_stock == expected_locked

@pytest.mark.parametrize('initial_stock, pre_locked, item_id, quantity, expected_locked', [
    ({"itemZ": 5}, {}, "itemZ", 1, {}),
])
def test_Warehouse_release_no_lock(initial_stock, pre_locked, item_id, quantity, expected_locked):
    warehouse = Warehouse(initial_stock)
    warehouse._locked_stock = pre_locked
    warehouse.release_item(item_id, quantity)
    assert warehouse._locked_stock == expected_locked

# OrderProcessor tests
def test_OrderProcessor_partial_rollback(monkeypatch):
    warehouse = Warehouse({"a": 5, "b": 5})
    processor = OrderProcessor(warehouse)
    order_id = "ORD_PARTIAL"
    user_data = {"email": "test@example.com", "age": 30, "tier": "STANDARD", "payment_method": "CC"}
    items = [
        {"id": "a", "qty": 3, "price": 10.0},
        {"id": "b", "qty": 6, "price": 10.0}
    ]
    result = processor.process_order(order_id, user_data, items, None)
    expected = {"status": "failed", "reason": "Out of stock: Insufficient stock for b"}
    assert result == expected
    # Ensure rollback happened (no items remain locked)
    assert warehouse._locked_stock == {}

@pytest.mark.parametrize('warehouse_stock, item, qty, price, expected', [
    ({"c": 5}, "c", 1, 10.0, {"status": "success", "order_id": "ORD_PAYPAL", "original_price": 10.0, "discount_applied": 0.0, "final_total": 12.2, "items_count": 1}),
])
def test_OrderProcessor_paypal_success(monkeypatch, warehouse_stock, item, qty, price, expected):
    warehouse = Warehouse(warehouse_stock)
    processor = OrderProcessor(warehouse)
    order_id = "ORD_PAYPAL"
    user_data = {"email": "test2@example.com", "age": 30, "tier": "STANDARD", "payment_method": "PAYPAL"}
    items = [ {"id": item, "qty": qty, "price": price} ]
    # Ensure no night discount affects result
    monkeypatch.setattr('datetime.datetime', lambda *args, **kwargs: datetime(2023, 1, 1, 12, 0))
    result = processor.process_order(order_id, user_data, items, None)
    assert result == expected

@pytest.mark.parametrize('warehouse_stock, items, order_id, user_data, expected', [
    ({"d": 5}, [ {"id": "d", "qty": 2, "price": 40.0} ], "ORD_CRYPTO", {"email": "crypto@example.com", "age": 30, "tier": "STANDARD", "payment_method": "CRYPTO"}, 
     {"status": "success", "order_id": "ORD_CRYPTO", "original_price": 80.0, "discount_applied": 0.0, "final_total": 97.6, "items_count": 1}),
])
def test_OrderProcessor_crypto_success(monkeypatch, warehouse_stock, items, order_id, user_data, expected):
    warehouse = Warehouse(warehouse_stock)
    processor = OrderProcessor(warehouse)
    # Ensure non-night time to avoid discount affecting result
    monkeypatch.setattr('datetime.datetime', lambda *args, **kwargs: datetime(2023, 1, 1, 12, 0))
    result = processor.process_order(order_id, user_data, items, None)
    assert result == expected

import pytest
from datetime import datetime

# New DiscountEngine tests
@pytest.mark.parametrize('total_amount, user_tier, promo_code, mock_datetime_hour, expected', [
    (100.0, "GOLD", None, 12, 0.10),
    (900.0, "PLATINUM", None, 12, 0.20),
    (200.0, "STANDARD", "XYZ-123", 12, 0.10),
    (200.0, "STANDARD", "badcode", 12, "ValueError"),
    (300.0, "STANDARD", "ABC-999", 12, 150.0),
])
def test_DiscountEngine_calculate_discount_param(monkeypatch, total_amount, user_tier, promo_code, mock_datetime_hour, expected):
    if mock_datetime_hour is not None:
        # Align with existing tests' monkeypatch approach
        from datetime import datetime as dt
        monkeypatch.setattr('datetime.datetime', lambda *args, **kwargs: dt(2023, 1, 1, mock_datetime_hour, 0))
    if expected == "ValueError":
        with pytest.raises(ValueError):
            DiscountEngine.calculate_discount(total_amount, user_tier, promo_code)
    else:
        result = DiscountEngine.calculate_discount(total_amount, user_tier, promo_code)
        assert result == expected


# New Warehouse tests
@pytest.mark.parametrize('initial_stock, item_id, quantity', [
    ({"itemA": 2}, "itemA", 3),
])
def test_Warehouse_lock_item_insufficient_stock(initial_stock, item_id, quantity):
    warehouse = Warehouse(initial_stock)
    with pytest.raises(InventoryError):
        warehouse.lock_item(item_id, quantity)


@pytest.mark.parametrize('initial_stock, item_id, quantity', [
    ({"itemA": 5}, "missing", 1),
])
def test_Warehouse_check_stock_unknown_item(initial_stock, item_id, quantity):
    warehouse = Warehouse(initial_stock)
    with pytest.raises(InventoryError):
        warehouse.check_stock(item_id, quantity)


def test_Warehouse_release_item_deletes_key_when_zero():
    warehouse = Warehouse({"itemB": 5})
    warehouse._locked_stock = {"itemB": 2}
    warehouse.release_item("itemB", 2)
    assert warehouse._locked_stock == {}


# New OrderProcessor tests
def test_OrderProcessor_invalid_email():
    warehouse = Warehouse({"x": 5})
    processor = OrderProcessor(warehouse)
    order_id = "ORD1"
    user_data = {"email": "bademail", "age": 30, "tier": "STANDARD", "payment_method": "CC"}
    items = [{"id": "x", "qty": 1, "price": 10.0}]
    with pytest.raises(UserValidationError):
        processor.process_order(order_id, user_data, items, None)


def test_OrderProcessor_age_under_18():
    warehouse = Warehouse({"x": 5})
    processor = OrderProcessor(warehouse)
    order_id = "ORD2"
    user_data = {"email": "test@example.com", "age": 16, "tier": "STANDARD", "payment_method": "CC"}
    items = [{"id": "x", "qty": 1, "price": 10.0}]
    with pytest.raises(UserValidationError):
        processor.process_order(order_id, user_data, items, None)


def test_OrderProcessor_age_over_100():
    warehouse = Warehouse({"x": 5})
    processor = OrderProcessor(warehouse)
    order_id = "ORD3"
    user_data = {"email": "test@example.com", "age": 101, "tier": "STANDARD", "payment_method": "CC"}
    items = [{"id": "x", "qty": 1, "price": 10.0}]
    with pytest.raises(UserValidationError):
        processor.process_order(order_id, user_data, items, None)


def test_OrderProcessor_invalid_promo_returns_error():
    warehouse = Warehouse({"y": 5})
    processor = OrderProcessor(warehouse)
    order_id = "ORD_ERR"
    user_data = {"email": "test@example.com", "age": 30, "tier": "STANDARD", "payment_method": "CC"}
    items = [{"id": "y", "qty": 1, "price": 10.0}]
    result = processor.process_order(order_id, user_data, items, "BAD-12")
    expected = {"status": "error", "reason": "Promo Error: Invalid promo code format"}
    assert result == expected


def test_OrderProcessor_paypal_fraud_detection():
    warehouse = Warehouse({"z": 5})
    processor = OrderProcessor(warehouse)
    order_id = "ORD_FRAUD"
    user_data = {"email": "test@example.com", "age": 30, "tier": "STANDARD", "payment_method": "PAYPAL"}
    # Price chosen so that final_price_with_tax rounds to 666.66
    items = [{"id": "z", "qty": 1, "price": 546.4426}]
    with pytest.raises(FraudDetectedError):
        # Ensure not using night discount
        monkeypatch = pytest.MonkeyPatch()
        monkeypatch.setattr('datetime.datetime', lambda *args, **kwargs: datetime(2023, 1, 1, 12, 0))
        try:
            processor.process_order(order_id, user_data, items, None)
        finally:
            monkeypatch.undo()


def test_OrderProcessor_crypto_min_amount():
    warehouse = Warehouse({"c": 5})
    processor = OrderProcessor(warehouse)
    order_id = "ORD_CRYPTO_MIN"
    user_data = {"email": "crypto@example.com", "age": 30, "tier": "STANDARD", "payment_method": "CRYPTO"}
    items = [{"id": "c", "qty": 1, "price": 40.0}]
    with pytest.raises(PaymentError):
        processor.process_order(order_id, user_data, items, None)


def test_OrderProcessor_zero_price_negative_qty():
    warehouse = Warehouse({"n": 5})
    processor = OrderProcessor(warehouse)
    order_id = "ORD_RETURN"
    user_data = {"email": "test@example.com", "age": 30, "tier": "STANDARD", "payment_method": "CC"}
    items = [{"id": "n", "qty": -1, "price": 0.0}]
    with pytest.raises(ValueError):
        processor.process_order(order_id, user_data, items, None)



@pytest.mark.parametrize('warehouse_stock, order_id, user_data, items, promo_code, mock_datetime_hour, expected', [
    ({}, "ORD_EMPTY", {"email": "empty@example.com", "age": 30, "tier": "STANDARD", "payment_method": "CC"}, 
     [], None, 12, 
     {"status": "success", "order_id": "ORD_EMPTY", "original_price": 0.0, "discount_applied": 0.0, "final_total": 0.0, "items_count": 0}),
])
def test_OrderProcessor_empty_items(monkeypatch, warehouse_stock, order_id, user_data, items, promo_code, mock_datetime_hour, expected):
    if mock_datetime_hour is not None:
        monkeypatch.setattr('datetime.datetime', lambda *args, **kwargs: datetime(2023, 1, 1, mock_datetime_hour, 0))
    warehouse = Warehouse(warehouse_stock)
    processor = OrderProcessor(warehouse)
    result = processor.process_order(order_id, user_data, items, promo_code)
    assert result == expected


@pytest.mark.parametrize('initial_stock, pre_locked, item_id, quantity, expected_locked', [
    ({"itemK": 5}, {"itemK": 2}, "itemK", 5, {}),
])
def test_Warehouse_release_over(initial_stock, pre_locked, item_id, quantity, expected_locked):
    warehouse = Warehouse(initial_stock)
    warehouse._locked_stock = pre_locked
    warehouse.release_item(item_id, quantity)
    assert warehouse._locked_stock == expected_locked