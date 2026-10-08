import pytest
from data.input_code.d06_complex_logic import *
from unittest.mock import patch, MagicMock

@pytest.mark.parametrize('order_id, user_data, items, promo_code, expected', [
    ("O1", {"email": "test@example.com", "age": 30, "tier": "STANDARD", "payment_method": "CC"}, [{"id": "A", "qty": 2, "price": 10.0}], None, 
     {"status": "success", "order_id": "O1", "original_price": 20.0, "discount_applied": 0.0, "final_total": 24.4, "items_count": 1}),
    ("O2", {"email": "gold@example.com", "age": 45, "tier": "GOLD", "payment_method": "CC"}, [{"id": "A", "qty": 1, "price": 10.0}], None, 
     {"status": "success", "order_id": "O2", "original_price": 10.0, "discount_applied": 0.1, "final_total": 10.98, "items_count": 1}),
    ("O3", {"email": "plat@example.com", "age": 55, "tier": "PLATINUM", "payment_method": "CC"}, [{"id": "B", "qty": 1, "price": 2000.0}], None, 
     {"status": "success", "order_id": "O3", "original_price": 2000.0, "discount_applied": 0.25, "final_total": 1830.0, "items_count": 1}),
    ("O4", {"email": "promo@example.com", "age": 40, "tier": "STANDARD", "payment_method": "CC"}, [{"id": "C", "qty": 1, "price": 100.0}], "ABC-123", 
     {"status": "success", "order_id": "O4", "original_price": 100.0, "discount_applied": 0.1, "final_total": 109.8, "items_count": 1}),
])
def test_process_order_success(order_id, user_data, items, promo_code, expected):
    warehouse = Warehouse({"A": 5, "B": 2, "C": 10})
    processor = OrderProcessor(warehouse)
    result = processor.process_order(order_id, user_data, items, promo_code)
    assert result == expected

def test_process_order_promo_invalid_format():
    warehouse = Warehouse({"D": 5})
    processor = OrderProcessor(warehouse)
    result = processor.process_order("O5", {"email": "badpromo@example.com", "age": 30, "tier": "STANDARD", "payment_method": "CC"}, 
                                     [{"id": "D", "qty": 1, "price": 50.0}], "AB12-34")
    assert result == {"status": "error", "reason": "Promo Error: Invalid promo code format"}

def test_process_order_invalid_email():
    warehouse = Warehouse({"E": 5})
    processor = OrderProcessor(warehouse)
    with pytest.raises(UserValidationError):
        processor.process_order("O6", {"email": "not-an-email", "age": 30, "tier": "STANDARD", "payment_method": "CC"}, 
                                [{"id": "E", "qty": 1, "price": 20.0}])

def test_process_order_age_under_18():
    warehouse = Warehouse({"F": 5})
    processor = OrderProcessor(warehouse)
    with pytest.raises(UserValidationError):
        processor.process_order("O7", {"email": "young@example.com", "age": 17, "tier": "STANDARD", "payment_method": "CC"}, 
                                [{"id": "F", "qty": 1, "price": 15.0}])

def test_process_order_age_over_100():
    warehouse = Warehouse({"G": 5})
    processor = OrderProcessor(warehouse)
    with pytest.raises(UserValidationError):
        processor.process_order("O8", {"email": "oldtimer@example.com", "age": 101, "tier": "STANDARD", "payment_method": "CC"}, 
                                [{"id": "G", "qty": 1, "price": 30.0}])

def test_process_order_item_not_found():
    warehouse = Warehouse({"H": 5})
    processor = OrderProcessor(warehouse)
    result = processor.process_order("O9", {"email": "missing@example.com", "age": 35, "tier": "STANDARD", "payment_method": "CC"}, 
                                     [{"id": "UNKNOWN", "qty": 1, "price": 10.0}])
    assert result == {"status": "failed", "reason": "Out of stock: Item UNKNOWN not found in warehouse."}

def test_process_order_insufficient_stock():
    warehouse = Warehouse({"I": 5})
    processor = OrderProcessor(warehouse)
    result = processor.process_order("O10", {"email": "shortstock@example.com", "age": 40, "tier": "STANDARD", "payment_method": "CC"}, 
                                     [{"id": "I", "qty": 10, "price": 5.0}])
    assert result == {"status": "failed", "reason": "Out of stock: Insufficient stock for I"}

def test_process_order_qty_neg_price_zero():
    warehouse = Warehouse({"J": 5})
    processor = OrderProcessor(warehouse)
    with pytest.raises(ValueError):
        processor.process_order("O11", {"email": "return@example.com", "age": 30, "tier": "STANDARD", "payment_method": "CC"}, 
                                [{"id": "J", "qty": -1, "price": 0.0}])

def test_process_order_paypal_fraud():
    warehouse = Warehouse({"K": 1})
    processor = OrderProcessor(warehouse)
    with pytest.raises(FraudDetectedError):
        processor.process_order("O12", {"email": "fraud@example.com", "age": 45, "tier": "STANDARD", "payment_method": "PAYPAL"}, 
                                [{"id": "K", "qty": 1, "price": 546.44}])

def test_process_order_crypto_min_amount():
    warehouse = Warehouse({"L": 1})
    processor = OrderProcessor(warehouse)
    with pytest.raises(PaymentError):
        processor.process_order("O13", {"email": "crypto@example.com", "age": 28, "tier": "STANDARD", "payment_method": "CRYPTO"}, 
                                [{"id": "L", "qty": 1, "price": 30.0}])

def test_calculate_discount():
    discount = DiscountEngine.calculate_discount(200.0, "STANDARD", "XYZ-999")
    assert discount == 100.0