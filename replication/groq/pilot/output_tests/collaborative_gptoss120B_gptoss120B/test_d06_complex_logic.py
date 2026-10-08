import pytest
from data.input_code.d06_complex_logic import *

# ------------------- Warehouse Tests ------------------- #

@pytest.mark.parametrize(
    "initial_stock,item_id,quantity,expected",
    [
        ({"itemA": 10}, "itemA", 5, True),
    ],
)
def test_warehouse_check_stock_success(initial_stock, item_id, quantity, expected):
    wh = Warehouse(initial_stock)
    assert wh.check_stock(item_id, quantity) == expected


def test_warehouse_check_stock_unknown_item():
    wh = Warehouse({"itemA": 10})
    with pytest.raises(InventoryError):
        wh.check_stock("itemX", 1)


def test_warehouse_lock_item_insufficient_stock():
    wh = Warehouse({"itemB": 3})
    with pytest.raises(InventoryError):
        wh.lock_item("itemB", 5)


# ------------------- DiscountEngine Tests ------------------- #

@pytest.mark.parametrize(
    "total_amount,user_tier,promo_code,mock_hour,expected",
    [
        # T4: night hour + GOLD tier, no promo
        (200.0, "GOLD", None, 2, 0.15),
        # T5: PLATINUM tier, amount>1000, valid promo
        (1500.0, "PLATINUM", "ABC-123", 12, 0.35),
        # T6: promo ending with 999 gives 50% off immediate
        (200.0, "STANDARD", "XYZ-999", 12, 100.0),
    ],
)
def test_discount_engine_success(total_amount, user_tier, promo_code, mock_hour, expected, monkeypatch):
    class MockDateTime:
        @classmethod
        def now(cls):
            return datetime(2020, 1, 1, hour=mock_hour)

    monkeypatch.setattr("data.input_code.d06_complex_logic.datetime", MockDateTime)
    result = DiscountEngine.calculate_discount(total_amount, user_tier, promo_code)
    # Use approx for floating‑point comparisons
    assert result == pytest.approx(expected)


def test_discount_engine_malformed_promo(monkeypatch):
    class MockDateTime:
        @classmethod
        def now(cls):
            return datetime(2020, 1, 1, hour=12)

    monkeypatch.setattr("data.input_code.d06_complex_logic.datetime", MockDateTime)
    with pytest.raises(ValueError):
        DiscountEngine.calculate_discount(100.0, "STANDARD", "bad_code")


# ------------------- OrderProcessor.validate_user Tests ------------------- #

@pytest.mark.parametrize(
    "email,age",
    [
        ("john.doe@example.com", 30),
    ],
)
def test_validate_user_success(email, age):
    op = OrderProcessor(Warehouse({}))
    # Should not raise
    op.validate_user(email, age)


@pytest.mark.parametrize(
    "email,age,expected_msg",
    [
        ("invalid-email", 30, "Invalid email format"),
        ("young@example.com", 16, "User must be 18+"),
        ("old@example.com", 101, "Age verification required for 100+"),
    ],
)
def test_validate_user_errors(email, age, expected_msg):
    op = OrderProcessor(Warehouse({}))
    with pytest.raises(UserValidationError) as exc:
        op.validate_user(email, age)
    assert expected_msg in str(exc.value)


# ------------------- OrderProcessor.process_order Tests ------------------- #

def _make_processor(initial_stock):
    return OrderProcessor(Warehouse(initial_stock))


@pytest.mark.parametrize(
    "order_id,user_data,items,promo_code,initial_stock,mock_hour,expected",
    [
        # T12
        (
            "ORD001",
            {"email": "alice@example.com", "age": 35, "tier": "STANDARD", "payment_method": "CC"},
            [{"id": "item1", "qty": 2, "price": 100.0}],
            None,
            {"item1": 10},
            12,
            {
                "status": "success",
                "order_id": "ORD001",
                "original_price": 200.0,
                "discount_applied": 0.0,
                "final_total": 244.0,
                "items_count": 1,
            },
        ),
        # T13
        (
            "ORD002",
            {"email": "bob@example.com", "age": 40, "tier": "GOLD", "payment_method": "CC"},
            [{"id": "item2", "qty": 2, "price": 100.0}],
            "ABC-123",
            {"item2": 10},
            3,
            {
                "status": "success",
                "order_id": "ORD002",
                "original_price": 200.0,
                "discount_applied": 0.25,
                "final_total": 183.0,
                "items_count": 1,
            },
        ),
        # T14 - invalid promo format
        (
            "ORD003",
            {"email": "carol@example.com", "age": 28, "tier": "STANDARD", "payment_method": "CC"},
            [{"id": "item3", "qty": 1, "price": 50.0}],
            "bad-promo",
            {"item3": 5},
            12,
            {"status": "error", "reason": "Promo Error: Invalid promo code format"},
        ),
        # T15 - missing item in warehouse
        (
            "ORD004",
            {"email": "dave@example.com", "age": 45, "tier": "STANDARD", "payment_method": "CC"},
            [{"id": "missing_item", "qty": 1, "price": 20.0}],
            None,
            {"itemX": 5},
            12,
            {
                "status": "failed",
                "reason": "Out of stock: Item missing_item not found in warehouse.",
            },
        ),
        # T16 - insufficient stock
        (
            "ORD005",
            {"email": "eve@example.com", "age": 32, "tier": "STANDARD", "payment_method": "CC"},
            [{"id": "item4", "qty": 10, "price": 15.0}],
            None,
            {"item4": 3},
            12,
            {
                "status": "failed",
                "reason": "Out of stock: Insufficient stock for item4",
            },
        ),
    ],
)
def test_process_order_success_and_handled_errors(
    order_id, user_data, items, promo_code, initial_stock, mock_hour, expected, monkeypatch
):
    # Mock datetime for DiscountEngine
    class MockDateTime:
        @classmethod
        def now(cls):
            return datetime(2020, 1, 1, hour=mock_hour)

    monkeypatch.setattr("data.input_code.d06_complex_logic.datetime", MockDateTime)

    processor = _make_processor(initial_stock)
    result = processor.process_order(order_id, user_data, items, promo_code)
    assert result == expected


def test_process_order_value_error_on_invalid_item(monkeypatch):
    # Setup to trigger the qty<0 and price==0 branch
    class MockDateTime:
        @classmethod
        def now(cls):
            return datetime(2020, 1, 1, hour=12)

    monkeypatch.setattr("data.input_code.d06_complex_logic.datetime", MockDateTime)

    processor = _make_processor({"item5": 5})
    user_data = {
        "email": "frank@example.com",
        "age": 27,
        "tier": "STANDARD",
        "payment_method": "CC",
    }
    items = [{"id": "item5", "qty": -1, "price": 0.0}]
    with pytest.raises(ValueError):
        processor.process_order("ORD006", user_data, items)


def test_process_order_fraud_detected_error(monkeypatch):
    # Mock datetime (hour irrelevant)
    class MockDateTime:
        @classmethod
        def now(cls):
            return datetime(2020, 1, 1, hour=12)

    monkeypatch.setattr("data.input_code.d06_complex_logic.datetime", MockDateTime)

    processor = _make_processor({"item6": 2})
    user_data = {
        "email": "grace@example.com",
        "age": 30,
        "tier": "STANDARD",
        "payment_method": "PAYPAL",
    }
    items = [{"id": "item6", "qty": 1, "price": 546.4426}]
    # The calculation leads to final_price_with_tax == 666.66, triggering FraudDetectedError
    with pytest.raises(FraudDetectedError):
        processor.process_order("ORD007", user_data, items)


def test_process_order_payment_error_crypto(monkeypatch):
    # Mock datetime (hour irrelevant)
    class MockDateTime:
        @classmethod
        def now(cls):
            return datetime(2020, 1, 1, hour=12)

    monkeypatch.setattr("data.input_code.d06_complex_logic.datetime", MockDateTime)

    processor = _make_processor({"item7": 5})
    user_data = {
        "email": "henry@example.com",
        "age": 29,
        "tier": "STANDARD",
        "payment_method": "CRYPTO",
    }
    items = [{"id": "item7", "qty": 1, "price": 40.0}]
    with pytest.raises(PaymentError):
        processor.process_order("ORD008", user_data, items)