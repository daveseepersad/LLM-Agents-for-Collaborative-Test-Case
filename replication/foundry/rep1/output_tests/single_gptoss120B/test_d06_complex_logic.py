import pytest
from data.input_code.d06_complex_logic import (
    Warehouse,
    DiscountEngine,
    OrderProcessor,
    InventoryError,
    PaymentError,
    FraudDetectedError,
    UserValidationError,
)

# Helper to mock datetime.now hour
class _FakeDateTime:
    def __init__(self, hour):
        self.hour = hour

    @classmethod
    def now(cls):
        return cls(_hour)

# ---------- Warehouse Tests ----------

def test_warehouse_lock_and_release_behaviour():
    wh = Warehouse({"a": 3})
    # lock within stock
    wh.lock_item("a", 2)
    assert wh._locked_stock["a"] == 2
    # release partially
    wh.release_item("a", 1)
    assert wh._locked_stock["a"] == 1
    # release remaining removes key
    wh.release_item("a", 1)
    assert "a" not in wh._locked_stock
    # insufficient stock raises
    with pytest.raises(InventoryError):
        wh.lock_item("a", 5)

# ---------- DiscountEngine Tests ----------

def test_discount_engine_invalid_promo(monkeypatch):
    global _hour
    _hour = 12
    monkeypatch.setattr("data.input_code.d06_complex_logic.datetime", _FakeDateTime)
    with pytest.raises(ValueError):
        DiscountEngine.calculate_discount(100.0, "STANDARD", "badcode")

# ---------- OrderProcessor Validation Tests ----------
def test_validate_user_success():
    op = OrderProcessor(Warehouse({}))
    op.validate_user("test.user@example.com", 30)  # should not raise

def test_validate_user_invalid_email():
    op = OrderProcessor(Warehouse({}))
    with pytest.raises(UserValidationError):
        op.validate_user("invalid-email", 30)

def test_validate_user_underage():
    op = OrderProcessor(Warehouse({}))
    with pytest.raises(UserValidationError):
        op.validate_user("user@example.com", 17)

def test_validate_user_overage():
    op = OrderProcessor(Warehouse({}))
    with pytest.raises(UserValidationError):
        op.validate_user("user@example.com", 101)

# ---------- OrderProcessor Process Order Success ----------
def test_process_order_success(monkeypatch):
    # Setup warehouse with sufficient stock
    wh = Warehouse({"1": 5, "2": 5})
    op = OrderProcessor(wh)

    # Mock datetime to avoid night discount
    global _hour
    _hour = 12
    monkeypatch.setattr("data.input_code.d06_complex_logic.datetime", _FakeDateTime)

    items = [
        {"id": "1", "qty": 2, "price": 50.0},
        {"id": "2", "qty": 1, "price": 100.0},
    ]
    user_data = {
        "email": "buyer@example.com",
        "age": 30,
        "tier": "GOLD",
        "payment_method": "CC",
    }

    result = op.process_order("ORD123", user_data, items, promo_code="ABC-123")
    # Expected discount: GOLD 0.10 + promo 0.10 = 0.20
    total_price = 2 * 50.0 + 1 * 100.0  # 200.0
    discounted = total_price * (1 - 0.20)  # 160.0
    final_with_tax = round(discounted * (1 + op.tax_rate), 2)  # 160 * 1.22 = 195.2
    assert result["status"] == "success"
    assert result["order_id"] == "ORD123"
    assert result["original_price"] == total_price
    assert result["discount_applied"] == 0.20
    assert result["final_total"] == final_with_tax
    assert result["items_count"] == 2

# ---------- Process Order Inventory Failure ----------
def test_process_order_inventory_failure():
    wh = Warehouse({"1": 1})
    op = OrderProcessor(wh)
    items = [{"id": "1", "qty": 2, "price": 10.0}]  # qty exceeds stock
    user_data = {"email": "user@example.com", "age": 25}
    result = op.process_order("ORDFAIL", user_data, items)
    assert result["status"] == "failed"
    assert "Out of stock" in result["reason"]
    # Ensure no locked stock remains
    assert wh._locked_stock == {}

# ---------- Process Order Invalid Promo Code ----------

# ---------- Process Order PayPal Fraud Detection ----------
def test_process_order_paypal_fraud(monkeypatch):
    wh = Warehouse({"1": 1})
    op = OrderProcessor(wh)
    # Force tax_rate to 0 to hit exact amount
    op.tax_rate = 0.0
    items = [{"id": "1", "qty": 1, "price": 666.66}]
    user_data = {
        "email": "rich@example.com",
        "age": 30,
        "payment_method": "PAYPAL",
    }
    # No discount, hour non‑night
    global _hour
    _hour = 12
    monkeypatch.setattr("data.input_code.d06_complex_logic.datetime", _FakeDateTime)

    with pytest.raises(FraudDetectedError):
        op.process_order("ORDFRAUD", user_data, items)

# ---------- Process Order Crypto Minimum Amount ----------
def test_process_order_crypto_min_amount():
    wh = Warehouse({"1": 1})
    op = OrderProcessor(wh)
    items = [{"id": "1", "qty": 1, "price": 30.0}]
    user_data = {
        "email": "crypto@example.com",
        "age": 30,
        "payment_method": "CRYPTO",
    }
    # No discount, total 30, tax adds 22% => 36.6 < 50 triggers error
    with pytest.raises(PaymentError):
        op.process_order("ORDCRYPTO", user_data, items)