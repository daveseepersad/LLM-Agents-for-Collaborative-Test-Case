import pytest
import data.input_code.d06_complex_logic as logic
from data.input_code.d06_complex_logic import *

# Dummy datetime providers to control current hour in tests
class DummyDateTimeHour2:
    @staticmethod
    def now():
        return type('D', (), {'hour': 2})()

class DummyDateTimeHour14:
    @staticmethod
    def now():
        return type('D', (), {'hour': 14})()

class DummyDateTimeHour3:
    @staticmethod
    def now():
        return type('D', (), {'hour': 3})()

class DummyDateTimeHour12:
    @staticmethod
    def now():
        return type('D', (), {'hour': 12})()

class DummyDateTimeHour10:
    @staticmethod
    def now():
        return type('D', (), {'hour': 10})()

def test_warehouse_check_stock_not_found():
    wh = Warehouse({})
    with pytest.raises(InventoryError):
        wh.check_stock("missing_item", 1)

def test_warehouse_lock_insufficient():
    wh = Warehouse({"A": 5})
    with pytest.raises(InventoryError):
        wh.lock_item("A", 10)

def test_warehouse_lock_and_release():
    wh = Warehouse({"B": 10})
    wh.lock_item("B", 3)
    assert wh._locked_stock == {"B": 3}
    wh.release_item("B", 3)
    assert wh._locked_stock == {}

@pytest.mark.parametrize("hour_provider, expected", [
    (DummyDateTimeHour2, 0.15000000000000002),
])
def test_discount_night_gold(monkeypatch, hour_provider, expected):
    monkeypatch.setattr(logic, 'datetime', hour_provider)
    assert DiscountEngine.calculate_discount(200.0, "GOLD", None) == expected

@pytest.mark.parametrize("hour_provider, expected", [
    (DummyDateTimeHour14, 0.35),
])
def test_discount_platinum_high_promo(monkeypatch, hour_provider, expected):
    monkeypatch.setattr(logic, 'datetime', hour_provider)
    assert DiscountEngine.calculate_discount(1500.0, "PLATINUM", "ABC-123") == expected

@pytest.mark.parametrize("hour_provider, expected", [
    (DummyDateTimeHour12, 100.0),
])
def test_discount_super_code(monkeypatch, hour_provider, expected):
    monkeypatch.setattr(logic, 'datetime', hour_provider)
    assert DiscountEngine.calculate_discount(200.0, "STANDARD", "XYZ-999") == expected

def test_discount_invalid_promo(monkeypatch):
    monkeypatch.setattr(logic, 'datetime', DummyDateTimeHour10)
    with pytest.raises(ValueError):
        DiscountEngine.calculate_discount(100.0, "STANDARD", "bad_code")

def test_validate_email_invalid():
    op = OrderProcessor(Warehouse({}))
    with pytest.raises(UserValidationError):
        op.validate_user("invalid_email", 30)

def test_validate_age_under():
    op = OrderProcessor(Warehouse({}))
    with pytest.raises(UserValidationError):
        op.validate_user("test@example.com", 16)

def test_validate_age_over():
    op = OrderProcessor(Warehouse({}))
    with pytest.raises(UserValidationError):
        op.validate_user("senior@example.com", 101)

def test_order_success_cc(monkeypatch):
    monkeypatch.setattr(logic, 'datetime', DummyDateTimeHour3)
    wh = Warehouse({"X1": 5})
    op = OrderProcessor(wh)
    result = op.process_order(
        "ORD001",
        {"email": "user@example.com", "age": 30, "tier": "GOLD", "payment_method": "CC"},
        [{"id": "X1", "qty": 2, "price": 100.0}],
        promo_code=None
    )
    assert result == {
        "status": "success",
        "order_id": "ORD001",
        "original_price": 200.0,
        "discount_applied": 0.15000000000000002,
        "final_total": 207.4,
        "items_count": 1
    }

def test_order_inventory_fail():
    wh = Warehouse({"Y1": 3})
    op = OrderProcessor(wh)
    result = op.process_order(
        "ORD002",
        {"email": "buyer@example.com", "age": 25, "tier": "STANDARD", "payment_method": "CC"},
        [{"id": "Y1", "qty": 10, "price": 50.0}],
        promo_code=None
    )
    assert result == {"status": "failed", "reason": "Out of stock: Insufficient stock for Y1"}

def test_order_promo_error():
    wh = Warehouse({"Z1": 5})
    op = OrderProcessor(wh)
    result = op.process_order(
        "ORD003",
        {"email": "shopper@example.com", "age": 40, "tier": "STANDARD", "payment_method": "CC"},
        [{"id": "Z1", "qty": 1, "price": 20.0}],
        promo_code="WRONG-12"
    )
    assert result == {"status": "error", "reason": "Promo Error: Invalid promo code format"}

def test_order_crypto_min():
    wh = Warehouse({"C1": 5})
    op = OrderProcessor(wh)
    with pytest.raises(PaymentError):
        op.process_order(
            "ORD005",
            {"email": "crypto@example.com", "age": 28, "tier": "STANDARD", "payment_method": "CRYPTO"},
            [{"id": "C1", "qty": 1, "price": 30.0}],
            promo_code=None
        )

def test_order_free_return_error():
    wh = Warehouse({"R1": 10})
    op = OrderProcessor(wh)
    with pytest.raises(ValueError):
        op.process_order(
            "ORD006",
            {"email": "return@example.com", "age": 45, "tier": "STANDARD", "payment_method": "CC"},
            [{"id": "R1", "qty": -1, "price": 0.0}],
            promo_code=None
        )