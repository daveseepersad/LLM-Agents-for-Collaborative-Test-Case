import pytest
from data.input_code.d06_complex_logic import *

@pytest.fixture
def warehouse():
    return Warehouse({"item1": 100, "item2": 50})

@pytest.fixture
def order_processor(warehouse):
    return OrderProcessor(warehouse)

def test_check_stock(warehouse):
    assert warehouse.check_stock("item1", 10) == True
    assert warehouse.check_stock("item1", 100) == True
    assert warehouse.check_stock("item1", 101) == False
    with pytest.raises(InventoryError):
        warehouse.check_stock("item3", 10)

def test_lock_and_release_item(warehouse):
    warehouse.lock_item("item1", 10)
    assert warehouse._locked_stock["item1"] == 10
    warehouse.release_item("item1", 5)
    assert warehouse._locked_stock["item1"] == 5
    warehouse.release_item("item1", 5)
    assert "item1" not in warehouse._locked_stock

def test_calculate_discount():
    assert DiscountEngine.calculate_discount(500, "GOLD") == 0.10
    assert DiscountEngine.calculate_discount(1500, "PLATINUM") == 0.25
    assert DiscountEngine.calculate_discount(1500, "PLATINUM", "ABC-999") == 750.0
    with pytest.raises(ValueError):
        DiscountEngine.calculate_discount(500, "GOLD", "INVALID")

def test_validate_user():
    order_processor = OrderProcessor(Warehouse({}))
    order_processor.validate_user("test@test.com", 25)
    with pytest.raises(UserValidationError):
        order_processor.validate_user("invalid-email", 25)
    with pytest.raises(UserValidationError):
        order_processor.validate_user("test@test.com", 17)
    with pytest.raises(UserValidationError):
        order_processor.validate_user("test@test.com", 101)

def test_process_order_success(order_processor):
    order_data = {
        "email": "test@test.com",
        "age": 25,
        "tier": "GOLD",
        "payment_method": "CC"
    }
    items = [{"id": "item1", "qty": 2, "price": 100.0}]
    result = order_processor.process_order("order1", order_data, items)
    assert result["status"] == "success"
    assert result["final_total"] > 0

def test_process_order_insufficient_stock(order_processor):
    order_data = {
        "email": "test@test.com",
        "age": 25,
        "tier": "GOLD",
        "payment_method": "CC"
    }
    items = [{"id": "item1", "qty": 101, "price": 100.0}]
    result = order_processor.process_order("order2", order_data, items)
    assert result["status"] == "failed"
    assert "Out of stock" in result["reason"]

def test_process_order_invalid_promo_code(order_processor):
    order_data = {
        "email": "test@test.com",
        "age": 25,
        "tier": "GOLD",
        "payment_method": "CC"
    }
    items = [{"id": "item1", "qty": 2, "price": 100.0}]
    result = order_processor.process_order("order3", order_data, items, "INVALID")
    assert result["status"] == "error"
    assert "Promo Error" in result["reason"]

def test_process_order_paypal_no_fraud(order_processor):
    order_data = {
        "email": "test@test.com",
        "age": 25,
        "tier": "GOLD",
        "payment_method": "PAYPAL"
    }
    items = [{"id": "item1", "qty": 2, "price": 100.0}]
    # Ensure no FraudDetectedError is unexpectedly raised
    try:
        result = order_processor.process_order("order4", order_data, items)
    except FraudDetectedError:
        pytest.fail("Fraud detected unexpectedly")
    assert result["status"] == "success"
    assert "final_total" in result

def test_process_order_crypto_minimum(order_processor):
    order_data = {
        "email": "test@test.com",
        "age": 25,
        "tier": "GOLD",
        "payment_method": "CRYPTO"
    }
    items = [{"id": "item1", "qty": 1, "price": 10.0}]
    with pytest.raises(PaymentError):
        order_processor.process_order("order5", order_data, items)

def test_discount_night_with_monkeypatched_datetime(monkeypatch):
    class FakeDateTime:
        @classmethod
        def now(cls):
            import datetime as real_dt
            return real_dt.datetime(2020, 1, 1, 3, 0, 0)
    monkeypatch.setattr("data.input_code.d06_complex_logic.datetime", FakeDateTime, raising=True)
    assert DiscountEngine.calculate_discount(100.0, "STANDARD", None) == 0.05

def test_discount_platinum_no_extra_with_monkeypatched_datetime(monkeypatch):
    class FakeDateTime:
        @classmethod
        def now(cls):
            import datetime as real_dt
            return real_dt.datetime(2020, 1, 1, 12, 0, 0)
    monkeypatch.setattr("data.input_code.d06_complex_logic.datetime", FakeDateTime, raising=True)
    assert DiscountEngine.calculate_discount(900.0, "PLATINUM", None) == 0.20

def test_discount_cap_with_monkeypatched_datetime(monkeypatch):
    class FakeDateTime:
        @classmethod
        def now(cls):
            import datetime as real_dt
            return real_dt.datetime(2020, 1, 1, 2, 0, 0)
    monkeypatch.setattr("data.input_code.d06_complex_logic.datetime", FakeDateTime, raising=True)
    assert DiscountEngine.calculate_discount(2000.0, "PLATINUM", "ABC-123") == 0.40

def test_validate_user_age_100_passes():
    w = Warehouse({})
    op = OrderProcessor(w)
    op.validate_user("test@test.com", 100)

def test_process_order_neg_qty_zero_price_raises(order_processor):
    order_data = {
        "email": "test@test.com",
        "age": 30,
        "tier": "STANDARD",
        "payment_method": "CC"
    }
    items = [{"id": "item1", "qty": -1, "price": 0.0}]
    with pytest.raises(ValueError):
        order_processor.process_order("order_neg", order_data, items)

def test_process_order_paypal_fraud(monkeypatch, order_processor):
    class FakeDateTime:
        @classmethod
        def now(cls):
            import datetime as real_dt
            return real_dt.datetime(2020, 1, 1, 12, 0, 0)
    monkeypatch.setattr("data.input_code.d06_complex_logic.datetime", FakeDateTime, raising=True)
    order_data = {
        "email": "test@test.com",
        "age": 30,
        "tier": "STANDARD",
        "payment_method": "PAYPAL"
    }
    items = [{"id": "item1", "qty": 1, "price": 546.44}]
    with pytest.raises(FraudDetectedError):
        order_processor.process_order("order_fraud", order_data, items)

def test_process_order_crypto_success(monkeypatch, order_processor):
    class FakeDateTime:
        @classmethod
        def now(cls):
            import datetime as real_dt
            return real_dt.datetime(2020, 1, 1, 12, 0, 0)
    monkeypatch.setattr("data.input_code.d06_complex_logic.datetime", FakeDateTime, raising=True)
    order_data = {
        "email": "test@test.com",
        "age": 30,
        "tier": "GOLD",
        "payment_method": "CRYPTO"
    }
    items = [{"id": "item1", "qty": 1, "price": 60.0}]
    result = order_processor.process_order("order_crypto", order_data, items)
    assert result["status"] == "success"
    assert result["order_id"] == "order_crypto"

def test_discount_promo_normal_monkeypatched(monkeypatch):
    class FakeDateTime:
        @classmethod
        def now(cls):
            import datetime as real_dt
            return real_dt.datetime(2020, 1, 1, 12, 0, 0)
    monkeypatch.setattr("data.input_code.d06_complex_logic.datetime", FakeDateTime, raising=True)
    assert DiscountEngine.calculate_discount(200.0, "GOLD", "ABC-123") == 0.20

def test_discount_platinum_promo_monkeypatched(monkeypatch):
    class FakeDateTime:
        @classmethod
        def now(cls):
            import datetime as real_dt
            return real_dt.datetime(2020, 1, 1, 12, 0, 0)
    monkeypatch.setattr("data.input_code.d06_complex_logic.datetime", FakeDateTime, raising=True)
    assert DiscountEngine.calculate_discount(1500.0, "PLATINUM", "XYZ-123") == 0.35

def test_order_success_promo(order_processor, monkeypatch):
    class FakeDateTime:
        @classmethod
        def now(cls):
            import datetime as real_dt
            return real_dt.datetime(2020, 1, 1, 12, 0, 0)
    monkeypatch.setattr("data.input_code.d06_complex_logic.datetime", FakeDateTime, raising=True)
    order_data = {
        "email": "test@test.com",
        "age": 30,
        "tier": "GOLD",
        "payment_method": "CC"
    }
    items = [{"id": "item1", "qty": 2, "price": 100.0}]
    result = order_processor.process_order("order6", order_data, items, "ABC-123")
    assert result["status"] == "success"
    assert result["order_id"] == "order6"
    assert result["original_price"] == 200.0
    assert result["discount_applied"] == 0.20
    assert result["final_total"] == 195.2
    assert result["items_count"] == 1

def test_order_insufficient_rollback(order_processor):
    order_data = {
        "email": "test@test.com",
        "age": 30,
        "tier": "GOLD",
        "payment_method": "CC"
    }
    items = [{"id": "item1", "qty": 101, "price": 100.0}]
    result = order_processor.process_order("order7", order_data, items)
    assert result["status"] == "failed"
    assert "Out of stock" in result["reason"]

def test_order_invalid_promo_rollback(order_processor):
    order_data = {
        "email": "test@test.com",
        "age": 30,
        "tier": "GOLD",
        "payment_method": "CC"
    }
    items = [{"id": "item1", "qty": 1, "price": 100.0}]
    promo_code = "BADPROMO"
    result = order_processor.process_order("order8", order_data, items, promo_code)
    assert result["status"] == "error"

def test_warehouse_check_after_lock(warehouse):
    warehouse.lock_item("item1", 10)
    assert warehouse.check_stock("item1", 90) == True

def test_warehouse_lock_insufficient_after_lock(warehouse):
    warehouse.lock_item("item1", 90)
    with pytest.raises(InventoryError):
        warehouse.lock_item("item1", 15)

def test_discount_hour_boundary_no_night(monkeypatch):
    class FakeDateTime:
        @classmethod
        def now(cls):
            import datetime as real_dt
            return real_dt.datetime(2020, 1, 1, 6, 0, 0)
    monkeypatch.setattr("data.input_code.d06_complex_logic.datetime", FakeDateTime, raising=True)
    assert DiscountEngine.calculate_discount(100.0, "STANDARD", None) == 0.0

def test_discount_no_conditions_no_night(monkeypatch):
    class FakeDateTime:
        @classmethod
        def now(cls):
            import datetime as real_dt
            return real_dt.datetime(2020, 1, 1, 12, 0, 0)
    monkeypatch.setattr("data.input_code.d06_complex_logic.datetime", FakeDateTime, raising=True)
    assert DiscountEngine.calculate_discount(250.0, "STANDARD", None) == 0.0