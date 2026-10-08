import pytest
from data.input_code.d01_bank import *

@pytest.mark.parametrize('initial_balance, expected_exception', [
    (100, None),
    (-50, ValueError)
])
def test_init_bank_account(initial_balance, expected_exception):
    if expected_exception:
        with pytest.raises(expected_exception):
            BankAccount(initial_balance)
    else:
        acc = BankAccount(initial_balance)
        assert acc.balance == initial_balance
        assert acc.is_active is True

def test_deposit_ok():
    acc = BankAccount(100)
    result = acc.deposit(50)
    assert result == 150

def test_deposit_nonpositive():
    acc = BankAccount(100)
    with pytest.raises(ValueError):
        acc.deposit(0)

def test_deposit_frozen():
    acc = BankAccount(100)
    acc.freeze_account()
    with pytest.raises(ValueError):
        acc.deposit(50)

def test_withdraw_ok():
    acc = BankAccount(100)
    result = acc.withdraw(50)
    assert result == 50

def test_withdraw_frozen():
    acc = BankAccount(100)
    acc.freeze_account()
    with pytest.raises(ValueError):
        acc.withdraw(50)

def test_withdraw_nonpositive():
    acc = BankAccount(100)
    with pytest.raises(ValueError):
        acc.withdraw(0)

def test_withdraw_insufficient():
    acc = BankAccount(100)
    with pytest.raises(ValueError):
        acc.withdraw(150)

def test_freeze_ok():
    acc = BankAccount(100)
    acc.freeze_account()
    assert acc.is_active is False

def test_unfreeze_ok():
    acc = BankAccount(100)
    acc.freeze_account()
    acc.unfreeze_account()
    assert acc.is_active is True