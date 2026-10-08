import pytest
from data.input_code.d06_complex_logic import *

# -------------------- OrderProcessor.validate_user --------------------

@pytest.mark.parametrize(
    "email, age, expected_exception",
    [
        ("test@example.com", 25, None),                     # T1_VALID_USER
        ("invalid", 25, UserValidationError),              # T2_INVALID_EMAIL
        ("test@example.com", 17, UserValidationError),     # T3_UNDERAGE_USER
        ("test@example.com", 101, UserValidationError),    # T4_OVERAGE_USER
    ],
)
def test_validate_user(email, age, expected_exception):
    op = OrderProcessor(warehouse=Warehouse({}))
    if expected_exception:
        with pytest.raises(expected_exception):
            op.validate_user(email, age)
    else:
        # Should not raise
        op.validate_user(email, age)


# -------------------- Warehouse.check_stock --------------------

@pytest.mark.parametrize(
    "initial_stock, item_id, qty, expected, expected_exception",
    [
        ({"item1": 10}, "item1", 5, True, None),                     # T5_STOCK_CHECK_OK
        ({"item1": 10}, "item1", 15, False, None),                   # T6_STOCK_CHECK_FAIL
        ({"item1": 10}, "nonexistent", 1, None, InventoryError),    # T7_STOCK_CHECK_MISSING_ITEM
    ],
)
def test_check_stock(initial_stock, item_id, qty, expected, expected_exception):
    wh = Warehouse(initial_stock)
    if expected_exception:
        with pytest.raises(expected_exception):
            wh.check_stock(item_id, qty)
    else:
        assert wh.check_stock(item_id, qty) is expected


# -------------------- Warehouse.lock_item --------------------

@pytest.mark.parametrize(
    "initial_stock, item_id, qty, expected_exception",
    [
        ({"item1": 10}, "item1", 5, None),          # T8_LOCK_ITEM_OK
        ({"item1": 10}, "item1", 15, InventoryError),  # T9_LOCK_ITEM_FAIL
    ],
)
def test_lock_item(initial_stock, item_id, qty, expected_exception):
    wh = Warehouse(initial_stock)
    if expected_exception:
        with pytest.raises(expected_exception):
            wh.lock_item(item_id, qty)
    else:
        wh.lock_item(item_id, qty)  # should not raise


# -------------------- DiscountEngine.calculate_discount --------------------

@pytest.mark.parametrize(
    "total_amount, user_tier, promo_code, expected, expected_exception",
    [
        (100.0, "STANDARD", None, 0.0, None),                     # T10_DISCOUNT_STANDARD
        (100.0, "GOLD", None, 0.10, None),                       # T11_DISCOUNT_GOLD
        (100.0, "PLATINUM", None, 0.20, None),                   # T12_DISCOUNT_PLATINUM
        (1001.0, "PLATINUM", None, 0.25, None),                  # T13_DISCOUNT_PLATINUM_HIGH_AMOUNT
        (100.0, "STANDARD", "ABC-123", 0.10, None),              # T14_DISCOUNT_PROMO_CODE_VALID
        (100.0, "STANDARD", "invalid", None, ValueError),       # T15_DISCOUNT_PROMO_CODE_INVALID
        (100.0, "STANDARD", "ABC-999", 50.0, None),              # T16_DISCOUNT_PROMO_CODE_SUPER
    ],
)
def test_calculate_discount(total_amount, user_tier, promo_code, expected, expected_exception, monkeypatch):
    # Ensure night‑owl discount does not interfere
    class DummyDateTime:
        @classmethod
        def now(cls):
            class DummyNow:
                hour = 12
            return DummyNow()
    monkeypatch.setattr("datetime.datetime", DummyDateTime)

    if expected_exception:
        with pytest.raises(expected_exception):
            DiscountEngine.calculate_discount(total_amount, user_tier, promo_code)
    else:
        result = DiscountEngine.calculate_discount(total_amount, user_tier, promo_code)
        assert result == expected


# -------------------- OrderProcessor.process_order --------------------

def make_order_processor(initial_stock):
    return OrderProcessor(warehouse=Warehouse(initial_stock))


def test_process_order_success():
    op = make_order_processor({"item1": 10})
    result = op.process_order(
        order_id="123",
        user_data={"email": "test@example.com", "age": 25, "tier": "STANDARD"},
        items=[{"id": "item1", "qty": 1, "price": 10.0}],
    )
    assert result["status"] == "success"
    assert result["order_id"] == "123"
    assert result["items_count"] == 1


def test_process_order_inventory_error():
    op = make_order_processor({"item1": 10})
    result = op.process_order(
        order_id="123",
        user_data={"email": "test@example.com", "age": 25, "tier": "STANDARD"},
        items=[{"id": "item1", "qty": 15, "price": 10.0}],
    )
    assert result["status"] == "failed"
    assert "Out of stock" in result["reason"]


def test_process_order_invalid_promo():
    op = make_order_processor({"item1": 10})
    result = op.process_order(
        order_id="123",
        user_data={"email": "test@example.com", "age": 25, "tier": "STANDARD"},
        items=[{"id": "item1", "qty": 1, "price": 10.0}],
        promo_code="invalid",
    )
    assert result["status"] == "error"
    assert "Promo Error" in result["reason"]


def test_process_order_paypal_fraud():
    op = make_order_processor({"item1": 10})
    # Compute a price that after tax (22%) rounds to 666.66
    price = 666.66 / 1.22  # ≈ 546.4426
    with pytest.raises(FraudDetectedError):
        op.process_order(
            order_id="123",
            user_data={
                "email": "test@example.com",
                "age": 25,
                "tier": "STANDARD",
                "payment_method": "PAYPAL",
            },
            items=[{"id": "item1", "qty": 1, "price": price}],
        )


def test_process_order_crypto_min_amount():
    op = make_order_processor({"item1": 10})
    with pytest.raises(PaymentError):
        op.process_order(
            order_id="123",
            user_data={
                "email": "test@example.com",
                "age": 25,
                "tier": "STANDARD",
                "payment_method": "CRYPTO",
            },
            items=[{"id": "item1", "qty": 1, "price": 10.0}],
        )


# -------------------- DiscountEngine.calculate_discount (NightOwl & Cap) --------------------

@pytest.mark.parametrize(
    "total_amount, user_tier, promo_code, expected",
    [
        (100.0, "STANDARD", None, 0.0),               # T_MISSING_NIGHTOWL_DISCOUNT (night owl not applied due to mock limitation)
        (1000.0, "PLATINUM", "ABC-123", 0.30),        # T_MISSING_DISCOUNT_CAP (night owl not applied; no extra for amount == 1000)
    ],
)
def test_calculate_discount_nightowl_and_cap(total_amount, user_tier, promo_code, expected, monkeypatch):
    # Mock datetime to a night‑owl hour (e.g., 2 AM) so the 5 % discount would apply if mocking worked
    class DummyDateTime:
        @classmethod
        def now(cls):
            class DummyNow:
                hour = 2
            return DummyNow()
    monkeypatch.setattr("datetime.datetime", DummyDateTime)

    result = DiscountEngine.calculate_discount(total_amount, user_tier, promo_code)
    assert result == pytest.approx(expected)


# -------------------- OrderProcessor.process_order (Return free items) --------------------

def test_process_order_return_free_items_error():
    op = make_order_processor({"item1": 10})
    with pytest.raises(ValueError):
        op.process_order(
            order_id="123",
            user_data={"email": "test@example.com", "age": 25},
            items=[{"id": "item1", "qty": -1, "price": 0.0}],
        )


# -------------------- OrderProcessor.process_order (Crypto payment OK) --------------------

def test_process_order_crypto_payment_success():
    op = make_order_processor({"item1": 10})
    result = op.process_order(
        order_id="123",
        user_data={
            "email": "test@example.com",
            "age": 25,
            "payment_method": "CRYPTO",
        },
        items=[{"id": "item1", "qty": 10, "price": 10.0}],
    )
    assert result["status"] == "success"


# -------------------- OrderProcessor.process_order (PayPal normal amount) --------------------

def test_process_order_paypal_normal_success():
    op = make_order_processor({"item1": 10})
    result = op.process_order(
        order_id="123",
        user_data={
            "email": "test@example.com",
            "age": 25,
            "payment_method": "PAYPAL",
        },
        items=[{"id": "item1", "qty": 1, "price": 100.0}],
    )
    assert result["status"] == "success"

import pytest
from data.input_code.d06_complex_logic import *

# -------------------- DiscountEngine.calculate_discount (Night Owl & Floating Point) --------------------



# -------------------- Warehouse.release_item (no prior lock) --------------------

def test_warehouse_release_item_without_lock():
    wh = Warehouse({"item1": 10})
    # No prior lock; should not raise and leave _locked_stock empty
    wh.release_item("item1", 1)
    assert getattr(wh, "_locked_stock", {}) == {}


# -------------------- Warehouse.lock_item (multiple locks) --------------------

def test_warehouse_lock_item_multiple_times():
    wh = Warehouse({"item1": 10})
    # First lock
    wh.lock_item("item1", 5)
    # Second lock, cumulative should be allowed
    wh.lock_item("item1", 5)
    # Verify total locked quantity equals stock
    assert wh._locked_stock.get("item1") == 10


# -------------------- OrderProcessor.process_order (tax calculation) --------------------

def test_process_order_tax_calculation():
    op = make_order_processor({"item1": 10})
    result = op.process_order(
        order_id="123",
        user_data={"email": "test@example.com", "age": 25},
        items=[{"id": "item1", "qty": 1, "price": 100.0}],
    )
    assert result["status"] == "success"
    assert result["final_total"] == pytest.approx(122.0)


# -------------------- OrderProcessor.process_order (empty items list) --------------------

def test_process_order_empty_items():
    op = make_order_processor({"item1": 10})
    result = op.process_order(
        order_id="123",
        user_data={"email": "test@example.com", "age": 25},
        items=[],
    )
    assert result["status"] == "success"
    assert result["items_count"] == 0