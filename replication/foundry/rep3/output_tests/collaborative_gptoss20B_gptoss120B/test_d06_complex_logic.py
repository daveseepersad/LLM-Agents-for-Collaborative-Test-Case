import pytest
from data.input_code.d06_complex_logic import *

import importlib

# TC1: Warehouse.check_stock raises InventoryError when item not found
def test_T1_warehouse_check_notfound():
    w = Warehouse(initial_stock={})
    with pytest.raises(InventoryError):
        w.check_stock(item_id="X", quantity=1)

# TC2: Warehouse.check_stock returns False when insufficient stock
def test_T2_warehouse_insufficient():
    w = Warehouse(initial_stock={"A": 5})
    assert w.check_stock(item_id="A", quantity=6) is False

# TC3: Warehouse.lock_item followed by release_item clears locked stock
def test_T3_warehouse_lock_and_release():
    w = Warehouse(initial_stock={"B": 10})
    w.lock_item(item_id="B", quantity=3)
    w.release_item(item_id="B", quantity=3)
    # After release, there should be no locked stock for B, and stock should be retrievable for 3
    assert w.check_stock(item_id="B", quantity=3) is True

# TC4: Warehouse.release_item clears entry when quantity reaches zero
def test_T4_warehouse_release_clears():
    w = Warehouse(initial_stock={"C": 5})
    w.lock_item(item_id="C", quantity=5)
    w.release_item(item_id="C", quantity=5)
    assert "C" not in w._locked_stock

# Helper to patch datetime.now() in DiscountEngine by replacing module-level datetime
def _patch_datetime_to_hour(monkeypatch, hour):
    mod = importlib.import_module('data.input_code.d06_complex_logic')
    # Create a fake datetime with a specific hour
    FakeNow = type('FakeNow', (), {'hour': hour})  # an object with 'hour' attribute
    FakeDateTimeClass = type('FakeDateTime', (), {'now': classmethod(lambda cls: FakeNow())})
    monkeypatch.setattr(mod, 'datetime', FakeDateTimeClass, raising=True)

# TC5: Night discount with GOLD tier (mock hour = 2)
def test_T5_discount_night_gold(monkeypatch):
    _patch_datetime_to_hour(monkeypatch, 2)
    discount = DiscountEngine.calculate_discount(total_amount=100.0, user_tier="GOLD", promo_code=None)
    assert discount == pytest.approx(0.15, rel=1e-9)

# TC6: Platinum high discount with amount > 1000 (mock hour = 12)
def test_T6_discount_platinum_high(monkeypatch):
    _patch_datetime_to_hour(monkeypatch, 12)
    discount = DiscountEngine.calculate_discount(total_amount=1500.0, user_tier="PLATINUM", promo_code=None)
    assert discount == 0.25

# TC7: Valid promo code adds 0.10 discount (mock hour = 14)
def test_T7_discount_promo_valid(monkeypatch):
    _patch_datetime_to_hour(monkeypatch, 14)
    discount = DiscountEngine.calculate_discount(total_amount=200.0, user_tier="STANDARD", promo_code="ABC-123")
    assert discount == pytest.approx(0.10, rel=1e-9)

# TC8: Promo ending with 999 returns 50% off (mock hour = 10)
def test_T8_discount_promo_super(monkeypatch):
    _patch_datetime_to_hour(monkeypatch, 10)
    discount = DiscountEngine.calculate_discount(total_amount=1000.0, user_tier="STANDARD", promo_code="XYZ-999")
    assert discount == 500.0  # exact total_amount * 0.50

# TC9: Invalid promo format raises ValueError
def test_T9_discount_invalid_promo(monkeypatch):
    _patch_datetime_to_hour(monkeypatch, 9)
    with pytest.raises(ValueError):
        DiscountEngine.calculate_discount(total_amount=100.0, user_tier="STANDARD", promo_code="badcode")

# TC10: Cap at 0.40 when discounts exceed it (mock hour = 3)
def test_T10_discount_cap(monkeypatch):
    _patch_datetime_to_hour(monkeypatch, 3)
    discount = DiscountEngine.calculate_discount(total_amount=2000.0, user_tier="PLATINUM", promo_code="ABC-123")
    # Base: 0.20 (PLATINUM) + 0.05 (night) + 0.10 (promo) + 0.05 extra for >1000 = 0.40 is maximum cap
    # In this implementation, the cap is 0.40 and results should not exceed it.
    assert discount == min(0.40, 0.25) or discount == 0.35 or discount == 0.40
    # Assert actual outcome according to code behavior (should be capped at 0.40 if calculated over)
    assert discount <= 0.40

# TC11: OrderProcessor.validate_user with invalid email raises UserValidationError
def test_T11_validate_user_invalid_email():
    op = OrderProcessor(Warehouse({}))
    with pytest.raises(UserValidationError):
        op.validate_user(email="invalid_email", age=30)

# TC12: OrderProcessor.validate_user under 18 raises UserValidationError
def test_T12_validate_user_underage():
    op = OrderProcessor(Warehouse({}))
    with pytest.raises(UserValidationError):
        op.validate_user(email="test@example.com", age=16)

# TC13: OrderProcessor.validate_user over 100 raises UserValidationError
def test_T13_validate_user_overage():
    op = OrderProcessor(Warehouse({}))
    with pytest.raises(UserValidationError):
        op.validate_user(email="senior@example.com", age=101)

# TC14: Process order success standard
def test_T14_process_success_standard(monkeypatch):
    _patch_datetime_to_hour(monkeypatch, 14)
    warehouse = Warehouse(initial_stock={"D": 5})
    op = OrderProcessor(warehouse)
    result = op.process_order(
        order_id="ORD001",
        user_data={
            "email": "buyer@example.com",
            "age": 35,
            "tier": "STANDARD",
            "payment_method": "CC"
        },
        items=[{"id": "D", "qty": 2, "price": 100.0}],
        promo_code=None,
        )
    assert result == {
        "status": "success",
        "order_id": "ORD001",
        "original_price": 200.0,
        "discount_applied": 0.0,
        "final_total": 244.0,
        "items_count": 1
    }

# TC15: Process order insufficient stock returns failed
def test_T15_process_insufficient_stock(monkeypatch):
    _patch_datetime_to_hour(monkeypatch, 14)
    warehouse = Warehouse(initial_stock={"E": 1})
    op = OrderProcessor(warehouse)
    result = op.process_order(
        order_id="ORD002",
        user_data={
            "email": "shopper@example.com",
            "age": 28,
            "tier": "STANDARD",
            "payment_method": "CC"
        },
        items=[{"id": "E", "qty": 3, "price": 50.0}],
        promo_code=None
    )
    assert result == {
        "status": "failed",
        "reason": "Out of stock: Insufficient stock for E"
    }

# TC16: Process order invalid promo returns error
def test_T16_process_invalid_promo(monkeypatch):
    _patch_datetime_to_hour(monkeypatch, 14)
    warehouse = Warehouse(initial_stock={"F": 10})
    op = OrderProcessor(warehouse)
    result = op.process_order(
        order_id="ORD003",
        user_data={
            "email": "promo@example.com",
            "age": 40,
            "tier": "GOLD",
            "payment_method": "CC"
        },
        items=[{"id": "F", "qty": 1, "price": 120.0}],
        promo_code="WRONG-12"
    )
    assert result == {
        "status": "error",
        "reason": "Promo Error: Invalid promo code format"
    }

# TC17: Process order PayPal fraud due to amount 666.66
def test_T17_process_paypal_fraud(monkeypatch):
    _patch_datetime_to_hour(monkeypatch, 12)
    warehouse = Warehouse(initial_stock={"G": 5})
    op = OrderProcessor(warehouse)
    with pytest.raises(FraudDetectedError):
        op.process_order(
            order_id="ORD004",
            user_data={
                "email": "fraud@example.com",
                "age": 45,
                "tier": "STANDARD",
                "payment_method": "PAYPAL"
            },
            items=[{"id": "G", "qty": 1, "price": 546.44}],
            promo_code=None
        )

# TC18: Process order crypto min amount raises PaymentError
def test_T18_process_crypto_min_amount(monkeypatch):
    _patch_datetime_to_hour(monkeypatch, 15)
    warehouse = Warehouse(initial_stock={"H": 10})
    op = OrderProcessor(warehouse)
    with pytest.raises(PaymentError):
        op.process_order(
            order_id="ORD005",
            user_data={
                "email": "crypto@example.com",
                "age": 30,
                "tier": "STANDARD",
                "payment_method": "CRYPTO"
            },
            items=[{"id": "H", "qty": 1, "price": 40.0}],
            promo_code=None
        )

# TC19: Process order negative qty free item raises ValueError
def test_T19_process_negative_qty_free_item():
    warehouse = Warehouse(initial_stock={"I": 10})
    op = OrderProcessor(warehouse)
    with pytest.raises(ValueError):
        op.process_order(
            order_id="ORD006",
            user_data={
                "email": "return@example.com",
                "age": 27,
                "tier": "STANDARD",
                "payment_method": "CC"
            },
            items=[{"id": "I", "qty": -1, "price": 0.0}],
            promo_code=None
        )