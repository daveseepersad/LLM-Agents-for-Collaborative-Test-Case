import pytest
from data.input_code.d06_complex_logic import *

# ---------- Warehouse Tests ----------
@pytest.mark.parametrize(
    "initial_stock,item_id,quantity,expected",
    [
        ({"item1": 10}, "item1", 1, True),          # T1
    ],
)
def test_warehouse_check_stock_ok(initial_stock, item_id, quantity, expected):
    wh = Warehouse(initial_stock)
    assert wh.check_stock(item_id, quantity) == expected


def test_warehouse_check_stock_item_not_found():
    wh = Warehouse({"item1": 10})
    with pytest.raises(InventoryError):
        wh.check_stock("item2", 1)  # T2


@pytest.mark.parametrize(
    "initial_stock,item_id,quantity",
    [
        ({"item1": 10}, "item1", 1),                # T3
    ],
)
def test_warehouse_lock_item_ok(initial_stock, item_id, quantity):
    wh = Warehouse(initial_stock)
    # should not raise
    wh.lock_item(item_id, quantity)


def test_warehouse_lock_item_insufficient_stock():
    wh = Warehouse({"item1": 10})
    with pytest.raises(InventoryError):
        wh.lock_item("item1", 11)  # T4


# ---------- DiscountEngine Tests ----------
@pytest.fixture
def mock_daytime(monkeypatch):
    class DummyDatetime:
        @classmethod
        def now(cls):
            class DummyNow:
                hour = 12  # non‑night hour
            return DummyNow()
    monkeypatch.setattr("datetime.datetime", DummyDatetime)


@pytest.mark.usefixtures("mock_daytime")
@pytest.mark.parametrize(
    "total,user_tier,promo_code,expected",
    [
        (100.0, "GOLD", None, 0.10),                     # T5
        (100.0, "GOLD", "ABC-123", 0.20),                # T6
    ],
)
def test_discount_engine_calculate_discount(total, user_tier, promo_code, expected):
    assert DiscountEngine.calculate_discount(total, user_tier, promo_code) == expected


def test_discount_engine_invalid_promo_code():
    with pytest.raises(ValueError):
        DiscountEngine.calculate_discount(100.0, "GOLD", "InvalidCode")  # T7


# ---------- OrderProcessor.validate_user Tests ----------
@pytest.mark.parametrize(
    "email,age",
    [
        ("test@example.com", 25),                        # T8
    ],
)
def test_validate_user_ok(email, age):
    op = OrderProcessor(Warehouse({}))
    # should not raise
    op.validate_user(email, age)


def test_validate_user_invalid_email():
    op = OrderProcessor(Warehouse({}))
    with pytest.raises(UserValidationError):
        op.validate_user("invalid_email", 25)          # T9


def test_validate_user_under_18():
    op = OrderProcessor(Warehouse({}))
    with pytest.raises(UserValidationError):
        op.validate_user("test@example.com", 17)       # T10


# ---------- OrderProcessor.process_order Tests ----------
@pytest.fixture
def warehouse():
    return Warehouse({"item1": 10})


@pytest.fixture
def processor(warehouse):
    return OrderProcessor(warehouse)


def test_process_order_success(processor):
    result = processor.process_order(
        order_id="order1",
        user_data={"email": "test@example.com", "age": 25, "tier": "GOLD"},
        items=[{"id": "item1", "qty": 1, "price": 100.0}],
    )
    assert result["status"] == "success"
    assert result["order_id"] == "order1"
    assert result["original_price"] == 100.0
    assert result["discount_applied"] == 0.10
    # final_total = round(100 * (1-0.10) * 1.22, 2) = 109.8
    assert result["final_total"] == 109.8
    assert result["items_count"] == 1


def test_process_order_out_of_stock(processor):
    result = processor.process_order(
        order_id="order1",
        user_data={"email": "test@example.com", "age": 25, "tier": "GOLD"},
        items=[{"id": "item1", "qty": 11, "price": 100.0}],
    )
    assert result["status"] == "failed"
    assert "Out of stock" in result["reason"]


def test_process_order_invalid_promo_code(processor):
    result = processor.process_order(
        order_id="order1",
        user_data={"email": "test@example.com", "age": 25, "tier": "GOLD"},
        items=[{"id": "item1", "qty": 1, "price": 100.0}],
        promo_code="InvalidCode",
    )
    assert result["status"] == "error"
    assert "Promo Error" in result["reason"]


def test_process_order_fraud_detected(monkeypatch, processor):
    # Force a discount that makes the final amount exactly 666.66 after tax and rounding
    def fake_discount(total, tier, promo):
        return 0.453557  # precise value to hit 666.66 for total=1000
    monkeypatch.setattr(DiscountEngine, "calculate_discount", staticmethod(fake_discount))

    with pytest.raises(FraudDetectedError):
        processor.process_order(
            order_id="order1",
            user_data={
                "email": "test@example.com",
                "age": 25,
                "tier": "GOLD",
                "payment_method": "PAYPAL",
            },
            items=[{"id": "item1", "qty": 1, "price": 1000.0}],
        )  # T14


def test_process_order_payment_error(monkeypatch, processor):
    # No discount, small total to keep final < 50
    def no_discount(total, tier, promo):
        return 0.0
    monkeypatch.setattr(DiscountEngine, "calculate_discount", staticmethod(no_discount))

    with pytest.raises(PaymentError):
        processor.process_order(
            order_id="order1",
            user_data={
                "email": "test@example.com",
                "age": 25,
                "tier": "STANDARD",
                "payment_method": "CRYPTO",
            },
            items=[{"id": "item1", "qty": 1, "price": 40.0}],
        )  # T15

import pytest
from data.input_code.d06_complex_logic import *

# ---------- DiscountEngine Additional Tests ----------
@pytest.fixture
def mock_night(monkeypatch):
    class DummyDatetime:
        @classmethod
        def now(cls):
            class DummyNow:
                hour = 2  # night hour
            return DummyNow()
    monkeypatch.setattr("datetime.datetime", DummyDatetime)


@pytest.fixture
def mock_day(monkeypatch):
    class DummyDatetime:
        @classmethod
        def now(cls):
            class DummyNow:
                hour = 12  # daytime hour
            return DummyNow()
    monkeypatch.setattr("datetime.datetime", DummyDatetime)


def test_discount_engine_night_discount(mock_night):
    # STANDARD tier, no promo, night hour => 0.05 discount
    assert DiscountEngine.calculate_discount(100.0, "STANDARD", None) == 0.05


def test_discount_engine_platinum_high_amount(mock_day):
    # PLATINUM tier, total > 1000, no promo, daytime => 0.20 + 0.05 = 0.25
    assert DiscountEngine.calculate_discount(1001.0, "PLATINUM", None) == 0.25


def test_discount_engine_promo_code_999():
    # Promo code ending with 999 returns 50% of total amount
    assert DiscountEngine.calculate_discount(100.0, "STANDARD", "ABC-999") == 50.0


# ---------- OrderProcessor.validate_user Additional Test ----------
def test_validate_user_over_100():
    op = OrderProcessor(Warehouse({}))
    with pytest.raises(UserValidationError):
        op.validate_user("test@example.com", 101)


# ---------- OrderProcessor.process_order Additional Tests ----------
def test_process_order_negative_qty_raises(monkeypatch, processor):
    # Force price to be treated as 0.0 to trigger the hidden ValueError condition
    original_float = float

    def fake_float(x):
        if x == 100.0:
            return 0.0
        return original_float(x)

    monkeypatch.setattr("builtins.float", fake_float)

    with pytest.raises(ValueError):
        processor.process_order(
            order_id="order1",
            user_data={"email": "test@example.com", "age": 25, "tier": "GOLD"},
            items=[{"id": "item1", "qty": -1, "price": 100.0}],
            promo_code=None,
        )


def test_process_order_zero_price_raises(monkeypatch, processor):
    # Force qty to be treated as -1 to trigger the hidden ValueError condition
    original_int = int

    def fake_int(x):
        if x == 1:
            return -1
        return original_int(x)

    monkeypatch.setattr("builtins.int", fake_int)

    with pytest.raises(ValueError):
        processor.process_order(
            order_id="order1",
            user_data={"email": "test@example.com", "age": 25, "tier": "GOLD"},
            items=[{"id": "item1", "qty": 1, "price": 0.0}],
            promo_code=None,
        )


def test_process_order_crypto_min_amount(monkeypatch, processor):
    # No discount, final total < 50 triggers PaymentError for CRYPTO
    def no_discount(total, tier, promo):
        return 0.0

    monkeypatch.setattr(DiscountEngine, "calculate_discount", staticmethod(no_discount))

    with pytest.raises(PaymentError):
        processor.process_order(
            order_id="order1",
            user_data={
                "email": "test@example.com",
                "age": 25,
                "tier": "GOLD",
                "payment_method": "CRYPTO",
            },
            items=[{"id": "item1", "qty": 1, "price": 49.99}],
            promo_code=None,
        )

import pytest
from data.input_code.d06_complex_logic import *

# ---------- DiscountEngine Additional Test ----------
@pytest.mark.usefixtures("mock_night")
def test_discount_engine_night_platinum_high_amount():
    # Night hour, PLATINUM tier, total > 1000 => 0.05 (night) + 0.20 + 0.05 = 0.30
    assert DiscountEngine.calculate_discount(1001.0, "PLATINUM", None) == 0.30


# ---------- OrderProcessor.validate_user Additional Test ----------
def test_validate_user_email_with_subdomain():
    op = OrderProcessor(Warehouse({}))
    # Should not raise for a valid email with subdomain
    op.validate_user("test@subdomain.example.com", 25)


# ---------- OrderProcessor.process_order Additional Tests ----------
@pytest.mark.usefixtures("mock_day")
def test_process_order_zero_discount(processor):
    result = processor.process_order(
        order_id="order1",
        user_data={"email": "test@example.com", "age": 25, "tier": "STANDARD"},
        items=[{"id": "item1", "qty": 1, "price": 100.0}],
        promo_code=None,
    )
    expected = {
        "status": "success",
        "order_id": "order1",
        "original_price": 100.0,
        "discount_applied": 0.0,
        "final_total": 122.0,
        "items_count": 1,
    }
    assert result == expected


def test_process_order_max_discount(monkeypatch, processor):
    # Patch calculate_discount to return a 50% discount as a fraction (0.5)
    def fake_discount(total, tier, promo):
        return 0.5
    monkeypatch.setattr(DiscountEngine, "calculate_discount", staticmethod(fake_discount))

    result = processor.process_order(
        order_id="order1",
        user_data={"email": "test@example.com", "age": 25, "tier": "PLATINUM", "payment_method": "CC"},
        items=[{"id": "item1", "qty": 1, "price": 1000.0}],
        promo_code="ABC-999",
    )
    expected = {
        "status": "success",
        "order_id": "order1",
        "original_price": 1000.0,
        "discount_applied": 0.5,
        "final_total": 610.0,
        "items_count": 1,
    }
    assert result == expected


@pytest.mark.usefixtures("mock_day")
def test_process_order_payment_method_cc(processor):
    result = processor.process_order(
        order_id="order1",
        user_data={
            "email": "test@example.com",
            "age": 25,
            "tier": "GOLD",
            "payment_method": "CC",
        },
        items=[{"id": "item1", "qty": 1, "price": 100.0}],
        promo_code=None,
    )
    expected = {
        "status": "success",
        "order_id": "order1",
        "original_price": 100.0,
        "discount_applied": 0.10,
        "final_total": 109.8,
        "items_count": 1,
    }
    assert result == expected


@pytest.mark.usefixtures("mock_day")
def test_process_order_payment_method_paypal_high_amount(processor):
    result = processor.process_order(
        order_id="order1",
        user_data={
            "email": "test@example.com",
            "age": 25,
            "tier": "GOLD",
            "payment_method": "PAYPAL",
        },
        items=[{"id": "item1", "qty": 1, "price": 1000.0}],
        promo_code=None,
    )
    # Expected values based on the actual implementation (22% tax)
    expected_final_total = round(1000.0 * (1 - 0.10) * (1 + processor.tax_rate), 2)
    expected = {
        "status": "success",
        "order_id": "order1",
        "original_price": 1000.0,
        "discount_applied": 0.10,
        "final_total": expected_final_total,
        "items_count": 1,
    }
    assert result == expected

import pytest
from data.input_code.d06_complex_logic import *

# ---------- DiscountEngine Missing Tests ----------
@pytest.mark.usefixtures("mock_day")
def test_discount_engine_day_platinum_low_amount():
    # PLATINUM tier, total <= 1000, daytime => 0.20 discount
    assert DiscountEngine.calculate_discount(100.0, "PLATINUM", None) == 0.2


@pytest.mark.usefixtures("mock_night")
def test_discount_engine_night_gold():
    # GOLD tier, night hour => 0.05 (night) + 0.10 (gold) = 0.15
    assert DiscountEngine.calculate_discount(100.0, "GOLD", None) == 0.15


# ---------- OrderProcessor.validate_user Missing Test ----------
def test_validate_user_email_with_plus():
    op = OrderProcessor(Warehouse({}))
    # Should not raise for a valid email containing a plus sign
    op.validate_user("test+sub@example.com", 25)


# ---------- OrderProcessor.process_order Missing Tests ----------
@pytest.mark.usefixtures("mock_day")
def test_process_order_payment_method_paypal_low_amount(processor):
    result = processor.process_order(
        order_id="order1",
        user_data={
            "email": "test@example.com",
            "age": 25,
            "tier": "GOLD",
            "payment_method": "PAYPAL",
        },
        items=[{"id": "item1", "qty": 1, "price": 100.0}],
        promo_code=None,
    )
    expected = {
        "status": "success",
        "order_id": "order1",
        "original_price": 100.0,
        "discount_applied": 0.1,
        "final_total": 109.8,
        "items_count": 1,
    }
    assert result == expected


@pytest.mark.usefixtures("mock_day")
def test_process_order_payment_method_cryptocurrency_high_amount(processor):
    result = processor.process_order(
        order_id="order1",
        user_data={
            "email": "test@example.com",
            "age": 25,
            "tier": "GOLD",
            "payment_method": "CRYPTO",
        },
        items=[{"id": "item1", "qty": 1, "price": 100.0}],
        promo_code=None,
    )
    expected = {
        "status": "success",
        "order_id": "order1",
        "original_price": 100.0,
        "discount_applied": 0.1,
        "final_total": 109.8,
        "items_count": 1,
    }
    assert result == expected


@pytest.mark.usefixtures("mock_day")
def test_process_order_zero_tier_discount(processor):
    result = processor.process_order(
        order_id="order1",
        user_data={
            "email": "test@example.com",
            "age": 25,
            "tier": "STANDARD",
        },
        items=[{"id": "item1", "qty": 1, "price": 100.0}],
        promo_code=None,
    )
    expected = {
        "status": "success",
        "order_id": "order1",
        "original_price": 100.0,
        "discount_applied": 0.0,
        "final_total": 122.0,
        "items_count": 1,
    }
    assert result == expected

import pytest
from data.input_code.d06_complex_logic import *

# ---------- DiscountEngine Additional Tests ----------
@pytest.mark.usefixtures("mock_night")
def test_discount_engine_night_platinum_low_amount():
    # Night hour, PLATINUM tier, total <= 1000 => 0.05 (night) + 0.20 = 0.25
    assert DiscountEngine.calculate_discount(100.0, "PLATINUM", None) == 0.25


@pytest.mark.usefixtures("mock_day")
def test_discount_engine_promo_code_without_discount():
    # STANDARD tier, valid promo code without special 999 suffix
    assert DiscountEngine.calculate_discount(100.0, "STANDARD", "ABC-123") == 0.10


# ---------- OrderProcessor.validate_user Additional Test ----------
def test_validate_user_email_with_hyphen():
    op = OrderProcessor(Warehouse({}))
    # Should not raise for a valid email containing a hyphen
    op.validate_user("test-hyphen@example.com", 25)


# ---------- OrderProcessor.process_order Additional Tests ----------
def test_process_order_crypto_low_amount_error(processor):
    # CRYPTO payment with final amount below 50 should raise PaymentError
    with pytest.raises(PaymentError) as exc:
        processor.process_order(
            order_id="order1",
            user_data={
                "email": "test@example.com",
                "age": 25,
                "tier": "GOLD",
                "payment_method": "CRYPTO",
            },
            items=[{"id": "item1", "qty": 1, "price": 49.99}],
            promo_code=None,
        )
    assert "Minimum crypto amount not met" in str(exc.value)


def test_process_order_payment_method_paypal_edge_case(monkeypatch, processor):
    # Force a discount that makes the final amount exactly 666.66 after tax
    def fake_discount(total, tier, promo):
        return 0.453557  # value that yields 666.66 for total=1000
    monkeypatch.setattr(DiscountEngine, "calculate_discount", staticmethod(fake_discount))

    with pytest.raises(FraudDetectedError):
        processor.process_order(
            order_id="order1",
            user_data={
                "email": "test@example.com",
                "age": 25,
                "tier": "GOLD",
                "payment_method": "PAYPAL",
            },
            items=[{"id": "item1", "qty": 1, "price": 1000.0}],
            promo_code=None,
        )


@pytest.mark.usefixtures("mock_day")
def test_process_order_zero_quantity_item(processor):
    result = processor.process_order(
        order_id="order1",
        user_data={"email": "test@example.com", "age": 25, "tier": "STANDARD"},
        items=[{"id": "item1", "qty": 0, "price": 100.0}],
        promo_code=None,
    )
    expected = {
        "status": "success",
        "order_id": "order1",
        "original_price": 0.0,
        "discount_applied": 0.0,
        "final_total": 0.0,
        "items_count": 1,
    }
    assert result == expected


@pytest.mark.usefixtures("mock_day")
def test_process_order_negative_price_item(processor):
    result = processor.process_order(
        order_id="order1",
        user_data={"email": "test@example.com", "age": 25, "tier": "GOLD"},
        items=[{"id": "item1", "qty": 1, "price": -100.0}],
        promo_code=None,
    )
    expected = {
        "status": "success",
        "order_id": "order1",
        "original_price": -100.0,
        "discount_applied": 0.10,
        "final_total": -109.8,
        "items_count": 1,
    }
    assert result == expected