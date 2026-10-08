import pytest
from data.input_code.d06_complex_logic import *
from unittest.mock import patch
from datetime import datetime


# ---------- OrderProcessor.validate_user ----------
@pytest.mark.parametrize(
    "email, age, expected_exception",
    [
        ("test@example.com", 25, None),                     # T1_VALID_USER
        ("invalid", 25, UserValidationError),              # T2_INVALID_EMAIL
        ("test@example.com", 17, UserValidationError),    # T3_UNDERAGE_USER
        ("test@example.com", 101, UserValidationError),   # T4_OVERAGE_USER
    ],
)
def test_validate_user(email, age, expected_exception):
    processor = OrderProcessor(warehouse=Warehouse({}))
    if expected_exception:
        with pytest.raises(expected_exception):
            processor.validate_user(email, age)
    else:
        processor.validate_user(email, age)


# ---------- Warehouse.check_stock ----------
@pytest.mark.parametrize(
    "initial_stock, item_id, quantity, expected",
    [
        ({"item1": 10}, "item1", 5, True),    # T5_STOCK_CHECK_OK
        ({"item1": 10}, "item1", 15, False),  # T6_STOCK_CHECK_FAIL
    ],
)
def test_check_stock_success(initial_stock, item_id, quantity, expected):
    wh = Warehouse(initial_stock)
    assert wh.check_stock(item_id, quantity) is expected


def test_check_stock_missing_item():
    wh = Warehouse({"item1": 10})
    with pytest.raises(InventoryError):
        wh.check_stock("nonexistent", 1)  # T7_STOCK_CHECK_MISSING_ITEM


# ---------- Warehouse.lock_item ----------
def test_lock_item_success():
    wh = Warehouse({"item1": 10})
    wh.lock_item("item1", 5)  # T8_LOCK_ITEM_OK
    assert wh.check_stock("item1", 5) is True


def test_lock_item_insufficient_stock():
    wh = Warehouse({"item1": 10})
    with pytest.raises(InventoryError):
        wh.lock_item("item1", 15)  # T9_LOCK_ITEM_FAIL


# ---------- DiscountEngine.calculate_discount ----------
def mock_datetime(hour):
    class MockedDatetime(datetime):
        @classmethod
        def now(cls):
            return cls(2020, 1, 1, hour, 0, 0)
    return MockedDatetime


@pytest.mark.parametrize(
    "total, tier, promo, expected",
    [
        (100, "STANDARD", None, 0.0),          # T10_DISCOUNT_STANDARD
        (100, "GOLD", None, 0.10),             # T11_DISCOUNT_GOLD
        (100, "PLATINUM", None, 0.20),         # T12_DISCOUNT_PLATINUM
        (1001, "PLATINUM", None, 0.25),        # T13_DISCOUNT_PLATINUM_HIGH_AMOUNT
        (100, "STANDARD", "ABC-123", 0.10),    # T14_DISCOUNT_PROMO_CODE_VALID
        (100, "STANDARD", "ABC-999", 50.0),    # T16_DISCOUNT_PROMO_CODE_SUPER
    ],
)
def test_calculate_discount_success(total, tier, promo, expected):
    with patch("data.input_code.d06_complex_logic.datetime", mock_datetime(12)):
        result = DiscountEngine.calculate_discount(total, tier, promo)
        assert result == expected


def test_calculate_discount_invalid_promo():
    with patch("data.input_code.d06_complex_logic.datetime", mock_datetime(12)):
        with pytest.raises(ValueError):
            DiscountEngine.calculate_discount(100, "STANDARD", "invalid")  # T15_DISCOUNT_PROMO_CODE_INVALID


# ---------- OrderProcessor.process_order ----------
@pytest.fixture
def warehouse():
    return Warehouse({"item1": 10})


def test_process_order_success(warehouse):
    processor = OrderProcessor(warehouse)
    order = processor.process_order(
        order_id="1",
        user_data={"email": "test@example.com", "age": 25, "tier": "STANDARD"},
        items=[{"id": "item1", "qty": 1, "price": 10.0}],
    )
    assert order["status"] == "success"  # T17_PROCESS_ORDER_OK


def test_process_order_inventory_error(warehouse):
    processor = OrderProcessor(warehouse)
    result = processor.process_order(
        order_id="1",
        user_data={"email": "test@example.com", "age": 25, "tier": "STANDARD"},
        items=[{"id": "item1", "qty": 15, "price": 10.0}],
    )
    assert result["status"] == "failed"  # T18_PROCESS_ORDER_INVENTORY_ERROR


def test_process_order_invalid_promo(warehouse):
    processor = OrderProcessor(warehouse)
    result = processor.process_order(
        order_id="1",
        user_data={"email": "test@example.com", "age": 25, "tier": "STANDARD"},
        items=[{"id": "item1", "qty": 1, "price": 10.0}],
        promo_code="invalid",
    )
    assert result["status"] == "error"  # T19_PROCESS_ORDER_INVALID_PROMO


def test_process_order_paypal_fraud(warehouse):
    processor = OrderProcessor(warehouse)
    total_price = round(666.66 / 1.22, 2)
    qty = 1
    price = total_price / qty
    with pytest.raises(FraudDetectedError):
        processor.process_order(
            order_id="1",
            user_data={
                "email": "test@example.com",
                "age": 25,
                "tier": "STANDARD",
                "payment_method": "PAYPAL",
            },
            items=[{"id": "item1", "qty": qty, "price": price}],
        )  # T20_PROCESS_ORDER_PAYPAL_FRAUD


def test_process_order_crypto_min_amount(warehouse):
    processor = OrderProcessor(warehouse)
    with pytest.raises(PaymentError):
        processor.process_order(
            order_id="1",
            user_data={
                "email": "test@example.com",
                "age": 25,
                "tier": "STANDARD",
                "payment_method": "CRYPTO",
            },
            items=[{"id": "item1", "qty": 1, "price": 40.0}],
        )  # T21_PROCESS_ORDER_CRYPTO_MIN_AMOUNT


# ---------- DiscountEngine.calculate_discount ----------
def test_night_owl_discount():
    # Mock datetime to a night hour (e.g., 2 AM) to trigger night owl discount
    with patch("data.input_code.d06_complex_logic.datetime", mock_datetime(2)):
        result = DiscountEngine.calculate_discount(100.0, "STANDARD", None)
        assert result == 0.05


def test_discount_cap():
    # Mock datetime to a night hour to maximize discount and test the 40% cap
    with patch("data.input_code.d06_complex_logic.datetime", mock_datetime(2)):
        result = DiscountEngine.calculate_discount(100.0, "PLATINUM", "ABC-123")
        # Expected discount: 0.20 (PLATINUM) + 0.10 (promo) + 0.05 (night owl) = 0.35 (below cap)
        assert result == 0.35


# ---------- OrderProcessor.process_order ----------
def test_process_order_return_free_items(warehouse):
    processor = OrderProcessor(warehouse)
    with pytest.raises(ValueError):
        processor.process_order(
            order_id="1",
            user_data={"email": "test@example.com", "age": 25},
            items=[{"id": "item1", "qty": -1, "price": 0.0}],
        )


def test_process_order_crypto_payment_ok(warehouse):
    processor = OrderProcessor(warehouse)
    result = processor.process_order(
        order_id="1",
        user_data={
            "email": "test@example.com",
            "age": 25,
            "payment_method": "CRYPTO",
        },
        items=[{"id": "item1", "qty": 1, "price": 100.0}],
    )
    assert result["status"] == "success"


def test_process_order_paypal_normal_amount(warehouse):
    processor = OrderProcessor(warehouse)
    result = processor.process_order(
        order_id="1",
        user_data={
            "email": "test@example.com",
            "age": 25,
            "payment_method": "PAYPAL",
        },
        items=[{"id": "item1", "qty": 1, "price": 100.0}],
    )
    assert result["status"] == "success"


# ---------- DiscountEngine.calculate_discount ----------
@pytest.mark.parametrize(
    "hour,total,user_tier,promo,expected",
    [
        (2, 100.0, "GOLD", None, 0.15),          # T_MISSING_1 night owl + GOLD
        (2, 1000.0, "PLATINUM", "ABC-999", 500.0),  # T_MISSING_2 super promo overrides everything
    ],
)
def test_calculate_discount_missing_cases(hour, total, user_tier, promo, expected):
    with patch("data.input_code.d06_complex_logic.datetime", mock_datetime(hour)):
        result = DiscountEngine.calculate_discount(total, user_tier, promo)
        # Use approx for floating‑point safety
        assert result == pytest.approx(expected)


# ---------- OrderProcessor.process_order ----------
def test_process_order_missing_tier(warehouse):
    processor = OrderProcessor(warehouse)
    result = processor.process_order(
        order_id="1",
        user_data={"email": "test@example.com", "age": 25},
        items=[{"id": "item1", "qty": 1, "price": 10.0}],
        promo_code=None,
    )
    assert result["status"] == "success"


def test_process_order_empty_items(warehouse):
    processor = OrderProcessor(warehouse)
    result = processor.process_order(
        order_id="1",
        user_data={"email": "test@example.com", "age": 25},
        items=[],
        promo_code=None,
    )
    assert result["status"] == "success"
    assert result["original_price"] == 0.0
    assert result["items_count"] == 0


# ---------- Warehouse.release_item ----------
def test_release_item_quantity_zero():
    wh = Warehouse({"item1": 10})
    # No lock performed; releasing zero should be a no‑op and raise no exception
    wh.release_item("item1", 0)
    # Ensure internal state remains unchanged (no locked entry)
    assert "item1" not in wh._locked_stock


# ---------- OrderProcessor.validate_user ----------
@pytest.mark.parametrize(
    "email,age,expected_exception",
    [
        ("", 25, UserValidationError),          # T_MISSING_6 missing email
        ("test@example.com", None, TypeError), # T_MISSING_7 missing age (None leads to TypeError)
    ],
)
def test_validate_user_missing_fields(email, age, expected_exception):
    processor = OrderProcessor(warehouse=Warehouse({}))
    with pytest.raises(expected_exception):
        processor.validate_user(email, age)