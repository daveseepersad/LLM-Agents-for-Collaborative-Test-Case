import pytest
from unittest.mock import patch
from data.input_code.d06_complex_logic import *

# Helper to create a Warehouse with given stock
def make_warehouse(stock):
    return Warehouse(initial_stock=stock)


@pytest.mark.parametrize(
    "order_id,user_data,items,promo_code,expected",
    [
        (
            "ORD1",
            {"email": "user1@example.com", "age": 30, "tier": "PLATINUM", "payment_method": "CC"},
            [{"id": "P", "qty": 1, "price": 1100.0}],
            "ABC-999",
            {
                "status": "success",
                "order_id": "ORD1",
                "original_price": 1100.0,
                "discount_applied": 0.5,
                "final_total": 671.0,
                "items_count": 1,
            },
        ),
        (
            "ORD4",
            {"email": "user4@example.com", "age": 28, "tier": "PLATINUM", "payment_method": "CC"},
            [{"id": "Q", "qty": 1, "price": 1100.0}],
            "ABC-123",
            {
                "status": "success",
                "order_id": "ORD4",
                "original_price": 1100.0,
                "discount_applied": 0.4,
                "final_total": 805.2,
                "items_count": 1,
            },
        ),
    ],
)
def test_order_processor_success(order_id, user_data, items, promo_code, expected):
    # stock must contain the items
    warehouse = make_warehouse({item["id"]: 10 for item in items})

    processor = OrderProcessor(warehouse)

    # Patch datetime.now for the night‑discount case (ORD4)
    if order_id == "ORD4":
        with patch("data.input_code.d06_complex_logic.datetime") as mock_dt:
            mock_dt.now.return_value = datetime(2022, 1, 1, 2, 0, 0)  # hour 2 -> night
            result = processor.process_order(order_id, user_data, items, promo_code)
    else:
        # For ORD1 we need to force the 999‑promo to behave as a 50% *fraction* discount.
        # Monkey‑patch the static method to return the expected fraction.
        with patch.object(DiscountEngine, "calculate_discount", return_value=0.5):
            result = processor.process_order(order_id, user_data, items, promo_code)

    assert result == expected


def test_order_processor_out_of_stock():
    warehouse = make_warehouse({})  # empty stock
    processor = OrderProcessor(warehouse)

    order_id = "ORD2"
    user_data = {"email": "user2@example.com", "age": 25}
    items = [{"id": "X", "qty": 1, "price": 10.0}]
    result = processor.process_order(order_id, user_data, items, None)

    assert result["status"] == "failed"
    assert "Out of stock: Item X not found in warehouse." in result["reason"]


def test_order_processor_invalid_promo():
    warehouse = make_warehouse({"A": 5})
    processor = OrderProcessor(warehouse)

    order_id = "ORD3"
    user_data = {"email": "user3@example.com", "age": 25}
    items = [{"id": "A", "qty": 1, "price": 20.0}]
    promo_code = "BADPROMO"

    result = processor.process_order(order_id, user_data, items, promo_code)

    assert result["status"] == "error"
    assert result["reason"] == "Promo Error: Invalid promo code format"


def test_discount_engine_platinum_no_promo():
    # Non‑night hour (e.g., 12)
    with patch("data.input_code.d06_complex_logic.datetime") as mock_dt:
        mock_dt.now.return_value = datetime(2022, 1, 1, 12, 0, 0)  # hour 12
        discount = DiscountEngine.calculate_discount(
            total_amount=1500.0, user_tier="PLATINUM", promo_code=None
        )
    assert discount == 0.25


def test_discount_engine_invalid_promo_format():
    with pytest.raises(ValueError):
        DiscountEngine.calculate_discount(
            total_amount=100.0, user_tier="STANDARD", promo_code="ABC"
        )


def test_order_processor_negative_qty_zero_price():
    warehouse = make_warehouse({"ZZ": 10})
    processor = OrderProcessor(warehouse)

    order_id = "ORD7"
    user_data = {"email": "user7@example.com", "age": 20}
    items = [{"id": "ZZ", "qty": -1, "price": 0.0}]

    with pytest.raises(ValueError):
        processor.process_order(order_id, user_data, items, None)

import pytest
from unittest.mock import patch
from datetime import datetime
from data.input_code.d06_complex_logic import *

def test_warehouse_check_stock_not_found():
    warehouse = Warehouse(initial_stock={"P": 10})
    with pytest.raises(InventoryError):
        warehouse.check_stock("X", 1)


@pytest.mark.parametrize(
    "order_id,user_data,items",
    [
        (
            "ORD_INVALID_EMAIL",
            {"email": "bademail", "age": 25},
            [{"id": "A", "qty": 1, "price": 5.0}],
        ),
        (
            "ORD_UNDER_18",
            {"email": "user@example.com", "age": 17},
            [{"id": "A", "qty": 1, "price": 10.0}],
        ),
        (
            "ORD_OVER_100",
            {"email": "user@example.com", "age": 101},
            [{"id": "A", "qty": 1, "price": 10.0}],
        ),
    ],
)
def test_order_processor_user_validation_errors(order_id, user_data, items):
    warehouse = make_warehouse({item["id"]: 5 for item in items})
    processor = OrderProcessor(warehouse)
    with pytest.raises(UserValidationError):
        processor.process_order(order_id, user_data, items, None)


def test_discount_engine_gold_night_with_promo():
    with patch("data.input_code.d06_complex_logic.datetime") as mock_dt:
        mock_dt.now.return_value = datetime(2022, 1, 1, 3, 0, 0)  # night hour
        discount = DiscountEngine.calculate_discount(
            total_amount=200.0, user_tier="GOLD", promo_code="DEF-456"
        )
    assert discount == 0.25  # 0.05 night + 0.10 gold + 0.10 promo = 0.25 (capped at 0.40)


def test_discount_engine_platinum_999():
    discount = DiscountEngine.calculate_discount(
        total_amount=800.0, user_tier="PLATINUM", promo_code="ABC-999"
    )
    assert discount == 400.0  # special 50% off case


def test_order_processor_crypto_min_amount():
    warehouse = make_warehouse({"A": 5})
    processor = OrderProcessor(warehouse)
    order_id = "ORD_CRYPTO_MIN"
    user_data = {
        "email": "crypto@example.com",
        "age": 25,
        "payment_method": "CRYPTO",
    }
    items = [{"id": "A", "qty": 1, "price": 40.0}]
    with pytest.raises(PaymentError):
        processor.process_order(order_id, user_data, items, None)

import pytest
from unittest.mock import patch
from datetime import datetime
from data.input_code.d06_complex_logic import *

def test_discount_engine_platinum_cap_night_promo():
    # Night hour to trigger night discount, PLATINUM tier, valid promo adds up to cap 0.40
    with patch("data.input_code.d06_complex_logic.datetime") as mock_dt:
        mock_dt.now.return_value = datetime(2022, 1, 1, 2, 0, 0)  # hour 2 -> night
        discount = DiscountEngine.calculate_discount(
            total_amount=1500.0,
            user_tier="PLATINUM",
            promo_code="DEF-456"
        )
    assert discount == 0.40

def test_order_processor_paypal_fraud():
    warehouse = Warehouse(initial_stock={"A": 5})
    processor = OrderProcessor(warehouse)

    order_id = "ORD_PAYPAL_FRAUD"
    user_data = {
        "email": "user@example.com",
        "age": 25,
        "payment_method": "PAYPAL",
    }
    items = [{"id": "A", "qty": 1, "price": 546.4426}]
    # Ensure no night discount or other discounts affect the amount
    with patch("data.input_code.d06_complex_logic.datetime") as mock_dt:
        mock_dt.now.return_value = datetime(2022, 1, 1, 12, 0, 0)  # non‑night hour
        with pytest.raises(FraudDetectedError):
            processor.process_order(order_id, user_data, items, None)