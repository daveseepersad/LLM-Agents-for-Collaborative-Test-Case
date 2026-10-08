import pytest
from data.input_code.d06_complex_logic import *
import data.input_code.d06_complex_logic as d06

def make_mock_datetime_cls(hour: int):
    class MockDateTime:
        @classmethod
        def now(cls):
            class NowObj:
                pass
            n = NowObj()
            n.hour = hour
            return n
    return MockDateTime

CASES = [
    {
        "id": "TC01_SUCCESS_STANDARD",
        "mock_datetime_hour": 12,
        "order_input": {
            "order_id": "ORD001",
            "user_data": {"email": "john.doe@example.com", "age": 30, "tier": "GOLD", "payment_method": "CC"},
            "items": [{"id": "itemA", "qty": 2, "price": 50.0}],
            "promo_code": None,
            "warehouse_stock": {"itemA": 10}
        },
        "expected": {
            "status": "success",
            "order_id": "ORD001",
            "original_price": 100.0,
            "discount_applied": 0.10,
            "final_total": 109.8,
            "items_count": 1
        }
    },
    {
        "id": "TC02_NIGHT_OWL_DISCOUNT",
        "mock_datetime_hour": 2,
        "order_input": {
            "order_id": "ORD002",
            "user_data": {"email": "alice@example.org", "age": 45, "tier": "STANDARD", "payment_method": "CC"},
            "items": [{"id": "itemB", "qty": 1, "price": 200.0}],
            "promo_code": None,
            "warehouse_stock": {"itemB": 5}
        },
        "expected": {
            "status": "success",
            "order_id": "ORD002",
            "original_price": 200.0,
            "discount_applied": 0.05,
            "final_total": 231.8,
            "items_count": 1
        }
    },
    {
        "id": "TC03_PLATINUM_HIGH_AMOUNT",
        "mock_datetime_hour": 12,
        "order_input": {
            "order_id": "ORD003",
            "user_data": {"email": "bob@example.com", "age": 55, "tier": "PLATINUM", "payment_method": "CC"},
            "items": [{"id": "itemC", "qty": 1, "price": 1500.0}],
            "promo_code": None,
            "warehouse_stock": {"itemC": 2}
        },
        "expected": {
            "status": "success",
            "order_id": "ORD003",
            "original_price": 1500.0,
            "discount_applied": 0.25,
            "final_total": 1372.5,
            "items_count": 1
        }
    },
    {
        "id": "TC04_PROMO_VALID",
        "mock_datetime_hour": 12,
        "order_input": {
            "order_id": "ORD004",
            "user_data": {"email": "carol@example.net", "age": 28, "tier": "STANDARD", "payment_method": "CC"},
            "items": [{"id": "itemD", "qty": 3, "price": 30.0}],
            "promo_code": "ABC-123",
            "warehouse_stock": {"itemD": 10}
        },
        "expected": {
            "status": "success",
            "order_id": "ORD004",
            "original_price": 90.0,
            "discount_applied": 0.10,
            "final_total": 98.82,
            "items_count": 1
        }
    },
    {
        "id": "TC05_PROMO_SUPER",
        "mock_datetime_hour": 12,
        "order_input": {
            "order_id": "ORD005",
            "user_data": {"email": "dave@example.org", "age": 40, "tier": "STANDARD", "payment_method": "CC"},
            "items": [{"id": "itemE", "qty": 2, "price": 250.0}],
            "promo_code": "XYZ-999",
            "warehouse_stock": {"itemE": 5}
        },
        "expected": {
            "status": "success",
            "order_id": "ORD005",
            "original_price": 500.0,
            "discount_applied": 250.0,
            "final_total": -151890.0,
            "items_count": 1
        }
    },
    {
        "id": "TC06_PROMO_INVALID",
        "mock_datetime_hour": 12,
        "order_input": {
            "order_id": "ORD006",
            "user_data": {"email": "eve@example.com", "age": 35, "tier": "STANDARD", "payment_method": "CC"},
            "items": [{"id": "itemF", "qty": 1, "price": 100.0}],
            "promo_code": "badcode",
            "warehouse_stock": {"itemF": 3}
        },
        "expected": {
            "status": "error",
            "reason": "Promo Error: Invalid promo code format"
        }
    },
    {
        "id": "TC07_INVENTORY_INSUFFICIENT",
        "mock_datetime_hour": 12,
        "order_input": {
            "order_id": "ORD007",
            "user_data": {"email": "frank@example.com", "age": 50, "tier": "STANDARD", "payment_method": "CC"},
            "items": [{"id": "itemG", "qty": 5, "price": 20.0}],
            "promo_code": None,
            "warehouse_stock": {"itemG": 3}
        },
        "expected": {
            "status": "failed",
            "reason": "Out of stock: Insufficient stock for itemG"
        }
    },
    {
        "id": "TC08_USER_INVALID_EMAIL",
        "mock_datetime_hour": 12,
        "order_input": {
            "order_id": "ORD008",
            "user_data": {"email": "invalid-email", "age": 25, "tier": "STANDARD", "payment_method": "CC"},
            "items": [{"id": "itemH", "qty": 1, "price": 10.0}],
            "promo_code": None,
            "warehouse_stock": {"itemH": 5}
        },
        "expected": {
            "status": "error",
            "reason": "UserValidationError"
        }
    },
    {
        "id": "TC09_USER_UNDERAGE",
        "mock_datetime_hour": 12,
        "order_input": {
            "order_id": "ORD009",
            "user_data": {"email": "young@example.com", "age": 16, "tier": "STANDARD", "payment_method": "CC"},
            "items": [{"id": "itemI", "qty": 1, "price": 15.0}],
            "promo_code": None,
            "warehouse_stock": {"itemI": 5}
        },
        "expected": {
            "status": "error",
            "reason": "UserValidationError"
        }
    },
    {
        "id": "TC10_USER_OVER_100",
        "mock_datetime_hour": 12,
        "order_input": {
            "order_id": "ORD010",
            "user_data": {"email": "oldtimer@example.com", "age": 101, "tier": "STANDARD", "payment_method": "CC"},
            "items": [{"id": "itemJ", "qty": 1, "price": 30.0}],
            "promo_code": None,
            "warehouse_stock": {"itemJ": 5}
        },
        "expected": {
            "status": "error",
            "reason": "UserValidationError"
        }
    },
    {
        "id": "TC11_HIDDEN_DIVISION_ERROR",
        "mock_datetime_hour": 12,
        "order_input": {
            "order_id": "ORD011",
            "user_data": {"email": "returner@example.com", "age": 40, "tier": "STANDARD", "payment_method": "CC"},
            "items": [{"id": "itemK", "qty": -1, "price": 0.0}],
            "promo_code": None,
            "warehouse_stock": {"itemK": 10}
        },
        "expected": {
            "status": "error",
            "reason": "ValueError"
        }
    },
    {
        "id": "TC12_PAYPAL_FRAUD",
        "mock_datetime_hour": 12,
        "order_input": {
            "order_id": "ORD012",
            "user_data": {"email": "fraud@example.com", "age": 35, "tier": "STANDARD", "payment_method": "PAYPAL"},
            "items": [{"id": "itemL", "qty": 1, "price": 546.44}],
            "promo_code": None,
            "warehouse_stock": {"itemL": 2}
        },
        "expected": {
            "status": "error",
            "reason": "FraudDetectedError"
        }
    },
    {
        "id": "TC13_CRYPTO_MIN_AMOUNT",
        "mock_datetime_hour": 12,
        "order_input": {
            "order_id": "ORD013",
            "user_data": {"email": "crypto@example.com", "age": 29, "tier": "STANDARD", "payment_method": "CRYPTO"},
            "items": [{"id": "itemM", "qty": 1, "price": 40.0}],
            "promo_code": None,
            "warehouse_stock": {"itemM": 5}
        },
        "expected": {
            "status": "error",
            "reason": "PaymentError"
        }
    }
]

@pytest.mark.parametrize("case", CASES, ids=[c["id"] for c in CASES])
def test_order_processor_cases(case, monkeypatch):
    # Patch datetime to control discount timing
    hour = case.get("mock_datetime_hour", 12)
    monkeypatch.setattr(d06, "datetime", make_mock_datetime_cls(hour))

    input_data = case["order_input"]
    warehouse = Warehouse(input_data["warehouse_stock"])
    processor = OrderProcessor(warehouse)

    order_id = input_data["order_id"]
    user_data = input_data["user_data"]
    items = input_data["items"]
    promo_code = input_data.get("promo_code")

    expected = case.get("expected")

    exception_map = {
        "UserValidationError": d06.UserValidationError,
        "FraudDetectedError": d06.FraudDetectedError,
        "PaymentError": d06.PaymentError,
        "ValueError": ValueError,
        "InventoryError": d06.InventoryError,
    }

    expect_exc = None
    if isinstance(expected, dict) and "reason" in expected:
        reason = expected["reason"]
        if isinstance(reason, str) and reason in exception_map:
            expect_exc = exception_map[reason]

    if expect_exc:
        with pytest.raises(expect_exc):
            processor.process_order(order_id=order_id, user_data=user_data, items=items, promo_code=promo_code)
        return

    result = processor.process_order(order_id=order_id, user_data=user_data, items=items, promo_code=promo_code)

    assert isinstance(expected, dict)
    assert result == expected

def test_T01_WAREHOUSE_ITEM_NOT_FOUND():
    w = Warehouse({"itemA": 5})
    with pytest.raises(d06.InventoryError):
        w.check_stock("missing_item", 1)

def test_T02_WAREHOUSE_RELEASE_DELETION():
    w = Warehouse({"itemX": 5})
    w.lock_item("itemX", 2)
    w.release_item("itemX", 2)
    assert w._locked_stock == {}

def test_T03_DISCOUNT_PLATINUM_NO_EXTRA(monkeypatch):
    monkeypatch.setattr(d06, "datetime", make_mock_datetime_cls(12))
    result = DiscountEngine.calculate_discount(800.0, "PLATINUM", None)
    assert result == 0.20

def test_T04_DISCOUNT_NIGHT_EDGE_NO_DISCOUNT(monkeypatch):
    monkeypatch.setattr(d06, "datetime", make_mock_datetime_cls(6))
    result = DiscountEngine.calculate_discount(100.0, "STANDARD", None)
    assert result == 0.0

def test_T05_DISCOUNT_NIGHT_EDGE_WITH_DISCOUNT(monkeypatch):
    monkeypatch.setattr(d06, "datetime", make_mock_datetime_cls(0))
    result = DiscountEngine.calculate_discount(100.0, "STANDARD", None)
    assert result == 0.05

def test_T06_VALIDATE_USER_EDGE_AGE_18():
    o = OrderProcessor(Warehouse({}))
    o.validate_user("valid18@example.com", 18)

def test_T07_VALIDATE_USER_EDGE_AGE_100():
    o = OrderProcessor(Warehouse({}))
    o.validate_user("valid100@example.com", 100)

def test_T08_PROCESS_ORDER_MULTIPLE_ITEMS_INVENTORY_FAIL_ROLLBACK():
    warehouse = Warehouse({"item1": 5, "item2": 3})
    processor = OrderProcessor(warehouse)
    order_id = "ORD008"
    user_data = {"email": "user@example.com", "age": 30, "tier": "STANDARD", "payment_method": "CC"}
    items = [
        {"id": "item1", "qty": 2, "price": 20.0},
        {"id": "item2", "qty": 4, "price": 15.0}
    ]
    promo_code = None
    result = processor.process_order(order_id, user_data, items, promo_code)
    expected = {"status": "failed", "reason": "Out of stock: Insufficient stock for item2"}
    assert result == expected

def test_T09_PROCESS_ORDER_PAYPAL_SUCCESS(monkeypatch):
    monkeypatch.setattr(d06, "datetime", make_mock_datetime_cls(12))
    warehouse = Warehouse({"itemP": 10})
    processor = OrderProcessor(warehouse)
    order_id = "ORD009"
    user_data = {"email": "paypal@example.com", "age": 35, "tier": "STANDARD", "payment_method": "PAYPAL"}
    items = [{"id": "itemP", "qty": 1, "price": 100.0}]
    result = processor.process_order(order_id, user_data, items, promo_code=None)
    expected = {
        "status": "success",
        "order_id": "ORD009",
        "original_price": 100.0,
        "discount_applied": 0.0,
        "final_total": 122.0,
        "items_count": 1
    }
    assert result == expected

def test_T10_PROCESS_ORDER_CRYPTO_SUCCESS(monkeypatch):
    monkeypatch.setattr(d06, "datetime", make_mock_datetime_cls(12))
    warehouse = Warehouse({"itemC": 5})
    processor = OrderProcessor(warehouse)
    order_id = "ORD010"
    user_data = {"email": "crypto@example.com", "age": 28, "tier": "STANDARD", "payment_method": "CRYPTO"}
    items = [{"id": "itemC", "qty": 1, "price": 60.0}]
    result = processor.process_order(order_id, user_data, items, promo_code=None)
    expected = {
        "status": "success",
        "order_id": "ORD010",
        "original_price": 60.0,
        "discount_applied": 0.0,
        "final_total": 73.2,
        "items_count": 1
    }
    assert result == expected