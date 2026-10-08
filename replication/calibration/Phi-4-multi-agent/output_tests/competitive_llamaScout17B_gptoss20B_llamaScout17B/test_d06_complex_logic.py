import pytest
from data.input_code.d06_complex_logic import *

@pytest.fixture
def warehouse():
    return Warehouse({"item1": 10, "item2": 5})

@pytest.fixture
def order_processor(warehouse):
    return OrderProcessor(warehouse)

def test_check_stock(warehouse):
    assert warehouse.check_stock("item1", 5) == True
    with pytest.raises(InventoryError):
        warehouse.check_stock("item3", 1)

def test_lock_item(warehouse):
    warehouse.lock_item("item1", 5)
    assert warehouse._locked_stock["item1"] == 5
    with pytest.raises(InventoryError):
        warehouse.lock_item("item1", 6)

def test_release_item(warehouse):
    warehouse.lock_item("item1", 5)
    warehouse.release_item("item1", 5)
    assert "item1" not in warehouse._locked_stock

def test_calculate_discount():
    assert DiscountEngine.calculate_discount(500, "GOLD") == 0.10
    assert DiscountEngine.calculate_discount(1500, "PLATINUM") == 0.25
    assert DiscountEngine.calculate_discount(1500, "PLATINUM", "ABC-999") == 750.0
    with pytest.raises(ValueError):
        DiscountEngine.calculate_discount(100, "GOLD", "INVALID")

def test_validate_user():
    order_processor = OrderProcessor(Warehouse({}))
    order_processor.validate_user("test@test.com", 25)
    with pytest.raises(UserValidationError):
        order_processor.validate_user("invalid-email", 25)
    with pytest.raises(UserValidationError):
        order_processor.validate_user("test@test.com", 17)
    with pytest.raises(UserValidationError):
        order_processor.validate_user("test@test.com", 101)

def test_process_order_success(order_processor):
    result = order_processor.process_order(
        "order1",
        {"email": "test@test.com", "age": 25, "tier": "GOLD", "payment_method": "CC"},
        [{"id": "item1", "qty": 2, "price": 100.0}],
        "ABC-123"
    )
    assert result["status"] == "success"
    assert result["final_total"] == pytest.approx(195.2)

def test_process_order_insufficient_stock(order_processor):
    result = order_processor.process_order(
        "order2",
        {"email": "test@test.com", "age": 25, "tier": "GOLD", "payment_method": "CC"},
        [{"id": "item1", "qty": 11, "price": 100.0}]
    )
    assert result["status"] == "failed"
    assert "Out of stock" in result["reason"]

def test_process_order_invalid_promo_code(order_processor):
    result = order_processor.process_order(
        "order3",
        {"email": "test@test.com", "age": 25, "tier": "GOLD", "payment_method": "CC"},
        [{"id": "item1", "qty": 2, "price": 100.0}],
        "INVALID"
    )
    assert result["status"] == "error"
    assert "Promo Error" in result["reason"]

def test_process_order_fraud_detected(order_processor):
    result = order_processor.process_order(
        "order4",
        {"email": "test@test.com", "age": 25, "tier": "GOLD", "payment_method": "PAYPAL"},
        [{"id": "item1", "qty": 4, "price": 166.66}],
    )
    assert result["status"] == "success"
    assert result["final_total"] == pytest.approx(731.97)

def test_process_order_crypto_minimum(order_processor):
    with pytest.raises(PaymentError):
        order_processor.process_order(
            "order5",
            {"email": "test@test.com", "age": 25, "tier": "GOLD", "payment_method": "CRYPTO"},
            [{"id": "item1", "qty": 1, "price": 10.0}]
        )

def test_process_order_return_free_items(order_processor):
    with pytest.raises(ValueError):
        order_processor.process_order(
            "order6",
            {"email": "test@test.com", "age": 25, "tier": "GOLD", "payment_method": "CC"},
            [{"id": "item1", "qty": -1, "price": 0.0}],
            None
        )

def test_t_missing_nightowl(monkeypatch):
    import data.input_code.d06_complex_logic as d06
    class FakeDateTime:
        @staticmethod
        def now():
            class FakeTime:
                hour = 1
            return FakeTime()
    monkeypatch.setattr(d06, 'datetime', FakeDateTime)
    assert DiscountEngine.calculate_discount(500.0, "STANDARD", None) == 0.05

def test_t_missing_platinum_over_1000(monkeypatch):
    import data.input_code.d06_complex_logic as d06
    class FakeDateTime:
        @staticmethod
        def now():
            class FakeTime:
                hour = 12
            return FakeTime()
    monkeypatch.setattr(d06, 'datetime', FakeDateTime)
    assert DiscountEngine.calculate_discount(1500.0, "PLATINUM", None) == pytest.approx(0.25)

def test_t_missing_email_regex():
    with pytest.raises(UserValidationError) as exc:
        OrderProcessor(Warehouse({})).validate_user("simple@test", 25)
    assert "Invalid email format" in str(exc.value)

def test_t_missing_age_over_100():
    with pytest.raises(UserValidationError) as exc:
        OrderProcessor(Warehouse({})).validate_user("test@test.com", 101)
    assert "Age verification required for 100+" in str(exc.value)

def test_t_missing_zero_price_division():
    with pytest.raises(ValueError) as exc:
        OrderProcessor(Warehouse({"item1": 5})).process_order(
            "order7",
            {"email": "test@test.com", "age": 25, "tier": "GOLD", "payment_method": "CC"},
            [{"id": "item1", "qty": -1, "price": 0.0}],
            None
        )
    assert "Cannot return free items" in str(exc.value)

def test_t_missing_crypto_minimum():
    with pytest.raises(PaymentError) as exc:
        OrderProcessor(Warehouse({"item1": 10})).process_order(
            "order8",
            {"email": "test@test.com", "age": 25, "tier": "GOLD", "payment_method": "CRYPTO"},
            [{"id": "item1", "qty": 1, "price": 20.0}],
            None
        )
    assert "Minimum crypto amount not met" in str(exc.value)

def test_t_missing_invalid_promo_code(monkeypatch):
    import data.input_code.d06_complex_logic as d06
    class FakeDateTime:
        @staticmethod
        def now():
            class FakeTime:
                hour = 12
            return FakeTime()
    monkeypatch.setattr(d06, 'datetime', FakeDateTime)
    with pytest.raises(ValueError) as exc:
        DiscountEngine.calculate_discount(1000.0, "GOLD", "INVALID")
    assert "Invalid promo code format" in str(exc.value)

@pytest.mark.parametrize("hour,total_amount,user_tier,promo_code,expected", [
    (12, 1000.0, "GOLD", "ABC-000", 0.20),
])
def test_t_missing_promo_code_validation_no_night(monkeypatch, hour, total_amount, user_tier, promo_code, expected):
    import data.input_code.d06_complex_logic as d06
    def make_fake(h):
        class FakeDateTime:
            @staticmethod
            def now():
                class FakeTime:
                    hour = h
                return FakeTime()
        return FakeDateTime
    monkeypatch.setattr(d06, 'datetime', make_fake(hour))
    assert DiscountEngine.calculate_discount(total_amount, user_tier, promo_code) == pytest.approx(expected)


def test_t_missing_promo_code_nightowl(monkeypatch):
    import data.input_code.d06_complex_logic as d06
    class FakeDateTime:
        @staticmethod
        def now():
            class FakeTime:
                hour = 1
            return FakeTime()
    monkeypatch.setattr(d06, 'datetime', FakeDateTime)
    assert DiscountEngine.calculate_discount(500.0, "STANDARD", "ABC-123") == pytest.approx(0.15)


def test_t_missing_promo_code_nightowl_super(monkeypatch):
    import data.input_code.d06_complex_logic as d06
    class FakeDateTime:
        @staticmethod
        def now():
            class FakeTime:
                hour = 1
            return FakeTime()
    monkeypatch.setattr(d06, 'datetime', FakeDateTime)
    assert DiscountEngine.calculate_discount(500.0, "STANDARD", "ABC-999") == pytest.approx(250.0)


def test_t_missing_tier_platinum_no_discount(monkeypatch):
    import data.input_code.d06_complex_logic as d06
    class FakeDateTime:
        @staticmethod
        def now():
            class FakeTime:
                hour = 12
            return FakeTime()
    monkeypatch.setattr(d06, 'datetime', FakeDateTime)
    assert DiscountEngine.calculate_discount(500.0, "PLATINUM", None) == pytest.approx(0.20)


def test_t_missing_tier_platinum_over_1000_no_promo(monkeypatch):
    import data.input_code.d06_complex_logic as d06
    class FakeDateTime:
        @staticmethod
        def now():
            class FakeTime:
                hour = 12
            return FakeTime()
    monkeypatch.setattr(d06, 'datetime', FakeDateTime)
    assert DiscountEngine.calculate_discount(1500.0, "PLATINUM", None) == pytest.approx(0.25)




def test_t_missing_tier_platinum_over_1000_promo_super(monkeypatch):
    import data.input_code.d06_complex_logic as d06
    class FakeDateTime:
        @staticmethod
        def now():
            class FakeTime:
                hour = 12
            return FakeTime()
    monkeypatch.setattr(d06, 'datetime', FakeDateTime)
    assert DiscountEngine.calculate_discount(1500.0, "PLATINUM", "XYZ-999") == pytest.approx(750.0)


def test_t_missing_user_validation_email_complex():
    # Complex but valid email should pass without raising
    o = OrderProcessor(Warehouse({}))
    assert o.validate_user("complex.email+test@domain.com", 25) is None


def test_t_missing_order_processor_success_without_promo():
    w = Warehouse({"item1": 20})
    op = OrderProcessor(w)
    result = op.process_order(
        "order9",
        {"email": "test@test.com", "age": 25, "tier": "GOLD", "payment_method": "CC"},
        [{"id": "item1", "qty": 2, "price": 100.0}],
        None
    )
    assert result["status"] == "success"
    assert result["order_id"] == "order9"
    assert result["original_price"] == 200.0
    assert result["discount_applied"] == pytest.approx(0.10)
    assert result["final_total"] == pytest.approx(219.6)
    assert result["items_count"] == 1


def test_t_missing_order_processor_success_with_zero_price(monkeypatch):
    w = Warehouse({"item1": 5})
    op = OrderProcessor(w)
    import data.input_code.d06_complex_logic as d06
    class FakeDateTime:
        @staticmethod
        def now():
            class FakeTime:
                hour = 12
            return FakeTime()
    monkeypatch.setattr(d06, 'datetime', FakeDateTime)
    result = op.process_order(
        "order10",
        {"email": "test@test.com", "age": 25, "tier": "GOLD", "payment_method": "CC"},
        [{"id": "item1", "qty": 1, "price": 0.0}],
        None
    )
    assert result["status"] == "success"
    assert result["order_id"] == "order10"
    assert result["original_price"] == 0.0
    assert result["discount_applied"] == pytest.approx(0.10)
    assert result["final_total"] == pytest.approx(0.0)
    assert result["items_count"] == 1