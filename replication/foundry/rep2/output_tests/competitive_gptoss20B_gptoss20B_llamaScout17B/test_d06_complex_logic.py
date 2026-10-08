import pytest
from data.input_code.d06_complex_logic import *
from unittest.mock import patch
from datetime import datetime

@pytest.mark.parametrize('email, age', [
    ('not-an-email', 30),
    ('user@example.com', 17),
])
def test_validate_user_raises(email, age):
    warehouse = Warehouse({"A": 5})
    processor = OrderProcessor(warehouse)
    with pytest.raises(UserValidationError):
        processor.validate_user(email, age)

@pytest.mark.parametrize('case', [
    {
        "order_id": "T3",
        "user_data": {"email": "tester@example.com", "age": 30, "payment_method": "CC"},
        "items": [{"id": "X", "qty": 1, "price": 10.0}],
        "promo_code": None,
        "warehouse_initial_stock": {"A": 5},
        "expected": {"status": "failed", "reason": "Out of stock: Item X not found in warehouse."}
    },
    {
        "order_id": "T4",
        "user_data": {"email": "tester@example.com", "age": 30, "payment_method": "CC"},
        "items": [{"id": "A", "qty": 99, "price": 1.0}],
        "promo_code": None,
        "warehouse_initial_stock": {"A": 5},
        "expected": {"status": "failed", "reason": "Out of stock: Insufficient stock for A"}
    },
    {
        "order_id": "T5",
        "user_data": {"email": "tester@example.com", "age": 25, "payment_method": "CC"},
        "items": [{"id": "A", "qty": -1, "price": 0.0}],
        "promo_code": None,
        "warehouse_initial_stock": {"A": 5},
        "expected": ValueError
    },
    {
        "order_id": "T6",
        "user_data": {"email": "tester@example.com", "age": 28, "payment_method": "CC"},
        "items": [{"id": "A", "qty": 1, "price": 1.0}],
        "promo_code": "abc-123",
        "warehouse_initial_stock": {"A": 5},
        "expected": {"status": "error", "reason": "Promo Error: Invalid promo code format"}
    },
    {
        "order_id": "T7",
        "user_data": {"email": "tester@example.com", "age": 28, "payment_method": "CC", "tier": "GOLD"},
        "items": [{"id": "A", "qty": 2, "price": 100.0}],
        "promo_code": "ABC-999",
        "warehouse_initial_stock": {"A": 10},
        "expected": {
            "status": "success",
            "order_id": "T7",
            "original_price": 200.0,
            "discount_applied": 100.0,
            "final_total": -24156.0,
            "items_count": 1
        }
    },
    {
        "order_id": "T8",
        "user_data": {"email": "tester@example.com", "age": 30, "payment_method": "CRYPTO"},
        "items": [{"id": "A", "qty": 1, "price": 10.0}],
        "promo_code": None,
        "warehouse_initial_stock": {"A": 5},
        "expected": PaymentError
    },
    {
        "order_id": "T9",
        "user_data": {"email": "tester@example.com", "age": 30, "payment_method": "PAYPAL"},
        "items": [{"id": "A", "qty": 2, "price": 20.0}],
        "promo_code": None,
        "warehouse_initial_stock": {"A": 5},
        "expected": {
            "status": "success",
            "order_id": "T9",
            "original_price": 40.0,
            "discount_applied": 0.0,
            "final_total": 48.8,
            "items_count": 1
        }
    }
])
@patch('data.input_code.d06_complex_logic.datetime')
def test_process_order_cases(mock_datetime, case):
    mock_datetime.now.return_value = datetime(2023, 1, 1, 12, 0, 0)  # Mock datetime.now()
    warehouse = Warehouse(dict(case["warehouse_initial_stock"]))
    processor = OrderProcessor(warehouse)

    order_id = case["order_id"]
    user_data = case["user_data"]
    items = case["items"]
    promo_code = case.get("promo_code")

    expected = case["expected"]
    if isinstance(expected, type) and issubclass(expected, Exception):
        with pytest.raises(expected):
            processor.process_order(order_id, user_data, items, promo_code)
    else:
        result = processor.process_order(order_id, user_data, items, promo_code)
        assert result == expected

import pytest
@pytest.mark.parametrize("case", [
    {"total_amount": 400.0, "user_tier": "STANDARD", "promo_code": "XYZ-999", "expected": 200.0},
    {"total_amount": 1200.0, "user_tier": "PLATINUM", "promo_code": None, "expected": 0.25},
    {"total_amount": 1200.0, "user_tier": "PLATINUM", "promo_code": "ABC-123", "expected": 0.35}
])
@patch('data.input_code.d06_complex_logic.datetime')
def test_discount_engine_calculation(mock_datetime, case):
    mock_datetime.now.return_value = datetime(2023, 1, 1, 12, 0, 0)
    result = DiscountEngine.calculate_discount(
        total_amount=case["total_amount"],
        user_tier=case["user_tier"],
        promo_code=case.get("promo_code")
    )
    assert result == pytest.approx(case["expected"], rel=1e-9)

import pytest

def test_validate_user_age_over_100_raises():
    warehouse = Warehouse({"A": 5})
    processor = OrderProcessor(warehouse)
    with pytest.raises(UserValidationError):
        processor.validate_user("user@example.com", 101)

def test_process_order_invalid_email_raises():
    warehouse = Warehouse({"A": 5})
    processor = OrderProcessor(warehouse)
    order_id = "T11"
    user_data = {"email": "not-an-email", "age": 25}
    items = [{"id": "A", "qty": 1, "price": 5.0}]
    promo_code = None
    with pytest.raises(UserValidationError):
        processor.process_order(order_id, user_data, items, promo_code)

@pytest.mark.parametrize('case', [
    {
        "order_id": "T12",
        "user_data": {"email": "tester@example.com", "age": 30, "payment_method": "CC"},
        "items": [
            {"id": "A", "qty": 1, "price": 5.0},
            {"id": "B", "qty": 1, "price": 5.0}
        ],
        "promo_code": None,
        "warehouse_initial_stock": {"A": 5, "B": 0},
        "expected": {"status": "failed", "reason": "Out of stock: Insufficient stock for B"}
    },
    {
        "order_id": "T13",
        "user_data": {"email": "tester@example.com", "age": 101, "payment_method": "CC"},
        "items": [{"id": "A", "qty": 1, "price": 5.0}],
        "promo_code": None,
        "warehouse_initial_stock": {"A": 5},
        "expected": UserValidationError
    }
])
@patch('data.input_code.d06_complex_logic.datetime')
def test_new_process_order_cases(mock_datetime, case):
    mock_datetime.now.return_value = datetime(2023, 1, 1, 12, 0, 0)  
    warehouse = Warehouse(dict(case["warehouse_initial_stock"]))
    processor = OrderProcessor(warehouse)

    order_id = case["order_id"]
    user_data = case["user_data"]
    items = case["items"]
    promo_code = case.get("promo_code")

    expected = case["expected"]
    if isinstance(expected, type) and issubclass(expected, Exception):
        with pytest.raises(expected):
            processor.process_order(order_id, user_data, items, promo_code)
    else:
        result = processor.process_order(order_id, user_data, items, promo_code)
        assert result == expected