import pytest
from unittest.mock import patch
from datetime import datetime
from data.input_code.d06_complex_logic import *

# ----------------------------------------------------------------------
# Fixture to neutralize time‑dependent logic in DiscountEngine
# ----------------------------------------------------------------------
@pytest.fixture(autouse=True)
def mock_datetime_now():
    """Patch datetime.now() used inside the module to return a fixed hour (12)."""
    with patch('data.input_code.d06_complex_logic.datetime') as mock_dt:
        mock_dt.now.return_value = datetime(2022, 1, 1, 12, 0, 0)
        # Preserve the original datetime constructor for any other uses
        mock_dt.side_effect = lambda *args, **kw: datetime(*args, **kw)
        yield

# ----------------------------------------------------------------------
# DiscountEngine tests
# ----------------------------------------------------------------------
@pytest.mark.parametrize(
    "total_amount,user_tier,promo_code,expected",
    [
        (1500.0, "PLATINUM", None, 0.25),               # D1
        (300.0, "STANDARD", "ABC-999", 150.0),          # D2 (50% off)
        (500.0, "GOLD", "ABC-123", 0.20),               # D3
        (100.0, "STANDARD", "BADCODE", "ValueError"),  # D4
        (0.0, "STANDARD", None, 0.0),                  # D5
        (1200.0, "PLATINUM", "PROMO-000", "ValueError"),# D6 (invalid promo code)
    ]
)
def test_discount_engine(total_amount, user_tier, promo_code, expected):
    if isinstance(expected, str) and expected == "ValueError":
        with pytest.raises(ValueError):
            DiscountEngine.calculate_discount(total_amount, user_tier, promo_code)
    else:
        result = DiscountEngine.calculate_discount(total_amount, user_tier, promo_code)
        assert result == expected

# ----------------------------------------------------------------------
# OrderProcessor.validate_user tests
# ----------------------------------------------------------------------
@pytest.mark.parametrize(
    "email,age,expect_exception",
    [
        ("u@example.com", 25, None),                     # V1 – valid
        ("", 25, UserValidationError),                  # V2 – invalid email
        ("test@example.com", 17, UserValidationError),  # V3 – underage
        ("test@example.com", 101, UserValidationError), # V4 – over 100
    ]
)
def test_validate_user(email, age, expect_exception):
    processor = OrderProcessor(warehouse=Warehouse({}))
    if expect_exception:
        with pytest.raises(expect_exception):
            processor.validate_user(email, age)
    else:
        # Should not raise any exception
        processor.validate_user(email, age)

# ----------------------------------------------------------------------
# OrderProcessor.process_order test (crypto payment below threshold)
# ----------------------------------------------------------------------
def test_process_order_crypto_payment_error():
    # Warehouse with enough stock for the item
    warehouse = Warehouse(initial_stock={"ITEMX": 5})
    processor = OrderProcessor(warehouse=warehouse)

    order_id = "ORD-CRYPTO-FAIL"
    user_data = {
        "email": "buyer@example.com",
        "age": 28,
        "payment_method": "CRYPTO",
        "tier": "STANDARD"
    }
    items = [{"id": "ITEMX", "qty": 1, "price": 10.0}]
    promo_code = None

    with pytest.raises(PaymentError):
        processor.process_order(order_id, user_data, items, promo_code)

def test_warehouse_check_stock_missing_item():
    wh = Warehouse(initial_stock={"X": 1})
    with pytest.raises(InventoryError) as exc:
        wh.check_stock("Y", 1)
    assert "Item Y not found in warehouse." in str(exc.value)


def test_process_order_success_cc():
    warehouse = Warehouse(initial_stock={"A": 10, "B": 5})
    processor = OrderProcessor(warehouse=warehouse)

    order_id = "ORD-TEST-01"
    user_data = {
        "email": "customer@example.com",
        "age": 30,
        "payment_method": "CC",
        "tier": "STANDARD",
    }
    items = [
        {"id": "A", "qty": 2, "price": 20.0},
        {"id": "B", "qty": 1, "price": 15.0},
    ]

    result = processor.process_order(order_id, user_data, items, promo_code=None)

    assert result == {
        "status": "success",
        "order_id": "ORD-TEST-01",
        "original_price": 55.0,
        "discount_applied": 0.0,
        "final_total": 67.1,
        "items_count": 2,
    }


def test_process_order_invalid_promo():
    warehouse = Warehouse(initial_stock={"A": 2})
    processor = OrderProcessor(warehouse=warehouse)

    order_id = "ORD-TEST-02"
    user_data = {
        "email": "customer2@example.com",
        "age": 25,
        "payment_method": "CC",
        "tier": "STANDARD",
    }
    items = [{"id": "A", "qty": 1, "price": 10.0}]
    promo_code = "BADPROMO"

    result = processor.process_order(order_id, user_data, items, promo_code)

    assert result["status"] == "error"
    assert result["reason"] == "Promo Error: Invalid promo code format"


def test_process_order_inventory_not_found():
    warehouse = Warehouse(initial_stock={"ITEMX": 5})
    processor = OrderProcessor(warehouse=warehouse)

    order_id = "ORD-TEST-03"
    user_data = {
        "email": "a@example.com",
        "age": 22,
        "payment_method": "CC",
        "tier": "STANDARD",
    }
    items = [{"id": "ITEM_NOT_FOUND", "qty": 1, "price": 5.0}]

    result = processor.process_order(order_id, user_data, items, promo_code=None)

    assert result["status"] == "failed"
    assert result["reason"] == "Out of stock: Item ITEM_NOT_FOUND not found in warehouse."


def test_process_order_partial_rollback():
    warehouse = Warehouse(initial_stock={"A": 2, "B": 0})
    processor = OrderProcessor(warehouse=warehouse)

    order_id = "ORD-TEST-04"
    user_data = {
        "email": "user@example.com",
        "age": 28,
        "payment_method": "CC",
        "tier": "STANDARD",
    }
    items = [
        {"id": "A", "qty": 2, "price": 3.0},
        {"id": "B", "qty": 1, "price": 10.0},
    ]

    result = processor.process_order(order_id, user_data, items, promo_code=None)

    assert result["status"] == "failed"
    assert result["reason"] == "Out of stock: Insufficient stock for B"

import pytest
from unittest.mock import patch
from datetime import datetime
from data.input_code.d06_complex_logic import DiscountEngine, Warehouse, InventoryError

# ----------------------------------------------------------------------
# DiscountEngine night discount tests for GOLD tier
# ----------------------------------------------------------------------
@pytest.mark.parametrize(
    "total_amount,user_tier,promo_code,expected",
    [
        (100.0, "GOLD", None, 0.15000000000000002),          # night (0.05) + gold (0.10)
        (100.0, "GOLD", "ABC-123", 0.25),    # night + gold + promo (0.10)
    ],
)
def test_discount_engine_night_gold(total_amount, user_tier, promo_code, expected):
    # Mock datetime to a night hour (e.g., 02:00)
    with patch("data.input_code.d06_complex_logic.datetime") as mock_dt:
        mock_dt.now.return_value = datetime(2022, 1, 1, 2, 0, 0)
        # Preserve normal datetime construction for any other uses
        mock_dt.side_effect = lambda *args, **kw: datetime(*args, **kw)

        result = DiscountEngine.calculate_discount(total_amount, user_tier, promo_code)
        assert result == expected


# ----------------------------------------------------------------------
# Warehouse.lock_item insufficient stock test
# ----------------------------------------------------------------------
def test_warehouse_lock_insufficient_stock():
    warehouse = Warehouse(initial_stock={"ITEM": 1})
    with pytest.raises(InventoryError):
        warehouse.lock_item("ITEM", 2)

import pytest
from unittest.mock import patch
from datetime import datetime
from data.input_code.d06_complex_logic import DiscountEngine

@pytest.mark.parametrize(
    "total_amount,user_tier,promo_code,expected",
    [
        (800.0, "PLATINUM", None, 0.25),          # T_MISSING_PLAT_NIGHT_NO_PROMO
        (800.0, "PLATINUM", "ABC-123", 0.35),    # T_MISSING_PLAT_NIGHT_WITH_PROMO
        (2000.0, "PLATINUM", "ABC-999", 1000.0), # T_MISSING_PLAT_NIGHT_WITH_999 (50% off returns amount)
        (1500.0, "PLATINUM", "ABC-123", 0.40),   # T_MISSING_PLAT_NIGHT_CAP
    ],
)
def test_discount_engine_night_platinum_cases(total_amount, user_tier, promo_code, expected):
    # Mock datetime to a night hour (e.g., 02:00) to trigger the night discount
    with patch("data.input_code.d06_complex_logic.datetime") as mock_dt:
        mock_dt.now.return_value = datetime(2022, 1, 1, 2, 0, 0)
        # Preserve normal datetime construction for any other uses
        mock_dt.side_effect = lambda *args, **kw: datetime(*args, **kw)

        result = DiscountEngine.calculate_discount(total_amount, user_tier, promo_code)
        assert result == expected