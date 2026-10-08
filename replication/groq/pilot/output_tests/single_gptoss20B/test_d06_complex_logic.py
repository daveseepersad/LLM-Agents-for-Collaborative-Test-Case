import pytest
from datetime import datetime
from data.input_code.d06_complex_logic import (
    Warehouse,
    DiscountEngine,
    OrderProcessor,
    InventoryError,
    PaymentError,
    FraudDetectedError,
    UserValidationError,
)

# ---------- Warehouse Tests ----------

def test_warehouse_check_stock_item_not_found():
    wh = Warehouse({"A": 10})
    with pytest.raises(InventoryError, match="Item B not found"):
        wh.check_stock("B", 1)

def test_warehouse_check_stock_insufficient():
    wh = Warehouse({"A": 5})
    wh._locked_stock["A"] = 3  # 2 available
    assert wh.check_stock("A", 3) is False

def test_warehouse_check_stock_sufficient():
    wh = Warehouse({"A": 5})
    wh._locked_stock["A"] = 2  # 3 available
    assert wh.check_stock("A", 3) is True

def test_warehouse_lock_item_success_and_locked_stock():
    wh = Warehouse({"A": 5})
    wh.lock_item("A", 3)
    assert wh._locked_stock["A"] == 3

def test_warehouse_lock_item_insufficient():
    wh = Warehouse({"A": 5})
    with pytest.raises(InventoryError, match="Insufficient stock"):
        wh.lock_item("A", 6)

def test_warehouse_release_item_decrement_and_delete():
    wh = Warehouse({"A": 5})
    wh.lock_item("A", 5)
    wh.release_item("A", 3)
    assert wh._locked_stock["A"] == 2
    wh.release_item("A", 2)
    assert "A" not in wh._locked_stock

# ---------- DiscountEngine Tests ----------

@pytest.fixture
def mock_datetime(monkeypatch):
    class DummyDatetime:
        @classmethod
        def now(cls):
            return datetime(2023, 1, 1, 2, 0, 0)  # 2 AM
    monkeypatch.setattr("data.input_code.d06_complex_logic.datetime", DummyDatetime)

def test_discount_nightowl(mock_datetime):
    discount = DiscountEngine.calculate_discount(100.0, "STANDARD")
    assert discount == 0.05  # only nightowl

def test_discount_gold():
    # Ensure hour not in nightowl
    class DummyDatetime:
        @classmethod
        def now(cls):
            return datetime(2023, 1, 1, 10, 0, 0)
    monkeypatch = pytest.MonkeyPatch()
    monkeypatch.setattr("data.input_code.d06_complex_logic.datetime", DummyDatetime)
    discount = DiscountEngine.calculate_discount(100.0, "GOLD")
    assert discount == 0.10
    monkeypatch.undo()

def test_discount_platinum_over_1000():
    class DummyDatetime:
        @classmethod
        def now(cls):
            return datetime(2023, 1, 1, 10, 0, 0)
    monkeypatch = pytest.MonkeyPatch()
    monkeypatch.setattr("data.input_code.d06_complex_logic.datetime", DummyDatetime)
    discount = DiscountEngine.calculate_discount(1500.0, "PLATINUM")
    assert discount == 0.25  # 0.20 + 0.05
    monkeypatch.undo()

def test_discount_platinum_under_1000():
    class DummyDatetime:
        @classmethod
        def now(cls):
            return datetime(2023, 1, 1, 10, 0, 0)
    monkeypatch = pytest.MonkeyPatch()
    monkeypatch.setattr("data.input_code.d06_complex_logic.datetime", DummyDatetime)
    discount = DiscountEngine.calculate_discount(800.0, "PLATINUM")
    assert discount == 0.20
    monkeypatch.undo()

def test_discount_promo_valid():
    class DummyDatetime:
        @classmethod
        def now(cls):
            return datetime(2023, 1, 1, 10, 0, 0)
    monkeypatch = pytest.MonkeyPatch()
    monkeypatch.setattr("data.input_code.d06_complex_logic.datetime", DummyDatetime)
    discount = DiscountEngine.calculate_discount(200.0, "STANDARD", "ABC-123")
    assert discount == 0.10
    monkeypatch.undo()

def test_discount_promo_999():
    class DummyDatetime:
        @classmethod
        def now(cls):
            return datetime(2023, 1, 1, 10, 0, 0)
    monkeypatch = pytest.MonkeyPatch()
    monkeypatch.setattr("data.input_code.d06_complex_logic.datetime", DummyDatetime)
    result = DiscountEngine.calculate_discount(200.0, "STANDARD", "XYZ-999")
    assert result == 100.0  # 50% off of 200
    monkeypatch.undo()

def test_discount_invalid_promo():
    class DummyDatetime:
        @classmethod
        def now(cls):
            return datetime(2023, 1, 1, 10, 0, 0)
    monkeypatch = pytest.MonkeyPatch()
    monkeypatch.setattr("data.input_code.d06_complex_logic.datetime", DummyDatetime)
    with pytest.raises(ValueError, match="Invalid promo code format"):
        DiscountEngine.calculate_discount(200.0, "STANDARD", "abc-123")
    monkeypatch.undo()

# ---------- OrderProcessor Tests ----------

def test_validate_user_invalid_email():
    op = OrderProcessor(Warehouse({}))
    with pytest.raises(UserValidationError, match="Invalid email format"):
        op.validate_user("invalid-email", 30)

def test_validate_user_underage():
    op = OrderProcessor(Warehouse({}))
    with pytest.raises(UserValidationError, match="User must be 18"):
        op.validate_user("user@example.com", 17)

def test_validate_user_over100():
    op = OrderProcessor(Warehouse({}))
    with pytest.raises(UserValidationError, match="Age verification required"):
        op.validate_user("user@example.com", 101)


def test_process_order_inventory_error(monkeypatch):
    class DummyDatetime:
        @classmethod
        def now(cls):
            return datetime(2023, 1, 1, 10, 0, 0)
    monkeypatch.setattr("data.input_code.d06_complex_logic.datetime", DummyDatetime)

    wh = Warehouse({"1": 1})
    op = OrderProcessor(wh)
    user_data = {"email": "user@example.com", "age": 30, "tier": "STANDARD", "payment_method": "CC"}
    items = [
        {"id": "1", "qty": 2, "price": 50.0},  # insufficient
    ]
    result = op.process_order("ORD124", user_data, items)
    assert result["status"] == "failed"
    assert "Out of stock" in result["reason"]
    # Ensure no locked stock remains
    assert wh._locked_stock == {}

def test_process_order_promo_error(monkeypatch):
    class DummyDatetime:
        @classmethod
        def now(cls):
            return datetime(2023, 1, 1, 10, 0, 0)
    monkeypatch.setattr("data.input_code.d06_complex_logic.datetime", DummyDatetime)

    wh = Warehouse({"1": 5})
    op = OrderProcessor(wh)
    user_data = {"email": "user@example.com", "age": 30, "tier": "STANDARD", "payment_method": "CC"}
    items = [
        {"id": "1", "qty": 1, "price": 50.0},
    ]
    result = op.process_order("ORD125", user_data, items, promo_code="invalid")
    assert result["status"] == "error"
    assert "Promo Error" in result["reason"]
    # Ensure rollback
    assert wh._locked_stock == {}

def test_process_order_division_by_zero_error(monkeypatch):
    class DummyDatetime:
        @classmethod
        def now(cls):
            return datetime(2023, 1, 1, 10, 0, 0)
    monkeypatch.setattr("data.input_code.d06_complex_logic.datetime", DummyDatetime)

    wh = Warehouse({"1": 5})
    op = OrderProcessor(wh)
    user_data = {"email": "user@example.com", "age": 30, "tier": "STANDARD", "payment_method": "CC"}
    items = [
        {"id": "1", "qty": -1, "price": 0.0},  # triggers ValueError
    ]
    with pytest.raises(ValueError, match="Cannot return free items"):
        op.process_order("ORD126", user_data, items)


def test_process_order_crypto_minimum(monkeypatch):
    # Prepare warehouse with sufficient stock
    wh = Warehouse({"1": 10})
    op = OrderProcessor(wh)
    user_data = {"email": "user@example.com", "age": 30, "tier": "STANDARD", "payment_method": "CRYPTO"}
    # Monkeypatch DiscountEngine to avoid discount
    monkeypatch.setattr(
        "data.input_code.d06_complex_logic.DiscountEngine.calculate_discount",
        lambda total, tier, promo=None: 0.0,
    )
    items = [
        {"id": "1", "qty": 1, "price": 30.0},  # final_total will be 36.6 < 50
    ]
    with pytest.raises(PaymentError, match="Minimum crypto amount not met"):
        op.process_order("ORD128", user_data, items)