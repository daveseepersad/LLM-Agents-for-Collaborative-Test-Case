import pytest
import datetime as real_datetime
from data.input_code.d06_complex_logic import *
import data.input_code.d06_complex_logic as d06_complex_logic

# Helper to mock datetime.now()
class FixedDateTime(real_datetime.datetime):
    @classmethod
    def now(cls):
        # Fixed hour outside the night‑discount window
        return cls(2023, 1, 1, 12, 0, 0)

@pytest.fixture(autouse=True)
def mock_datetime(monkeypatch):
    """Patch the datetime class used in the source module with FixedDateTime for all tests."""
    monkeypatch.setattr(d06_complex_logic, "datetime", FixedDateTime)


# ---------- OrderProcessor.validate_user ----------
def test_validate_user_success():
    op = OrderProcessor(Warehouse({}))
    # Should not raise
    op.validate_user(email="test@example.com", age=25)


@pytest.mark.parametrize(
    "email, age",
    [
        ("invalid", 25),               # invalid email
        ("test@example.com", 17),      # underage
        ("test@example.com", 101),     # overage
    ],
)
def test_validate_user_errors(email, age):
    op = OrderProcessor(Warehouse({}))
    with pytest.raises(UserValidationError):
        op.validate_user(email=email, age=age)


# ---------- Warehouse ----------
@pytest.mark.parametrize(
    "stock, item_id, qty, expected",
    [
        ({"item1": 10}, "item1", 5, True),   # sufficient stock
        ({"item1": 10}, "item1", 15, False), # insufficient stock
    ],
)
def test_check_stock(stock, item_id, qty, expected):
    wh = Warehouse(stock)
    assert wh.check_stock(item_id, qty) is expected


def test_check_stock_missing_item():
    wh = Warehouse({"item1": 10})
    with pytest.raises(InventoryError):
        wh.check_stock("nonexistent", 1)


def test_lock_item_success():
    wh = Warehouse({"item1": 10})
    wh.lock_item("item1", 5)  # should not raise
    # after locking, available should be 5
    assert wh.check_stock("item1", 5) is True
    assert wh.check_stock("item1", 6) is False


def test_lock_item_insufficient_stock():
    wh = Warehouse({"item1": 10})
    with pytest.raises(InventoryError):
        wh.lock_item("item1", 15)


# ---------- DiscountEngine ----------
@pytest.mark.parametrize(
    "total, tier, promo, expected",
    [
        (100, "STANDARD", None, 0.0),               # no discount
        (100, "GOLD", None, 0.10),                  # gold tier
        (100, "PLATINUM", None, 0.20),              # platinum tier below threshold
        (1001, "PLATINUM", None, 0.25),             # platinum tier above 1000
        (100, "STANDARD", "ABC-123", 0.10),         # valid promo adds 10%
        (100, "STANDARD", "ABC-999", 50.0),         # super promo returns 50% of total
    ],
)
def test_calculate_discount(total, tier, promo, expected):
    result = DiscountEngine.calculate_discount(total, tier, promo)
    assert result == expected


def test_calculate_discount_invalid_promo():
    with pytest.raises(ValueError):
        DiscountEngine.calculate_discount(100, "STANDARD", "invalid")


# ---------- OrderProcessor.process_order ----------
def test_process_order_success():
    wh = Warehouse({"item1": 10})
    op = OrderProcessor(wh)
    result = op.process_order(
        order_id="1",
        user_data={"email": "test@example.com", "age": 25, "tier": "STANDARD"},
        items=[{"id": "item1", "qty": 1, "price": 10.0}],
    )
    assert result["status"] == "success"
    assert result["order_id"] == "1"
    assert result["items_count"] == 1


def test_process_order_inventory_error():
    wh = Warehouse({"item1": 10})
    op = OrderProcessor(wh)
    result = op.process_order(
        order_id="1",
        user_data={"email": "test@example.com", "age": 25, "tier": "STANDARD"},
        items=[{"id": "item1", "qty": 15, "price": 10.0}],
    )
    assert result["status"] == "failed"
    assert "Out of stock" in result["reason"]


def test_process_order_invalid_promo():
    wh = Warehouse({"item1": 10})
    op = OrderProcessor(wh)
    result = op.process_order(
        order_id="1",
        user_data={"email": "test@example.com", "age": 25, "tier": "STANDARD"},
        items=[{"id": "item1", "qty": 1, "price": 10.0}],
        promo_code="invalid",
    )
    assert result["status"] == "error"
    assert "Promo Error" in result["reason"]


def test_process_order_paypal_fraud():
    wh = Warehouse({"item1": 10})
    op = OrderProcessor(wh)
    with pytest.raises(FraudDetectedError):
        op.process_order(
            order_id="1",
            user_data={
                "email": "test@example.com",
                "age": 25,
                "tier": "STANDARD",
                "payment_method": "PAYPAL",
            },
            items=[{"id": "item1", "qty": 1, "price": 546.4426}],
        )


def test_process_order_crypto_min_amount():
    wh = Warehouse({"item1": 10})
    op = OrderProcessor(wh)
    with pytest.raises(PaymentError):
        op.process_order(
            order_id="1",
            user_data={
                "email": "test@example.com",
                "age": 25,
                "tier": "STANDARD",
                "payment_method": "CRYPTO",
            },
            items=[{"id": "item1", "qty": 1, "price": 10.0}],
        )

import pytest
from data.input_code.d06_complex_logic import DiscountEngine, OrderProcessor, Warehouse, FraudDetectedError, PaymentError, UserValidationError, InventoryError

# Helper datetime mock for night discount
class NightDateTime:
    @classmethod
    def now(cls):
        # Hour within 0-5 to trigger night discount
        return real_datetime.datetime(2023, 1, 1, 2, 0, 0)

import datetime as real_datetime

def test_T_MISSING_NIGHT_DISCOUNT(monkeypatch):
    # Mock datetime to night hour
    monkeypatch.setattr('data.input_code.d06_complex_logic.datetime', NightDateTime)
    result = DiscountEngine.calculate_discount(
        total_amount=100.0,
        user_tier="STANDARD",
        promo_code=None
    )
    assert result == 0.05


@pytest.mark.parametrize(
    "order_id,user_data,items,promo_code,expected_status",
    [
        (
            "1",
            {"email": "test@example.com", "age": 25, "payment_method": "CRYPTO"},
            [{"id": "item1", "qty": 6, "price": 10.0}],
            None,
            "success",
        ),
        (
            "1",
            {"email": "test@example.com", "age": 25, "payment_method": "PAYPAL"},
            [{"id": "item1", "qty": 1, "price": 10.0}],
            None,
            "success",
        ),
    ],
)
def test_T_MISSING_CRYPTO_AND_PAYPAL(order_id, user_data, items, promo_code, expected_status):
    wh = Warehouse({"item1": 10})
    op = OrderProcessor(wh)
    result = op.process_order(
        order_id=order_id,
        user_data=user_data,
        items=items,
        promo_code=promo_code,
    )
    assert result["status"] == expected_status

def test_T_MISSING_RETURN_FREE_ITEMS():
    wh = Warehouse({"item1": 10})
    op = OrderProcessor(wh)
    with pytest.raises(ValueError):
        op.process_order(
            order_id="1",
            user_data={"email": "test@example.com", "age": 25},
            items=[{"id": "item1", "qty": -1, "price": 0.0}],
            promo_code=None,
        )

def test_T_MISSING_WAREHOUSE_LOCK_RELEASE():
    wh = Warehouse({"item1": 10})
    # lock some quantity first
    wh.lock_item("item1", 5)
    assert "item1" in wh._locked_stock
    # now release it
    wh.release_item("item1", 5)
    # after full release, the key should be removed
    assert "item1" not in wh._locked_stock

def test_T_MISSING_INVALID_USER_TIER():
    result = DiscountEngine.calculate_discount(
        total_amount=100.0,
        user_tier="INVALID_TIER",
        promo_code=None,
    )
    assert result == 0.0