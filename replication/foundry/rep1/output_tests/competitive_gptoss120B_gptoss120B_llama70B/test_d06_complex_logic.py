import pytest
from data.input_code.d06_complex_logic import *
from unittest.mock import Mock

# ---------- Warehouse.check_stock ----------
@pytest.mark.parametrize(
    "stock, item_id, quantity, expected, exception",
    [
        ({"A": 5}, "B", 1, None, InventoryError),   # missing item
        ({"A": 5}, "A", 6, False, None),            # insufficient stock
        ({"A": 10}, "A", 4, True, None),            # sufficient stock
    ],
)
def test_warehouse_check_stock(stock, item_id, quantity, expected, exception):
    wh = Warehouse(stock)
    if exception:
        with pytest.raises(exception):
            wh.check_stock(item_id, quantity)
    else:
        assert wh.check_stock(item_id, quantity) is expected


# ---------- Warehouse.lock_item ----------
def test_warehouse_lock_success():
    wh = Warehouse({"A": 10})
    wh.lock_item("A", 3)
    assert wh._locked_stock == {"A": 3}


def test_warehouse_lock_failure():
    wh = Warehouse({"A": 2})
    with pytest.raises(InventoryError):
        wh.lock_item("A", 5)


# ---------- Warehouse.release_item ----------
def test_warehouse_release_deletion():
    wh = Warehouse({"A": 10})
    # pre‑lock 4 items
    wh._locked_stock = {"A": 4}
    wh.release_item("A", 4)
    assert wh._locked_stock == {}


# ---------- DiscountEngine.calculate_discount ----------
@pytest.mark.parametrize(
    "hour, total, tier, promo, expected",
    [
        (2, 200.0, "GOLD", None, 0.15000000000000002),                     # night + gold
        (10, 1500.0, "PLATINUM", None, 0.25),               # platinum + >1000
        (12, 300.0, "STANDARD", "ABC-123", 0.10),           # valid promo
        (14, 400.0, "GOLD", "XYZ-999", 200.0),              # super promo 50%
        (9, 100.0, "STANDARD", "invalid_code", "ValueError"),  # bad promo
        (3, 2000.0, "PLATINUM", "ABC-123", 0.40),           # max cap
    ],
)
def test_discount_engine(monkeypatch, hour, total, tier, promo, expected):
    # mock datetime.now().hour
    mock_dt = Mock()
    mock_dt.now.return_value = Mock(hour=hour)
    monkeypatch.setattr("data.input_code.d06_complex_logic.datetime", mock_dt)

    if expected == "ValueError":
        with pytest.raises(ValueError):
            DiscountEngine.calculate_discount(total, tier, promo)
    else:
        result = DiscountEngine.calculate_discount(total, tier, promo)
        assert result == expected


# ---------- OrderProcessor.validate_user ----------
@pytest.mark.parametrize(
    "email, age, exception",
    [
        ("bademail", 25, UserValidationError),   # invalid email
        ("young@domain.com", 16, UserValidationError),  # underage
        ("old@domain.com", 101, UserValidationError),   # overage
    ],
)
def test_validate_user(email, age, exception):
    op = OrderProcessor(Warehouse({}))
    with pytest.raises(exception):
        op.validate_user(email, age)


# ---------- OrderProcessor.process_order ----------
def test_process_order_success(monkeypatch):
    # mock datetime for night discount
    mock_dt = Mock()
    mock_dt.now.return_value = Mock(hour=2)
    monkeypatch.setattr("data.input_code.d06_complex_logic.datetime", mock_dt)

    wh = Warehouse({"A": 5, "B": 3})
    op = OrderProcessor(wh)
    result = op.process_order(
        order_id="ORD001",
        user_data={
            "email": "user@example.com",
            "age": 30,
            "tier": "GOLD",
            "payment_method": "CC",
        },
        items=[
            {"id": "A", "qty": 2, "price": 50.0},
            {"id": "B", "qty": 1, "price": 100.0},
        ],
        promo_code=None,
    )
    assert result == {
        "status": "success",
        "order_id": "ORD001",
        "original_price": 200.0,
        "discount_applied": 0.15000000000000002,
        "final_total": 207.4,
        "items_count": 2,
    }


def test_process_order_inventory_failure():
    wh = Warehouse({"X": 1, "Y": 2})
    op = OrderProcessor(wh)
    result = op.process_order(
        order_id="ORD002",
        user_data={
            "email": "buyer@test.com",
            "age": 45,
            "tier": "STANDARD",
            "payment_method": "CC",
        },
        items=[
            {"id": "X", "qty": 1, "price": 20.0},
            {"id": "Y", "qty": 5, "price": 10.0},
        ],
        promo_code=None,
    )
    assert result == {
        "status": "failed",
        "reason": "Out of stock: Insufficient stock for Y",
    }


def test_process_order_invalid_promo_error(monkeypatch):
    # mock datetime (any hour, no discount)
    mock_dt = Mock()
    mock_dt.now.return_value = Mock(hour=12)
    monkeypatch.setattr("data.input_code.d06_complex_logic.datetime", mock_dt)

    wh = Warehouse({"C": 10})
    op = OrderProcessor(wh)
    result = op.process_order(
        order_id="ORD003",
        user_data={
            "email": "shopper@domain.com",
            "age": 28,
            "tier": "STANDARD",
            "payment_method": "CC",
        },
        items=[{"id": "C", "qty": 1, "price": 30.0}],
        promo_code="BAD-12",
    )
    assert result == {
        "status": "error",
        "reason": "Promo Error: Invalid promo code format",
    }


def test_process_order_hidden_value_error():
    wh = Warehouse({"D": 5})
    op = OrderProcessor(wh)
    with pytest.raises(ValueError):
        op.process_order(
            order_id="ORD004",
            user_data={
                "email": "returner@example.org",
                "age": 40,
                "tier": "STANDARD",
                "payment_method": "CC",
            },
            items=[{"id": "D", "qty": -1, "price": 0.0}],
            promo_code=None,
        )


def test_process_order_paypal_fraud(monkeypatch):
    # Force discount to produce final amount 666.66 after rounding
    def fake_discount(*args, **kwargs):
        return 0.08926  # approx value to hit 666.66 after tax and rounding
    monkeypatch.setattr(
        "data.input_code.d06_complex_logic.DiscountEngine.calculate_discount",
        staticmethod(fake_discount),
    )
    wh = Warehouse({"E": 2})
    op = OrderProcessor(wh)
    with pytest.raises(FraudDetectedError):
        op.process_order(
            order_id="ORD005",
            user_data={
                "email": "fraud@evil.com",
                "age": 35,
                "tier": "STANDARD",
                "payment_method": "PAYPAL",
            },
            items=[{"id": "E", "qty": 1, "price": 600.0}],
            promo_code=None,
        )


def test_process_order_crypto_min_amount(monkeypatch):
    # No discount, total 30 -> tax makes 36.6 < 50, should raise PaymentError
    wh = Warehouse({"F": 5})
    op = OrderProcessor(wh)
    with pytest.raises(PaymentError):
        op.process_order(
            order_id="ORD006",
            user_data={
                "email": "crypto@buyer.com",
                "age": 27,
                "tier": "STANDARD",
                "payment_method": "CRYPTO",
            },
            items=[{"id": "F", "qty": 1, "price": 30.0}],
            promo_code=None,
        )