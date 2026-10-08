import pytest
from data.input_code.d06_complex_logic import *
from types import SimpleNamespace

# Helper to create a dummy datetime class with a controllable now()
def _dummy_datetime(hour):
    class DummyDateTime:
        @staticmethod
        def now():
            return SimpleNamespace(hour=hour)
    return DummyDateTime


# ---------- Warehouse Tests ----------
@pytest.mark.parametrize(
    "initial_stock,item_id,quantity,expected_exception",
    [
        ({"itemA": 10}, "missing_item", 1, InventoryError),
    ],
)
def test_warehouse_check_stock_item_not_found(initial_stock, item_id, quantity, expected_exception):
    wh = Warehouse(initial_stock)
    with pytest.raises(expected_exception):
        wh.check_stock(item_id, quantity)


def test_warehouse_check_stock_insufficient_due_to_locked():
    wh = Warehouse({"itemA": 5})
    # lock some stock to make it insufficient
    wh.lock_item("itemA", 2)
    assert wh.check_stock("itemA", 4) is False


def test_warehouse_lock_item_success():
    wh = Warehouse({"itemA": 10})
    # should not raise
    wh.lock_item("itemA", 3)
    # internal state check (optional)
    assert wh._locked_stock.get("itemA", 0) == 3


# ---------- DiscountEngine Tests ----------
@pytest.mark.parametrize(
    "hour,total_amount,user_tier,promo_code,expected",
    [
        (2, 100.0, "STANDARD", None, 0.05),                     # night hour discount
        (12, 1500.0, "PLATINUM", None, 0.25),                  # platinum + high amount
        (12, 200.0, "STANDARD", "ABC-123", 0.10),              # valid promo
        (12, 200.0, "STANDARD", "XYZ-999", 100.0),             # super promo (50% off)
        (3, 2000.0, "PLATINUM", "ABC-123", 0.40),              # cap at 40%
    ],
)
def test_discount_engine_calculate(monkeypatch, hour, total_amount, user_tier, promo_code, expected):
    # replace the datetime class in the module with a dummy that returns the desired hour
    monkeypatch.setattr(
        "data.input_code.d06_complex_logic.datetime",
        _dummy_datetime(hour),
        raising=False,
    )
    result = DiscountEngine.calculate_discount(total_amount, user_tier, promo_code)
    assert result == expected


def test_discount_engine_invalid_promo(monkeypatch):
    monkeypatch.setattr(
        "data.input_code.d06_complex_logic.datetime",
        _dummy_datetime(12),
        raising=False,
    )
    with pytest.raises(ValueError):
        DiscountEngine.calculate_discount(100.0, "STANDARD", "badcode")


# ---------- OrderProcessor.validate_user Tests ----------
@pytest.mark.parametrize(
    "email,age,expected_exception",
    [
        ("invalid_email", 30, UserValidationError),
        ("test@example.com", 17, UserValidationError),
        ("old@example.com", 101, UserValidationError),
    ],
)
def test_validate_user_exceptions(email, age, expected_exception):
    op = OrderProcessor(Warehouse({}))
    with pytest.raises(expected_exception):
        op.validate_user(email, age)


# ---------- OrderProcessor.process_order Tests ----------
def test_process_order_success_standard(monkeypatch):
    # Mock datetime for discount calculation (no night discount)
    monkeypatch.setattr(
        "data.input_code.d06_complex_logic.datetime",
        _dummy_datetime(12),
        raising=False,
    )
    wh = Warehouse({"item1": 5})
    op = OrderProcessor(wh)

    order = op.process_order(
        order_id="ORD123",
        user_data={
            "email": "user@example.com",
            "age": 30,
            "tier": "GOLD",
            "payment_method": "CC",
        },
        items=[{"id": "item1", "qty": 2, "price": 50.0}],
        promo_code=None,
    )
    assert order == {
        "status": "success",
        "order_id": "ORD123",
        "original_price": 100.0,
        "discount_applied": 0.10,
        "final_total": 109.8,
        "items_count": 1,
    }


def test_process_order_promo_invalid(monkeypatch):
    monkeypatch.setattr(
        "data.input_code.d06_complex_logic.datetime",
        _dummy_datetime(12),
        raising=False,
    )
    wh = Warehouse({"item1": 5})
    op = OrderProcessor(wh)

    order = op.process_order(
        order_id="ORD124",
        user_data={
            "email": "user@example.com",
            "age": 30,
            "tier": "STANDARD",
            "payment_method": "CC",
        },
        items=[{"id": "item1", "qty": 1, "price": 20.0}],
        promo_code="BAD-12",
    )
    assert order == {
        "status": "error",
        "reason": "Promo Error: Invalid promo code format",
    }


def test_process_order_inventory_error(monkeypatch):
    monkeypatch.setattr(
        "data.input_code.d06_complex_logic.datetime",
        _dummy_datetime(12),
        raising=False,
    )
    wh = Warehouse({"item1": 1})
    op = OrderProcessor(wh)

    order = op.process_order(
        order_id="ORD125",
        user_data={
            "email": "user@example.com",
            "age": 30,
            "tier": "STANDARD",
            "payment_method": "CC",
        },
        items=[
            {"id": "item1", "qty": 1, "price": 10.0},
            {"id": "item1", "qty": 2, "price": 10.0},
        ],
        promo_code=None,
    )
    assert order == {
        "status": "failed",
        "reason": "Out of stock: Insufficient stock for item1",
    }


def test_process_order_division_by_zero():
    wh = Warehouse({"item1": 10})
    op = OrderProcessor(wh)

    with pytest.raises(ValueError):
        op.process_order(
            order_id="ORD126",
            user_data={
                "email": "user@example.com",
                "age": 30,
                "tier": "STANDARD",
                "payment_method": "CC",
            },
            items=[{"id": "item1", "qty": -1, "price": 0.0}],
            promo_code=None,
        )


def test_process_order_fraud_paypal(monkeypatch):
    # Set hour to avoid night discount; total will be crafted to hit 666.66 after tax
    monkeypatch.setattr(
        "data.input_code.d06_complex_logic.datetime",
        _dummy_datetime(12),
        raising=False,
    )
    wh = Warehouse({"item1": 5})
    op = OrderProcessor(wh)

    # Compute price that after 22% tax equals 666.66 (rounded to 2 decimals)
    price = 546.4426
    with pytest.raises(FraudDetectedError):
        op.process_order(
            order_id="ORD127",
            user_data={
                "email": "user@example.com",
                "age": 30,
                "tier": "STANDARD",
                "payment_method": "PAYPAL",
            },
            items=[{"id": "item1", "qty": 1, "price": price}],
            promo_code=None,
        )


def test_process_order_crypto_low_amount(monkeypatch):
    monkeypatch.setattr(
        "data.input_code.d06_complex_logic.datetime",
        _dummy_datetime(12),
        raising=False,
    )
    wh = Warehouse({"item1": 5})
    op = OrderProcessor(wh)

    with pytest.raises(PaymentError):
        op.process_order(
            order_id="ORD128",
            user_data={
                "email": "user@example.com",
                "age": 30,
                "tier": "STANDARD",
                "payment_method": "CRYPTO",
            },
            items=[{"id": "item1", "qty": 1, "price": 40.0}],
            promo_code=None,
        )