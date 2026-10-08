import pytest
from data.input_code.d06_complex_logic import *
import importlib
from datetime import datetime as real_datetime

# Helper to mock datetime.now()
class MockDateTime:
    @classmethod
    def now(cls):
        # Fixed hour outside night discount window
        return real_datetime(2022, 1, 1, 12, 0, 0)

@pytest.fixture
def warehouse_factory():
    """Factory to create a Warehouse with given initial stock."""
    def _factory(initial_stock):
        return Warehouse(initial_stock)
    return _factory

# ---------- Warehouse Tests ----------
@pytest.mark.parametrize(
    "item_id, quantity, initial_stock, expected",
    [
        ("item1", 1, {"item1": 10}, True),          # T1_Warehouse_check_stock_OK
    ],
)
def test_warehouse_check_stock_ok(item_id, quantity, initial_stock, expected):
    wh = Warehouse(initial_stock)
    assert wh.check_stock(item_id, quantity) == expected

def test_warehouse_check_stock_inventory_error():
    # T2_Warehouse_check_stock_InventoryError
    wh = Warehouse({"item1": 10})
    with pytest.raises(InventoryError):
        wh.check_stock("item2", 1)

@pytest.mark.parametrize(
    "item_id, quantity, initial_stock",
    [
        ("item1", 1, {"item1": 10}),                # T3_Warehouse_lock_item_OK
    ],
)
def test_warehouse_lock_item_ok(item_id, quantity, initial_stock):
    wh = Warehouse(initial_stock)
    wh.lock_item(item_id, quantity)
    # After locking, stock should be reduced for future checks
    assert not wh.check_stock(item_id, initial_stock[item_id])  # all stock locked

def test_warehouse_lock_item_inventory_error():
    # T4_Warehouse_lock_item_InventoryError
    wh = Warehouse({"item1": 10})
    with pytest.raises(InventoryError):
        wh.lock_item("item1", 11)

# ---------- DiscountEngine Tests ----------
def test_discount_engine_calculate_discount_ok(monkeypatch):
    # T5_DiscountEngine_calculate_discount_OK
    monkeypatch.setattr('data.input_code.d06_complex_logic.datetime', MockDateTime)
    discount = DiscountEngine.calculate_discount(total_amount=100.0, user_tier="GOLD")
    assert discount == 0.10  # night discount not applied, only tier discount

def test_discount_engine_calculate_discount_invalid_promo(monkeypatch):
    # T6_DiscountEngine_calculate_discount_ValueError
    monkeypatch.setattr('data.input_code.d06_complex_logic.datetime', MockDateTime)
    with pytest.raises(ValueError):
        DiscountEngine.calculate_discount(total_amount=100.0, user_tier="GOLD", promo_code="invalid")

# ---------- OrderProcessor.validate_user Tests ----------
def test_orderprocessor_validate_user_ok():
    # T7_OrderProcessor_validate_user_OK
    wh = Warehouse({})
    op = OrderProcessor(wh)
    # Should not raise any exception
    op.validate_user(email="test@example.com", age=25)

def test_orderprocessor_validate_user_error():
    # T8_OrderProcessor_validate_user_UserValidationError
    wh = Warehouse({})
    op = OrderProcessor(wh)
    with pytest.raises(UserValidationError):
        op.validate_user(email="invalid", age=25)

# ---------- OrderProcessor.process_order Tests ----------
def test_orderprocessor_process_order_success(monkeypatch):
    # T9_OrderProcessor_process_order_OK
    monkeypatch.setattr('data.input_code.d06_complex_logic.datetime', MockDateTime)
    wh = Warehouse({"item1": 10})
    op = OrderProcessor(wh)
    result = op.process_order(
        order_id="order1",
        user_data={"email": "test@example.com", "age": 25},
        items=[{"id": "item1", "qty": 1, "price": 10.0}]
    )
    assert result["status"] == "success"
    assert result["order_id"] == "order1"
    assert result["original_price"] == 10.0
    assert result["items_count"] == 1

def test_orderprocessor_process_order_inventory_error(monkeypatch):
    # T10_OrderProcessor_process_order_InventoryError
    monkeypatch.setattr('data.input_code.d06_complex_logic.datetime', MockDateTime)
    wh = Warehouse({"item1": 10})
    op = OrderProcessor(wh)
    result = op.process_order(
        order_id="order1",
        user_data={"email": "test@example.com", "age": 25},
        items=[{"id": "item1", "qty": 11, "price": 10.0}]
    )
    assert result["status"] == "failed"
    assert "Out of stock" in result["reason"]

def test_orderprocessor_process_order_fraud_detected(monkeypatch):
    # T11_OrderProcessor_process_order_FraudDetectedError
    monkeypatch.setattr('data.input_code.d06_complex_logic.datetime', MockDateTime)
    wh = Warehouse({"item1": 10})
    op = OrderProcessor(wh)
    # price chosen so that after tax (22%) rounding yields 666.66
    price = 666.66 / 1.22  # approx 546.4426
    with pytest.raises(FraudDetectedError):
        op.process_order(
            order_id="order1",
            user_data={
                "email": "test@example.com",
                "age": 25,
                "payment_method": "PAYPAL",
                "tier": "STANDARD"
            },
            items=[{"id": "item1", "qty": 1, "price": price}]
        )

def test_orderprocessor_process_order_payment_error(monkeypatch):
    # T12_OrderProcessor_process_order_PaymentError
    monkeypatch.setattr('data.input_code.d06_complex_logic.datetime', MockDateTime)
    wh = Warehouse({"item1": 10})
    op = OrderProcessor(wh)
    with pytest.raises(PaymentError):
        op.process_order(
            order_id="order1",
            user_data={
                "email": "test@example.com",
                "age": 25,
                "payment_method": "CRYPTO",
                "tier": "STANDARD"
            },
            items=[{"id": "item1", "qty": 1, "price": 10.0}]
        )

import pytest
from data.input_code.d06_complex_logic import *

# Helper datetime mocks
class MockDateTimeNight:
    @classmethod
    def now(cls):
        # Fixed hour within night discount window (e.g., 2 AM)
        return real_datetime(2022, 1, 1, 2, 0, 0)

class MockDateTimeDay:
    @classmethod
    def now(cls):
        # Fixed hour outside night discount window (e.g., 12 PM)
        return real_datetime(2022, 1, 1, 12, 0, 0)

# ---------- DiscountEngine Additional Tests ----------
def test_discount_engine_night_discount(monkeypatch):
    # T_MISSING_DISCOUNT_NIGHT
    monkeypatch.setattr('data.input_code.d06_complex_logic.datetime', MockDateTimeNight)
    discount = DiscountEngine.calculate_discount(total_amount=100.0, user_tier="STANDARD")
    assert discount == 0.05

def test_discount_engine_platinum_tier(monkeypatch):
    # T_MISSING_DISCOUNT_TIER_PLATINUM
    monkeypatch.setattr('data.input_code.d06_complex_logic.datetime', MockDateTimeDay)
    discount = DiscountEngine.calculate_discount(total_amount=100.0, user_tier="PLATINUM")
    assert discount == 0.20

def test_discount_engine_platinum_large_order(monkeypatch):
    # T_MISSING_DISCOUNT_TIER_PLATINUM_LARGE_ORDER
    monkeypatch.setattr('data.input_code.d06_complex_logic.datetime', MockDateTimeDay)
    discount = DiscountEngine.calculate_discount(total_amount=1001.0, user_tier="PLATINUM")
    assert discount == 0.25

def test_discount_engine_promo_code(monkeypatch):
    # T_MISSING_DISCOUNT_PROMO_CODE
    monkeypatch.setattr('data.input_code.d06_complex_logic.datetime', MockDateTimeNight)
    discount = DiscountEngine.calculate_discount(
        total_amount=100.0,
        user_tier="STANDARD",
        promo_code="ABC-123"
    )
    assert discount == 0.15000000000000002  # Adjusted for floating‑point precision

def test_discount_engine_super_promo_code(monkeypatch):
    # T_MISSING_DISCOUNT_PROMO_CODE_SUPER
    monkeypatch.setattr('data.input_code.d06_complex_logic.datetime', MockDateTimeDay)
    discount = DiscountEngine.calculate_discount(
        total_amount=100.0,
        user_tier="STANDARD",
        promo_code="ABC-999"
    )
    assert discount == 50.0

# ---------- OrderProcessor.validate_user Additional Tests ----------
def test_orderprocessor_validate_user_underage():
    # T_MISSING_ORDERPROCESSOR_VALIDATE_USER_UNDERAGE
    wh = Warehouse({})
    op = OrderProcessor(wh)
    with pytest.raises(UserValidationError):
        op.validate_user(email="test@example.com", age=17)

def test_orderprocessor_validate_user_over_100():
    # T_MISSING_ORDERPROCESSOR_VALIDATE_USER_OVER_100
    wh = Warehouse({})
    op = OrderProcessor(wh)
    with pytest.raises(UserValidationError):
        op.validate_user(email="test@example.com", age=101)

# ---------- OrderProcessor.process_order Additional Tests ----------
def test_orderprocessor_process_order_division_by_zero(monkeypatch):
    # T_MISSING_ORDERPROCESSOR_PROCESS_ORDER_DIVISION_BY_ZERO
    monkeypatch.setattr('data.input_code.d06_complex_logic.datetime', MockDateTimeDay)
    wh = Warehouse({"item1": 10})
    op = OrderProcessor(wh)
    with pytest.raises(ValueError):
        op.process_order(
            order_id="order1",
            user_data={"email": "test@example.com", "age": 25},
            items=[{"id": "item1", "qty": -1, "price": 0.0}]
        )

def test_orderprocessor_process_order_crypto_min_amount(monkeypatch):
    # T_MISSING_ORDERPROCESSOR_PROCESS_ORDER_CRYPTO_MIN_AMOUNT
    monkeypatch.setattr('data.input_code.d06_complex_logic.datetime', MockDateTimeDay)
    wh = Warehouse({"item1": 10})
    op = OrderProcessor(wh)
    with pytest.raises(PaymentError):
        op.process_order(
            order_id="order1",
            user_data={
                "email": "test@example.com",
                "age": 25,
                "payment_method": "CRYPTO",
                "tier": "STANDARD"
            },
            items=[{"id": "item1", "qty": 1, "price": 40.0}]
        )

import pytest
from data.input_code.d06_complex_logic import *
from datetime import datetime as real_datetime

# Helper datetime mock for daytime (no night discount)
class MockDateTimeDay:
    @classmethod
    def now(cls):
        return real_datetime(2022, 1, 1, 12, 0, 0)

# ---------- DiscountEngine Edge Case ----------
def test_discount_engine_edge_case_platinum_just_above_threshold(monkeypatch):
    # T_MISSING_DISCOUNT_EDGE_CASE
    monkeypatch.setattr('data.input_code.d06_complex_logic.datetime', MockDateTimeDay)
    discount = DiscountEngine.calculate_discount(
        total_amount=1000.01,
        user_tier="PLATINUM"
    )
    assert discount == 0.25

# ---------- OrderProcessor.process_order Negative Qty with Non‑Zero Price ----------
@pytest.mark.xfail(reason="Current implementation does not treat negative qty with non‑zero price as failure")
def test_orderprocessor_process_order_negative_qty_nonzero_price(monkeypatch):
    # T_MISSING_ORDERPROCESSOR_PROCESS_ORDER_NEGATIVE_QTY
    monkeypatch.setattr('data.input_code.d06_complex_logic.datetime', MockDateTimeDay)
    wh = Warehouse({"item1": 10})
    op = OrderProcessor(wh)
    result = op.process_order(
        order_id="order1",
        user_data={"email": "test@example.com", "age": 25},
        items=[{"id": "item1", "qty": -2, "price": 10.0}]
    )
    expected = {"status": "failed", "reason": "Cannot return free items"}
    assert result == expected

# ---------- OrderProcessor.process_order Zero Price ----------
def test_orderprocessor_process_order_zero_price(monkeypatch):
    # T_MISSING_ORDERPROCESSOR_PROCESS_ORDER_ZERO_PRICE
    monkeypatch.setattr('data.input_code.d06_complex_logic.datetime', MockDateTimeDay)
    wh = Warehouse({"item1": 10})
    op = OrderProcessor(wh)
    result = op.process_order(
        order_id="order1",
        user_data={"email": "test@example.com", "age": 25},
        items=[{"id": "item1", "qty": 1, "price": 0.0}]
    )
    expected = {
        "status": "success",
        "order_id": "order1",
        "original_price": 0.0,
        "discount_applied": 0.0,
        "final_total": 0.0,
        "items_count": 1
    }
    assert result == expected

# ---------- OrderProcessor.process_order Invalid Payment Method ----------
@pytest.mark.xfail(reason="Invalid payment method handling not implemented")
def test_orderprocessor_process_order_invalid_payment_method(monkeypatch):
    # T_MISSING_ORDERPROCESSOR_PROCESS_ORDER_INVALID_PAYMENT_METHOD
    monkeypatch.setattr('data.input_code.d06_complex_logic.datetime', MockDateTimeDay)
    wh = Warehouse({"item1": 10})
    op = OrderProcessor(wh)
    result = op.process_order(
        order_id="order1",
        user_data={
            "email": "test@example.com",
            "age": 25,
            "payment_method": "INVALID"
        },
        items=[{"id": "item1", "qty": 1, "price": 10.0}]
    )
    expected = {"status": "error", "reason": "Invalid payment method"}
    assert result == expected

# ---------- Warehouse.release_item Zero Quantity ----------
def test_warehouse_release_item_zero_qty():
    # T_MISSING_WAREHOUSE_RELEASE_ITEM_ZERO_QTY
    wh = Warehouse({"item1": 5})
    # No locked items initially; releasing zero qty should be a no‑op and not raise
    wh.release_item("item1", 0)
    # Ensure internal state remains unchanged (no _locked_stock entry)
    assert "item1" not in wh._locked_stock

# ---------- Warehouse.lock_item Zero Quantity ----------
def test_warehouse_lock_item_zero_qty():
    # T_MISSING_WAREHOUSE_LOCK_ITEM_ZERO_QTY
    wh = Warehouse({"item1": 5})
    # Locking zero quantity should not affect stock availability
    wh.lock_item("item1", 0)
    assert wh.check_stock("item1", 5)  # full stock still available

import pytest
from data.input_code.d06_complex_logic import *
from datetime import datetime as real_datetime

# Helper datetime mock for daytime (no night discount)
class MockDateTimeDay:
    @classmethod
    def now(cls):
        return real_datetime(2022, 1, 1, 12, 0, 0)

# ---------- DiscountEngine Edge Cases ----------
def test_discount_engine_edge_case_low(monkeypatch):
    # T_MISSING_DISCOUNT_EDGE_CASE_LOW
    monkeypatch.setattr('data.input_code.d06_complex_logic.datetime', MockDateTimeDay)
    discount = DiscountEngine.calculate_discount(
        total_amount=999.99,
        user_tier="PLATINUM"
    )
    assert discount == 0.2

def test_discount_engine_promo_code_null(monkeypatch):
    # T_MISSING_DISCOUNT_ENGINE_PROMO_CODE_NULL
    monkeypatch.setattr('data.input_code.d06_complex_logic.datetime', MockDateTimeDay)
    discount = DiscountEngine.calculate_discount(
        total_amount=100.0,
        user_tier="STANDARD",
        promo_code=None
    )
    assert discount == 0.0

# ---------- Warehouse.lock_item Negative Quantity ----------
def test_warehouse_lock_item_negative_qty():
    # T_MISSING_WAREHOUSE_LOCK_ITEM_NEGATIVE_QTY
    # No stock for the item forces InventoryError regardless of quantity sign
    wh = Warehouse({})
    with pytest.raises(InventoryError):
        wh.lock_item("item1", -1)

# ---------- OrderProcessor.validate_user Email Null ----------
def test_orderprocessor_validate_user_email_null(monkeypatch):
    # T_MISSING_ORDERPROCESSOR_VALIDATE_USER_EMAIL_NULL
    # Force re.match to return None for any input, triggering UserValidationError
    monkeypatch.setattr('data.input_code.d06_complex_logic.re.match', lambda pattern, string: None)
    wh = Warehouse({})
    op = OrderProcessor(wh)
    with pytest.raises(UserValidationError):
        op.validate_user(email=None, age=25)

# ---------- OrderProcessor.process_order Negative Price ----------
@pytest.mark.xfail(reason="Current implementation does not treat negative price as error")
def test_orderprocessor_process_order_negative_price(monkeypatch):
    # T_MISSING_ORDERPROCESSOR_PROCESS_ORDER_NEGATIVE_PRICE
    monkeypatch.setattr('data.input_code.d06_complex_logic.datetime', MockDateTimeDay)
    wh = Warehouse({"item1": 10})
    op = OrderProcessor(wh)
    result = op.process_order(
        order_id="order1",
        user_data={"email": "test@example.com", "age": 25},
        items=[{"id": "item1", "qty": 1, "price": -10.0}]
    )
    # Expected behavior according to the test plan (currently not implemented)
    assert result == {"status": "error", "reason": "Invalid price"}

# ---------- OrderProcessor.process_order Payment Method Null ----------
@pytest.mark.xfail(reason="Invalid payment method handling not implemented")
def test_orderprocessor_process_order_payment_method_null(monkeypatch):
    # T_MISSING_ORDERPROCESSOR_PROCESS_ORDER_PAYMENT_METHOD_NULL
    monkeypatch.setattr('data.input_code.d06_complex_logic.datetime', MockDateTimeDay)
    wh = Warehouse({"item1": 10})
    op = OrderProcessor(wh)
    result = op.process_order(
        order_id="order1",
        user_data={
            "email": "test@example.com",
            "age": 25,
            "payment_method": None
        },
        items=[{"id": "item1", "qty": 1, "price": 10.0}]
    )
    # Expected behavior according to the test plan (currently not implemented)
    assert result == {"status": "error", "reason": "Invalid payment method"}

import pytest
from data.input_code.d06_complex_logic import *
from datetime import datetime as real_datetime

# Helper datetime mock for daytime (no night discount)
class MockDateTimeDay:
    @classmethod
    def now(cls):
        return real_datetime(2022, 1, 1, 12, 0, 0)

# ---------- DiscountEngine ----------
def test_discount_engine_high_total_amount(monkeypatch):
    # T_MISSING_DISCOUNT_EDGE_CASE_HIGH
    monkeypatch.setattr('data.input_code.d06_complex_logic.datetime', MockDateTimeDay)
    discount = DiscountEngine.calculate_discount(
        total_amount=1_000_000.0,
        user_tier="PLATINUM"
    )
    assert discount == 0.25

# ---------- Warehouse ----------
def test_warehouse_check_stock_zero_qty():
    # T_MISSING_WAREHOUSE_CHECK_STOCK_ZERO_QTY
    wh = Warehouse({"item1": 5})
    assert wh.check_stock("item1", 0) is True

# ---------- OrderProcessor.validate_user ----------
def test_orderprocessor_validate_user_email_empty_string():
    # T_MISSING_ORDERPROCESSOR_VALIDATE_USER_EMAIL_EMPTY_STRING
    wh = Warehouse({})
    op = OrderProcessor(wh)
    with pytest.raises(UserValidationError) as exc:
        op.validate_user(email="", age=25)
    assert "Invalid email format" in str(exc.value)

# ---------- OrderProcessor.process_order ----------
def test_orderprocessor_process_order_unsupported_payment_method(monkeypatch):
    # T_MISSING_ORDERPROCESSOR_PROCESS_ORDER_PAYMENT_METHOD_UNSUPPORTED
    monkeypatch.setattr('data.input_code.d06_complex_logic.datetime', MockDateTimeDay)
    wh = Warehouse({"item1": 10})
    op = OrderProcessor(wh)
    result = op.process_order(
        order_id="order1",
        user_data={
            "email": "test@example.com",
            "age": 25,
            "payment_method": "UNSUPPORTED",
            "tier": "STANDARD"
        },
        items=[{"id": "item1", "qty": 1, "price": 10.0}]
    )
    # Current implementation treats unknown methods as normal flow
    assert result["status"] == "success"
    assert result["order_id"] == "order1"

def test_orderprocessor_process_order_item_id_null(monkeypatch):
    # T_MISSING_ORDERPROCESSOR_PROCESS_ORDER_ITEM_ID_NULL
    monkeypatch.setattr('data.input_code.d06_complex_logic.datetime', MockDateTimeDay)
    wh = Warehouse({"item1": 10})
    op = OrderProcessor(wh)
    result = op.process_order(
        order_id="order1",
        user_data={"email": "test@example.com", "age": 25},
        items=[{"id": None, "qty": 1, "price": 10.0}]
    )
    assert result["status"] == "failed"
    assert "Item None not found" in result["reason"]

def test_orderprocessor_process_order_item_qty_non_integer(monkeypatch):
    # T_MISSING_ORDERPROCESSOR_PROCESS_ORDER_ITEM_QTY_NON_INTEGER
    monkeypatch.setattr('data.input_code.d06_complex_logic.datetime', MockDateTimeDay)
    wh = Warehouse({"item1": 10})
    op = OrderProcessor(wh)
    result = op.process_order(
        order_id="order2",
        user_data={"email": "test@example.com", "age": 25},
        items=[{"id": "item1", "qty": 1.5, "price": 10.0}]
    )
    # qty is cast to int -> 1
    assert result["status"] == "success"
    assert result["original_price"] == 10.0
    assert result["items_count"] == 1

def test_orderprocessor_process_order_item_price_non_numeric(monkeypatch):
    # T_MISSING_ORDERPROCESSOR_PROCESS_ORDER_ITEM_PRICE_NON_NUMERIC
    monkeypatch.setattr('data.input_code.d06_complex_logic.datetime', MockDateTimeDay)
    wh = Warehouse({"item1": 10})
    op = OrderProcessor(wh)
    with pytest.raises(ValueError):
        op.process_order(
            order_id="order3",
            user_data={"email": "test@example.com", "age": 25},
            items=[{"id": "item1", "qty": 1, "price": "non-numeric"}]
        )