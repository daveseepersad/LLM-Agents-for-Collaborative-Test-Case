import pytest
from data.input_code.d06_complex_logic import *
from datetime import datetime

# Helper to create a Warehouse with given stock
def make_warehouse(stock):
    return Warehouse(initial_stock=stock)


# ---------- OrderProcessor.process_order ----------

def test_T1_SUCCESS_STANDARD():
    wh = make_warehouse({"A1": 10})
    op = OrderProcessor(wh)
    result = op.process_order(
        order_id="ORD001",
        user_data={
            "email": "john.doe@example.com",
            "age": 30,
            "tier": "STANDARD",
            "payment_method": "CC"
        },
        items=[{"id": "A1", "qty": 2, "price": 50.0}],
        promo_code=None,
    )
    assert result == {
        "status": "success",
        "order_id": "ORD001",
        "original_price": 100.0,
        "discount_applied": 0.0,
        "final_total": 122.0,
        "items_count": 1,
    }


def test_T2_NIGHT_GOLD_PROMO(monkeypatch):
    # mock datetime.now().hour == 2
    class DummyDatetime(datetime):
        @classmethod
        def now(cls):
            return cls(2023, 1, 1, 2, 0, 0)

    monkeypatch.setattr("data.input_code.d06_complex_logic.datetime", DummyDatetime)

    wh = make_warehouse({"B2": 10})
    op = OrderProcessor(wh)
    result = op.process_order(
        order_id="ORD002",
        user_data={
            "email": "alice@example.org",
            "age": 45,
            "tier": "GOLD",
            "payment_method": "CC",
        },
        items=[{"id": "B2", "qty": 2, "price": 100.0}],
        promo_code="ABC-123",
    )
    assert result == {
        "status": "success",
        "order_id": "ORD002",
        "original_price": 200.0,
        "discount_applied": 0.25,
        "final_total": 183.0,
        "items_count": 1,
    }


def test_T3_PLATINUM_HIGH_TOTAL_999():
    wh = make_warehouse({"C3": 10})
    op = OrderProcessor(wh)
    result = op.process_order(
        order_id="ORD003",
        user_data={
            "email": "bob@example.net",
            "age": 55,
            "tier": "PLATINUM",
            "payment_method": "CC",
        },
        items=[{"id": "C3", "qty": 3, "price": 400.0}],
        promo_code="XYZ-999",
    )
    assert result == {
        "status": "success",
        "order_id": "ORD003",
        "original_price": 1200.0,
        "discount_applied": 600.0,
        "final_total": -876936.0,
        "items_count": 1,
    }


def test_T4_INVALID_PROMO():
    wh = make_warehouse({"D4": 5})
    op = OrderProcessor(wh)
    result = op.process_order(
        order_id="ORD004",
        user_data={
            "email": "carol@example.com",
            "age": 28,
            "tier": "STANDARD",
            "payment_method": "CC",
        },
        items=[{"id": "D4", "qty": 1, "price": 20.0}],
        promo_code="BAD-CODE",
    )
    assert result["status"] == "error"
    assert "Promo Error: Invalid promo code format" in result["reason"]


def test_T5_INSUFFICIENT_STOCK():
    wh = make_warehouse({"E5": 5})
    op = OrderProcessor(wh)
    result = op.process_order(
        order_id="ORD005",
        user_data={
            "email": "dave@example.com",
            "age": 40,
            "tier": "STANDARD",
            "payment_method": "CC",
        },
        items=[{"id": "E5", "qty": 10, "price": 5.0}],
        promo_code=None,
    )
    assert result["status"] == "failed"
    assert "Out of stock: Insufficient stock for E5" in result["reason"]


def test_T6_NEGATIVE_QTY_ZERO_PRICE():
    wh = make_warehouse({"F6": 10})
    op = OrderProcessor(wh)
    with pytest.raises(ValueError):
        op.process_order(
            order_id="ORD006",
            user_data={
                "email": "eve@example.com",
                "age": 35,
                "tier": "STANDARD",
                "payment_method": "CC",
            },
            items=[{"id": "F6", "qty": -1, "price": 0.0}],
            promo_code=None,
        )


# ---------- OrderProcessor.validate_user ----------

@pytest.mark.parametrize(
    "email,age",
    [
        ("invalid-email", 25),
        ("young@example.com", 16),
        ("oldtimer@example.com", 101),
    ],
)
def test_validate_user_errors(email, age):
    op = OrderProcessor(make_warehouse({}))
    with pytest.raises(UserValidationError):
        op.validate_user(email, age)


# ---------- Warehouse.check_stock ----------

def test_T12_WAREHOUSE_CHECK_STOCK():
    wh = make_warehouse({"KNOWN": 3})
    with pytest.raises(InventoryError):
        wh.check_stock("UNKNOWN", 1)


# ---------- Warehouse.release_item ----------

def test_T13_WAREHOUSE_RELEASE_DELETION():
    wh = Warehouse(initial_stock={"I9": 10})
    # manually set locked stock
    wh._locked_stock = {"I9": 5}
    wh.release_item("I9", 5)
    assert "I9" not in wh._locked_stock


# ---------- Additional payment edge cases ----------

def test_T10_FRAUD_PAYPAL(monkeypatch):
    # mock datetime.now() to any hour (not night) – hour not relevant for discount
    class DummyDatetime(datetime):
        @classmethod
        def now(cls):
            return cls(2023, 1, 1, 12, 0, 0)

    monkeypatch.setattr("data.input_code.d06_complex_logic.datetime", DummyDatetime)

    wh = make_warehouse({"G7": 5})
    op = OrderProcessor(wh)
    with pytest.raises(FraudDetectedError):
        op.process_order(
            order_id="ORD010",
            user_data={
                "email": "fraud@example.com",
                "age": 30,
                "tier": "STANDARD",
                "payment_method": "PAYPAL",
            },
            items=[{"id": "G7", "qty": 1, "price": 546.44}],
            promo_code=None,
        )


def test_T11_CRYPTO_MIN_AMOUNT():
    wh = make_warehouse({"H8": 5})
    op = OrderProcessor(wh)
    with pytest.raises(PaymentError):
        op.process_order(
            order_id="ORD011",
            user_data={
                "email": "crypto@example.com",
                "age": 27,
                "tier": "STANDARD",
                "payment_method": "CRYPTO",
            },
            items=[{"id": "H8", "qty": 2, "price": 20.0}],
            promo_code=None,
        )

import pytest
from datetime import datetime

# ---------- DiscountEngine.calculate_discount ----------
def test_T_MISS_NIGHT_ONLY(monkeypatch):
    # Mock datetime to hour 2 (night)
    class DummyDatetime(datetime):
        @classmethod
        def now(cls):
            return cls(2023, 1, 1, 2, 0, 0)

    monkeypatch.setattr("data.input_code.d06_complex_logic.datetime", DummyDatetime)

    discount = DiscountEngine.calculate_discount(
        total_amount=100.0,
        user_tier="STANDARD",
        promo_code=None,
    )
    assert discount == 0.05


def test_T_MISS_PLATINUM_NO_EXTRA(monkeypatch):
    # Mock datetime to hour 12 (daytime)
    class DummyDatetime(datetime):
        @classmethod
        def now(cls):
            return cls(2023, 1, 1, 12, 0, 0)

    monkeypatch.setattr("data.input_code.d06_complex_logic.datetime", DummyDatetime)

    discount = DiscountEngine.calculate_discount(
        total_amount=800.0,
        user_tier="PLATINUM",
        promo_code=None,
    )
    assert discount == 0.20


# ---------- OrderProcessor.validate_user ----------
@pytest.mark.parametrize(
    "email,age",
    [
        ("valid.user@example.com", 18),
        ("valid@example.co.uk", 100),
    ],
)
def test_T_MISS_VALIDATE_USER_EDGE(email, age):
    op = OrderProcessor(make_warehouse({}))
    # Should not raise any exception
    op.validate_user(email, age)


# ---------- OrderProcessor.process_order (PAYPAL success) ----------
def test_T_MISS_PAYPAL_SUCCESS(monkeypatch):
    # Ensure no night discount interferes
    class DummyDatetime(datetime):
        @classmethod
        def now(cls):
            return cls(2023, 1, 1, 12, 0, 0)

    monkeypatch.setattr("data.input_code.d06_complex_logic.datetime", DummyDatetime)

    wh = make_warehouse({"P1": 5})
    op = OrderProcessor(wh)
    result = op.process_order(
        order_id="ORD_PAYPAL",
        user_data={
            "email": "buyer@example.com",
            "age": 30,
            "tier": "STANDARD",
            "payment_method": "PAYPAL",
        },
        items=[{"id": "P1", "qty": 1, "price": 100.0}],
        promo_code=None,
    )
    assert result == {
        "status": "success",
        "order_id": "ORD_PAYPAL",
        "original_price": 100.0,
        "discount_applied": 0.0,
        "final_total": 122.0,
        "items_count": 1,
    }


# ---------- OrderProcessor.process_order (CRYPTO success) ----------
def test_T_MISS_CRYPTO_SUCCESS(monkeypatch):
    # Ensure no night discount interferes
    class DummyDatetime(datetime):
        @classmethod
        def now(cls):
            return cls(2023, 1, 1, 12, 0, 0)

    monkeypatch.setattr("data.input_code.d06_complex_logic.datetime", DummyDatetime)

    wh = make_warehouse({"C1": 5})
    op = OrderProcessor(wh)
    result = op.process_order(
        order_id="ORD_CRYPTO",
        user_data={
            "email": "crypto.user@example.com",
            "age": 45,
            "tier": "STANDARD",
            "payment_method": "CRYPTO",
        },
        items=[{"id": "C1", "qty": 2, "price": 30.0}],
        promo_code=None,
    )
    assert result == {
        "status": "success",
        "order_id": "ORD_CRYPTO",
        "original_price": 60.0,
        "discount_applied": 0.0,
        "final_total": 73.2,
        "items_count": 1,
    }

def test_T_MISS_PLATINUM_EXTRA_DISCOUNT(monkeypatch):
    # Mock datetime to a daytime hour to avoid night discount
    class DummyDatetime(datetime):
        @classmethod
        def now(cls):
            return cls(2023, 1, 1, 12, 0, 0)

    monkeypatch.setattr("data.input_code.d06_complex_logic.datetime", DummyDatetime)

    discount = DiscountEngine.calculate_discount(
        total_amount=1500.0,
        user_tier="PLATINUM",
        promo_code=None,
    )
    assert discount == 0.25


def test_T_MISS_WAREHOUSE_RELEASE_NO_LOCK():
    wh = Warehouse(initial_stock={"X1": 5})
    # No prior lock for X1
    wh.release_item("X1", 1)
    assert wh._locked_stock == {}


def test_T_MISS_INVENTORY_ROLLBACK():
    wh = make_warehouse({"A1": 5, "B2": 5})
    op = OrderProcessor(wh)
    result = op.process_order(
        order_id="ORD_ROLLBACK",
        user_data={
            "email": "valid.user@example.com",
            "age": 30,
            "tier": "STANDARD",
            "payment_method": "CC",
        },
        items=[
            {"id": "A1", "qty": 2, "price": 10.0},
            {"id": "B2", "qty": 10, "price": 5.0},
        ],
        promo_code=None,
    )
    assert result["status"] == "failed"
    assert "Out of stock" in result["reason"]
    # Ensure rollback released any previously locked items
    assert wh._locked_stock == {}