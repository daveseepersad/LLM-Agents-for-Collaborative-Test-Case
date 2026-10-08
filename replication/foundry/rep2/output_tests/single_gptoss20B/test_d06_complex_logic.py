import pytest
import data.input_code.d06_complex_logic as d06
from data.input_code.d06_complex_logic import (
    Warehouse,
    DiscountEngine,
    OrderProcessor,
    InventoryError,
    PaymentError,
    FraudDetectedError,
    UserValidationError,
)

# Helper to access module for monkeypatching datetime
import data.input_code.d06_complex_logic as _d06

class _FakeDateTimeNight:
    @classmethod
    def now(cls):
        class Dt: pass
        dt = Dt(); dt.hour = 2
        return dt

class _FakeDateTimeNoNight:
    @classmethod
    def now(cls):
        class Dt: pass
        dt = Dt(); dt.hour = 12
        return dt

def test_warehouse_stock_not_found_raises():
    wh = Warehouse({"item1": 5})
    with pytest.raises(InventoryError) as exc:
        wh.check_stock("item_unknown", 1)
    assert "not found" in str(exc.value)

def test_warehouse_lock_and_release():
    wh = Warehouse({"item": 2})
    assert wh.check_stock("item", 1) is True
    wh.lock_item("item", 1)
    # Now only 1 remaining effectively
    assert wh.check_stock("item", 1) is True
    wh.release_item("item", 1)
    # After release, we should be able to lock again
    assert wh.check_stock("item", 2) is True

def test_discount_night_gold(monkeypatch):
    # Patch to simulate night hour
    monkeypatch.setattr(_d06, "datetime", _FakeDateTimeNight)
    disc = DiscountEngine.calculate_discount(100.0, "GOLD")
    assert pytest.approx(disc, rel=1e-9) == 0.15  # 0.05 night + 0.10 GOLD

def test_discount_platinum_over_1000():
    # No night patch; ensure PLATINUM with amount > 1000 adds 0.05
    disc = DiscountEngine.calculate_discount(1500.0, "PLATINUM", promo_code=None)
    assert pytest.approx(disc, rel=1e-9) == 0.25  # 0.20 + 0.05

def test_discount_promo_999_ignores_others():
    disc = DiscountEngine.calculate_discount(100.0, "STANDARD", promo_code="ABC-999")
    assert pytest.approx(disc, rel=1e-9) == 50.0

def test_discount_promo_valid_non999(monkeypatch):
    # Ensure no night discount and valid promo adds 0.10
    monkeypatch.setattr(_d06, "datetime", _FakeDateTimeNoNight)
    disc = DiscountEngine.calculate_discount(100.0, "GOLD", promo_code="ABC-123")
    assert pytest.approx(disc, rel=1e-9) == 0.20  # 0.10 GOLD + 0.10 promo

def test_discount_promo_invalid_raises():
    with pytest.raises(ValueError):
        DiscountEngine.calculate_discount(100.0, "STANDARD", promo_code="bad")

def test_order_successful_process_order():
    wh = Warehouse({"A": 5, "B": 5})
    processor = OrderProcessor(wh)
    user_data = {"email": "valid@example.com", "age": 30, "tier": "STANDARD", "payment_method": "CC"}
    items = [
        {"id": "A", "qty": 2, "price": 20.0},
        {"id": "B", "qty": 1, "price": 15.0},
    ]
    result = processor.process_order("ORD-1", user_data, items)
    assert result["status"] == "success"
    assert result["order_id"] == "ORD-1"
    assert result["items_count"] == len(items)
    assert "final_total" in result
    assert "original_price" in result

def test_order_out_of_stock():
    wh = Warehouse({"A": 0})  # Not enough stock
    processor = OrderProcessor(wh)
    user_data = {"email": "valid@example.com", "age": 25}
    items = [{"id": "A", "qty": 1, "price": 10.0}]
    result = processor.process_order("ORD-2", user_data, items)
    assert result["status"] == "failed"
    assert "Out of stock" in result["reason"]

def test_order_promo_invalid_in_order():
    wh = Warehouse({"A": 5})
    processor = OrderProcessor(wh)
    user_data = {"email": "valid@example.com", "age": 25}
    items = [{"id": "A", "qty": 1, "price": 10.0}]
    result = processor.process_order("ORD-3", user_data, items, promo_code="BADPROMO")
    assert result["status"] == "error"
    assert result["reason"].startswith("Promo Error:")

def test_order_crypto_below_minimum_raises_payment_error():
    wh = Warehouse({"A": 5})
    processor = OrderProcessor(wh)
    user_data = {"email": "valid@example.com", "age": 25, "payment_method": "CRYPTO"}
    # Price such that final after tax is below 50
    items = [{"id": "A", "qty": 1, "price": 10.0}]
    with pytest.raises(PaymentError):
        processor.process_order("ORD-4", user_data, items)

def test_order_paypal_fraud_detected(monkeypatch):
    # Set price such that final after tax equals 666.66 with no discount
    wh = Warehouse({"A": 5})
    processor = OrderProcessor(wh)
    user_data = {"email": "valid@example.com", "age": 25, "payment_method": "PAYPAL"}
    items = [{"id": "A", "qty": 1, "price": 546.44}]  # total_price = 546.44
    # Patch to ensure no night discount alters computation
    monkeypatch.setattr(_d06, "datetime", _FakeDateTimeNoNight)
    with pytest.raises(FraudDetectedError):
        processor.process_order("ORD-5", user_data, items)