import pytest
from data.input_code.d06_complex_logic import *
from datetime import datetime

# ---------- Warehouse Tests ----------
@pytest.fixture
def warehouse():
    return Warehouse(initial_stock={"item1": 10, "item2": 20})


def test_warehouse_init():
    w = Warehouse(initial_stock={"a": 5})
    assert w._stock == {"a": 5}
    assert w._locked_stock == {}


@pytest.mark.parametrize(
    "item_id, qty, expected",
    [
        ("item1", 5, True),   # enough stock
        ("item2", 20, True),  # exact stock
    ],
)
def test_check_stock_success(warehouse, item_id, qty, expected):
    assert warehouse.check_stock(item_id, qty) is expected


def test_check_stock_missing_item(warehouse):
    with pytest.raises(InventoryError):
        warehouse.check_stock("item3", 5)


def test_lock_item_success(warehouse):
    warehouse.lock_item("item1", 5)
    assert warehouse._locked_stock["item1"] == 5
    # ensure stock still sufficient after lock
    assert warehouse.check_stock("item1", 5) is True


def test_lock_item_insufficient_stock(warehouse):
    with pytest.raises(InventoryError):
        warehouse.lock_item("item1", 15)


def test_release_item(warehouse):
    warehouse.lock_item("item1", 5)
    warehouse.release_item("item1", 5)
    assert "item1" not in warehouse._locked_stock


# ---------- DiscountEngine Tests ----------
def mock_datetime(monkeypatch, hour):
    class MockedDatetime(datetime):
        @classmethod
        def now(cls):
            return cls(2021, 1, 1, hour, 0, 0)

    monkeypatch.setattr("data.input_code.d06_complex_logic.datetime", MockedDatetime)


@pytest.mark.parametrize(
    "total, tier, promo, expected",
    [
        (100.0, "GOLD", None, 0.10),
        (100.0, "PLATINUM", None, 0.20),
        (1000.0, "PLATINUM", None, 0.20),  # total == 1000 not >1000, no extra 0.05
        (100.0, "GOLD", "ABC-123", 0.20),  # tier 0.10 + promo 0.10
        (100.0, "GOLD", "XYZ-999", 50.0),  # super promo returns 50% off immediate (price * 0.5)
    ],
)
def test_calculate_discount(monkeypatch, total, tier, promo, expected):
    # Ensure hour is outside night discount to keep test deterministic
    mock_datetime(monkeypatch, hour=12)
    result = DiscountEngine.calculate_discount(total, tier, promo)
    assert result == expected


def test_calculate_discount_invalid_promo(monkeypatch):
    mock_datetime(monkeypatch, hour=12)
    with pytest.raises(ValueError):
        DiscountEngine.calculate_discount(100.0, "GOLD", "invalid")


# ---------- OrderProcessor.validate_user Tests ----------
@pytest.fixture
def order_processor(warehouse):
    return OrderProcessor(warehouse)


@pytest.mark.parametrize(
    "email, age",
    [
        ("test@example.com", 25),
        ("user.name+tag@sub.domain.co", 30),
    ],
)
def test_validate_user_success(order_processor, email, age):
    # Should not raise
    order_processor.validate_user(email, age)


@pytest.mark.parametrize(
    "email, age, exc",
    [
        ("invalid", 25, UserValidationError),
        ("test@example.com", 15, UserValidationError),
        ("test@example.com", 101, UserValidationError),
    ],
)
def test_validate_user_errors(order_processor, email, age, exc):
    with pytest.raises(exc):
        order_processor.validate_user(email, age)


# ---------- OrderProcessor.process_order Tests ----------
def test_process_order_success(monkeypatch, warehouse):
    # Setup
    mock_datetime(monkeypatch, hour=12)
    processor = OrderProcessor(warehouse)

    order = processor.process_order(
        order_id="123",
        user_data={"email": "test@example.com", "age": 25, "tier": "GOLD"},
        items=[{"id": "item1", "qty": 2, "price": 10.0}],
        promo_code="ABC-123",
    )

    assert order == {
        "status": "success",
        "order_id": "123",
        "original_price": 20.0,
        "discount_applied": 0.20,
        "final_total": 19.52,  # includes 22% tax
        "items_count": 1,
    }


def test_process_order_insufficient_stock(monkeypatch, warehouse):
    mock_datetime(monkeypatch, hour=12)
    processor = OrderProcessor(warehouse)

    result = processor.process_order(
        order_id="123",
        user_data={"email": "test@example.com", "age": 25, "tier": "GOLD"},
        items=[{"id": "item1", "qty": 15, "price": 10.0}],
        promo_code="ABC-123",
    )

    assert result == {
        "status": "failed",
        "reason": "Out of stock: Insufficient stock for item1",
    }


def test_process_order_invalid_promo(monkeypatch, warehouse):
    mock_datetime(monkeypatch, hour=12)
    processor = OrderProcessor(warehouse)

    result = processor.process_order(
        order_id="123",
        user_data={"email": "test@example.com", "age": 25, "tier": "GOLD"},
        items=[{"id": "item1", "qty": 2, "price": 10.0}],
        promo_code="invalid",
    )

    assert result == {
        "status": "error",
        "reason": "Promo Error: Invalid promo code format",
    }


def test_process_order_fraud_detected(monkeypatch, warehouse):
    # Choose a price that after tax rounds to exactly 666.66
    mock_datetime(monkeypatch, hour=12)
    processor = OrderProcessor(warehouse)

    # Ensure enough stock
    warehouse._stock["item1"] = 100

    with pytest.raises(FraudDetectedError):
        processor.process_order(
            order_id="123",
            user_data={
                "email": "test@example.com",
                "age": 25,
                "tier": "STANDARD",
                "payment_method": "PAYPAL",
            },
            items=[{"id": "item1", "qty": 1, "price": 546.4426229508197}],
            promo_code=None,
        )


def test_process_order_crypto_payment_error(monkeypatch, warehouse):
    mock_datetime(monkeypatch, hour=12)
    processor = OrderProcessor(warehouse)

    # Total after discount will be low (<50)
    with pytest.raises(PaymentError):
        processor.process_order(
            order_id="123",
            user_data={
                "email": "test@example.com",
                "age": 25,
                "tier": "STANDARD",
                "payment_method": "CRYPTO",
            },
            items=[{"id": "item1", "qty": 2, "price": 5.0}],
            promo_code=None,
        )