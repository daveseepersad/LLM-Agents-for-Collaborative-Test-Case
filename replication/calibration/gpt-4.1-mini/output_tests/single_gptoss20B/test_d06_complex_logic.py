import pytest
import re
from datetime import datetime
from unittest.mock import patch
from data.input_code.d06_complex_logic import (
    Warehouse, DiscountEngine, OrderProcessor,
    InventoryError, PaymentError, FraudDetectedError, UserValidationError
)

def test_warehouse_check_stock_and_lock_release():
    wh = Warehouse({"item1": 10})
    assert wh.check_stock("item1", 5) is True
    wh.lock_item("item1", 5)
    assert wh.check_stock("item1", 6) is False
    wh.release_item("item1", 3)
    assert wh.check_stock("item1", 6) is True
    wh.release_item("item1", 2)
    # locked_stock for item1 should be removed after release to 0
    assert "item1" not in wh._locked_stock
    with pytest.raises(InventoryError):
        wh.check_stock("itemX", 1)
    with pytest.raises(InventoryError):
        wh.lock_item("item1", 11)

@patch("data.input_code.d06_complex_logic.datetime")
def test_discount_engine_various_conditions(mock_datetime):
    # Test night owl discount (hour 2)
    mock_datetime.now.return_value = datetime(2020,1,1,2,0,0)
    d = DiscountEngine.calculate_discount(500, "STANDARD")
    assert 0.05 <= d <= 0.05

    # Test GOLD tier discount
    mock_datetime.now.return_value = datetime(2020,1,1,12,0,0)
    d = DiscountEngine.calculate_discount(500, "GOLD")
    assert d == 0.10

    # Test PLATINUM tier discount below and above 1000
    d1 = DiscountEngine.calculate_discount(999.99, "PLATINUM")
    d2 = DiscountEngine.calculate_discount(1000.01, "PLATINUM")
    assert d1 == 0.20
    assert d2 == 0.25

    # Test valid promo code with normal discount
    d3 = DiscountEngine.calculate_discount(100, "STANDARD", "ABC-123")
    assert abs(d3 - 0.10) < 1e-6

    # Test promo code with 999 ending (50% off)
    d4 = DiscountEngine.calculate_discount(200, "STANDARD", "XYZ-999")
    assert d4 == 100.0

    # Test invalid promo code format raises
    with pytest.raises(ValueError):
        DiscountEngine.calculate_discount(100, "STANDARD", "badcode")

    # Test max discount cap at 0.40
    d5 = DiscountEngine.calculate_discount(100, "PLATINUM", "ABC-123")
    assert d5 <= 0.40

def test_order_processor_validate_user_errors():
    wh = Warehouse({"item1": 10})
    op = OrderProcessor(wh)
    # Invalid email
    with pytest.raises(UserValidationError):
        op.validate_user("bademail", 25)
    # Age under 18
    with pytest.raises(UserValidationError):
        op.validate_user("test@test.com", 17)
    # Age over 100
    with pytest.raises(UserValidationError):
        op.validate_user("test@test.com", 101)
    # Valid user passes
    op.validate_user("valid.email+test@test-domain.com", 30)



def test_discount_engine_max_discount_cap_and_nightowl_combined():
    # Combine night owl and platinum with promo code to test cap at 0.40
    with patch("data.input_code.d06_complex_logic.datetime") as mock_datetime:
        mock_datetime.now.return_value = datetime(2020,1,1,1,0,0)  # night owl active
        discount = DiscountEngine.calculate_discount(2000, "PLATINUM", "ABC-123")
        # Night owl 0.05 + platinum 0.20 + >1000 0.05 + promo 0.10 = 0.40 capped
        assert discount == 0.40

def test_warehouse_release_item_removes_key_when_qty_zero_or_less():
    wh = Warehouse({"item1": 10})
    wh.lock_item("item1", 5)
    wh.release_item("item1", 5)
    assert "item1" not in wh._locked_stock
    # Release more than locked should not error and remove key
    wh.lock_item("item1", 3)
    wh.release_item("item1", 5)
    assert "item1" not in wh._locked_stock

def test_order_processor_process_order_empty_items():
    wh = Warehouse({"item1": 10})
    op = OrderProcessor(wh)
    user_data = {"email": "a@b.com", "age": 30}
    result = op.process_order("order_empty", user_data, [])
    assert result["status"] == "success"
    assert result["items_count"] == 0
    assert result["original_price"] == 0.0
    assert result["final_total"] == 0.0

def test_order_processor_process_order_missing_user_data_keys():
    wh = Warehouse({"item1": 10})
    op = OrderProcessor(wh)
    items = [{"id": "item1", "qty": 1, "price": 10.0}]
    # Missing email and age keys default to "" and 0, should raise UserValidationError for age < 18
    with pytest.raises(UserValidationError):
        op.process_order("order_missing", {}, items)