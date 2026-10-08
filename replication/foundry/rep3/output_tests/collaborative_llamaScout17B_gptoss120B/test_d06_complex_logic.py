import pytest
from data.input_code.d06_complex_logic import *
import datetime

# ---------- Fixtures ----------
@pytest.fixture
def warehouse_factory():
    """Factory to create a Warehouse with given initial stock."""
    def _factory(initial_stock):
        return Warehouse(initial_stock)
    return _factory

@pytest.fixture
def order_processor_factory(warehouse_factory):
    """Factory to create an OrderProcessor with a Warehouse."""
    def _factory(initial_stock):
        wh = warehouse_factory(initial_stock)
        return OrderProcessor(wh)
    return _factory

# ---------- Helper for datetime mocking ----------
class FixedDatetime(datetime.datetime):
    @classmethod
    def now(cls):
        # Return a fixed datetime at 12:00 (no night discount)
        return cls(2023, 1, 1, 12, 0, 0)

# ---------- Tests for OrderProcessor.validate_user ----------
@pytest.mark.parametrize(
    "email, age, expect_exception",
    [
        ("test@example.com", 25, None),                     # valid
        ("invalid", 25, UserValidationError),               # invalid email
        ("test@example.com", 17, UserValidationError),      # underage
        ("test@example.com", 101, UserValidationError),     # over 100
    ]
)
def test_validate_user(email, age, expect_exception):
    processor = OrderProcessor(Warehouse({}))
    if expect_exception:
        with pytest.raises(expect_exception):
            processor.validate_user(email, age)
    else:
        # Should not raise
        processor.validate_user(email, age)

# ---------- Tests for Warehouse.check_stock ----------
@pytest.mark.parametrize(
    "initial_stock, item_id, qty, expect_exception, expected_result",
    [
        ({"item1": 10}, "item1", 5, None, True),          # enough stock
        ({"item1": 10}, "item2", 5, InventoryError, None) # item not found
    ]
)
def test_check_stock(initial_stock, item_id, qty, expect_exception, expected_result):
    wh = Warehouse(initial_stock)
    if expect_exception:
        with pytest.raises(expect_exception):
            wh.check_stock(item_id, qty)
    else:
        assert wh.check_stock(item_id, qty) == expected_result

# ---------- Tests for Warehouse.lock_item ----------
def test_lock_item_success():
    wh = Warehouse({"item1": 10})
    wh.lock_item("item1", 5)
    # After locking, available stock should be 5
    assert wh.check_stock("item1", 5) is True
    assert wh.check_stock("item1", 6) is False

def test_lock_item_insufficient():
    wh = Warehouse({"item1": 10})
    with pytest.raises(InventoryError):
        wh.lock_item("item1", 15)

# ---------- Tests for DiscountEngine.calculate_discount ----------
@pytest.fixture(autouse=True)
def mock_datetime_now(monkeypatch):
    """Patch datetime.datetime.now to a fixed time without night discount."""
    monkeypatch.setattr(datetime, "datetime", FixedDatetime)

@pytest.mark.parametrize(
    "total_amount, user_tier, promo_code, expected",
    [
        (100, "STANDARD", None, 0.0),          # no tier, no promo
        (100, "GOLD", None, 0.10),            # gold tier
        (100, "PLATINUM", None, 0.20),        # platinum tier
        (1001, "PLATINUM", None, 0.25),       # platinum high amount
        (100, "STANDARD", "ABC-123", 0.10),   # valid promo adds 10%
        (100, "STANDARD", "ABC-999", 50.0),   # super promo returns 50% of total_amount
    ]
)
def test_calculate_discount(total_amount, user_tier, promo_code, expected):
    if isinstance(expected, float) and expected > 1.0:
        # Super promo returns absolute discount amount
        result = DiscountEngine.calculate_discount(total_amount, user_tier, promo_code)
        assert result == expected
    else:
        result = DiscountEngine.calculate_discount(total_amount, user_tier, promo_code)
        assert result == expected

def test_calculate_discount_invalid_promo():
    with pytest.raises(ValueError):
        DiscountEngine.calculate_discount(100, "STANDARD", "invalid")

# ---------- Tests for OrderProcessor.process_order ----------
def test_process_order_success(order_processor_factory):
    processor = order_processor_factory({"item1": 10})
    order = processor.process_order(
        order_id="1",
        user_data={"email": "test@example.com", "age": 25, "tier": "STANDARD"},
        items=[{"id": "item1", "qty": 1, "price": 10.0}]
    )
    assert order["status"] == "success"
    assert order["order_id"] == "1"
    assert order["original_price"] == 10.0
    assert order["discount_applied"] == 0.0
    # final_total = 10 * (1 + 0.22) = 12.2 rounded to 2 decimals
    assert order["final_total"] == 12.2
    assert order["items_count"] == 1

def test_process_order_stock_fail(order_processor_factory):
    processor = order_processor_factory({"item1": 10})
    result = processor.process_order(
        order_id="1",
        user_data={"email": "test@example.com", "age": 25, "tier": "STANDARD"},
        items=[{"id": "item1", "qty": 15, "price": 10.0}]
    )
    assert result["status"] == "failed"
    assert "Out of stock" in result["reason"]

def test_process_order_invalid_promo(order_processor_factory):
    processor = order_processor_factory({"item1": 10})
    result = processor.process_order(
        order_id="1",
        user_data={"email": "test@example.com", "age": 25, "tier": "STANDARD"},
        items=[{"id": "item1", "qty": 1, "price": 10.0}],
        promo_code="invalid"
    )
    assert result["status"] == "error"
    assert "Promo Error" in result["reason"]

def test_process_order_paypal_fraud(order_processor_factory):
    processor = order_processor_factory({"item1": 10})
    # Calculate price that leads to final_price_with_tax == 666.66
    # Let total_price = X, discount = 0, tax 22% => X * 1.22 = 666.66 => X = 666.66 / 1.22
    total_price = round(666.66 / 1.22, 2)  # approx 546.28
    # Use price and qty to achieve this total
    qty = 1
    price = total_price
    with pytest.raises(FraudDetectedError):
        processor.process_order(
            order_id="1",
            user_data={"email": "test@example.com", "age": 25, "tier": "STANDARD", "payment_method": "PAYPAL"},
            items=[{"id": "item1", "qty": qty, "price": price}]
        )

def test_process_order_crypto_payment_error(order_processor_factory):
    processor = order_processor_factory({"item1": 10})
    # Use low total price so final with tax < 50
    with pytest.raises(PaymentError):
        processor.process_order(
            order_id="1",
            user_data={"email": "test@example.com", "age": 25, "tier": "STANDARD", "payment_method": "CRYPTO"},
            items=[{"id": "item1", "qty": 1, "price": 10.0}]
        )