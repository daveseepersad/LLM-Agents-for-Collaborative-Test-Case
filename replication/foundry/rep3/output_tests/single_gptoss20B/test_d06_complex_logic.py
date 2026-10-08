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


def patch_time(monkeypatch, hour: int):
    import data.input_code.d06_complex_logic as mod

    class FakeDateTime:
        @staticmethod
        def now():
            class O:
                hour = hour
            return O()

    monkeypatch.setattr(mod, "datetime", FakeDateTime)








def test_discount_engine_invalid_promo_raises():
    with pytest.raises(ValueError):
        DiscountEngine.calculate_discount(100.0, "STANDARD", "invalid")


def test_order_processor_success(monkeypatch):
    wh = Warehouse({"X": 5})
    op = OrderProcessor(wh)
    user = {"email": "user@example.com", "age": 30}
    items = [{"id": "X", "qty": 1, "price": 100.0}]
    result = op.process_order("ORD1", user, items)
    assert result["status"] == "success"
    assert result["order_id"] == "ORD1"
    assert result["original_price"] == 100.0
    assert result["final_total"] == 122.0  # 100 * 1.22
    assert result["items_count"] == 1


def test_order_processor_out_of_stock(monkeypatch):
    wh = Warehouse({"X": 1})
    op = OrderProcessor(wh)
    user = {"email": "user@example.com", "age": 30}
    items = [{"id": "X", "qty": 2, "price": 10.0}]
    result = op.process_order("ORD2", user, items)
    assert result["status"] == "failed"
    assert "Out of stock" in result["reason"]


def test_order_processor_invalid_promo(monkeypatch):
    wh = Warehouse({"A": 5})
    op = OrderProcessor(wh)
    user = {"email": "user@example.com", "age": 25}
    items = [{"id": "A", "qty": 1, "price": 20.0}]
    result = op.process_order("ORD3", user, items, promo_code="BADPROM")
    assert result["status"] == "error"
    assert result["reason"].startswith("Promo Error")


def test_order_processor_invalid_user_raises():
    wh = Warehouse({"A": 5})
    op = OrderProcessor(wh)
    user = {"email": "invalid-email", "age": 20}
    items = [{"id": "A", "qty": 1, "price": 10.0}]
    with pytest.raises(UserValidationError):
        op.process_order("ORD4", user, items)






