import pytest
from data.input_code.d06_complex_logic import *

# Helper to create OrderProcessor with a Warehouse
def make_processor(initial_stock):
    return OrderProcessor(Warehouse(initial_stock))


# ---------- Inventory related tests ----------
@pytest.mark.parametrize(
    "order_id, initial_stock, user_data, items, expected_reason",
    [
        (
            "ORD-T1",
            {"A": 5},
            {"email": "user@example.com", "age": 25, "payment_method": "CC"},
            [{"id": "B", "qty": 1, "price": 10.0}],
            "Out of stock: Item B not found in warehouse."
        ),
        (
            "ORD-T2",
            {"A": 5},
            {"email": "user2@example.com", "age": 30, "payment_method": "CC"},
            [{"id": "A", "qty": 6, "price": 2.0}],
            "Out of stock: Insufficient stock for A"
        ),
        (
            "ORD-T8",
            {"A": 2, "B": 2},
            {"email": "test@example.com", "age": 25, "payment_method": "CC"},
            [
                {"id": "A", "qty": 2, "price": 5.0},
                {"id": "B", "qty": 3, "price": 2.0}
            ],
            "Out of stock: Insufficient stock for B"
        ),
    ]
)
def test_inventory_errors(order_id, initial_stock, user_data, items, expected_reason):
    processor = make_processor(initial_stock)
    result = processor.process_order(order_id, user_data, items, promo_code=None)
    assert result["status"] == "failed"
    assert result["reason"] == expected_reason


# ---------- Promo code handling ----------
def test_promo_invalid_code():
    processor = make_processor({"A": 10})
    user_data = {"email": "buyer@example.com", "age": 30, "payment_method": "CC"}
    items = [{"id": "A", "qty": 1, "price": 10.0}]
    result = processor.process_order("ORD-T3", user_data, items, promo_code="BADPROMO")
    assert result["status"] == "error"
    assert result["reason"] == "Promo Error: Invalid promo code format"


def test_promo_999_discount():
    processor = make_processor({"A": 10})
    user_data = {"email": "gold@example.com", "age": 40, "tier": "GOLD", "payment_method": "CC"}
    items = [{"id": "A", "qty": 2, "price": 50.0}]
    result = processor.process_order("ORD-T4", user_data, items, promo_code="ABC-999")
    # DiscountEngine returns a monetary amount (50.0) which is stored in 'discount_applied'
    assert result["discount_applied"] == 50.0


# ---------- User validation ----------
@pytest.mark.parametrize(
    "email, age, expected_exception",
    [
        ("not-an-email", 25, UserValidationError),
        ("u@example.com", 101, UserValidationError),
    ]
)
def test_user_validation_errors(email, age, expected_exception):
    processor = make_processor({})
    with pytest.raises(expected_exception):
        processor.validate_user(email, age)


# ---------- Payment method edge cases ----------
def test_crypto_minimum_amount():
    processor = make_processor({"X": 5})
    user_data = {"email": "u@example.com", "age": 28, "payment_method": "CRYPTO"}
    items = [{"id": "X", "qty": 1, "price": 15.0}]
    with pytest.raises(PaymentError):
        processor.process_order("ORD-T6", user_data, items, promo_code=None)


def test_paypal_fraud_detection():
    processor = make_processor({"Z": 1})
    user_data = {"email": "pay@example.com", "age": 30, "payment_method": "PAYPAL"}
    items = [{"id": "Z", "qty": 1, "price": 546.44}]
    with pytest.raises(FraudDetectedError):
        processor.process_order("ORD-T7", user_data, items, promo_code=None)


# ---------- Negative quantity / free item ----------
def test_negative_qty_price_free():
    processor = make_processor({"A": 5})
    user_data = {"email": "u@example.com", "age": 25, "payment_method": "CC"}
    items = [{"id": "A", "qty": -1, "price": 0.0}]
    with pytest.raises(ValueError):
        processor.process_order("ORD-T9", user_data, items, promo_code=None)

# ---------- DiscountEngine tests ----------
@pytest.mark.parametrize(
    "total_amount, user_tier, promo_code, expected",
    [
        (1100.0, "PLATINUM", None, 0.25),
        (600.0, "GOLD", "ABC-123", 0.2),
    ]
)
def test_discount_engine(total_amount, user_tier, promo_code, expected):
    result = DiscountEngine.calculate_discount(total_amount, user_tier, promo_code)
    assert result == expected


def test_discount_engine_invalid_promo_format():
    with pytest.raises(ValueError):
        DiscountEngine.calculate_discount(100.0, "GOLD", "BADPROMO")


def test_discount_engine_promo_999_direct():
    result = DiscountEngine.calculate_discount(120.0, "GOLD", "ABC-999")
    assert result == 60.0

def test_discount_night_standard(monkeypatch):
    # Mock datetime.now() to return an hour within 0-5 (e.g., 2 AM)
    class FixedDatetime(datetime):
        @classmethod
        def now(cls):
            return datetime(2022, 1, 1, 2, 0, 0)

    module_path = DiscountEngine.__module__
    monkeypatch.setattr(f"{module_path}.datetime", FixedDatetime, raising=True)

    result = DiscountEngine.calculate_discount(
        total_amount=100.0,
        user_tier="STANDARD",
        promo_code=None,
    )
    assert result == 0.05


def test_discount_night_platinum_cap(monkeypatch):
    # Mock datetime.now() to return an hour within 0-5 (e.g., 3 AM)
    class FixedDatetime(datetime):
        @classmethod
        def now(cls):
            return datetime(2022, 1, 1, 3, 0, 0)

    module_path = DiscountEngine.__module__
    monkeypatch.setattr(f"{module_path}.datetime", FixedDatetime, raising=True)

    result = DiscountEngine.calculate_discount(
        total_amount=2000.0,
        user_tier="PLATINUM",
        promo_code="XYZ-123",
    )
    assert result == 0.40

import pytest
from datetime import datetime

# ---------- DiscountEngine night-time with GOLD tier and promo ----------
def test_discount_engine_night_gold_with_promo(monkeypatch):
    # Mock datetime.now() to a night hour (e.g., 2 AM)
    class FixedDatetime(datetime):
        @classmethod
        def now(cls):
            return datetime(2022, 1, 1, 2, 0, 0)

    module_path = DiscountEngine.__module__
    monkeypatch.setattr(f"{module_path}.datetime", FixedDatetime, raising=True)

    result = DiscountEngine.calculate_discount(
        total_amount=200.0,
        user_tier="GOLD",
        promo_code="ABC-123",
    )
    assert result == 0.25


# ---------- DiscountEngine no discount at midday ----------
def test_discount_engine_no_discount_midday(monkeypatch):
    # Mock datetime.now() to a midday hour (e.g., 12 PM)
    class FixedDatetime(datetime):
        @classmethod
        def now(cls):
            return datetime(2022, 1, 1, 12, 0, 0)

    module_path = DiscountEngine.__module__
    monkeypatch.setattr(f"{module_path}.datetime", FixedDatetime, raising=True)

    result = DiscountEngine.calculate_discount(
        total_amount=50.0,
        user_tier="STANDARD",
        promo_code=None,
    )
    assert result == 0.0


# ---------- OrderProcessor invalid email handling ----------
def test_process_order_invalid_email():
    processor = make_processor({"A": 5})
    user_data = {"email": "not-an-email", "age": 25, "payment_method": "CC"}
    items = [{"id": "A", "qty": 1, "price": 10.0}]
    with pytest.raises(UserValidationError):
        processor.process_order("ORD-INV-EMAIL", user_data, items, promo_code=None)

import pytest

# ---------- User validation under 18 ----------
@pytest.mark.parametrize(
    "email, age",
    [
        ("child@example.com", 16),
    ]
)
def test_validate_user_underage(email, age):
    processor = make_processor({})
    with pytest.raises(UserValidationError):
        processor.validate_user(email, age)


# ---------- Successful order processing with CC and no discounts ----------
def test_process_order_success_no_discount():
    processor = make_processor({"A": 5, "B": 5})
    user_data = {"email": "buyer@example.com", "age": 30, "payment_method": "CC"}
    items = [
        {"id": "A", "qty": 2, "price": 5.0},
        {"id": "B", "qty": 1, "price": 10.0},
    ]
    result = processor.process_order(
        "ORD-TEST-SUC", user_data, items, promo_code=None
    )
    assert result == {
        "status": "success",
        "order_id": "ORD-TEST-SUC",
        "original_price": 20.0,
        "discount_applied": 0.0,
        "final_total": 24.4,
        "items_count": 2,
    }


# ---------- PayPal path succeeds when not triggering fraud detection ----------
def test_process_order_paypal_success():
    processor = make_processor({"C": 2})
    user_data = {
        "email": "pp_ok@example.com",
        "age": 28,
        "payment_method": "PAYPAL",
    }
    items = [{"id": "C", "qty": 1, "price": 20.0}]
    result = processor.process_order(
        "ORD-PP-OK", user_data, items, promo_code=None
    )
    assert result == {
        "status": "success",
        "order_id": "ORD-PP-OK",
        "original_price": 20.0,
        "discount_applied": 0.0,
        "final_total": 24.4,
        "items_count": 1,
    }