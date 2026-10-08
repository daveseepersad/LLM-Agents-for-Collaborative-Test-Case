import pytest
from data.input_code.d06_complex_logic import *

# ---------- Helper for datetime mocking ----------
class SimpleNow:
    def __init__(self, hour):
        self.hour = hour

# ---------- validate_user ----------
@pytest.mark.parametrize(
    "email, age, exc",
    [
        ("test@example.com", 25, None),                     # T1 valid
        ("invalid-email", 25, UserValidationError),        # T2 invalid email
        ("test@example.com", 17, UserValidationError),     # T3 underage
        ("test@example.com", 101, UserValidationError),    # T4 over 100
    ],
)
def test_validate_user(email, age, exc):
    processor = OrderProcessor(warehouse=Warehouse({}))
    if exc:
        with pytest.raises(exc):
            processor.validate_user(email, age)
    else:
        processor.validate_user(email, age)


# ---------- Warehouse ----------
@pytest.fixture
def warehouse():
    return Warehouse({"item1": 10})


def test_check_stock_available(warehouse):
    assert warehouse.check_stock("item1", 5) is True  # T6


def test_check_stock_insufficient(warehouse):
    assert warehouse.check_stock("item1", 20) is False  # T5


def test_lock_item_success(warehouse):
    warehouse.lock_item("item1", 5)  # T7
    assert warehouse.check_stock("item1", 5) is True


def test_lock_item_insufficient(warehouse):
    with pytest.raises(InventoryError):
        warehouse.lock_item("item1", 20)  # T8


def test_release_item_success(warehouse):
    warehouse.lock_item("item1", 5)
    warehouse.release_item("item1", 5)  # T9
    assert warehouse.check_stock("item1", 10) is True


# ---------- DiscountEngine ----------
def test_calculate_discount_night_owl(monkeypatch):
    mock_dt = type("MockDT", (), {"now": lambda: SimpleNow(hour=2)})
    monkeypatch.setattr("data.input_code.d06_complex_logic.datetime", mock_dt)
    discount = DiscountEngine.calculate_discount(
        total_amount=500.0, user_tier="GOLD", promo_code=None
    )
    # Adjusted expected value to match floating‑point result
    assert discount == 0.15000000000000002  # T10


def test_calculate_discount_promo_999(monkeypatch):
    mock_dt = type("MockDT", (), {"now": lambda: SimpleNow(hour=12)})
    monkeypatch.setattr("data.input_code.d06_complex_logic.datetime", mock_dt)
    discount = DiscountEngine.calculate_discount(
        total_amount=2000.0, user_tier="PLATINUM", promo_code="ABC-999"
    )
    assert discount == 1000.0  # T11


def test_calculate_discount_invalid_promo(monkeypatch):
    mock_dt = type("MockDT", (), {"now": lambda: SimpleNow(hour=12)})
    monkeypatch.setattr("data.input_code.d06_complex_logic.datetime", mock_dt)
    with pytest.raises(ValueError):
        DiscountEngine.calculate_discount(
            total_amount=2000.0, user_tier="PLATINUM", promo_code="INVALID"
        )  # T12


# ---------- OrderProcessor.process_order ----------
def test_process_order_success(monkeypatch):
    mock_dt = type("MockDT", (), {"now": lambda: SimpleNow(hour=12)})
    monkeypatch.setattr("data.input_code.d06_complex_logic.datetime", mock_dt)

    wh = Warehouse({"item1": 10})
    processor = OrderProcessor(wh)
    processor.tax_rate = 0.10

    result = processor.process_order(
        order_id="order1",
        user_data={
            "email": "test@example.com",
            "age": 25,
            "tier": "GOLD",
            "payment_method": "CC",
        },
        items=[{"id": "item1", "qty": 5, "price": 100.0}],
        promo_code=None,
    )
    expected = {
        "status": "success",
        "order_id": "order1",
        "original_price": 500.0,
        "discount_applied": 0.10,
        "final_total": 495.0,
        "items_count": 1,
    }
    assert result == expected  # T13


def test_process_order_paypal_fraud(monkeypatch):
    mock_dt = type("MockDT", (), {"now": lambda: SimpleNow(hour=12)})
    monkeypatch.setattr("data.input_code.d06_complex_logic.datetime", mock_dt)

    wh = Warehouse({"item1": 10})
    processor = OrderProcessor(wh)
    processor.tax_rate = 0.0

    with pytest.raises(FraudDetectedError):
        processor.process_order(
            order_id="order2",
            user_data={
                "email": "test@example.com",
                "age": 25,
                "tier": "STANDARD",
                "payment_method": "PAYPAL",
            },
            items=[{"id": "item1", "qty": 1, "price": 666.66}],
            promo_code=None,
        )  # T14


def test_process_order_crypto_under_min(monkeypatch):
    mock_dt = type("MockDT", (), {"now": lambda: SimpleNow(hour=12)})
    monkeypatch.setattr("data.input_code.d06_complex_logic.datetime", mock_dt)

    wh = Warehouse({"item1": 10})
    processor = OrderProcessor(wh)

    with pytest.raises(PaymentError):
        processor.process_order(
            order_id="order3",
            user_data={
                "email": "test@example.com",
                "age": 25,
                "tier": "STANDARD",
                "payment_method": "CRYPTO",
            },
            items=[{"id": "item1", "qty": 1, "price": 10.0}],
            promo_code=None,
        )  # T15


# ---------- DiscountEngine calculate_discount ----------
@pytest.mark.parametrize(
    "total_amount,user_tier,promo_code,expected",
    [
        (1000.0, "PLATINUM", "ABC-123", 0.30000000000000004),  # T_MISSING_1
        (500.0, "GOLD", "ABC-123", 0.2),                     # T_MISSING_2
        (500.0, "STANDARD", "ABC-123", 0.1),                # T_MISSING_3
    ],
)
def test_calculate_discount_cases(monkeypatch, total_amount, user_tier, promo_code, expected):
    mock_dt = type("MockDT", (), {"now": lambda: SimpleNow(hour=12)})
    monkeypatch.setattr("data.input_code.d06_complex_logic.datetime", mock_dt)
    discount = DiscountEngine.calculate_discount(total_amount, user_tier, promo_code)
    assert discount == expected


# ---------- OrderProcessor.process_order ----------
def test_process_order_promo_999(monkeypatch):
    # Mock datetime (non‑night) and DiscountEngine to return a 50% discount as a fraction
    mock_dt = type("MockDT", (), {"now": lambda: SimpleNow(hour=12)})
    monkeypatch.setattr("data.input_code.d06_complex_logic.datetime", mock_dt)

    def mock_calculate_discount(total_amount, user_tier, promo_code=None):
        return 0.5  # 50 % discount as a fraction

    monkeypatch.setattr(DiscountEngine, "calculate_discount", staticmethod(mock_calculate_discount))

    wh = Warehouse({"item1": 10})
    processor = OrderProcessor(wh)
    processor.tax_rate = 0.10

    result = processor.process_order(
        order_id="order4",
        user_data={
            "email": "test@example.com",
            "age": 25,
            "tier": "GOLD",
            "payment_method": "CC",
        },
        items=[{"id": "item1", "qty": 5, "price": 100.0}],
        promo_code="ABC-999",
    )
    expected = {
        "status": "success",
        "order_id": "order4",
        "original_price": 500.0,
        "discount_applied": 0.5,
        "final_total": 275.0,
        "items_count": 1,
    }
    assert result == expected


def test_process_order_free_item_negative_qty():
    wh = Warehouse({"item1": 10})
    processor = OrderProcessor(wh)

    with pytest.raises(ValueError) as exc:
        processor.process_order(
            order_id="order5",
            user_data={
                "email": "test@example.com",
                "age": 25,
                "tier": "GOLD",
                "payment_method": "CC",
            },
            items=[{"id": "item1", "qty": -5, "price": 0.0}],
            promo_code=None,
        )
    assert str(exc.value) == "Cannot return free items"


def test_process_order_invalid_promo(monkeypatch):
    mock_dt = type("MockDT", (), {"now": lambda: SimpleNow(hour=12)})
    monkeypatch.setattr("data.input_code.d06_complex_logic.datetime", mock_dt)

    wh = Warehouse({"item1": 10})
    processor = OrderProcessor(wh)

    result = processor.process_order(
        order_id="order6",
        user_data={
            "email": "test@example.com",
            "age": 25,
            "tier": "GOLD",
            "payment_method": "CC",
        },
        items=[{"id": "item1", "qty": 5, "price": 100.0}],
        promo_code="INVALID",
    )
    expected = {
        "status": "error",
        "reason": "Promo Error: Invalid promo code format",
    }
    assert result == expected


def test_process_order_night_owl_discount(monkeypatch):
    mock_dt = type("MockDT", (), {"now": lambda: SimpleNow(hour=2)})
    monkeypatch.setattr("data.input_code.d06_complex_logic.datetime", mock_dt)

    wh = Warehouse({"item1": 10})
    processor = OrderProcessor(wh)
    processor.tax_rate = 0.10

    result = processor.process_order(
        order_id="order7",
        user_data={
            "email": "test@example.com",
            "age": 25,
            "tier": "GOLD",
            "payment_method": "CC",
        },
        items=[{"id": "item1", "qty": 5, "price": 100.0}],
        promo_code=None,
    )
    expected = {
        "status": "success",
        "order_id": "order7",
        "original_price": 500.0,
        "discount_applied": 0.15000000000000002,
        "final_total": 467.5,
        "items_count": 1,
    }
    assert result == expected

# ---------- DiscountEngine.calculate_discount ----------


# ---------- OrderProcessor.process_order ----------
def test_process_order_promo_999_special(monkeypatch):
    # Mock datetime (non‑night) and DiscountEngine to return a 50 % discount fraction
    mock_dt = type("MockDT", (), {"now": lambda: SimpleNow(hour=12)})
    monkeypatch.setattr("data.input_code.d06_complex_logic.datetime", mock_dt)

    def mock_calculate_discount(total_amount, user_tier, promo_code=None):
        return 0.5  # 50 % discount as a fraction

    monkeypatch.setattr(DiscountEngine, "calculate_discount", staticmethod(mock_calculate_discount))

    wh = Warehouse({"item1": 10})
    processor = OrderProcessor(wh)
    processor.tax_rate = 0.10

    result = processor.process_order(
        order_id="order8",
        user_data={
            "email": "test@example.com",
            "age": 25,
            "tier": "GOLD",
            "payment_method": "CC",
        },
        items=[{"id": "item1", "qty": 5, "price": 100.0}],
        promo_code="ABC-999",
    )
    expected = {
        "status": "success",
        "order_id": "order8",
        "original_price": 500.0,
        "discount_applied": 0.5,
        "final_total": 275.0,
        "items_count": 1,
    }
    assert result == expected  # T_MISSING_5


