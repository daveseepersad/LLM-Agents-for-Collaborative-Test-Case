import pytest
from data.input_code.d06_complex_logic import *
from unittest.mock import MagicMock
from datetime import datetime

@pytest.mark.parametrize('total_amount, user_tier, promo_code, expected', [
    (100.0, "STANDARD", None, 0.0),
    (100.0, "GOLD", None, 0.1),
    (100.0, "PLATINUM", None, 0.2),
    (1000.1, "PLATINUM", None, 0.25),
    (100.0, "STANDARD", "ABC-123", 0.1),
    (100.0, "STANDARD", "ABC-999", 50.0)
])
def test_discount_engine_success(total_amount, user_tier, promo_code, expected):
    assert DiscountEngine.calculate_discount(total_amount, user_tier, promo_code) == expected

def test_discount_engine_error():
    with pytest.raises(ValueError):
        DiscountEngine.calculate_discount(100.0, "STANDARD", "bad")

def test_warehouse_check_stock_success():
    warehouse = Warehouse({"item1": 10})
    assert warehouse.check_stock("item1", 5) == True

def test_warehouse_check_stock_error():
    warehouse = Warehouse({"item1": 10})
    with pytest.raises(InventoryError):
        warehouse.check_stock("item2", 5)

def test_order_processor_validate_user_success():
    order_processor = OrderProcessor(Warehouse({}))
    try:
        order_processor.validate_user("test@example.com", 20)
    except UserValidationError:
        pytest.fail("User validation failed")

def test_order_processor_validate_user_error():
    order_processor = OrderProcessor(Warehouse({}))
    with pytest.raises(UserValidationError):
        order_processor.validate_user("not-an-email", 20)

def test_order_processor_process_order_success():
    warehouse = Warehouse({"item1": 10})
    order_processor = OrderProcessor(warehouse)
    result = order_processor.process_order("order1", {"email": "test@example.com", "age": 20}, [{"id": "item1", "qty": 5, "price": 10.0}], None)
    assert result["status"] == "success"

def test_order_processor_process_order_error():
    warehouse = Warehouse({"item1": 10})
    order_processor = OrderProcessor(warehouse)
    result = order_processor.process_order("order1", {"email": "test@example.com", "age": 20}, [{"id": "item2", "qty": 5, "price": 10.0}], None)
    assert result["status"] == "failed"

def test_order_processor_process_order_promo_error():
    warehouse = Warehouse({"item1": 10})
    order_processor = OrderProcessor(warehouse)
    result = order_processor.process_order("order1", {"email": "test@example.com", "age": 20}, [{"id": "item1", "qty": 5, "price": 10.0}], "bad")
    assert result["status"] == "error"

def test_order_processor_process_order_user_error():
    warehouse = Warehouse({"item1": 10})
    order_processor = OrderProcessor(warehouse)
    with pytest.raises(UserValidationError):
        order_processor.process_order("order1", {"email": "not-an-email", "age": 20}, [{"id": "item1", "qty": 5, "price": 10.0}], None)

def test_order_processor_validate_user_over_100():
    order_processor = OrderProcessor(Warehouse({}))
    with pytest.raises(UserValidationError):
        order_processor.validate_user("user@example.com", 101)

def test_order_processor_process_order_paypal_fraud():
    warehouse = Warehouse({"item1": 10})
    order_processor = OrderProcessor(warehouse)
    with pytest.raises(FraudDetectedError):
        order_processor.process_order("order1", {"email": "test@example.com", "age": 20, "payment_method": "PAYPAL"}, [{"id": "item1", "qty": 1, "price": 546.44}], None)

def test_order_processor_process_order_crypto_min_amount():
    warehouse = Warehouse({"item1": 10})
    order_processor = OrderProcessor(warehouse)
    with pytest.raises(PaymentError):
        order_processor.process_order("order2", {"email": "test@example.com", "age": 25, "payment_method": "CRYPTO"}, [{"id": "item1", "qty": 1, "price": 40.0}], None)


def test_order_processor_rollback_on_inventory_error():
    warehouse = Warehouse({"item1": 10, "item2": 0})
    order_processor = OrderProcessor(warehouse)
    result = order_processor.process_order("order-rollback", {"email": "test@example.com", "age": 25}, [{"id": "item1", "qty": 2, "price": 10.0}, {"id": "item2", "qty": 3, "price": 5.0}], None)
    assert result["status"] == "failed"

def test_order_processor_trap_free_items_neg_qty_zero_price():
    warehouse = Warehouse({"item1": 10})
    order_processor = OrderProcessor(warehouse)
    with pytest.raises(ValueError):
        order_processor.process_order("order-trap", {"email": "user@example.com", "age": 22}, [{"id": "item1", "qty": -1, "price": 0.0}], None)

def test_order_processor_validate_user_below_18():
    order_processor = OrderProcessor(Warehouse({}))
    with pytest.raises(UserValidationError):
        order_processor.validate_user("child@example.com", 17)