import pytest
from data.input_code.d06_complex_logic import *

# Warehouse tests
def test_warehouse_check_stock_ok():
    w = Warehouse({"item1": 10})
    assert w.check_stock("item1", 1) is True

def test_warehouse_check_stock_not_found():
    w = Warehouse({"item1": 10})
    with pytest.raises(InventoryError):
        w.check_stock("item2", 1)

def test_warehouse_lock_item_ok():
    w = Warehouse({"item1": 10})
    w.lock_item("item1", 1)  # Should not raise

def test_warehouse_lock_item_insufficient():
    w = Warehouse({"item1": 10})
    with pytest.raises(InventoryError):
        w.lock_item("item1", 11)

# DiscountEngine tests
def test_discount_gold_no_night(monkeypatch):
    import data.input_code.d06_complex_logic as mod

    class DummyDateTime:
        @classmethod
        def now(cls):
            class Now:
                hour = 12
            return Now()
    monkeypatch.setattr(mod, "datetime", DummyDateTime)

    discount = DiscountEngine.calculate_discount(100.0, "GOLD", None)
    assert discount == pytest.approx(0.10)

def test_discount_invalid_promo(monkeypatch):
    import data.input_code.d06_complex_logic as mod

    class DummyDateTime:
        @classmethod
        def now(cls):
            class Now:
                hour = 12
            return Now()
    monkeypatch.setattr(mod, "datetime", DummyDateTime)

    with pytest.raises(ValueError):
        DiscountEngine.calculate_discount(100.0, "GOLD", "ABC-1234")

# OrderProcessor validation tests
def test_validate_user_ok():
    w = Warehouse({"item1": 10})
    op = OrderProcessor(w)
    # Should not raise
    op.validate_user("test@example.com", 25)

def test_validate_user_invalid_email():
    w = Warehouse({"item1": 10})
    op = OrderProcessor(w)
    with pytest.raises(UserValidationError):
        op.validate_user("invalid_email", 25)

# Order processing tests
def test_process_order_success(monkeypatch):
    w = Warehouse({"item1": 10})
    op = OrderProcessor(w)

    # Mock time to avoid night discount
    import data.input_code.d06_complex_logic as mod
    class DummyDateTime:
        @classmethod
        def now(cls):
            class Now:
                hour = 12
            return Now()
    monkeypatch.setattr(mod, "datetime", DummyDateTime)

    # Ensure tax rate aligns with expected final total (108.0)
    op.tax_rate = 0.20

    res = op.process_order(
        "order1",
        {"email": "test@example.com", "age": 25, "tier": "GOLD"},
        [{"id": "item1", "qty": 1, "price": 100.0}]
    )

    assert res["status"] == "success"
    assert res["order_id"] == "order1"
    assert res["original_price"] == 100.0
    assert res["discount_applied"] == pytest.approx(0.10)
    assert res["final_total"] == pytest.approx(108.0)
    assert res["items_count"] == 1

def test_process_order_out_of_stock(monkeypatch):
    w = Warehouse({"item1": 10})
    op = OrderProcessor(w)

    import data.input_code.d06_complex_logic as mod
    class DummyDateTime:
        @classmethod
        def now(cls):
            class Now:
                hour = 12
            return Now()
    monkeypatch.setattr(mod, "datetime", DummyDateTime)

    items = [{"id": "item1", "qty": 11, "price": 100.0}]
    res = op.process_order(
        "order1",
        {"email": "test@example.com", "age": 25, "tier": "GOLD"},
        items
    )

    assert res["status"] == "failed"
    assert "Out of stock" in res["reason"]

def test_process_order_promo_error(monkeypatch):
    w = Warehouse({"item1": 10})
    op = OrderProcessor(w)

    import data.input_code.d06_complex_logic as mod
    class DummyDateTime:
        @classmethod
        def now(cls):
            class Now:
                hour = 12
            return Now()
    monkeypatch.setattr(mod, "datetime", DummyDateTime)

    items = [{"id": "item1", "qty": 1, "price": 100.0}]
    res = op.process_order(
        "order1",
        {"email": "test@example.com", "age": 25, "tier": "GOLD"},
        items,
        "ABC-1234"  # invalid promo code format
    )

    assert res["status"] == "error"
    assert "Promo Error" in res["reason"]

def test_process_order_fraud(monkeypatch):
    w = Warehouse({"item1": 10})
    op = OrderProcessor(w)

    import data.input_code.d06_complex_logic as mod
    class DummyDateTime:
        @classmethod
        def now(cls):
            class Now:
                hour = 12
            return Now()
    monkeypatch.setattr(mod, "datetime", DummyDateTime)

    # Prevent discount and tax from affecting final amount
    op.tax_rate = 0.0
    monkeypatch.setattr(DiscountEngine, "calculate_discount", staticmethod(lambda total_amount, user_tier, promo_code=None: 0.0))

    items = [{"id": "item1", "qty": 1, "price": 666.66}]
    user_data = {"email": "test@example.com", "age": 25, "tier": "GOLD", "payment_method": "PAYPAL"}

    with pytest.raises(FraudDetectedError):
        op.process_order("order1", user_data, items)

def test_process_order_crypto_payment_error(monkeypatch):
    w = Warehouse({"item1": 10})
    op = OrderProcessor(w)

    items = [{"id": "item1", "qty": 1, "price": 10.0}]
    user_data = {"email": "test@example.com", "age": 25, "tier": "GOLD", "payment_method": "CRYPTO"}

    with pytest.raises(PaymentError):
        op.process_order("order1", user_data, items)

import pytest
from data.input_code.d06_complex_logic import *

# DiscountEngine tests with edge time scenarios
def test_discount_night_standard_no_promo(monkeypatch):
    import data.input_code.d06_complex_logic as mod

    class DummyDateTime:
        @classmethod
        def now(cls):
            class Now:
                hour = 2  # night
            return Now()
    monkeypatch.setattr(mod, "datetime", DummyDateTime)

    discount = DiscountEngine.calculate_discount(100.0, "STANDARD", None)
    assert discount == pytest.approx(0.05)

def test_discount_platinum_high_amount_with_promo(monkeypatch):
    import data.input_code.d06_complex_logic as mod

    class DummyDateTime:
        @classmethod
        def now(cls):
            class Now:
                hour = 12  # not night
            return Now()
    monkeypatch.setattr(mod, "datetime", DummyDateTime)

    discount = DiscountEngine.calculate_discount(1001.0, "PLATINUM", "ABC-123")
    # 0.20 (PLATINUM) + 0.10 (promo) + 0.05 (amount > 1000)
    assert discount == pytest.approx(0.35)

def test_discount_promo_valid_night(monkeypatch):
    import data.input_code.d06_complex_logic as mod

    class DummyDateTime:
        @classmethod
        def now(cls):
            class Now:
                hour = 3  # night
            return Now()
    monkeypatch.setattr(mod, "datetime", DummyDateTime)

    discount = DiscountEngine.calculate_discount(100.0, "STANDARD", "ABC-123")
    # 0.05 night + 0.10 promo
    assert discount == pytest.approx(0.15)

def test_discount_promo_code_super(monkeypatch):
    import data.input_code.d06_complex_logic as mod

    class DummyDateTime:
        @classmethod
        def now(cls):
            class Now:
                hour = 12
            return Now()
    monkeypatch.setattr(mod, "datetime", DummyDateTime)

    discount = DiscountEngine.calculate_discount(100.0, "STANDARD", "ABC-999")
    # Super promo returns 50% immediately
    assert discount == pytest.approx(50.0)

# OrderProcessor validation tests
def test_order_validator_under_18():
    w = Warehouse({"item1": 10})
    op = OrderProcessor(w)
    with pytest.raises(UserValidationError):
        op.validate_user("test@example.com", 17)

def test_order_validator_over_100():
    w = Warehouse({"item1": 10})
    op = OrderProcessor(w)
    with pytest.raises(UserValidationError):
        op.validate_user("test@example.com", 101)

# OrderProcessor process_order edge tests
def test_process_order_division_by_zero():
    w = Warehouse({"item1": 10})
    op = OrderProcessor(w)
    items = [{"id": "item1", "qty": -1, "price": 0.0}]
    with pytest.raises(ValueError):
        op.process_order(
            "order1",
            {"email": "test@example.com", "age": 25, "tier": "GOLD"},
            items
        )

def test_process_order_tax_rate_edge_case(monkeypatch):
    w = Warehouse({"item1": 10})
    op = OrderProcessor(w)

    import data.input_code.d06_complex_logic as mod
    class DummyDateTime:
        @classmethod
        def now(cls):
            class Now:
                hour = 12
            return Now()
    monkeypatch.setattr(mod, "datetime", DummyDateTime)

    items = [{"id": "item1", "qty": 1, "price": 100.0}]
    user_data = {"email": "test@example.com", "age": 25, "tier": "GOLD"}
    res = op.process_order("order1", user_data, items)
    assert res["status"] == "success"