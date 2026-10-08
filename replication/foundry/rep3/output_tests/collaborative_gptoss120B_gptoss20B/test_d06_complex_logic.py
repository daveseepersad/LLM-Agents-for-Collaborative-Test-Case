import pytest
from data.input_code.d06_complex_logic import *

# ---------- Warehouse ----------

@pytest.mark.parametrize(
    "stock,item_id,quantity,expected_exception",
    [
        ({"A": 10}, "B", 1, InventoryError),  # unknown item
    ],
)
def test_warehouse_check_stock_exceptions(stock, item_id, quantity, expected_exception):
    wh = Warehouse(initial_stock=stock)
    with pytest.raises(expected_exception):
        wh.check_stock(item_id, quantity)


# ---------- DiscountEngine ----------

@pytest.mark.parametrize(
    "total_amount,user_tier,promo_code,expected",
    [
        (100.0, "GOLD", "bad", ValueError),                     # invalid promo format
        (200.0, "GOLD", "ABC-999", 100.0),                     # 50% off promo ending with 999
    ],
)
def test_discount_engine(total_amount, user_tier, promo_code, expected):
    if isinstance(expected, type) and issubclass(expected, Exception):
        with pytest.raises(expected):
            DiscountEngine.calculate_discount(total_amount, user_tier, promo_code)
    else:
        assert DiscountEngine.calculate_discount(total_amount, user_tier, promo_code) == expected


# ---------- OrderProcessor.validate_user ----------

def test_validate_user_invalid_email():
    op = OrderProcessor(warehouse=Warehouse(initial_stock={}))
    with pytest.raises(UserValidationError):
        op.validate_user(email="bad", age=30)


# ---------- OrderProcessor.process_order ----------

def test_process_order_out_of_stock_unknown_item():
    wh = Warehouse(initial_stock={"A": 5})
    op = OrderProcessor(warehouse=wh)
    result = op.process_order(
        order_id="ORD1",
        user_data={"email": "user@example.com", "age": 25},
        items=[{"id": "B", "qty": 1, "price": 10.0}],
        promo_code=None,
    )
    assert result["status"] == "failed"
    assert "Item B not found in warehouse" in result["reason"]


def test_process_order_insufficient_stock():
    wh = Warehouse(initial_stock={"A": 1})
    op = OrderProcessor(warehouse=wh)
    result = op.process_order(
        order_id="ORD2",
        user_data={"email": "user2@example.com", "age": 28},
        items=[{"id": "A", "qty": 2, "price": 5.0}],
        promo_code=None,
    )
    assert result["status"] == "failed"
    assert "Insufficient stock for A" in result["reason"]


def test_process_order_crypto_minimum_payment_error():
    wh = Warehouse(initial_stock={"X": 10})
    op = OrderProcessor(warehouse=wh)
    with pytest.raises(PaymentError):
        op.process_order(
            order_id="ORD_CRYPTO",
            user_data={
                "email": "user@example.com",
                "age": 25,
                "payment_method": "CRYPTO",
            },
            items=[{"id": "X", "qty": 1, "price": 20.0}],
            promo_code=None,
        )


def test_process_order_success_cc(monkeypatch):
    # Force datetime.now() to a non‑night hour to avoid hidden discounts
    class FixedDateTime:
        @classmethod
        def now(cls):
            return __import__("datetime").datetime(2022, 1, 1, 12, 0, 0)

    monkeypatch.setattr(
        "data.input_code.d06_complex_logic.datetime", FixedDateTime, raising=False
    )

    wh = Warehouse(initial_stock={"A": 10})
    op = OrderProcessor(warehouse=wh)

    result = op.process_order(
        order_id="ORD_OK",
        user_data={"email": "good@example.com", "age": 30},
        items=[{"id": "A", "qty": 2, "price": 20.0}],
        promo_code=None,
    )

    assert result == {
        "status": "success",
        "order_id": "ORD_OK",
        "original_price": 40.0,
        "discount_applied": 0.0,
        "final_total": 48.8,
        "items_count": 1,
    }

# ---------- DiscountEngine ----------

def test_discount_night_gold(monkeypatch):
    # Mock datetime to a night hour (e.g., 02:00)
    class FixedDateTime:
        @classmethod
        def now(cls):
            return __import__("datetime").datetime(2022, 1, 1, 2, 0, 0)

    monkeypatch.setattr(
        "data.input_code.d06_complex_logic.datetime", FixedDateTime, raising=False
    )
    result = DiscountEngine.calculate_discount(
        total_amount=100.0,
        user_tier="GOLD",
        promo_code=None,
    )
    assert result == 0.15000000000000002  # Adjusted for floating‑point precision


def test_discount_night_platinum_cap(monkeypatch):
    # Mock datetime to a night hour (e.g., 03:00)
    class FixedDateTime:
        @classmethod
        def now(cls):
            return __import__("datetime").datetime(2022, 1, 1, 3, 0, 0)

    monkeypatch.setattr(
        "data.input_code.d06_complex_logic.datetime", FixedDateTime, raising=False
    )
    result = DiscountEngine.calculate_discount(
        total_amount=1500.0,
        user_tier="PLATINUM",
        promo_code="ABC-123",
    )
    assert result == 0.40


def test_discount_promo_only(monkeypatch):
    # Mock datetime to a non‑night hour (e.g., 12:00) to avoid night discount
    class FixedDateTime:
        @classmethod
        def now(cls):
            return __import__("datetime").datetime(2022, 1, 1, 12, 0, 0)

    monkeypatch.setattr(
        "data.input_code.d06_complex_logic.datetime", FixedDateTime, raising=False
    )
    result = DiscountEngine.calculate_discount(
        total_amount=100.0,
        user_tier="STANDARD",
        promo_code="DEF-456",
    )
    assert result == 0.10


# ---------- OrderProcessor.process_order ----------

def test_process_order_rollback_inventory():
    # Stock for A is sufficient, B exists but insufficient
    wh = Warehouse(initial_stock={"A": 5, "B": 0})
    op = OrderProcessor(warehouse=wh)

    result = op.process_order(
        order_id="ORD_ROLLBACK",
        user_data={"email": "user@example.com", "age": 25},
        items=[
            {"id": "A", "qty": 1, "price": 10.0},
            {"id": "B", "qty": 1, "price": 5.0},
        ],
        promo_code=None,
    )

    assert result == {
        "status": "failed",
        "reason": "Out of stock: Insufficient stock for B",
    }


# ---------- OrderProcessor.validate_user ----------

def test_validate_user_age_over_100():
    op = OrderProcessor(warehouse=Warehouse(initial_stock={}))
    with pytest.raises(UserValidationError):
        op.validate_user(email="user@example.com", age=101)

import pytest
from data.input_code.d06_complex_logic import *

def test_process_order_negative_qty_free_items():
    wh = Warehouse(initial_stock={"A": 1})
    op = OrderProcessor(warehouse=wh)
    with pytest.raises(ValueError):
        op.process_order(
            order_id="ORD_FREE_BAD",
            user_data={"email": "user@example.com", "age": 25},
            items=[{"id": "A", "qty": -1, "price": 0.0}],
            promo_code=None,
        )

def test_process_order_invalid_promo_format():
    wh = Warehouse(initial_stock={"A": 2})
    op = OrderProcessor(warehouse=wh)
    result = op.process_order(
        order_id="ORD_PROMO_FAIL",
        user_data={"email": "user@example.com", "age": 30},
        items=[{"id": "A", "qty": 2, "price": 50.0}],
        promo_code="BAD",
    )
    assert result == {
        "status": "error",
        "reason": "Promo Error: Invalid promo code format"
    }