import pytest
from data.input_code.d06_complex_logic import *

@pytest.mark.parametrize('order_id, user_data, items, promo_code, expected', [
    ("order1", {"email": "test@example.com", "age": 25, "payment_method": "PAYPAL"}, [{"id": "item1", "qty": 2, "price": 333.33}], "ABC-123", "FraudDetectedError"),
    ("order1", {"email": "test@example.com", "age": 25, "payment_method": "CRYPTO"}, [{"id": "item1", "qty": 1, "price": 10.0}], "ABC-123", "PaymentError")
])
def test_order_processor_process_order_edge_cases(warehouse, order_id, user_data, items, promo_code, expected):
    order_processor = OrderProcessor(warehouse)
    if expected == "FraudDetectedError":
        with pytest.raises(FraudDetectedError):
            order_processor.process_order(order_id, user_data, items, promo_code)
    elif expected == "PaymentError":
        with pytest.raises(PaymentError):
            order_processor.process_order(order_id, user_data, items, promo_code)

@pytest.mark.parametrize('order_id, user_data, items, promo_code, expected', [
    ("order1", {"email": "test@example.com", "age": 25, "payment_method": "PAYPAL"}, [{"id": "item1", "qty": 2, "price": 333.33}], "ABC-123", {"status": "success", "order_id": "order1", "original_price": 666.66, "discount_applied": 0.1, "final_total": 599.94, "items_count": 2}),
])
def test_order_processor_process_order_edge_cases_final_price(warehouse, order_id, user_data, items, promo_code, expected):
    order_processor = OrderProcessor(warehouse)
    result = order_processor.process_order(order_id, user_data, items, promo_code)
    assert result == expected