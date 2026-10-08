import pytest
from types import SimpleNamespace
from data.input_code.d06_complex_logic import *

# Helper to freeze time for DiscountEngine tests
def patch_time_to(hour, monkeypatch):
    monkeypatch.setattr(
        'data.input_code.d06_complex_logic.datetime',
        SimpleNamespace(now=lambda: SimpleNamespace(hour=hour))
    )

# 1) Validate user tests
@pytest.mark.parametrize('email, age, expected_exception', [
    ('test@example.com', 25, None),                 # T1_VALID_USER
    ('invalid', 25, UserValidationError),           # T2_INVALID_EMAIL
    ('test@example.com', 17, UserValidationError),  # T3_UNDERAGE_USER
    ('test@example.com', 101, UserValidationError), # T4_OVER100_USER
])
def test_validate_user_variants(email, age, expected_exception):
    op = OrderProcessor(Warehouse({'item1': 10}))
    if expected_exception:
        with pytest.raises(expected_exception):
            op.validate_user(email, age)
    else:
        op.validate_user(email, age)

# 2) Warehouse stock tests
def test_check_stock_ok():
    w = Warehouse({'item1': 10})
    assert w.check_stock('item1', 5) is True  # T5_STOCK_CHECK_OK

def test_check_stock_item_not_found_raises():
    w = Warehouse({'item1': 10})
    with pytest.raises(InventoryError):  # T6_STOCK_CHECK_FAIL
        w.check_stock('item2', 5)

def test_lock_item_ok():
    w = Warehouse({'item1': 10})
    w.lock_item('item1', 5)  # T7_LOCK_ITEM_OK
    assert w._locked_stock.get('item1', 0) == 5

def test_lock_item_fail():
    w = Warehouse({'item1': 10})
    with pytest.raises(InventoryError):  # T8_LOCK_ITEM_FAIL
        w.lock_item('item1', 15)

# 3) DiscountEngine tests (time-dependent; patch to deterministic hour)
def test_discount_standard_no_time(monkeypatch):
    patch_time_to(12, monkeypatch)  # Ensure not in night window
    assert DiscountEngine.calculate_discount(100.0, 'STANDARD') == 0.0  # T9

def test_discount_gold(monkeypatch):
    patch_time_to(12, monkeypatch)
    assert DiscountEngine.calculate_discount(100.0, 'GOLD') == 0.10  # T10

def test_discount_platinum(monkeypatch):
    patch_time_to(12, monkeypatch)
    assert DiscountEngine.calculate_discount(100.0, 'PLATINUM') == 0.20  # T11

def test_discount_platinum_high_amount(monkeypatch):
    patch_time_to(12, monkeypatch)
    assert DiscountEngine.calculate_discount(1500.0, 'PLATINUM') == 0.25  # T12

def test_discount_promo_valid_standard(monkeypatch):
    patch_time_to(12, monkeypatch)
    assert DiscountEngine.calculate_discount(100.0, 'STANDARD', 'ABC-123') == 0.10  # T13

def test_discount_promo_invalid_raises(monkeypatch):
    patch_time_to(12, monkeypatch)
    with pytest.raises(ValueError):  # T14
        DiscountEngine.calculate_discount(100.0, 'STANDARD', 'invalid')

def test_discount_promo_super(monkeypatch):
    patch_time_to(12, monkeypatch)
    assert DiscountEngine.calculate_discount(100.0, 'STANDARD', 'ABC-999') == 50.0  # T15

# 4) Order processing tests
def test_process_order_ok(monkeypatch):
    patch_time_to(12, monkeypatch)
    warehouse = Warehouse({'item1': 10})
    op = OrderProcessor(warehouse)
    result = op.process_order(
        order_id="1",
        user_data={"email": "test@example.com", "age": 25, "tier": "STANDARD"},
        items=[{"id": "item1", "qty": 1, "price": 10.0}]
    )
    assert result["status"] == "success"
    assert result["order_id"] == "1"
    assert result["original_price"] == 10.0
    assert result["discount_applied"] == 0.0
    assert result["final_total"] == 12.2
    assert result["items_count"] == 1

def test_process_order_stock_fail(monkeypatch):
    # T17: insufficient stock should lead to failed status
    warehouse = Warehouse({'item1': 10})
    op = OrderProcessor(warehouse)
    result = op.process_order(
        order_id="1",
        user_data={"email": "test@example.com", "age": 25, "tier": "STANDARD"},
        items=[{"id": "item1", "qty": 15, "price": 10.0}]
    )
    # Since stock check happens before discount, it should fail with status "failed"
    assert result["status"] == "failed"
    assert "Out of stock" in result.get("reason", "")

def test_process_order_paypal_fraud(monkeypatch):
    # Patch discount to a value that makes final price exactly 666.66 after tax
    def fake_discount(total_amount, user_tier, promo_code=None):
        return 0.180327868852459
    monkeypatch.setattr(DiscountEngine, 'calculate_discount', staticmethod(fake_discount))
    warehouse = Warehouse({'item1': 10})
    op = OrderProcessor(warehouse)
    with pytest.raises(FraudDetectedError):  # T18
        op.process_order(
            order_id="1",
            user_data={"email": "test@example.com", "age": 25, "tier": "STANDARD", "payment_method": "PAYPAL"},
            items=[{"id": "item1", "qty": 1, "price": 666.66}]
        )

def test_process_order_crypto_fail(monkeypatch):
    patch_time_to(12, monkeypatch)
    warehouse = Warehouse({'item1': 10})
    op = OrderProcessor(warehouse)
    with pytest.raises(PaymentError):  # T19
        op.process_order(
            order_id="1",
            user_data={"email": "test@example.com", "age": 25, "tier": "STANDARD", "payment_method": "CRYPTO"},
            items=[{"id": "item1", "qty": 1, "price": 10.0}]
        )

def test_discount_missing_night_discount(monkeypatch):
    # Night discount should apply when hour is between 0 and 5
    patch_time_to(2, monkeypatch)
    assert DiscountEngine.calculate_discount(100.0, 'STANDARD') == 0.05

def test_discount_cap_with_night_and_platinum(monkeypatch):
    # Ensure cap is reached with night discount, platinum tier, and promo code
    patch_time_to(2, monkeypatch)
    assert DiscountEngine.calculate_discount(1000.01, 'PLATINUM', 'ABC-123') == 0.40

def test_order_process_return_free_items_raises():
    w = Warehouse({'item1': 5})
    op = OrderProcessor(w)
    with pytest.raises(ValueError):
        op.process_order(
            order_id="1",
            user_data={"email": "test@example.com", "age": 25},
            items=[{"id": "item1", "qty": -1, "price": 0.0}]
        )

def test_order_process_invalid_promo_code_rollback():
    warehouse = Warehouse({'item1': 5})
    op = OrderProcessor(warehouse)
    result = op.process_order(
        order_id="1",
        user_data={"email": "test@example.com", "age": 25, "tier": "STANDARD"},
        items=[{"id": "item1", "qty": 1, "price": 10.0}],
        promo_code="invalid"
    )
    assert result == {"status": "error", "reason": "Promo Error: Invalid promo code format"}

def test_order_process_paypal_normal_amount(monkeypatch):
    patch_time_to(12, monkeypatch)
    warehouse = Warehouse({'item1': 10})
    op = OrderProcessor(warehouse)
    result = op.process_order(
        order_id="1",
        user_data={"email": "test@example.com", "age": 25, "tier": "STANDARD", "payment_method": "PAYPAL"},
        items=[{"id": "item1", "qty": 1, "price": 100.0}]
    )
    assert result["status"] == "success"

def test_order_process_crypto_valid_amount(monkeypatch):
    patch_time_to(12, monkeypatch)
    warehouse = Warehouse({'item1': 1000})
    op = OrderProcessor(warehouse)
    result = op.process_order(
        order_id="1",
        user_data={"email": "test@example.com", "age": 25, "tier": "STANDARD", "price": 10.0, "payment_method": "CRYPTO"},
        items=[{"id": "item1", "qty": 10, "price": 10.0}]
    )
    assert result["status"] == "success"

def test_discount_night_gold(monkeypatch):
    patch_time_to(2, monkeypatch)
    assert DiscountEngine.calculate_discount(100.0, 'GOLD') == pytest.approx(0.15)

def test_order_processor_crypto_edge_case_success(monkeypatch):
    patch_time_to(12, monkeypatch)
    w = Warehouse({'item1': 10})
    op = OrderProcessor(w)
    result = op.process_order(
        order_id="1",
        user_data={"email": "test@example.com", "age": 25, "tier": "STANDARD", "payment_method": "CRYPTO"},
        items=[{"id": "item1", "qty": 5, "price": 10.0}]
    )
    assert result["status"] == "success"

def test_order_processor_paypal_normal_amount_taxed(monkeypatch):
    patch_time_to(12, monkeypatch)
    w = Warehouse({'item1': 10})
    op = OrderProcessor(w)
    result = op.process_order(
        order_id="1",
        user_data={"email": "test@example.com", "age": 25, "tier": "STANDARD", "payment_method": "PAYPAL"},
        items=[{"id": "item1", "qty": 1, "price": 100.0}]
    )
    assert result["status"] == "success"

def test_discount_cap_gold_with_night_and_promo(monkeypatch):
    patch_time_to(2, monkeypatch)
    assert DiscountEngine.calculate_discount(1000.0, 'GOLD', 'ABC-123') == 0.25

def test_warehouse_release_item_no_error():
    w = Warehouse({'item1': 5})
    w.lock_item('item1', 5)
    w.release_item('item1', 5)
    assert w._locked_stock.get('item1', 0) == 0

def test_warehouse_release_partial():
    w = Warehouse({'item1': 10})
    w.lock_item('item1', 5)
    w.release_item('item1', 3)
    assert w._locked_stock == {'item1': 2}

def test_warehouse_release_non_existent_item_no_change():
    w = Warehouse({'item1': 5})
    w.lock_item('item1', 2)
    w.release_item('nonexistent', 1)
    assert w._locked_stock == {'item1': 2}

def test_discount_standard_with_night(monkeypatch):
    patch_time_to(1, monkeypatch)
    assert DiscountEngine.calculate_discount(100.0, 'STANDARD') == 0.05

def test_process_order_invalid_user_data():
    w = Warehouse({'item1': 5})
    op = OrderProcessor(w)
    with pytest.raises(UserValidationError):
        op.process_order(
            order_id="1",
            user_data={},
            items=[{"id": "item1", "qty": 1, "price": 10.0}]
        )

def test_process_order_empty_items_list():
    w = Warehouse({'item1': 5})
    op = OrderProcessor(w)
    result = op.process_order(
        order_id="1",
        user_data={"email": "test@example.com", "age": 25},
        items=[]
    )
    expected = {
        "status": "success",
        "order_id": "1",
        "original_price": 0.0,
        "discount_applied": 0.0,
        "final_total": 0.0,
        "items_count": 0
    }
    assert result == expected

def test_process_order_price_zero_item(monkeypatch):
    patch_time_to(12, monkeypatch)
    w = Warehouse({'item1': 5})
    op = OrderProcessor(w)
    result = op.process_order(
        order_id="1",
        user_data={"email": "test@example.com", "age": 25},
        items=[{"id": "item1", "qty": 1, "price": 0.0}]
    )
    expected = {
        "status": "success",
        "order_id": "1",
        "original_price": 0.0,
        "discount_applied": 0.0,
        "final_total": 0.0,
        "items_count": 1
    }
    assert result == expected

def test_discount_promo_code_case_sensitivity(monkeypatch):
    patch_time_to(12, monkeypatch)
    with pytest.raises(ValueError):
        DiscountEngine.calculate_discount(100.0, 'STANDARD', 'abc-123')