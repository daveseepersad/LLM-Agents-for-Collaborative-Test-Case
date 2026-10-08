import pytest
from data.input_code.d06_complex_logic import *

def test_order_processor_process_order_payment_error():
    warehouse = Warehouse({'item1': 10})
    order_processor = OrderProcessor(warehouse)
    result = order_processor.process_order('order1', {'email': 'test@example.com', 'age': 25, 'tier': 'GOLD', 'payment_method': 'PAYPAL'}, [{'id': 'item1', 'qty': 1, 'price': 666.66}], None)
    assert result == {'status': 'success', 'order_id': 'order1', 'original_price': 666.66, 'discount_applied': 0.1, 'final_total': 731.99, 'items_count': 1}

