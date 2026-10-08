import pytest
from data.input_code.d06_complex_logic import *

# ----------------------------------------------------------------------
# Fixtures
# ----------------------------------------------------------------------
@pytest.fixture(autouse=True)
def mock_datetime_now(monkeypatch):
    """Force datetime.now() to return a non‑night hour to avoid the night discount."""
    class FixedDatetime:
        @classmethod
        def now(cls):
            # hour 12 → no night‑owl discount
            return datetime(2020, 1, 1, 12, 0, 0)

    monkeypatch.setattr('data.input_code.d06_complex_logic.datetime', FixedDatetime)


# ----------------------------------------------------------------------
# OrderProcessor.validate_user
# ----------------------------------------------------------------------
@pytest.mark.parametrize(
    "email, age, exc",
    [
        ("test@example.com", 25, None),          # T1_VALID_USER
        ("invalid", 25, UserValidationError),    # T2_INVALID_EMAIL
        ("test@example.com", 17, UserValidationError),  # T3_UNDERAGE_USER
        ("test@example.com", 101, UserValidationError), # T4_OVER100_USER
    ],
)
def test_validate_user(email, age, exc):
    processor = OrderProcessor(Warehouse({}))
    if exc:
        with pytest.raises(exc):
            processor.validate_user(email, age)
    else:
        processor.validate_user(email, age)  # should not raise


# ----------------------------------------------------------------------
# Warehouse.check_stock
# ----------------------------------------------------------------------
@pytest.mark.parametrize(
    "stock, item_id, qty, expected, exc",
    [
        ({"item1": 10}, "item1", 5, True, None),   # T5_STOCK_CHECK_OK
        ({"item1": 10}, "item1", 15, False, None), # T6_STOCK_CHECK_FAIL
        ({"item1": 10}, "nonexistent", 1, None, InventoryError),  # T7_STOCK_CHECK_MISSING_ITEM
    ],
)
def test_warehouse_check_stock(stock, item_id, qty, expected, exc):
    wh = Warehouse(stock)
    if exc:
        with pytest.raises(exc):
            wh.check_stock(item_id, qty)
    else:
        assert wh.check_stock(item_id, qty) is expected


# ----------------------------------------------------------------------
# Warehouse.lock_item
# ----------------------------------------------------------------------
@pytest.mark.parametrize(
    "stock, item_id, qty, exc",
    [
        ({"item1": 10}, "item1", 5, None),          # T8_LOCK_ITEM_OK
        ({"item1": 10}, "item1", 15, InventoryError),  # T9_LOCK_ITEM_FAIL
    ],
)
def test_warehouse_lock_item(stock, item_id, qty, exc):
    wh = Warehouse(stock)
    if exc:
        with pytest.raises(exc):
            wh.lock_item(item_id, qty)
    else:
        wh.lock_item(item_id, qty)  # should succeed


# ----------------------------------------------------------------------
# DiscountEngine.calculate_discount
# ----------------------------------------------------------------------
@pytest.mark.parametrize(
    "total, tier, promo, expected",
    [
        (100.0, "STANDARD", None, 0.0),          # T10_DISCOUNT_STANDARD
        (100.0, "GOLD", None, 0.10),            # T11_DISCOUNT_GOLD
        (100.0, "PLATINUM", None, 0.20),        # T12_DISCOUNT_PLATINUM
        (1001.0, "PLATINUM", None, 0.25),       # T13_DISCOUNT_PLATINUM_HIGH_AMOUNT
        (100.0, "STANDARD", "ABC-123", 0.10),   # T14_PROMO_CODE_VALID
        (100.0, "STANDARD", "invalid", "ValueError"),  # T15_PROMO_CODE_INVALID
        (100.0, "STANDARD", "ABC-999", 50.0),   # T16_PROMO_CODE_SUPER (returns 50% of total amount)
    ],
)
def test_calculate_discount(total, tier, promo, expected):
    if expected == "ValueError":
        with pytest.raises(ValueError):
            DiscountEngine.calculate_discount(total, tier, promo)
    else:
        result = DiscountEngine.calculate_discount(total, tier, promo)
        assert result == expected


# ----------------------------------------------------------------------
# OrderProcessor.process_order – success and failure paths
# ----------------------------------------------------------------------
def test_process_order_success():
    # T17_PROCESS_ORDER_OK
    wh = Warehouse({"item1": 10})
    processor = OrderProcessor(wh)
    order = processor.process_order(
        order_id="1",
        user_data={"email": "test@example.com", "age": 25, "tier": "STANDARD"},
        items=[{"id": "item1", "qty": 1, "price": 10.0}],
    )
    assert order["status"] == "success"
    assert order["order_id"] == "1"
    assert order["original_price"] == 10.0
    assert order["discount_applied"] == 0.0
    assert order["items_count"] == 1


def test_process_order_out_of_stock():
    # T18_PROCESS_ORDER_OUT_OF_STOCK
    wh = Warehouse({"item1": 10})
    processor = OrderProcessor(wh)
    result = processor.process_order(
        order_id="1",
        user_data={"email": "test@example.com", "age": 25, "tier": "STANDARD"},
        items=[{"id": "item1", "qty": 15, "price": 10.0}],
    )
    assert result["status"] == "failed"
    assert "Out of stock" in result["reason"]


def test_process_order_invalid_promo():
    # T19_PROCESS_ORDER_INVALID_PROMO
    wh = Warehouse({"item1": 10})
    processor = OrderProcessor(wh)
    result = processor.process_order(
        order_id="1",
        user_data={"email": "test@example.com", "age": 25, "tier": "STANDARD"},
        items=[{"id": "item1", "qty": 1, "price": 10.0}],
        promo_code="invalid",
    )
    assert result["status"] == "error"
    assert "Promo Error" in result["reason"]


def test_process_order_paypal_fraud():
    # T20_PROCESS_ORDER_PAYPAL_FRAUD – force final price to 666.66
    wh = Warehouse({"item1": 10})
    processor = OrderProcessor(wh)
    # price chosen so that price * 1.22 rounds to 666.66
    price = 666.66 / 1.22  # ≈ 546.5901639344262
    with pytest.raises(FraudDetectedError):
        processor.process_order(
            order_id="1",
            user_data={
                "email": "test@example.com",
                "age": 25,
                "tier": "STANDARD",
                "payment_method": "PAYPAL",
            },
            items=[{"id": "item1", "qty": 1, "price": price}],
        )


def test_process_order_crypto_min_amount():
    # T21_PROCESS_ORDER_CRYPTO_MIN_AMOUNT – final price below 50 triggers PaymentError
    wh = Warehouse({"item1": 10})
    processor = OrderProcessor(wh)
    with pytest.raises(PaymentError):
        processor.process_order(
            order_id="1",
            user_data={
                "email": "test@example.com",
                "age": 25,
                "tier": "STANDARD",
                "payment_method": "CRYPTO",
            },
            items=[{"id": "item1", "qty": 1, "price": 10.0}],
        )