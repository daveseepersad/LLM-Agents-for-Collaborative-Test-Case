import pytest
from unittest.mock import patch
from data.input_code.d06_complex_logic import *

# ---------- DiscountEngine Tests ----------
@pytest.mark.parametrize(
    "total_amount,user_tier,promo_code,expected",
    [
        # Night discount (mocked hour = 2)
        (100.0, "STANDARD", None, 0.05),
        # Gold tier adds 0.10 + night discount 0.05 = 0.15000000000000002
        (50.0, "GOLD", None, 0.15000000000000002),
        # Platinum tier >1000 adds 0.20 + 0.05 + night discount 0.05 = 0.30
        (1500.0, "PLATINUM", None, 0.30),
        # Valid promo code adds 0.10 + night discount 0.05 = 0.15000000000000002
        (60.0, "STANDARD", "ABC-123", 0.15000000000000002),
        # Promo code ending with 999 gives 50% off (returns amount, not percent)
        (80.0, "STANDARD", "DEF-999", 40.0),
    ],
)
def test_discount_engine_success(total_amount, user_tier, promo_code, expected):
    # Mock datetime to control night discount branch
    with patch("data.input_code.d06_complex_logic.datetime") as mock_dt:
        mock_dt.now.return_value = type("dt", (), {"hour": 2})
        result = DiscountEngine.calculate_discount(total_amount, user_tier, promo_code)
        assert result == expected


def test_discount_engine_invalid_promo():
    with pytest.raises(ValueError):
        DiscountEngine.calculate_discount(60.0, "STANDARD", "abc-123")


# ---------- OrderProcessor.validate_user Tests ----------
@pytest.mark.parametrize(
    "email,age,expected_exception",
    [
        ("not-an-email", 25, UserValidationError),
        ("user@example.com", 17, UserValidationError),
        ("user@example.com", 101, UserValidationError),
    ],
)
def test_validate_user_errors(email, age, expected_exception):
    processor = OrderProcessor(Warehouse({}))
    with pytest.raises(expected_exception):
        processor.validate_user(email, age)


# ---------- OrderProcessor.process_order Tests ----------
def test_process_order_success():
    warehouse = Warehouse({"A": 2, "B": 1})
    processor = OrderProcessor(warehouse)

    result = processor.process_order(
        order_id="ORD1",
        user_data={
            "email": "buyer@example.com",
            "age": 30,
            "tier": "STANDARD",
            "payment_method": "CC",
        },
        items=[
            {"id": "A", "qty": 2, "price": 5.0},
            {"id": "B", "qty": 1, "price": 10.0},
        ],
        promo_code=None,
    )

    assert result == {
        "status": "success",
        "order_id": "ORD1",
        "original_price": 20.0,
        "discount_applied": 0.0,
        "final_total": 24.4,
        "items_count": 2,
    }


def test_process_order_promo_invalid():
    warehouse = Warehouse({"A": 5})
    processor = OrderProcessor(warehouse)

    result = processor.process_order(
        order_id="ORD2",
        user_data={
            "email": "user2@example.com",
            "age": 25,
            "tier": "STANDARD",
            "payment_method": "CC",
        },
        items=[{"id": "A", "qty": 1, "price": 10.0}],
        promo_code="badfmt",
    )

    assert result["status"] == "error"
    assert "Promo Error" in result["reason"]


def test_process_order_paypal_fraud():
    warehouse = Warehouse({"A": 1})
    processor = OrderProcessor(warehouse)

    with pytest.raises(FraudDetectedError):
        processor.process_order(
            order_id="ORD3",
            user_data={
                "email": "pay@example.com",
                "age": 30,
                "tier": "STANDARD",
                "payment_method": "PAYPAL",
            },
            items=[{"id": "A", "qty": 1, "price": 546.4426229508}],
            promo_code=None,
        )


def test_process_order_crypto_minimum():
    warehouse = Warehouse({"C": 1})
    processor = OrderProcessor(warehouse)

    with pytest.raises(PaymentError):
        processor.process_order(
            order_id="ORD4",
            user_data={
                "email": "crypto@example.com",
                "age": 28,
                "tier": "STANDARD",
                "payment_method": "CRYPTO",
            },
            items=[{"id": "C", "qty": 1, "price": 30.0}],
            promo_code=None,
        )


def test_process_order_return_free_items():
    warehouse = Warehouse({"D": 1})
    processor = OrderProcessor(warehouse)

    with pytest.raises(ValueError):
        processor.process_order(
            order_id="ORD5",
            user_data={
                "email": "safe@example.com",
                "age": 25,
                "tier": "STANDARD",
                "payment_method": "CC",
            },
            items=[{"id": "D", "qty": -1, "price": 0.0}],
            promo_code=None,
        )

import pytest

# ---------- Warehouse.check_stock Tests ----------
@pytest.mark.parametrize(
    "initial_stock,item_id,quantity,expected",
    [
        ({"A": 5}, "A", 3, True),
    ],
)
def test_warehouse_check_stock_success(initial_stock, item_id, quantity, expected):
    wh = Warehouse(initial_stock)
    assert wh.check_stock(item_id, quantity) == expected


# ---------- OrderProcessor.process_order InventoryError Rollback Test ----------
def test_orderprocess_inv_error_rollback():
    warehouse = Warehouse({"A": 2, "B": 0})
    processor = OrderProcessor(warehouse)

    result = processor.process_order(
        order_id="ORD_ROLLBACK",
        user_data={
            "email": "rollback@example.com",
            "age": 30,
            "tier": "STANDARD",
            "payment_method": "CC",
        },
        items=[
            {"id": "A", "qty": 1, "price": 10.0},
            {"id": "B", "qty": 1, "price": 5.0},
        ],
        promo_code=None,
    )

    assert result == {
        "status": "failed",
        "reason": "Out of stock: Insufficient stock for B",
    }


# ---------- OrderProcessor.validate_user Success Test ----------
def test_orderprocess_validate_user_success():
    processor = OrderProcessor(Warehouse({}))
    # Should not raise any exception
    processor.validate_user("valid@example.com", 18)

# ---------- Warehouse.check_stock Unknown Item Test ----------
def test_warehouse_check_stock_unknown_item():
    wh = Warehouse({"A": 5})
    with pytest.raises(InventoryError):
        wh.check_stock("Z", 1)


# ---------- OrderProcessor.process_order Promo Applied Test ----------
def test_process_order_promo_applied():
    warehouse = Warehouse({"A": 2, "B": 1})
    processor = OrderProcessor(warehouse)

    with patch("data.input_code.d06_complex_logic.datetime") as mock_dt:
        mock_dt.now.return_value = type("dt", (), {"hour": 12})  # non-night hour
        result = processor.process_order(
            order_id="ORD_PROMO",
            user_data={
                "email": "buyer@example.com",
                "age": 28,
                "tier": "STANDARD",
                "payment_method": "CC",
            },
            items=[
                {"id": "A", "qty": 2, "price": 5.0},
                {"id": "B", "qty": 1, "price": 10.0},
            ],
            promo_code="ABC-123",
        )

    assert result == {
        "status": "success",
        "order_id": "ORD_PROMO",
        "original_price": 20.0,
        "discount_applied": 0.10,
        "final_total": 21.96,
        "items_count": 2,
    }


# ---------- OrderProcessor.process_order Invalid User Test ----------
def test_process_order_invalid_user():
    warehouse = Warehouse({"A": 1})
    processor = OrderProcessor(warehouse)

    with pytest.raises(UserValidationError):
        processor.process_order(
            order_id="ORD_INVALID",
            user_data={
                "email": "invalid-email",
                "age": 25,
                "tier": "STANDARD",
                "payment_method": "CC",
            },
            items=[{"id": "A", "qty": 1, "price": 10.0}],
            promo_code=None,
        )