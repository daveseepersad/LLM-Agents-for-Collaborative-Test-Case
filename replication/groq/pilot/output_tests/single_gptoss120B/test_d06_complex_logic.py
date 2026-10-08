import pytest
from unittest.mock import patch, MagicMock
from data.input_code.d06_complex_logic import (
    Warehouse,
    DiscountEngine,
    OrderProcessor,
    InventoryError,
    PaymentError,
    FraudDetectedError,
    UserValidationError,
)
from datetime import datetime


def test_warehouse_check_and_lock_release():
    wh = Warehouse({"item1": 10})
    # sufficient stock
    assert wh.check_stock("item1", 5) is True
    wh.lock_item("item1", 5)
    # after lock, available should be 5
    assert wh.check_stock("item1", 5) is True
    assert wh.check_stock("item1", 6) is False
    # release and ensure stock restored
    wh.release_item("item1", 5)
    assert wh.check_stock("item1", 10) is True
    # insufficient stock raises
    with pytest.raises(InventoryError):
        wh.lock_item("item1", 11)
    # unknown item raises
    with pytest.raises(InventoryError):
        wh.check_stock("unknown", 1)


def test_discount_engine_branches():
    # Night hour, GOLD tier, valid promo
    fake_now = datetime(2023, 1, 1, 2, 0, 0)  # hour = 2
    with patch("data.input_code.d06_complex_logic.datetime") as mock_dt:
        mock_dt.now.return_value = fake_now
        discount = DiscountEngine.calculate_discount(100.0, "GOLD", "ABC-123")
        # night 0.05 + gold 0.10 + promo 0.10 = 0.25
        assert discount == 0.25

    # Night hour, PLATINUM tier, amount > 1000, promo ends with 999 (super discount)
    fake_now = datetime(2023, 1, 1, 5, 0, 0)  # hour = 5
    with patch("data.input_code.d06_complex_logic.datetime") as mock_dt:
        mock_dt.now.return_value = fake_now
        result = DiscountEngine.calculate_discount(2000.0, "PLATINUM", "XYZ-999")
        # super discount returns amount * 0.5
        assert result == 2000.0 * 0.5

    # Night hour, PLATINUM tier, amount > 1000, valid promo not ending 999
    fake_now = datetime(2023, 1, 1, 3, 0, 0)
    with patch("data.input_code.d06_complex_logic.datetime") as mock_dt:
        mock_dt.now.return_value = fake_now
        discount = DiscountEngine.calculate_discount(1500.0, "PLATINUM", "DEF-456")
        # night 0.05 + platinum 0.20 + extra 0.05 (amount>1000) + promo 0.10 = 0.40 capped
        assert discount == 0.40

    # Invalid promo format raises
    with pytest.raises(ValueError):
        DiscountEngine.calculate_discount(100.0, "STANDARD", "badcode")


def test_validate_user_success_and_failures():
    processor = OrderProcessor(Warehouse({}))
    # valid
    processor.validate_user("test.user@example.com", 30)

    # invalid email
    with pytest.raises(UserValidationError):
        processor.validate_user("invalid-email", 30)

    # underage
    with pytest.raises(UserValidationError):
        processor.validate_user("test@example.com", 17)

    # over 100
    with pytest.raises(UserValidationError):
        processor.validate_user("test@example.com", 101)




def test_process_order_inventory_error_and_rollback():
    wh = Warehouse({"A": 1})
    processor = OrderProcessor(wh)
    user_data = {
        "email": "user@example.com",
        "age": 30,
        "tier": "STANDARD",
        "payment_method": "CC",
    }
    items = [
        {"id": "A", "qty": 1, "price": 10.0},
        {"id": "A", "qty": 1, "price": 10.0},  # second lock will fail (stock exhausted)
    ]
    result = processor.process_order("ORDFAIL", user_data, items)
    assert result["status"] == "failed"
    assert "Out of stock" in result["reason"]
    # after failure, locked stock should be cleared
    assert not hasattr(wh, "_locked_stock") or "A" not in wh._locked_stock




def test_process_order_fraud_detected_error():
    wh = Warehouse({"X": 1})
    processor = OrderProcessor(wh)
    processor.tax_rate = 0.0  # make final amount equal total
    user_data = {
        "email": "fraud@example.com",
        "age": 30,
        "tier": "STANDARD",
        "payment_method": "PAYPAL",
    }
    items = [{"id": "X", "qty": 1, "price": 666.66}]
    # No discount, tax 0 => final_price_with_tax == 666.66 triggers FraudDetectedError
    with pytest.raises(FraudDetectedError):
        processor.process_order("ORDFRAUD", user_data, items)


def test_process_order_crypto_payment_error():
    wh = Warehouse({"Y": 1})
    processor = OrderProcessor(wh)
    processor.tax_rate = 0.0
    user_data = {
        "email": "crypto@example.com",
        "age": 30,
        "tier": "STANDARD",
        "payment_method": "CRYPTO",
    }
    items = [{"id": "Y", "qty": 1, "price": 40.0}]
    # final amount 40 < 50 triggers PaymentError
    with pytest.raises(PaymentError):
        processor.process_order("ORDCRYPTO", user_data, items)


def test_process_order_negative_qty_zero_price_raises_value_error():
    wh = Warehouse({"Z": 5})
    processor = OrderProcessor(wh)
    user_data = {
        "email": "test@example.com",
        "age": 30,
        "tier": "STANDARD",
        "payment_method": "CC",
    }
    items = [{"id": "Z", "qty": -1, "price": 0.0}]
    with pytest.raises(ValueError, match="Cannot return free items"):
        processor.process_order("ORDNEG", user_data, items)