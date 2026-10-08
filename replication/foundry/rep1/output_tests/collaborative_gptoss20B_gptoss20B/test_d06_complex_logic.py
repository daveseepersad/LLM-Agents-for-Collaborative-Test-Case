import pytest
from data.input_code.d06_complex_logic import *

def _mock_datetime_now_hour(monkeypatch, hour: int):
    import data.input_code.d06_complex_logic as mod
    class DummyDateTime:
        @classmethod
        def now(cls):
            class _Now:
                pass
            _Now.hour = hour
            return _Now()
    monkeypatch.setattr(mod, "datetime", DummyDateTime)

# T1-T3: Validation errors for invalid user data
@pytest.mark.parametrize("email, age", [
    ("bad-email", 25),        # T1
    ("test@example.com", 17), # T2
    ("test@example.com", 101) # T3
])
def test_validate_user_errors(email, age):
    processor = OrderProcessor(Warehouse({"item1": 5}))
    with pytest.raises(UserValidationError):
        processor.validate_user(email, age)

# T4-T11: Process orders with various scenarios
test_cases = [
    # T4_INVENTORY_ITEM_NOT_FOUND
    {
        "id": "T4_INVENTORY_ITEM_NOT_FOUND",
        "input": {
            "warehouse_stock": {"item1": 5},
            "order_id": "ORD-004",
            "user_data": {"email": "buyer@example.com", "age": 30},
            "items": [
                {"id": "item2", "qty": 1, "price": 10.0}
            ],
            "promo_code": None
        },
        "expected": {"status": "failed", "reason": "Out of stock: Item item2 not found in warehouse."}
    },
    # T5_ORDER_SUCCESS_NO_DISCOUNT_NO_TAX
    {
        "id": "T5_ORDER_SUCCESS_NO_DISCOUNT_NO_TAX",
        "input": {
            "warehouse_stock": {"item1": 5},
            "order_id": "ORD-005",
            "user_data": {"email": "alice@example.com", "age": 30},
            "items": [
                {"id": "item1", "qty": 2, "price": 10.0}
            ],
            "promo_code": None
        },
        "expected": {"status": "success", "order_id": "ORD-005", "original_price": 20.0, "discount_applied": 0.0, "final_total": 24.4, "items_count": 1}
    },
    # T6_ORDER_CRYPTO_BELOW_MINIMUM
    {
        "id": "T6_ORDER_CRYPTO_BELOW_MINIMUM",
        "input": {
            "warehouse_stock": {"item1": 5},
            "order_id": "ORD-006",
            "user_data": {"email": "user6@example.com", "age": 30, "payment_method": "CRYPTO"},
            "items": [
                {"id": "item1", "qty": 1, "price": 20.0}
            ],
            "promo_code": None
        },
        "expected": "PaymentError"
    },
    # T7_PROMO_INVALID_FORMAT
    {
        "id": "T7_PROMO_INVALID_FORMAT",
        "input": {
            "warehouse_stock": {"item1": 5},
            "order_id": "ORD-007",
            "user_data": {"email": "promo@example.com", "age": 40},
            "items": [
                {"id": "item1", "qty": 1, "price": 50.0}
            ],
            "promo_code": "INVALID"
        },
        "expected": {"status": "error", "reason": "Promo Error: Invalid promo code format"}
    },
    # T8_PROMO_999_HALF_PRICE
    {
        "id": "T8_PROMO_999_HALF_PRICE",
        "input": {
            "warehouse_stock": {"item1": 5},
            "order_id": "ORD-008",
            "user_data": {"email": "promo999@example.com", "age": 28},
            "items": [
                {"id": "item1", "qty": 2, "price": 50.0}
            ],
            "promo_code": "ABC-999"
        },
        "expected": {"status": "success", "order_id": "ORD-008", "original_price": 100.0, "discount_applied": 50.0, "final_total": -5978.0, "items_count": 1}
    },
    # T9_ORDER_GOLD_NO_PROMO
    {
        "id": "T9_ORDER_GOLD_NO_PROMO",
        "input": {
            "warehouse_stock": {"item1": 5},
            "order_id": "ORD-009",
            "user_data": {"email": "gold@example.com", "age": 40, "tier": "GOLD"},
            "items": [
                {"id": "item1", "qty": 2, "price": 100.0}
            ],
            "promo_code": None
        },
        "expected": {"status": "success", "order_id": "ORD-009", "original_price": 200.0, "discount_applied": 0.1, "final_total": 219.6, "items_count": 1}
    },
    # T10_ORDER_PLATINUM_LARGE
    {
        "id": "T10_ORDER_PLATINUM_LARGE",
        "input": {
            "warehouse_stock": {"item1": 10},
            "order_id": "ORD-010",
            "user_data": {"email": "platinum@example.com", "age": 35, "tier": "PLATINUM"},
            "items": [
                {"id": "item1", "qty": 1, "price": 1200.0}
            ],
            "promo_code": None
        },
        "expected": {"status": "success", "order_id": "ORD-010", "original_price": 1200.0, "discount_applied": 0.25, "final_total": 1098.0, "items_count": 1}
    },
    # T11_ZERO_ITEMS
    {
        "id": "T11_ZERO_ITEMS",
        "input": {
            "warehouse_stock": {"item1": 5},
            "order_id": "ORD-011",
            "user_data": {"email": "zero@example.com", "age": 25},
            "items": [],
            "promo_code": None
        },
        "expected": {"status": "success", "order_id": "ORD-011", "original_price": 0.0, "discount_applied": 0.0, "final_total": 0.0, "items_count": 0}
    },
]

@pytest.mark.parametrize("case", test_cases)
def test_order_processing(case, monkeypatch):
    # Ensure deterministic discount by mocking current hour to a non-night value
    _mock_datetime_now_hour(monkeypatch, 12)

    input_data = case["input"]
    warehouse = Warehouse(dict(input_data["warehouse_stock"]))
    processor = OrderProcessor(warehouse)

    order_id = input_data["order_id"]
    user_data = input_data["user_data"]
    items = input_data["items"]
    promo_code = input_data.get("promo_code", None)

    expected = case["expected"]

    if isinstance(expected, dict):
        result = processor.process_order(order_id, user_data, items, promo_code)
        assert result == expected
    else:
        with pytest.raises(globals()[expected]):
            processor.process_order(order_id, user_data, items, promo_code)

import pytest
from data.input_code.d06_complex_logic import *

def test_t12_insufficient_stock():
    warehouse = Warehouse({"item1": 1})
    processor = OrderProcessor(warehouse)
    result = processor.process_order(
        "ORD-012",
        {"email": "stock@example.com", "age": 28},
        [{"id": "item1", "qty": 2, "price": 5.0}],
        None
    )
    assert result == {
        "status": "failed",
        "reason": "Out of stock: Insufficient stock for item1"
    }

def test_t13_night_platinum_cap40(monkeypatch):
    import data.input_code.d06_complex_logic as mod

    class DummyDateTime:
        @classmethod
        def now(cls):
            class _Now:
                pass
            _Now.hour = 2  # Night discount
            return _Now()

    monkeypatch.setattr(mod, "datetime", DummyDateTime)

    warehouse = Warehouse({"item1": 5})
    processor = OrderProcessor(warehouse)
    result = processor.process_order(
        "ORD-013",
        {"email": "nightplatinum@example.com", "age": 40, "tier": "PLATINUM"},
        [{"id": "item1", "qty": 2, "price": 600.0}],
        "ABC-123"
    )
    assert result == {
        "status": "success",
        "order_id": "ORD-013",
        "original_price": 1200.0,
        "discount_applied": 0.40,
        "final_total": 878.4,
        "items_count": 1
    }

def test_t14_return_free_items_valueerror():
    warehouse = Warehouse({"item1": 10})
    processor = OrderProcessor(warehouse)
    with pytest.raises(ValueError):
        processor.process_order(
            "ORD-014",
            {"email": "edge2@example.com", "age": 25},
            [{"id": "item1", "qty": -1, "price": 0.0}],
            None
        )