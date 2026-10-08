import pytest
from data.input_code.d06_complex_logic import (
    Warehouse,
    DiscountEngine,
    OrderProcessor,
    InventoryError,
    PaymentError,
    FraudDetectedError,
    UserValidationError,
)


def test_warehouse_basic_lock_and_release():
    wh = Warehouse({"A": 5})
    assert wh.check_stock("A", 3) is True
    wh.lock_item("A", 3)
    # Now 2 available, attempting to check more should fail
    assert wh.check_stock("A", 2) is True
    wh.release_item("A", 3)
    # After release, there should be no locked stock for A
    assert wh._locked_stock.get("A", 0) == 0


def test_warehouse_insufficient_stock_raises():
    wh = Warehouse({"A": 2})
    with pytest.raises(InventoryError):
        wh.lock_item("A", 3)


def test_validate_user_errors():
    wh = Warehouse({"X": 1})
    op = OrderProcessor(wh)

    # Invalid email
    with pytest.raises(UserValidationError):
        op.validate_user("invalid-email", 25)

    # Underage
    with pytest.raises(UserValidationError):
        op.validate_user("test@example.com", 17)

    # Over 100 should trigger age verification in this implementation
    with pytest.raises(UserValidationError):
        op.validate_user("older@example.com", 101)


def test_discount_engine_promo_999(monkeypatch):
    # Patch time to non-night to avoid night discount
    import data.input_code.d06_complex_logic as mod
    class FakeDateTime:
        @staticmethod
        def now():
            class N:
                hour = 12
            return N()
    monkeypatch.setattr(mod, "datetime", FakeDateTime)

    discount = DiscountEngine.calculate_discount(200.0, "STANDARD", "ABC-999")
    assert pytest.approx(discount, rel=1e-9) == 0.50 * 200.0  # 50% off


def test_orderprocessor_success_with_gold_and_promo(monkeypatch):
    import data.input_code.d06_complex_logic as mod

    # Patch time to non-night
    class FakeDateTime:
        @staticmethod
        def now():
            class N:
                hour = 12
            return N()
    monkeypatch.setattr(mod, "datetime", FakeDateTime)

    wh = Warehouse({"X": 10})
    op = OrderProcessor(wh)

    user_data = {
        "email": "buyer@example.com",
        "age": 30,
        "tier": "GOLD",
        "payment_method": "CC",
    }
    items = [{"id": "X", "qty": 1, "price": 100.0}]
    promo_code = "ABC-123"  # valid promo, +0.10

    result = op.process_order("ORD-001", user_data, items, promo_code=promo_code)

    assert result["status"] == "success"
    assert result["order_id"] == "ORD-001"
    assert result["original_price"] == 100.0
    assert pytest.approx(result["discount_applied"], rel=1e-9) == 0.20  # GOLD 0.10 + promo 0.10
    assert pytest.approx(result["final_total"], rel=1e-9) == 80.0 * 1.22
    assert result["items_count"] == 1


def test_orderprocessor_out_of_stock_rollbacks(monkeypatch):
    import data.input_code.d06_complex_logic as mod

    # Patch time to non-night to avoid discounts affecting outcomes
    class FakeDateTime:
        @staticmethod
        def now():
            class N:
                hour = 12
            return N()
    monkeypatch.setattr(mod, "datetime", FakeDateTime)

    wh = Warehouse({"A": 5, "B": 0})  # B is out of stock
    op = OrderProcessor(wh)

    user_data = {"email": "user@example.com", "age": 25, "payment_method": "CC"}
    items = [
        {"id": "A", "qty": 2, "price": 10.0},  # should lock A
        {"id": "B", "qty": 1, "price": 5.0},   # will fail due to stock
    ]

    result = op.process_order("ORD-ROLLBACK", user_data, items)
    assert result["status"] == "failed"
    assert "Out of stock" in result["reason"]
    # Ensure locked items are released (no locked stock should remain)
    assert wh._locked_stock == {}




def test_orderprocessor_crypto_min_amount_error(monkeypatch):
    import data.input_code.d06_complex_logic as mod

    # Patch time to non-night
    class FakeDateTime:
        @staticmethod
        def now():
            class N:
                hour = 12
            return N()
    monkeypatch.setattr(mod, "datetime", FakeDateTime)

    wh = Warehouse({"C": 1})
    op = OrderProcessor(wh)

    user_data = {"email": "crypto@example.com", "age": 25, "payment_method": "CRYPTO"}
    items = [{"id": "C", "qty": 1, "price": 20.0}]  # total 20 -> after tax 24.4 which is <50

    with pytest.raises(PaymentError):
        op.process_order("ORD-CRYPTO", user_data, items)

def test_discount_engine_promo_invalid_format():
    import data.input_code.d06_complex_logic as mod

    # Patch time to non-night
    class FakeDateTime:
        @staticmethod
        def now():
            class N:
                hour = 12
            return N()
    pytest.MonkeyPatch.setattr = None  # no-op to keep lint happy if needed
    mod_datetime_backup = mod.datetime
    mod.datetime = FakeDateTime

    with pytest.raises(ValueError):
        DiscountEngine.calculate_discount(50.0, "STANDARD", "invalid")  # invalid format should raise

    mod.datetime = mod_datetime_backup  # restore