import pytest
from data.input_code.d06_complex_logic import *

# ----------------------------------------------------------------------
# Helper to control datetime.now used inside DiscountEngine
# ----------------------------------------------------------------------
class FixedDatetime:
    @classmethod
    def now(cls):
        # Fixed hour outside the night discount window
        return datetime(2022, 1, 1, 12, 0, 0)

# ----------------------------------------------------------------------
# Validation tests for OrderProcessor.validate_user
# ----------------------------------------------------------------------
@pytest.fixture(autouse=True)
def mock_datetime(monkeypatch):
    # Apply the datetime mock for all tests that may invoke DiscountEngine
    monkeypatch.setattr('data.input_code.d06_complex_logic.datetime', FixedDatetime)

@pytest.mark.parametrize(
    "email, age, exc_type",
    [
        ("bademail", 25, UserValidationError),          # invalid email format
        ("user@example.com", 17, UserValidationError), # underage
        ("user@example.com", 101, UserValidationError) # over 100
    ]
)
def test_validate_user_errors(email, age, exc_type):
    op = OrderProcessor(Warehouse({}))
    with pytest.raises(exc_type):
        op.validate_user(email, age)

# ----------------------------------------------------------------------
# Warehouse stock checks
# ----------------------------------------------------------------------
def test_warehouse_check_stock_missing_item():
    wh = Warehouse({"A": 5})
    with pytest.raises(InventoryError) as e:
        wh.check_stock("B", 1)
    assert "Item B not found in warehouse." in str(e.value)

def test_warehouse_lock_item_insufficient_stock():
    wh = Warehouse({"A": 2})
    with pytest.raises(InventoryError) as e:
        wh.lock_item("A", 5)
    assert "Insufficient stock for A" in str(e.value)

# ----------------------------------------------------------------------
# DiscountEngine calculations
# ----------------------------------------------------------------------
@pytest.mark.parametrize(
    "total, tier, promo, expected",
    [
        (200.0, "STANDARD", "ABC-999", 100.0),   # 50% off fast path
        (1200.0, "PLATINUM", "XYZ-999", 600.0)  # platinum with 999 promo
    ]
)
def test_discount_engine_fast_path(total, tier, promo, expected):
    result = DiscountEngine.calculate_discount(total, tier, promo)
    assert result == expected

def test_discount_engine_invalid_promo():
    with pytest.raises(ValueError) as e:
        DiscountEngine.calculate_discount(50.0, "GOLD", "BADPROMO")
    assert "Invalid promo code format" in str(e.value)

# ----------------------------------------------------------------------
# OrderProcessor end‑to‑end scenarios
# ----------------------------------------------------------------------
def test_order_success():
    wh = Warehouse({"it1": 5})
    op = OrderProcessor(wh)

    result = op.process_order(
        order_id="ORD1",
        user_data={"email": "buyer@example.com", "age": 30, "tier": "STANDARD"},
        items=[{"id": "it1", "qty": 2, "price": 20.0}],
        promo_code=None
    )

    assert result == {
        "status": "success",
        "order_id": "ORD1",
        "original_price": 40.0,
        "discount_applied": 0.0,
        "final_total": 48.8,
        "items_count": 1
    }

def test_order_promo_invalid():
    wh = Warehouse({"i1": 2})
    op = OrderProcessor(wh)

    result = op.process_order(
        order_id="ORD2",
        user_data={"email": "buyer2@example.com", "age": 25, "tier": "STANDARD"},
        items=[{"id": "i1", "qty": 1, "price": 10.0}],
        promo_code="BADPROMO"
    )

    assert result == {
        "status": "error",
        "reason": "Promo Error: Invalid promo code format"
    }

def test_order_out_of_stock():
    wh = Warehouse({})
    op = OrderProcessor(wh)

    result = op.process_order(
        order_id="ORD3",
        user_data={"email": "buyer3@example.com", "age": 28, "tier": "STANDARD"},
        items=[{"id": "missing", "qty": 1, "price": 5.0}],
        promo_code=None
    )

    assert result == {
        "status": "failed",
        "reason": "Out of stock: Item missing not found in warehouse."
    }

def test_order_crypto_below_minimum():
    wh = Warehouse({"c1": 1})
    op = OrderProcessor(wh)

    with pytest.raises(PaymentError) as e:
        op.process_order(
            order_id="ORD4",
            user_data={
                "email": "crypto@example.com",
                "age": 25,
                "tier": "STANDARD",
                "payment_method": "CRYPTO"
            },
            items=[{"id": "c1", "qty": 1, "price": 5.0}],
            promo_code=None
        )
    assert "Minimum crypto amount not met" in str(e.value)

import pytest
from datetime import datetime
from data.input_code.d06_complex_logic import *

def test_discount_engine_night_discount(monkeypatch):
    class FixedNightDatetime:
        @classmethod
        def now(cls):
            # Hour within night discount window (0-5)
            return datetime(2022, 1, 1, 2, 0, 0)

    monkeypatch.setattr('data.input_code.d06_complex_logic.datetime', FixedNightDatetime)
    result = DiscountEngine.calculate_discount(100.0, "STANDARD", None)
    assert result == 0.05

def test_discount_engine_night_platinum_cap(monkeypatch):
    class FixedNightDatetime:
        @classmethod
        def now(cls):
            # Hour within night discount window (0-5)
            return datetime(2022, 1, 1, 3, 0, 0)

    monkeypatch.setattr('data.input_code.d06_complex_logic.datetime', FixedNightDatetime)
    result = DiscountEngine.calculate_discount(1200.0, "PLATINUM", "ABC-123")
    assert result == 0.40

import pytest
from data.input_code.d06_complex_logic import *

def test_warehouse_release_no_lock_no_effect():
    wh = Warehouse({"A": 5})
    # Ensure the item is not locked initially
    assert "A" not in wh._locked_stock
    # Release should be a no‑op and not raise
    wh.release_item("A", 2)
    # Verify state unchanged
    assert "A" not in wh._locked_stock
    assert wh._stock["A"] == 5

@pytest.mark.parametrize(
    "total_amount, user_tier, promo_code, expected",
    [
        (200.0, "GOLD", None, 0.1),
    ]
)
def test_discount_gold_no_night(total_amount, user_tier, promo_code, expected):
    result = DiscountEngine.calculate_discount(total_amount, user_tier, promo_code)
    assert result == expected

def test_order_validate_18_ok():
    op = OrderProcessor(Warehouse({}))
    # Should pass without raising any exception
    op.validate_user("ok@example.com", 18)

def test_warehouse_release_not_locked_no_effect():
    wh = Warehouse({"X": 10})
    # No lock exists for 'not_locked'
    assert "not_locked" not in wh._locked_stock
    # Release should be a no‑op and not raise
    wh.release_item("not_locked", 1)
    # Verify state unchanged
    assert "not_locked" not in wh._locked_stock
    assert wh._stock["X"] == 10

import pytest
from data.input_code.d06_complex_logic import *

@pytest.mark.parametrize(
    "total_amount, user_tier, promo_code, expected",
    [
        (1200.0, "PLATINUM", None, 0.25),          # No promo, amount > 1000
        (1500.0, "PLATINUM", "ABC-123", 0.35),    # Valid promo adds 0.10
    ]
)
def test_discount_platinum_cases(total_amount, user_tier, promo_code, expected):
    result = DiscountEngine.calculate_discount(total_amount, user_tier, promo_code)
    assert result == expected

import pytest
from data.input_code.d06_complex_logic import *

def test_order_paypal_fraud_suspect_amount():
    wh = Warehouse({"fp": 5})
    op = OrderProcessor(wh)

    with pytest.raises(FraudDetectedError) as e:
        op.process_order(
            order_id="ORD_PAYPAL_FRAUD",
            user_data={
                "email": "fraud@example.com",
                "age": 35,
                "tier": "STANDARD",
                "payment_method": "PAYPAL"
            },
            items=[{"id": "fp", "qty": 2, "price": 273.22}],
            promo_code=None
        )
    assert "Suspicious transaction amount" in str(e.value)


def test_order_promo_applies_discount():
    wh = Warehouse({"p3": 3})
    op = OrderProcessor(wh)

    result = op.process_order(
        order_id="ORD_PROMO_APPLY",
        user_data={
            "email": "promo_apply@example.com",
            "age": 28,
            "tier": "STANDARD"
        },
        items=[{"id": "p3", "qty": 1, "price": 100.0}],
        promo_code="ABC-123"
    )

    assert result == {
        "status": "success",
        "order_id": "ORD_PROMO_APPLY",
        "original_price": 100.0,
        "discount_applied": 0.1,
        "final_total": 109.8,
        "items_count": 1
    }