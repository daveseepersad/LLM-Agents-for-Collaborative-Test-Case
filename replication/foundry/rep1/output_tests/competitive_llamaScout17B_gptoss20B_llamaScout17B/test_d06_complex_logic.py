import pytest
import types
from data.input_code.d06_complex_logic import *




def test_T_MISSING_PLATINUM_HIGH_AMOUNT():
    result = DiscountEngine.calculate_discount(1500.0, "PLATINUM", None)
    assert round(result, 2) == 0.25

def test_T_MISSING_PROMO_CODE_999():
    result = DiscountEngine.calculate_discount(100.0, "STANDARD", "ABC-999")
    assert result == 50.0

def test_T_MISSING_INVALID_PROMO_CODE():
    with pytest.raises(ValueError):
        DiscountEngine.calculate_discount(100.0, "STANDARD", "invalid")

def test_T_MISSING_USER_VALIDATION_EDGE_AGE():
    processor = OrderProcessor(Warehouse({}))
    with pytest.raises(UserValidationError):
        processor.validate_user("test@example.com", 101)



def test_T_MISSING_WAREHOUSE_LOCK_RELEASE():
    w = Warehouse({"item1": 10})
    w.lock_item("item1", 1)
    w.release_item("item1", 1)
    assert True

def test_T_MISSING_WAREHOUSE_INSUFFICIENT_STOCK():
    w = Warehouse({"item1": 10})
    result = w.check_stock("item1", 11)
    assert result == False

def test_T_MISSING_RETURN_FREE_ITEMS():
    w = Warehouse({"item1": 10})
    processor = OrderProcessor(w)
    user_data = {"email": "test@example.com", "age": 25}
    items = [{"id": "item1", "qty": -1, "price": 0.0}]
    with pytest.raises(ValueError):
        processor.process_order("123", user_data, items)