import pytest
from data.input_code.d01_bank import *

@pytest.mark.parametrize("initial_balance, expect_error", [
    (100, None),
    (-50, ValueError)
])
def test_init_balance(initial_balance, expect_error):
    if expect_error:
        with pytest.raises(expect_error):
            BankAccount(initial_balance)
    else:
        ba = BankAccount(initial_balance)
        assert ba.balance == initial_balance
        assert ba.is_active

def test_deposit_ok():
    ba = BankAccount(100)
    result = ba.deposit(50)
    assert result == 150
    assert ba.balance == 150

def test_deposit_on_frozen_raises():
    ba = BankAccount(100)
    ba.freeze_account()
    with pytest.raises(ValueError):
        ba.deposit(50)

def test_deposit_nonpositive_raises():
    ba = BankAccount(100)
    with pytest.raises(ValueError):
        ba.deposit(0)

def test_withdraw_ok():
    ba = BankAccount(100)
    result = ba.withdraw(50)
    assert result == 50
    assert ba.balance == 50

def test_withdraw_on_frozen_raises():
    ba = BankAccount(100)
    ba.freeze_account()
    with pytest.raises(ValueError):
        ba.withdraw(50)

def test_withdraw_nonpositive_raises():
    ba = BankAccount(100)
    with pytest.raises(ValueError):
        ba.withdraw(0)

def test_withdraw_insufficient_raises():
    ba = BankAccount(100)
    with pytest.raises(ValueError):
        ba.withdraw(150)

def test_freeze_ok():
    ba = BankAccount(100)
    ba.freeze_account()
    assert ba.is_active is False

def test_unfreeze_ok():
    ba = BankAccount(100)
    ba.freeze_account()
    ba.unfreeze_account()
    assert ba.is_active is True