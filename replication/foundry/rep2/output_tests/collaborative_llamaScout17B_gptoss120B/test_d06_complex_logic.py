import pytest
from data.input_code.d06_complex_logic import *

# ----------------------------------------------------------------------
# Helper to mock datetime.now().hour for DiscountEngine tests
# ----------------------------------------------------------------------
class _FixedDatetime:
    def __init__(self, hour):
        self._hour = hour

    def now(self):
        return self

    @property
    def hour(self):
        return self._hour


# ----------------------------------------------------------------------
# validate_user tests
# ----------------------------------------------------------------------
@pytest.mark.parametrize(
    "email, age, expected_exception",
    [
        ("test@example.com", 25, None),                     # valid
        ("invalid", 25, UserValidationError),              # invalid email
        ("test@example.com", 17, UserValidationError),     # underage
        ("test@example.com", 101, UserValidationError),    # overage
    ],
)
def test_orderprocessor_validate_user(email, age, expected_exception):
    op = OrderProcessor(warehouse=Warehouse({}))
    if expected_exception:
        with pytest.raises(expected_exception):
            op.validate_user(email, age)
    else:
        # should not raise
        op.validate_user(email, age)


# ----------------------------------------------------------------------
# Warehouse.check_stock tests
# ----------------------------------------------------------------------
@pytest.mark.parametrize(
    "initial_stock, item_id, qty, expected",
    [
        ({"item1": 10}, "item1", 5, True),   # sufficient stock
        ({"item1": 10}, "item1", 15, False), # insufficient stock
    ],
)
def test_warehouse_check_stock(initial_stock, item_id, qty, expected):
    wh = Warehouse(initial_stock)
    assert wh.check_stock(item_id, qty) is expected


def test_warehouse_check_stock_missing_item():
    wh = Warehouse({"item1": 10})
    with pytest.raises(InventoryError):
        wh.check_stock("nonexistent", 1)


# ----------------------------------------------------------------------
# Warehouse.lock_item tests
# ----------------------------------------------------------------------
def test_warehouse_lock_item_success():
    wh = Warehouse({"item1": 10})
    wh.lock_item("item1", 5)
    # after locking, available should be 5
    assert wh.check_stock("item1", 5) is True
    assert wh.check_stock("item1", 6) is False


def test_warehouse_lock_item_insufficient_stock():
    wh = Warehouse({"item1": 10})
    with pytest.raises(InventoryError):
        wh.lock_item("item1", 15)


# ----------------------------------------------------------------------
# DiscountEngine.calculate_discount tests
# ----------------------------------------------------------------------
@pytest.mark.parametrize(
    "hour, total, tier, promo, expected",
    [
        (12, 100, "STANDARD", None, 0.0),          # no discounts
        (12, 100, "GOLD", None, 0.10),            # gold tier
        (12, 100, "PLATINUM", None, 0.20),        # platinum tier
        (12, 1001, "PLATINUM", None, 0.25),       # platinum + high amount
        (12, 100, "STANDARD", "ABC-123", 0.10),   # valid promo adds 10%
        (12, 100, "STANDARD", "ABC-999", 50.0),   # super promo returns amount
    ],
)
def test_discountengine_calculate_discount(monkeypatch, hour, total, tier, promo, expected):
    # mock datetime to control night discount (set to non‑night hour)
    monkeypatch.setattr(
        "data.input_code.d06_complex_logic.datetime",
        _FixedDatetime(hour),
        raising=False,
    )
    result = DiscountEngine.calculate_discount(total, tier, promo)
    assert result == expected


def test_discountengine_invalid_promo_code(monkeypatch):
    monkeypatch.setattr(
        "data.input_code.d06_complex_logic.datetime",
        _FixedDatetime(12),
        raising=False,
    )
    with pytest.raises(ValueError):
        DiscountEngine.calculate_discount(100, "STANDARD", "invalid")


# ----------------------------------------------------------------------
# OrderProcessor.process_order tests
# ----------------------------------------------------------------------
@pytest.fixture
def warehouse_with_stock():
    return Warehouse({"item1": 10})


@pytest.fixture
def order_processor(warehouse_with_stock):
    return OrderProcessor(warehouse_with_stock)


def test_process_order_success(order_processor):
    result = order_processor.process_order(
        order_id="1",
        user_data={"email": "test@example.com", "age": 25, "tier": "STANDARD"},
        items=[{"id": "item1", "qty": 1, "price": 10.0}],
    )
    assert result["status"] == "success"
    assert result["order_id"] == "1"
    assert result["original_price"] == 10.0
    assert result["discount_applied"] == 0.0
    assert result["items_count"] == 1


def test_process_order_inventory_error(order_processor):
    result = order_processor.process_order(
        order_id="1",
        user_data={"email": "test@example.com", "age": 25, "tier": "STANDARD"},
        items=[{"id": "item1", "qty": 15, "price": 10.0}],
    )
    assert result["status"] == "failed"
    assert "Out of stock" in result["reason"]


def test_process_order_invalid_promo(order_processor):
    result = order_processor.process_order(
        order_id="1",
        user_data={"email": "test@example.com", "age": 25, "tier": "STANDARD"},
        items=[{"id": "item1", "qty": 1, "price": 10.0}],
        promo_code="invalid",
    )
    assert result["status"] == "error"
    assert "Promo Error" in result["reason"]


def test_process_order_paypal_fraud(monkeypatch):
    # Force final price to hit the evil amount 666.66
    # Use a high quantity/price to reach that total after tax
    wh = Warehouse({"item1": 10})
    op = OrderProcessor(wh)

    # Mock DiscountEngine to return 0% discount so we can control the amount
    monkeypatch.setattr(
        "data.input_code.d06_complex_logic.DiscountEngine.calculate_discount",
        lambda total, tier, promo=None: 0.0,
        raising=False,
    )
    # Choose values that after 22% tax give 666.66
    # Let total_price = X, final = X * 1.22 = 666.66 => X = 666.66 / 1.22
    total_price = round(666.66 / 1.22, 2)
    qty = 1
    price = total_price

    with pytest.raises(FraudDetectedError):
        op.process_order(
            order_id="1",
            user_data={
                "email": "test@example.com",
                "age": 25,
                "tier": "STANDARD",
                "payment_method": "PAYPAL",
            },
            items=[{"id": "item1", "qty": qty, "price": price}],
        )


def test_process_order_crypto_min_amount(monkeypatch):
    wh = Warehouse({"item1": 10})
    op = OrderProcessor(wh)

    # Mock DiscountEngine to give 0% discount
    monkeypatch.setattr(
        "data.input_code.d06_complex_logic.DiscountEngine.calculate_discount",
        lambda total, tier, promo=None: 0.0,
        raising=False,
    )
    # Choose a total that after tax is below 50
    total_price = 40.0  # after 22% tax -> 48.8
    with pytest.raises(PaymentError):
        op.process_order(
            order_id="1",
            user_data={
                "email": "test@example.com",
                "age": 25,
                "tier": "STANDARD",
                "payment_method": "CRYPTO",
            },
            items=[{"id": "item1", "qty": 1, "price": total_price}],
        )