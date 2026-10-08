import pytest
from data.input_code.d06_complex_logic import *
import datetime as dt


def _mock_datetime_now(monkeypatch, hour):
    """Helper to mock datetime.now() used in the source module."""
    class MockDateTime:
        @staticmethod
        def now():
            return dt.datetime(2020, 1, 1, hour)

    # Patch the `datetime` name inside the source module
    monkeypatch.setattr(
        "data.input_code.d06_complex_logic.datetime", MockDateTime, raising=False
    )


# ---------- Warehouse Tests ----------
@pytest.mark.parametrize(
    "initial_stock,item_id,quantity,expected",
    [
        ({"item1": 10}, "item1", 5, True),
    ],
)
def test_warehouse_check_stock_success(initial_stock, item_id, quantity, expected):
    wh = Warehouse(initial_stock)
    assert wh.check_stock(item_id, quantity) == expected


def test_warehouse_check_stock_not_found():
    wh = Warehouse({"item1": 10})
    with pytest.raises(InventoryError):
        wh.check_stock("missing_item", 1)


def test_warehouse_lock_insufficient():
    wh = Warehouse({"item1": 3})
    with pytest.raises(InventoryError):
        wh.lock_item("item1", 5)


def test_warehouse_lock_and_release():
    wh = Warehouse({"item1": 10})
    wh.lock_item("item1", 4)
    # after lock, stock should be sufficient for remaining 6
    assert wh.check_stock("item1", 6) is True
    wh.release_item("item1", 4)
    # after release, full stock should be available again
    assert wh.check_stock("item1", 10) is True


# ---------- DiscountEngine Tests ----------
@pytest.mark.parametrize(
    "mock_hour,total_amount,user_tier,promo_code,expected",
    [
        (2, 100.0, "GOLD", None, 0.15000000000000002),          # night + GOLD (float precision)
        (12, 1500.0, "PLATINUM", None, 0.25),                 # PLATINUM + >1000
        (12, 200.0, "STANDARD", "ABC-123", 0.10),             # valid promo
        (12, 300.0, "STANDARD", "XYZ-999", 150.0),            # super promo returns price*0.5
        (12, 100.0, "STANDARD", "badcode", "ValueError"),    # invalid promo
        (3, 2000.0, "PLATINUM", "ABC-123", 0.40),             # cap at 40%
    ],
)
def test_discount_engine(
    mock_hour, total_amount, user_tier, promo_code, expected, monkeypatch
):
    _mock_datetime_now(monkeypatch, mock_hour)
    if isinstance(expected, str) and expected == "ValueError":
        with pytest.raises(ValueError):
            DiscountEngine.calculate_discount(total_amount, user_tier, promo_code)
    else:
        result = DiscountEngine.calculate_discount(total_amount, user_tier, promo_code)
        assert result == expected


# ---------- OrderProcessor User Validation ----------
@pytest.mark.parametrize(
    "email,age,expected_exception",
    [
        ("elder@example.com", 101, UserValidationError),
        ("bademail@", 30, UserValidationError),
    ],
)
def test_validate_user_errors(email, age, expected_exception):
    op = OrderProcessor(Warehouse({}))
    with pytest.raises(expected_exception):
        op.validate_user(email, age)


# ---------- OrderProcessor Process Order Tests ----------
def test_process_order_success_cc(monkeypatch):
    wh = Warehouse({"item1": 10})
    op = OrderProcessor(wh)
    _mock_datetime_now(monkeypatch, 12)

    result = op.process_order(
        order_id="ORD001",
        user_data={
            "email": "user@example.com",
            "age": 30,
            "tier": "GOLD",
            "payment_method": "CC",
        },
        items=[{"id": "item1", "qty": 2, "price": 100.0}],
        promo_code=None,
    )
    assert result == {
        "status": "success",
        "order_id": "ORD001",
        "original_price": 200.0,
        "discount_applied": 0.1,
        "final_total": 219.6,
        "items_count": 1,
    }


def test_process_order_inventory_failure(monkeypatch):
    wh = Warehouse({"itemX": 2})
    op = OrderProcessor(wh)
    _mock_datetime_now(monkeypatch, 12)

    result = op.process_order(
        order_id="ORD002",
        user_data={
            "email": "buyer@test.com",
            "age": 25,
            "tier": "STANDARD",
            "payment_method": "CC",
        },
        items=[{"id": "itemX", "qty": 5, "price": 20.0}],
        promo_code=None,
    )
    assert result["status"] == "failed"
    assert "Out of stock" in result["reason"]


def test_process_order_invalid_promo_error(monkeypatch):
    wh = Warehouse({"item1": 10})
    op = OrderProcessor(wh)
    _mock_datetime_now(monkeypatch, 12)

    result = op.process_order(
        order_id="ORD003",
        user_data={
            "email": "shopper@test.com",
            "age": 40,
            "tier": "STANDARD",
            "payment_method": "CC",
        },
        items=[{"id": "item1", "qty": 1, "price": 50.0}],
        promo_code="WRONG-12",
    )
    assert result["status"] == "error"
    assert "Promo Error" in result["reason"]


def test_process_order_super_promo(monkeypatch):
    wh = Warehouse({"item2": 5})
    op = OrderProcessor(wh)
    _mock_datetime_now(monkeypatch, 12)

    result = op.process_order(
        order_id="ORD004",
        user_data={
            "email": "vip@example.com",
            "age": 45,
            "tier": "PLATINUM",
            "payment_method": "CC",
        },
        items=[{"id": "item2", "qty": 2, "price": 150.0}],
        promo_code="XYZ-999",
    )
    # DiscountEngine returns 150.0 (price * 0.5) for this promo
    assert result["status"] == "success"
    assert result["order_id"] == "ORD004"
    assert result["original_price"] == 300.0
    assert result["discount_applied"] == 150.0
    # final total = (300 * (1-150.0)) * 1.22 = -54534.0
    assert result["final_total"] == -54534.0
    assert result["items_count"] == 1


def test_process_order_fraud_detected_error(monkeypatch):
    wh = Warehouse({"item3": 10})
    op = OrderProcessor(wh)
    # Adjust tax_rate so that final amount equals 666.66
    op.tax_rate = (666.66 / 546.44) - 1  # approx 0.219999...
    _mock_datetime_now(monkeypatch, 12)

    with pytest.raises(FraudDetectedError):
        op.process_order(
            order_id="ORD005",
            user_data={
                "email": "fraud@test.com",
                "age": 35,
                "tier": "STANDARD",
                "payment_method": "PAYPAL",
            },
            items=[{"id": "item3", "qty": 1, "price": 546.44}],
            promo_code=None,
        )


def test_process_order_crypto_low_amount(monkeypatch):
    wh = Warehouse({"item4": 5})
    op = OrderProcessor(wh)
    _mock_datetime_now(monkeypatch, 12)

    with pytest.raises(PaymentError):
        op.process_order(
            order_id="ORD006",
            user_data={
                "email": "crypto@test.com",
                "age": 28,
                "tier": "STANDARD",
                "payment_method": "CRYPTO",
            },
            items=[{"id": "item4", "qty": 1, "price": 30.0}],
            promo_code=None,
        )


def test_process_order_user_validation_error(monkeypatch):
    wh = Warehouse({"item5": 10})
    op = OrderProcessor(wh)
    _mock_datetime_now(monkeypatch, 12)

    with pytest.raises(UserValidationError):
        op.process_order(
            order_id="ORD007",
            user_data={
                "email": "invalid-email",
                "age": 25,
                "tier": "STANDARD",
                "payment_method": "CC",
            },
            items=[{"id": "item5", "qty": 1, "price": 100.0}],
            promo_code=None,
        )