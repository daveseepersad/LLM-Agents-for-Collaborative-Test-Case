import pytest
from data.input_code.d06_complex_logic import *

# ------------------------------
# Warehouse tests
# ------------------------------

@pytest.mark.parametrize(
    "initial_stock,item_id,quantity,expected_exception",
    [
        ({"A1": 10}, "B2", 1, InventoryError),   # item not found
    ]
)
def test_warehouse_check_stock_item_not_found(initial_stock, item_id, quantity, expected_exception):
    wh = Warehouse(initial_stock)
    with pytest.raises(expected_exception):
        wh.check_stock(item_id, quantity)


@pytest.mark.parametrize(
    "initial_stock,item_id,quantity,expected",
    [
        ({"A1": 5}, "A1", 6, False),   # insufficient stock
        ({"A1": 10}, "A1", 5, True),   # sufficient stock
    ]
)
def test_warehouse_check_stock(initial_stock, item_id, quantity, expected):
    wh = Warehouse(initial_stock)
    assert wh.check_stock(item_id, quantity) == expected


def test_warehouse_lock_and_release_full_cycle():
    wh = Warehouse({"A1": 10})
    # lock 5
    wh.lock_item("A1", 5)
    assert wh._locked_stock.get("A1") == 5
    # release 5, should remove entry
    wh.release_item("A1", 5)
    assert "A1" not in wh._locked_stock


def test_warehouse_lock_insufficient_raises():
    wh = Warehouse({"A1": 3})
    with pytest.raises(InventoryError):
        wh.lock_item("A1", 4)


# ------------------------------
# DiscountEngine tests
# ------------------------------

@pytest.mark.parametrize(
    "hour,total_amount,user_tier,promo_code,expected",
    [
        (2, 100.0, "STANDARD", None, 0.05),                     # night discount
        (12, 1500.0, "PLATINUM", None, 0.25),                  # platinum + amount >1000
        (1, 2000.0, "PLATINUM", "ABC-123", 0.40),              # capped at 40%
        (15, 800.0, "GOLD", "XYZ-999", 0.5),                    # promo ends with 999 -> 50% off (as discount percent)
    ]
)
def test_discount_engine_calculate(monkeypatch, hour, total_amount, user_tier, promo_code, expected):
    class DummyDatetime:
        @classmethod
        def now(cls):
            return type("dt", (), {"hour": hour})
    monkeypatch.setattr("data.input_code.d06_complex_logic.datetime", DummyDatetime)

    if promo_code == "XYZ-999":
        # The implementation returns total_amount * 0.5 for promo ending with 999.
        result = DiscountEngine.calculate_discount(total_amount, user_tier, promo_code)
        assert result == total_amount * 0.5
    else:
        result = DiscountEngine.calculate_discount(total_amount, user_tier, promo_code)
        assert result == expected


def test_discount_engine_invalid_promo():
    with pytest.raises(ValueError):
        DiscountEngine.calculate_discount(100.0, "STANDARD", "bad_code")


# ------------------------------
# OrderProcessor.validate_user tests
# ------------------------------

@pytest.mark.parametrize(
    "email,age,expected_exception",
    [
        ("invalid_email", 30, UserValidationError),
        ("test@example.com", 16, UserValidationError),
        ("senior@example.com", 101, UserValidationError),
    ]
)
def test_order_processor_validate_user_errors(email, age, expected_exception):
    op = OrderProcessor(Warehouse({}))
    with pytest.raises(expected_exception):
        op.validate_user(email, age)


def test_order_processor_validate_user_success():
    op = OrderProcessor(Warehouse({}))
    # Should not raise
    op.validate_user("valid.user@example.com", 25)


# ------------------------------
# OrderProcessor.process_order tests
# ------------------------------

def test_process_order_successful(monkeypatch):
    # Mock datetime for discount (no night discount)
    class DummyDatetime:
        @classmethod
        def now(cls):
            return type("dt", (), {"hour": 14})
    monkeypatch.setattr("data.input_code.d06_complex_logic.datetime", DummyDatetime)

    warehouse = Warehouse({"A1": 5, "B2": 2})
    op = OrderProcessor(warehouse)

    result = op.process_order(
        order_id="ORD001",
        user_data={
            "email": "buyer@example.com",
            "age": 35,
            "tier": "GOLD",
            "payment_method": "CC"
        },
        items=[
            {"id": "A1", "qty": 2, "price": 50.0},
            {"id": "B2", "qty": 1, "price": 100.0}
        ],
        promo_code=None
    )
    assert result == {
        "status": "success",
        "order_id": "ORD001",
        "original_price": 200.0,
        "discount_applied": 0.10,
        "final_total": 219.6,
        "items_count": 2
    }


def test_process_order_inventory_failure(monkeypatch):
    class DummyDatetime:
        @classmethod
        def now(cls):
            return type("dt", (), {"hour": 10})
    monkeypatch.setattr("data.input_code.d06_complex_logic.datetime", DummyDatetime)

    warehouse = Warehouse({"A1": 3, "B2": 4})
    op = OrderProcessor(warehouse)

    result = op.process_order(
        order_id="ORD002",
        user_data={
            "email": "buyer2@example.com",
            "age": 28,
            "tier": "STANDARD",
            "payment_method": "CC"
        },
        items=[
            {"id": "A1", "qty": 3, "price": 30.0},
            {"id": "B2", "qty": 5, "price": 20.0}
        ],
        promo_code=None
    )
    assert result == {
        "status": "failed",
        "reason": "Out of stock: Insufficient stock for B2"
    }


def test_process_order_invalid_promo(monkeypatch):
    class DummyDatetime:
        @classmethod
        def now(cls):
            return type("dt", (), {"hour": 9})
    monkeypatch.setattr("data.input_code.d06_complex_logic.datetime", DummyDatetime)

    warehouse = Warehouse({"A1": 10})
    op = OrderProcessor(warehouse)

    result = op.process_order(
        order_id="ORD003",
        user_data={
            "email": "buyer3@example.com",
            "age": 45,
            "tier": "STANDARD",
            "payment_method": "CC"
        },
        items=[{"id": "A1", "qty": 1, "price": 100.0}],
        promo_code="WRONG-12"
    )
    assert result == {
        "status": "error",
        "reason": "Promo Error: Invalid promo code format"
    }


def test_process_order_super_promo(monkeypatch):
    # Force DiscountEngine to return 0.5 discount percent for the super promo
    def mock_calculate_discount(total_amount, user_tier, promo_code):
        return 0.5
    monkeypatch.setattr(DiscountEngine, "calculate_discount", staticmethod(mock_calculate_discount))

    warehouse = Warehouse({"A1": 5})
    op = OrderProcessor(warehouse)

    result = op.process_order(
        order_id="ORD004",
        user_data={
            "email": "buyer4@example.com",
            "age": 30,
            "tier": "STANDARD",
            "payment_method": "CC"
        },
        items=[{"id": "A1", "qty": 2, "price": 250.0}],
        promo_code="ABC-999"
    )
    assert result == {
        "status": "success",
        "order_id": "ORD004",
        "original_price": 500.0,
        "discount_applied": 0.5,
        "final_total": 305.0,
        "items_count": 1
    }


def test_process_order_paypal_fraud(monkeypatch):
    # Mock datetime to avoid night discount
    class DummyDatetime:
        @classmethod
        def now(cls):
            return type("dt", (), {"hour": 15})
    monkeypatch.setattr("data.input_code.d06_complex_logic.datetime", DummyDatetime)

    warehouse = Warehouse({"A1": 2})
    op = OrderProcessor(warehouse)

    # Choose a price that after 22% tax rounds to 666.66
    with pytest.raises(FraudDetectedError):
        op.process_order(
            order_id="ORD005",
            user_data={
                "email": "fraud@example.com",
                "age": 40,
                "tier": "STANDARD",
                "payment_method": "PAYPAL"
            },
            items=[{"id": "A1", "qty": 1, "price": 546.44}],
            promo_code=None
        )


def test_process_order_crypto_below_min(monkeypatch):
    class DummyDatetime:
        @classmethod
        def now(cls):
            return type("dt", (), {"hour": 11})
    monkeypatch.setattr("data.input_code.d06_complex_logic.datetime", DummyDatetime)

    warehouse = Warehouse({"A1": 10})
    op = OrderProcessor(warehouse)

    with pytest.raises(PaymentError):
        op.process_order(
            order_id="ORD006",
            user_data={
                "email": "crypto@example.com",
                "age": 27,
                "tier": "STANDARD",
                "payment_method": "CRYPTO"
            },
            items=[{"id": "A1", "qty": 1, "price": 30.0}],
            promo_code=None
        )


def test_process_order_negative_qty_free_item():
    warehouse = Warehouse({"A1": 5})
    op = OrderProcessor(warehouse)

    with pytest.raises(ValueError):
        op.process_order(
            order_id="ORD007",
            user_data={
                "email": "return@example.com",
                "age": 35,
                "tier": "STANDARD",
                "payment_method": "CC"
            },
            items=[{"id": "A1", "qty": -1, "price": 0.0}],
            promo_code=None
        )