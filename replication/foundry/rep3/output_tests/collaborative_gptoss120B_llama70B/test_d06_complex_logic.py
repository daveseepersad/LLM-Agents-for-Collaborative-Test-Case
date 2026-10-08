import pytest
from data.input_code.d06_complex_logic import *


def test_order_processor_process_order_promo_valid():
    warehouse = Warehouse({"item1": 5})
    order_processor = OrderProcessor(warehouse)
    result = order_processor.process_order("ORD126", {"email": "buyer@example.com", "age": 28, "tier": "STANDARD", "payment_method": "CC"}, [{"id": "item1", "qty": 1, "price": 30.0}], "ABC-123")
    assert result["status"] == "success"


def test_order_processor_process_order_invalid_email():
    warehouse = Warehouse({"item1": 5})
    order_processor = OrderProcessor(warehouse)
    with pytest.raises(UserValidationError):
        order_processor.process_order("ORD126", {"email": "invalid", "age": 28, "tier": "STANDARD", "payment_method": "CC"}, [{"id": "item1", "qty": 1, "price": 30.0}], "ABC-123")

def test_order_processor_process_order_age_under_18():
    warehouse = Warehouse({"item1": 5})
    order_processor = OrderProcessor(warehouse)
    with pytest.raises(UserValidationError):
        order_processor.process_order("ORD126", {"email": "buyer@example.com", "age": 17, "tier": "STANDARD", "payment_method": "CC"}, [{"id": "item1", "qty": 1, "price": 30.0}], "ABC-123")

def test_order_processor_process_order_age_over_100():
    warehouse = Warehouse({"item1": 5})
    order_processor = OrderProcessor(warehouse)
    with pytest.raises(UserValidationError):
        order_processor.process_order("ORD126", {"email": "buyer@example.com", "age": 101, "tier": "STANDARD", "payment_method": "CC"}, [{"id": "item1", "qty": 1, "price": 30.0}], "ABC-123")


def test_order_processor_process_order_payment_error():
    warehouse = Warehouse({"item1": 5})
    order_processor = OrderProcessor(warehouse)
    with pytest.raises(PaymentError):
        order_processor.process_order("ORD126", {"email": "buyer@example.com", "age": 28, "tier": "STANDARD", "payment_method": "CRYPTO"}, [{"id": "item1", "qty": 1, "price": 10.0}], "ABC-123")