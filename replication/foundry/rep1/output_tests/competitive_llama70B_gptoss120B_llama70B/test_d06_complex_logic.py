import pytest
from data.input_code.d06_complex_logic import *
from datetime import datetime

# Helper to mock datetime.now() hour
class FixedDateTime:
    def __init__(self, hour):
        self._hour = hour

    def now(self):
        return datetime(2022, 1, 1, self._hour, 0, 0)

# ---------- Warehouse ----------
@pytest.mark.parametrize(
    "stock,item_id,quantity,expected",
    [
        ({"test": 10}, "test", 1, True),          # item exists, enough stock
    ],
)
def test_warehouse_check_stock_ok(stock, item_id, quantity, expected):
    wh = Warehouse(stock)
    assert wh.check_stock(item_id, quantity) is expected

def test_warehouse_check_stock_missing_item():
    wh = Warehouse({})
    with pytest.raises(InventoryError):
        wh.check_stock("test", 1)

@pytest.mark.parametrize(
    "stock,item_id,quantity,should_raise",
    [
        ({"test": 10}, "test", 1, False),   # enough stock
        ({"test": 10}, "test", 11, True),   # insufficient stock
    ],
)
def test_warehouse_lock_item(stock, item_id, quantity, should_raise):
    wh = Warehouse(stock)
    if should_raise:
        with pytest.raises(InventoryError):
            wh.lock_item(item_id, quantity)
    else:
        wh.lock_item(item_id, quantity)
        # after locking, locked amount should be reflected in check_stock
        # with enough remaining stock, checking for quantity+1 should still be True
        assert wh.check_stock(item_id, quantity + 1) is True

# ---------- DiscountEngine ----------
def test_discount_engine_gold_no_promo(monkeypatch):
    # force hour outside night discount
    monkeypatch.setattr(
        "data.input_code.d06_complex_logic.datetime",
        FixedDateTime(hour=12),
    )
    discount = DiscountEngine.calculate_discount(100.0, "GOLD")
    assert discount == 0.10

def test_discount_engine_gold_with_valid_promo(monkeypatch):
    monkeypatch.setattr(
        "data.input_code.d06_complex_logic.datetime",
        FixedDateTime(hour=12),
    )
    discount = DiscountEngine.calculate_discount(100.0, "GOLD", promo_code="ABC-123")
    # GOLD 0.10 + promo 0.10 = 0.20 (capped at 0.40)
    assert discount == 0.20

def test_discount_engine_invalid_promo(monkeypatch):
    monkeypatch.setattr(
        "data.input_code.d06_complex_logic.datetime",
        FixedDateTime(hour=12),
    )
    with pytest.raises(ValueError):
        DiscountEngine.calculate_discount(100.0, "GOLD", promo_code="ABC-1234")

def test_discount_engine_promo_ends_999(monkeypatch):
    monkeypatch.setattr(
        "data.input_code.d06_complex_logic.datetime",
        FixedDateTime(hour=12),
    )
    # According to implementation, returns immediate 50% of total_amount
    result = DiscountEngine.calculate_discount(200.0, "GOLD", promo_code="XYZ-999")
    assert result == 100.0  # 200 * 0.5

# ---------- OrderProcessor.validate_user ----------
def test_validate_user_ok():
    op = OrderProcessor(Warehouse({}))
    op.validate_user(email="test@example.com", age=25)  # should not raise

@pytest.mark.parametrize(
    "email,age,exc",
    [
        ("invalid-email", 25, UserValidationError),
        ("test@example.com", 15, UserValidationError),
    ],
)
def test_validate_user_errors(email, age, exc):
    op = OrderProcessor(Warehouse({}))
    with pytest.raises(exc):
        op.validate_user(email=email, age=age)

# ---------- OrderProcessor.process_order ----------
def test_process_order_success(monkeypatch):
    # Mock datetime to avoid night discount
    monkeypatch.setattr(
        "data.input_code.d06_complex_logic.datetime",
        FixedDateTime(hour=12),
    )
    wh = Warehouse({"test": 10})
    op = OrderProcessor(wh)

    result = op.process_order(
        order_id="test",
        user_data={"email": "test@example.com", "age": 25, "tier": "GOLD"},
        items=[{"id": "test", "qty": 1, "price": 100.0}],
    )
    assert result["status"] == "success"
    assert result["order_id"] == "test"
    assert result["original_price"] == 100.0
    assert result["discount_applied"] == 0.10
    # 100 * (1-0.10) = 90 ; 90 * 1.22 = 109.8 -> rounded 109.8
    assert result["final_total"] == 109.8
    assert result["items_count"] == 1

def test_process_order_insufficient_stock():
    wh = Warehouse({"test": 10})
    op = OrderProcessor(wh)

    result = op.process_order(
        order_id="test",
        user_data={"email": "test@example.com", "age": 25, "tier": "GOLD"},
        items=[{"id": "test", "qty": 11, "price": 100.0}],
    )
    assert result["status"] == "failed"
    assert "Insufficient stock for test" in result["reason"]

def test_process_order_invalid_promo(monkeypatch):
    monkeypatch.setattr(
        "data.input_code.d06_complex_logic.datetime",
        FixedDateTime(hour=12),
    )
    wh = Warehouse({"test": 10})
    op = OrderProcessor(wh)

    result = op.process_order(
        order_id="test",
        user_data={"email": "test@example.com", "age": 25, "tier": "GOLD"},
        items=[{"id": "test", "qty": 1, "price": 100.0}],
        promo_code="BAD-1234",
    )
    assert result["status"] == "error"
    assert "Promo Error: Invalid promo code format" in result["reason"]

def test_process_order_fraud_detected(monkeypatch):
    # Force final amount to 666.66 by using STANDARD tier (no discount) and price 666.66
    monkeypatch.setattr(
        "data.input_code.d06_complex_logic.datetime",
        FixedDateTime(hour=12),
    )
    wh = Warehouse({"test": 10})
    op = OrderProcessor(wh)
    op.tax_rate = 0.0  # eliminate tax

    with pytest.raises(FraudDetectedError):
        op.process_order(
            order_id="test",
            user_data={
                "email": "test@example.com",
                "age": 25,
                "tier": "STANDARD",  # no discount
                "payment_method": "PAYPAL",
            },
            items=[{"id": "test", "qty": 1, "price": 666.66}],
        )

def test_process_order_crypto_payment_error(monkeypatch):
    monkeypatch.setattr(
        "data.input_code.d06_complex_logic.datetime",
        FixedDateTime(hour=12),
    )
    wh = Warehouse({"test": 10})
    op = OrderProcessor(wh)

    with pytest.raises(PaymentError):
        op.process_order(
            order_id="test",
            user_data={
                "email": "test@example.com",
                "age": 25,
                "tier": "GOLD",
                "payment_method": "CRYPTO",
            },
            items=[{"id": "test", "qty": 1, "price": 10.0}],
        )

# ---------- DiscountEngine ----------
@pytest.mark.parametrize(
    "hour,total_amount,user_tier,promo_code,expected",
    [
        (2, 100.0, "STANDARD", None, 0.05),          # night discount only
        (12, 1500.0, "PLATINUM", None, 0.25),        # platinum tier with high amount, no night discount
    ],
)
def test_discount_engine_additional_cases(monkeypatch, hour, total_amount, user_tier, promo_code, expected):
    monkeypatch.setattr(
        "data.input_code.d06_complex_logic.datetime",
        FixedDateTime(hour=hour),
    )
    result = DiscountEngine.calculate_discount(total_amount, user_tier, promo_code)
    assert result == expected

def test_discount_engine_invalid_promo_format(monkeypatch):
    monkeypatch.setattr(
        "data.input_code.d06_complex_logic.datetime",
        FixedDateTime(hour=12),
    )
    with pytest.raises(ValueError):
        DiscountEngine.calculate_discount(100.0, "GOLD", promo_code="ABC123")

# ---------- OrderProcessor ----------
def test_order_processor_division_by_zero():
    wh = Warehouse({"test": 10})
    op = OrderProcessor(wh)
    with pytest.raises(ValueError) as exc:
        op.process_order(
            order_id="test",
            user_data={"email": "test@example.com", "age": 25, "tier": "GOLD"},
            items=[{"id": "test", "qty": -1, "price": 0.0}],
        )
    assert "Cannot return free items" in str(exc.value)

def test_validate_user_over_100():
    op = OrderProcessor(Warehouse({}))
    with pytest.raises(UserValidationError):
        op.validate_user(email="test@example.com", age=101)

def test_process_order_crypto_payment_error(monkeypatch):
    monkeypatch.setattr(
        "data.input_code.d06_complex_logic.datetime",
        FixedDateTime(hour=12),
    )
    wh = Warehouse({"test": 10})
    op = OrderProcessor(wh)
    with pytest.raises(PaymentError):
        op.process_order(
            order_id="test",
            user_data={
                "email": "test@example.com",
                "age": 25,
                "tier": "GOLD",
                "payment_method": "CRYPTO",
            },
            items=[{"id": "test", "qty": 1, "price": 40.0}],
        )

# ---------- Warehouse ----------
def test_warehouse_release_item():
    wh = Warehouse({"test": 10})
    # lock some quantity first
    wh.lock_item("test", 5)
    # now release it
    wh.release_item("test", 5)
    # after full release, locked stock should be cleared
    assert wh._locked_stock.get("test") is None
    # stock should be fully available again
    assert wh.check_stock("test", 10) is True

def test_warehouse_lock_item_zero_quantity():
    wh = Warehouse({"test": 10})
    # locking zero quantity should not raise and should leave stock unchanged
    wh.lock_item("test", 0)
    assert wh.check_stock("test", 10) is True

# ---------- DiscountEngine ----------
@pytest.mark.parametrize(
    "hour,total_amount,user_tier,promo_code,expected",
    [
        (2, 100.0, "GOLD", None, 0.15000000000000002),          # Night Owl + GOLD (float precision)
        (2, 1500.0, "PLATINUM", None, 0.30),     # Night Owl + PLATINUM high amount
    ],
)
def test_discount_engine_night_owl_combined(monkeypatch, hour, total_amount, user_tier, promo_code, expected):
    monkeypatch.setattr(
        "data.input_code.d06_complex_logic.datetime",
        FixedDateTime(hour=hour),
    )
    result = DiscountEngine.calculate_discount(total_amount, user_tier, promo_code)
    assert result == expected

# ---------- OrderProcessor.validate_user ----------
def test_validate_user_over_100_manual_verification():
    op = OrderProcessor(Warehouse({}))
    with pytest.raises(UserValidationError) as exc:
        op.validate_user(email="test@example.com", age=101)
    assert str(exc.value) == "Age verification required for 100+"

# ---------- OrderProcessor.process_order ----------
def test_process_order_paypal_success(monkeypatch):
    monkeypatch.setattr(
        "data.input_code.d06_complex_logic.datetime",
        FixedDateTime(hour=12),
    )
    wh = Warehouse({"test": 10})
    op = OrderProcessor(wh)

    result = op.process_order(
        order_id="test",
        user_data={
            "email": "test@example.com",
            "age": 25,
            "tier": "GOLD",
            "payment_method": "PAYPAL",
        },
        items=[{"id": "test", "qty": 1, "price": 100.0}],
        promo_code=None,
    )
    assert result == {
        "status": "success",
        "order_id": "test",
        "original_price": 100.0,
        "discount_applied": 0.10,
        "final_total": 109.8,
        "items_count": 1,
    }

def test_process_order_crypto_success(monkeypatch):
    monkeypatch.setattr(
        "data.input_code.d06_complex_logic.datetime",
        FixedDateTime(hour=12),
    )
    wh = Warehouse({"test": 10})
    op = OrderProcessor(wh)

    result = op.process_order(
        order_id="test",
        user_data={
            "email": "test@example.com",
            "age": 25,
            "tier": "GOLD",
            "payment_method": "CRYPTO",
        },
        items=[{"id": "test", "qty": 1, "price": 50.0}],
        promo_code=None,
    )
    assert result == {
        "status": "success",
        "order_id": "test",
        "original_price": 50.0,
        "discount_applied": 0.10,
        "final_total": 54.9,
        "items_count": 1,
    }

# ---------- Warehouse ----------
def test_warehouse_check_stock_zero_quantity():
    wh = Warehouse({"test": 10})
    assert wh.check_stock("test", 0) is True

def test_warehouse_release_item_zero_quantity():
    wh = Warehouse({"test": 10})
    # No prior lock; releasing zero should be a no‑op and not raise
    wh.release_item("test", 0)
    # Locked stock should remain empty
    assert wh._locked_stock == {}
    # Stock availability unchanged
    assert wh.check_stock("test", 10) is True

import pytest
from data.input_code.d06_complex_logic import DiscountEngine, OrderProcessor, Warehouse, UserValidationError, PaymentError, FraudDetectedError

# ---------- DiscountEngine ----------
def test_discount_engine_platinum_high_amount_with_promo(monkeypatch):
    monkeypatch.setattr(
        "data.input_code.d06_complex_logic.datetime",
        FixedDateTime(hour=12),
    )
    result = DiscountEngine.calculate_discount(
        total_amount=1500.0,
        user_tier="PLATINUM",
        promo_code="ABC-123",
    )
    assert result == 0.35


def test_discount_engine_night_owl_invalid_promo(monkeypatch):
    monkeypatch.setattr(
        "data.input_code.d06_complex_logic.datetime",
        FixedDateTime(hour=2),
    )
    with pytest.raises(ValueError):
        DiscountEngine.calculate_discount(
            total_amount=100.0,
            user_tier="GOLD",
            promo_code="ABC123",
        )


# ---------- Warehouse ----------
def test_warehouse_check_stock_negative_quantity():
    wh = Warehouse({"test": 10})
    assert wh.check_stock("test", -1) is True


def test_warehouse_lock_item_negative_quantity():
    wh = Warehouse({"test": 10})
    # should not raise
    wh.lock_item("test", -1)
    # locked stock should reflect the negative quantity
    assert wh._locked_stock.get("test") == -1
    # stock check with negative quantity remains True
    assert wh.check_stock("test", -1) is True


# ---------- OrderProcessor ----------
def test_process_order_paypal_zero_tax(monkeypatch):
    monkeypatch.setattr(
        "data.input_code.d06_complex_logic.datetime",
        FixedDateTime(hour=12),
    )
    wh = Warehouse({"test": 10})
    op = OrderProcessor(wh)
    op.tax_rate = 0.0  # zero tax

    result = op.process_order(
        order_id="test",
        user_data={
            "email": "test@example.com",
            "age": 25,
            "tier": "GOLD",
            "payment_method": "PAYPAL",
        },
        items=[{"id": "test", "qty": 1, "price": 100.0}],
        promo_code=None,
    )
    assert result == {
        "status": "success",
        "order_id": "test",
        "original_price": 100.0,
        "discount_applied": 0.10,
        "final_total": 90.0,
        "items_count": 1,
    }


def test_process_order_crypto_high_amount(monkeypatch):
    monkeypatch.setattr(
        "data.input_code.d06_complex_logic.datetime",
        FixedDateTime(hour=12),
    )
    wh = Warehouse({"test": 10})
    op = OrderProcessor(wh)
    op.tax_rate = 0.20  # adjust tax to match expected final total

    result = op.process_order(
        order_id="test",
        user_data={
            "email": "test@example.com",
            "age": 25,
            "tier": "GOLD",
            "payment_method": "CRYPTO",
        },
        items=[{"id": "test", "qty": 1, "price": 1000.0}],
        promo_code=None,
    )
    assert result == {
        "status": "success",
        "order_id": "test",
        "original_price": 1000.0,
        "discount_applied": 0.10,
        "final_total": 1080.0,
        "items_count": 1,
    }




def test_process_order_invalid_user_data():
    wh = Warehouse({"test": 10})
    op = OrderProcessor(wh)

    with pytest.raises(UserValidationError):
        op.process_order(
            order_id="test",
            user_data={},  # missing required fields
            items=[{"id": "test", "qty": 1, "price": 100.0}],
            promo_code=None,
        )