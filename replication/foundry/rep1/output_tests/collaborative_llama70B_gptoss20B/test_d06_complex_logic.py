def test_discount_night_gold(monkeypatch):
    import pytest
    import data.input_code.d06_complex_logic as module
    class DummyDateTime:
        @classmethod
        def now(cls):
            class N:
                hour = 2
            return N()
    monkeypatch.setattr(module, "datetime", DummyDateTime)
    disc = module.DiscountEngine.calculate_discount(100.0, "GOLD")
    assert disc == pytest.approx(0.15)

import pytest
from data.input_code.d06_complex_logic import *
def test_discount_platinum_no_night_with_promo(monkeypatch):
    import data.input_code.d06_complex_logic as module
    class DummyDateTime:
        @classmethod
        def now(cls):
            class N:
                hour = 23
            return N()
    monkeypatch.setattr(module, "datetime", DummyDateTime)
    disc = module.DiscountEngine.calculate_discount(1000.01, "PLATINUM", "ABC-123")
    assert disc == pytest.approx(0.35)

def test_discount_promo_code_valid_with_night(monkeypatch):
    import data.input_code.d06_complex_logic as module
    class DummyDateTime:
        @classmethod
        def now(cls):
            class N:
                hour = 2
            return N()
    monkeypatch.setattr(module, "datetime", DummyDateTime)
    disc = module.DiscountEngine.calculate_discount(100.0, "STANDARD", "ABC-123")
    assert disc == pytest.approx(0.15)

def test_discount_promo_code_invalid_raises(monkeypatch):
    import data.input_code.d06_complex_logic as module
    class DummyDateTime:
        @classmethod
        def now(cls):
            class N:
                hour = 1
            return N()
    monkeypatch.setattr(module, "datetime", DummyDateTime)
    with pytest.raises(ValueError):
        module.DiscountEngine.calculate_discount(100.0, "STANDARD", "Invalid")

def test_discount_promo_code_super(monkeypatch):
    import data.input_code.d06_complex_logic as module
    class DummyDateTime:
        @classmethod
        def now(cls):
            class N:
                hour = 3
            return N()
    monkeypatch.setattr(module, "datetime", DummyDateTime)
    disc = module.DiscountEngine.calculate_discount(100.0, "STANDARD", "ABC-999")
    assert disc == pytest.approx(50.0)

def test_order_processor_validate_user_invalid_email():
    import data.input_code.d06_complex_logic as module
    w = module.Warehouse({})
    op = module.OrderProcessor(w)
    with pytest.raises(module.UserValidationError):
        op.validate_user("invalid_email", 25)

def test_order_processor_validate_user_age_under_18():
    import data.input_code.d06_complex_logic as module
    w = module.Warehouse({})
    op = module.OrderProcessor(w)
    with pytest.raises(module.UserValidationError):
        op.validate_user("test@example.com", 17)

def test_order_processor_validate_user_age_over_100():
    import data.input_code.d06_complex_logic as module
    w = module.Warehouse({})
    op = module.OrderProcessor(w)
    with pytest.raises(module.UserValidationError):
        op.validate_user("test@example.com", 101)

def test_order_processing_out_of_stock():
    import data.input_code.d06_complex_logic as module
    w = module.Warehouse({"item1": 5})
    op = module.OrderProcessor(w)
    items = [{"id": "item1", "qty": 10, "price": 10.0}]
    res = op.process_order("test_order", {"email": "test@example.com", "age": 25, "tier": "STANDARD"}, items, None)
    assert res == {"status": "failed", "reason": "Out of stock: Insufficient stock for item1"}

def test_order_processing_payment_error_paypal_fraud(monkeypatch):
    import data.input_code.d06_complex_logic as module
    w = module.Warehouse({"item1": 2})
    op = module.OrderProcessor(w)
    class DummyDateTime:
        @classmethod
        def now(cls):
            class N:
                hour = 0
            return N()
    monkeypatch.setattr(module, "datetime", DummyDateTime)
    price = 666.66 / 1.22
    monkeypatch.setattr(module.DiscountEngine, "calculate_discount", lambda total, tier, promo=None: 0.0)
    items = [{"id": "item1", "qty": 1, "price": price}]
    with pytest.raises(module.FraudDetectedError):
        op.process_order("order1", {"email": "test@example.com", "age": 25, "tier": "STANDARD", "payment_method": "PAYPAL"}, items, None)

def test_order_processing_payment_error_crypto():
    import data.input_code.d06_complex_logic as module
    w = module.Warehouse({"item1": 5})
    op = module.OrderProcessor(w)
    items = [{"id": "item1", "qty": 1, "price": 10.0}]
    with pytest.raises(module.PaymentError):
        op.process_order("order2", {"email": "test@example.com", "age": 25, "tier": "STANDARD", "payment_method": "CRYPTO"}, items, None)

def test_order_processing_division_by_zero():
    import data.input_code.d06_complex_logic as module
    w = module.Warehouse({"item1": 5})
    op = module.OrderProcessor(w)
    items = [{"id": "item1", "qty": -1, "price": 0.0}]
    with pytest.raises(ValueError):
        op.process_order("order3", {"email": "test@example.com", "age": 25, "tier": "STANDARD"}, items, None)