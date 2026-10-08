import pytest
from unittest.mock import patch

from data.input_code.d06_complex_logic import (
    Warehouse,
    DiscountEngine,
    OrderProcessor,
    InventoryError,
    PaymentError,
    FraudDetectedError,
    UserValidationError,
)


# ---------- Warehouse Tests ----------
def test_check_stock_success_and_failure():
    wh = Warehouse({"item1": 10})
    # sufficient stock
    assert wh.check_stock("item1", 5) is True
    # insufficient stock
    assert wh.check_stock("item1", 11) is False
    # item not present raises
    with pytest.raises(InventoryError):
        wh.check_stock("missing", 1)


def test_lock_and_release_item():
    wh = Warehouse({"item1": 5})
    # lock within stock
    wh.lock_item("item1", 3)
    assert wh._locked_stock["item1"] == 3
    # lock more than available raises
    with pytest.raises(InventoryError):
        wh.lock_item("item1", 3)  # only 2 left
    # release partially
    wh.release_item("item1", 2)
    assert wh._locked_stock["item1"] == 1
    # release remaining removes key
    wh.release_item("item1", 1)
    assert "item1" not in wh._locked_stock


# ---------- DiscountEngine Tests ----------


def test_discount_promo_code_handling():
    # Valid promo adds 0.10
    disc = DiscountEngine.calculate_discount(200, "STANDARD", promo_code="XYZ-999")
    # Ends with 999 => immediate 50% off, function returns total_amount*0.5
    assert disc == 200 * 0.5

    # Valid promo without 999 adds 0.10
    disc = DiscountEngine.calculate_discount(200, "STANDARD", promo_code="ABC-123")
    assert disc == pytest.approx(0.10)

    # Invalid format raises
    with pytest.raises(ValueError):
        DiscountEngine.calculate_discount(200, "STANDARD", promo_code="badcode")




# ---------- OrderProcessor.validate_user Tests ----------
def test_validate_user_success():
    op = OrderProcessor(Warehouse({}))
    op.validate_user("test.user@example.com", 30)  # should not raise


@pytest.mark.parametrize(
    "email,age,expected_msg",
    [
        ("invalid-email", 30, "Invalid email format"),
        ("test@example.com", 17, "User must be 18+"),
        ("test@example.com", 101, "Age verification required for 100+"),
    ],
)
def test_validate_user_errors(email, age, expected_msg):
    op = OrderProcessor(Warehouse({}))
    with pytest.raises(UserValidationError) as exc:
        op.validate_user(email, age)
    assert expected_msg in str(exc.value)


# ---------- OrderProcessor.process_order Tests ----------


def test_process_order_inventory_failure_and_rollback():
    wh = Warehouse({"A": 1})
    op = OrderProcessor(wh)
    items = [{"id": "A", "qty": 2, "price": 10.0}]  # exceeds stock
    user = {"email": "user@example.com", "age": 30}
    result = op.process_order("ORD2", user, items)
    assert result["status"] == "failed"
    assert "Out of stock" in result["reason"]
    # Ensure no locked stock remains
    assert not wh._locked_stock


def test_process_order_invalid_promo_triggers_error_and_rollback():
    wh = Warehouse({"A": 5})
    op = OrderProcessor(wh)
    items = [{"id": "A", "qty": 1, "price": 20.0}]
    user = {"email": "user@example.com", "age": 30}
    result = op.process_order("ORD3", user, items, promo_code="BAD-12")
    assert result["status"] == "error"
    assert "Promo Error" in result["reason"]
    # locked stock should be released
    assert not wh._locked_stock






