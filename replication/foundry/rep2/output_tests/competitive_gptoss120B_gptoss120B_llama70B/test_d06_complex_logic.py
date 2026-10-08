import pytest
from data.input_code.d06_complex_logic import *

# ---------- Warehouse Tests ----------
@pytest.mark.parametrize(
    "initial_stock,item_id,quantity,expected_exception",
    [
        ({"itemX": 10}, "unknown", 1, InventoryError),
    ],
)
def test_warehouse_check_stock_missing_item(initial_stock, item_id, quantity, expected_exception):
    wh = Warehouse(initial_stock)
    with pytest.raises(expected_exception):
        wh.check_stock(item_id, quantity)


@pytest.mark.parametrize(
    "initial_stock,item_id,quantity,expected_result",
    [
        ({"itemY": 5}, "itemY", 6, False),
    ],
)
def test_warehouse_check_stock_insufficient(initial_stock, item_id, quantity, expected_result):
    wh = Warehouse(initial_stock)
    assert wh.check_stock(item_id, quantity) is expected_result


def test_warehouse_lock_item_happy_path():
    wh = Warehouse({"itemZ": 10})
    wh.lock_item("itemZ", 4)
    assert wh._locked_stock.get("itemZ") == 4


# ---------- DiscountEngine Tests ----------
@pytest.mark.parametrize(
    "total_amount,user_tier,promo_code,mock_hour,expected",
    [
        (200.0, "GOLD", "ABC-123", 2, 0.25),          # night (0-5) + GOLD + promo
        (1500.0, "PLATINUM", "XYZ-456", 10, 0.35),   # PLATINUM >1000, promo, no night, cap 0.40
        (800.0, "STANDARD", "ABC-999", 12, 400.0),   # super promo returns 50% of total
    ],
)
def test_discount_engine_calculate(monkeypatch, total_amount, user_tier, promo_code, mock_hour, expected):
    class MockDateTime:
        @classmethod
        def now(cls):
            return type("dt", (), {"hour": mock_hour})
    # Patch the datetime class used inside the module
    monkeypatch.setattr("data.input_code.d06_complex_logic.datetime", MockDateTime)
    result = DiscountEngine.calculate_discount(total_amount, user_tier, promo_code)
    assert result == expected


def test_discount_engine_invalid_promo(monkeypatch):
    class MockDateTime:
        @classmethod
        def now(cls):
            return type("dt", (), {"hour": 12})
    monkeypatch.setattr("data.input_code.d06_complex_logic.datetime", MockDateTime)
    with pytest.raises(ValueError):
        DiscountEngine.calculate_discount(100.0, "STANDARD", "bad_code")


# ---------- OrderProcessor.validate_user Tests ----------
@pytest.mark.parametrize(
    "email,age,expected_exception",
    [
        ("invalid_email", 25, UserValidationError),
        ("young@example.com", 16, UserValidationError),
        ("oldtimer@example.com", 101, UserValidationError),
    ],
)
def test_validate_user_exceptions(email, age, expected_exception):
    op = OrderProcessor(Warehouse({}))
    with pytest.raises(expected_exception):
        op.validate_user(email, age)


def test_validate_user_success():
    op = OrderProcessor(Warehouse({}))
    # Should not raise any exception
    op.validate_user("john.doe@example.com", 30)


# ---------- OrderProcessor.process_order Tests ----------
def test_process_order_success():
    wh = Warehouse({"A1": 5})
    op = OrderProcessor(wh)
    result = op.process_order(
        order_id="ORD-001",
        user_data={
            "email": "alice@example.com",
            "age": 28,
            "tier": "STANDARD",
            "payment_method": "CC",
        },
        items=[{"id": "A1", "qty": 2, "price": 50.0}],
        promo_code=None,
    )
    assert result == {
        "status": "success",
        "order_id": "ORD-001",
        "original_price": 100.0,
        "discount_applied": 0.0,
        "final_total": 122.0,
        "items_count": 1,
    }


def test_process_order_inventory_failure():
    wh = Warehouse({"B1": 5})
    op = OrderProcessor(wh)
    result = op.process_order(
        order_id="ORD-002",
        user_data={
            "email": "bob@example.com",
            "age": 35,
            "tier": "GOLD",
            "payment_method": "CC",
        },
        items=[{"id": "B1", "qty": 10, "price": 20.0}],
        promo_code=None,
    )
    assert result["status"] == "failed"
    assert "Out of stock" in result["reason"]


def test_process_order_invalid_promo():
    wh = Warehouse({"C1": 10})
    op = OrderProcessor(wh)
    result = op.process_order(
        order_id="ORD-003",
        user_data={
            "email": "carol@example.com",
            "age": 40,
            "tier": "STANDARD",
            "payment_method": "CC",
        },
        items=[{"id": "C1", "qty": 1, "price": 30.0}],
        promo_code="WRONG-12",
    )
    assert result["status"] == "error"
    assert result["reason"].startswith("Promo Error:")


def test_process_order_fraudulent_paypal(monkeypatch):
    # Mock datetime to avoid night discount
    class MockDateTime:
        @classmethod
        def now(cls):
            return type("dt", (), {"hour": 12})
    monkeypatch.setattr("data.input_code.d06_complex_logic.datetime", MockDateTime)

    wh = Warehouse({"D1": 5})
    op = OrderProcessor(wh)
    with pytest.raises(FraudDetectedError):
        op.process_order(
            order_id="ORD-004",
            user_data={
                "email": "dave@example.com",
                "age": 45,
                "tier": "STANDARD",
                "payment_method": "PAYPAL",
            },
            items=[{"id": "D1", "qty": 1, "price": 546.445}],
            promo_code=None,
        )


def test_process_order_crypto_below_minimum():
    wh = Warehouse({"E1": 10})
    op = OrderProcessor(wh)
    with pytest.raises(PaymentError):
        op.process_order(
            order_id="ORD-005",
            user_data={
                "email": "eve@example.com",
                "age": 29,
                "tier": "STANDARD",
                "payment_method": "CRYPTO",
            },
            items=[{"id": "E1", "qty": 1, "price": 30.0}],
            promo_code=None,
        )


def test_process_order_return_free_item_error():
    wh = Warehouse({"F1": 5})
    op = OrderProcessor(wh)
    with pytest.raises(ValueError):
        op.process_order(
            order_id="ORD-006",
            user_data={
                "email": "frank@example.com",
                "age": 33,
                "tier": "STANDARD",
                "payment_method": "CC",
            },
            items=[{"id": "F1", "qty": -1, "price": 0.0}],
            promo_code=None,
        )


# ---------- DiscountEngine Additional Tests ----------
@pytest.mark.parametrize(
    "total_amount,user_tier,promo_code,mock_hour,expected",
    [
        (800.0, "PLATINUM", None, 12, 0.20),
    ],
)
def test_discount_engine_platinum_low(monkeypatch, total_amount, user_tier, promo_code, mock_hour, expected):
    class MockDateTime:
        @classmethod
        def now(cls):
            return type("dt", (), {"hour": mock_hour})

    monkeypatch.setattr("data.input_code.d06_complex_logic.datetime", MockDateTime)
    result = DiscountEngine.calculate_discount(total_amount, user_tier, promo_code)
    assert result == expected


# ---------- Warehouse Release Tests ----------
def test_warehouse_release_partial():
    wh = Warehouse({"A": 5})
    wh.lock_item("A", 3)
    wh.release_item("A", 2)
    assert wh._locked_stock.get("A") == 1


def test_warehouse_release_full():
    wh = Warehouse({"B": 5})
    wh.lock_item("B", 3)
    wh.release_item("B", 3)
    assert wh._locked_stock.get("B") is None


# ---------- OrderProcessor.process_order Tests ----------
def test_process_order_paypal_success(monkeypatch):
    class MockDateTime:
        @classmethod
        def now(cls):
            return type("dt", (), {"hour": 12})

    monkeypatch.setattr("data.input_code.d06_complex_logic.datetime", MockDateTime)

    wh = Warehouse({"X1": 5})
    op = OrderProcessor(wh)
    result = op.process_order(
        order_id="ORD-100",
        user_data={
            "email": "test@example.com",
            "age": 30,
            "tier": "STANDARD",
            "payment_method": "PAYPAL",
        },
        items=[{"id": "X1", "qty": 1, "price": 100.0}],
        promo_code=None,
    )
    assert result == {
        "status": "success",
        "order_id": "ORD-100",
        "original_price": 100.0,
        "discount_applied": 0.0,
        "final_total": 122.0,
        "items_count": 1,
    }


def test_process_order_crypto_success(monkeypatch):
    class MockDateTime:
        @classmethod
        def now(cls):
            return type("dt", (), {"hour": 12})

    monkeypatch.setattr("data.input_code.d06_complex_logic.datetime", MockDateTime)

    wh = Warehouse({"Y1": 5})
    op = OrderProcessor(wh)
    result = op.process_order(
        order_id="ORD-101",
        user_data={
            "email": "crypto@example.com",
            "age": 35,
            "tier": "STANDARD",
            "payment_method": "CRYPTO",
        },
        items=[{"id": "Y1", "qty": 2, "price": 30.0}],
        promo_code=None,
    )
    assert result == {
        "status": "success",
        "order_id": "ORD-101",
        "original_price": 60.0,
        "discount_applied": 0.0,
        "final_total": 73.2,
        "items_count": 1,
    }


def test_process_order_super_promo(monkeypatch):
    class MockDateTime:
        @classmethod
        def now(cls):
            return type("dt", (), {"hour": 12})

    monkeypatch.setattr("data.input_code.d06_complex_logic.datetime", MockDateTime)

    wh = Warehouse({"Z1": 5})
    op = OrderProcessor(wh)
    result = op.process_order(
        order_id="ORD-200",
        user_data={
            "email": "superpromo@example.com",
            "age": 30,
            "tier": "STANDARD",
            "payment_method": "CC",
        },
        items=[{"id": "Z1", "qty": 1, "price": 200.0}],
        promo_code="ABC-999",
    )
    assert result == {
        "status": "success",
        "order_id": "ORD-200",
        "original_price": 200.0,
        "discount_applied": 100.0,
        "final_total": -24156.0,
        "items_count": 1,
    }


# ---------- Warehouse Additional Tests ----------
def test_warehouse_check_stock_true():
    wh = Warehouse({"itemA": 10})
    assert wh.check_stock("itemA", 5) is True


def test_warehouse_lock_item_insufficient():
    wh = Warehouse({"itemB": 3})
    with pytest.raises(InventoryError):
        wh.lock_item("itemB", 5)


def test_warehouse_release_item_no_lock():
    wh = Warehouse({"itemC": 4})
    # Release without prior lock; should not raise and leave locked_stock unchanged
    wh.release_item("itemC", 2)
    assert wh._locked_stock.get("itemC") is None


# ---------- DiscountEngine Additional Tests ----------
@pytest.mark.parametrize(
    "total_amount,user_tier,promo_code,mock_hour,expected",
    [
        (500.0, "GOLD", None, 7, 0.10),  # No night discount
        (1500.0, "PLATINUM", "ABC-123", 2, 0.40),  # Cap at 0.40
    ],
)
def test_discount_engine_additional(monkeypatch, total_amount, user_tier, promo_code, mock_hour, expected):
    class MockDateTime:
        @classmethod
        def now(cls):
            return type("dt", (), {"hour": mock_hour})

    monkeypatch.setattr("data.input_code.d06_complex_logic.datetime", MockDateTime)
    result = DiscountEngine.calculate_discount(total_amount, user_tier, promo_code)
    assert result == expected


# ---------- OrderProcessor Additional Tests ----------
def test_order_processor_inventory_rollback(monkeypatch):
    # Ensure no night discount influences the flow
    class MockDateTime:
        @classmethod
        def now(cls):
            return type("dt", (), {"hour": 12})

    monkeypatch.setattr("data.input_code.d06_complex_logic.datetime", MockDateTime)

    wh = Warehouse({"I1": 5, "I2": 2})
    op = OrderProcessor(wh)
    result = op.process_order(
        order_id="ORD-ROLL-1",
        user_data={
            "email": "test@example.com",
            "age": 30,
            "tier": "STANDARD",
            "payment_method": "CC",
        },
        items=[
            {"id": "I1", "qty": 3, "price": 10.0},
            {"id": "I2", "qty": 5, "price": 20.0},
        ],
        promo_code=None,
    )
    assert result["status"] == "failed"
    # After rollback, no items should remain locked
    assert wh._locked_stock == {}


def test_order_processor_invalid_promo_rollback(monkeypatch):
    # Ensure no night discount influences the flow
    class MockDateTime:
        @classmethod
        def now(cls):
            return type("dt", (), {"hour": 12})

    monkeypatch.setattr("data.input_code.d06_complex_logic.datetime", MockDateTime)

    wh = Warehouse({"J1": 4, "J2": 4})
    op = OrderProcessor(wh)
    result = op.process_order(
        order_id="ORD-ROLL-2",
        user_data={
            "email": "user@example.com",
            "age": 40,
            "tier": "GOLD",
            "payment_method": "CC",
        },
        items=[
            {"id": "J1", "qty": 2, "price": 15.0},
            {"id": "J2", "qty": 1, "price": 25.0},
        ],
        promo_code="BAD001",  # Invalid format triggers ValueError
    )
    assert result["status"] == "error"
    # After rollback, no items should remain locked
    assert wh._locked_stock == {}