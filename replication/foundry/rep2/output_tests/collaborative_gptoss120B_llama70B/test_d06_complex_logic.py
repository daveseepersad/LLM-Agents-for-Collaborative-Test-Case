import pytest
from data.input_code.d06_complex_logic import *


def test_order_processor_process_order_fraud_detected_error_success():
    warehouse = Warehouse({'itemA': 10})
    order_processor = OrderProcessor(warehouse)
    result = order_processor.process_order('ORD005', {'email': 'fraud@example.com', 'age': 40, 'tier': 'STANDARD', 'payment_method': 'PAYPAL'}, [{'id': 'itemA', 'qty': 3, 'price': 222.21}], None)
    assert result['status'] == 'success'
    assert 'order_id' in result
    assert 'original_price' in result
    assert 'discount_applied' in result
    assert 'final_total' in result
    assert 'items_count' in result