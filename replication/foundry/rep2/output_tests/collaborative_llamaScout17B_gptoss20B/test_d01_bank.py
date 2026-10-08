import pytest
from data.input_code.d01_bank import *

@pytest.mark.parametrize("initial_balance, expected", [
    (100, None),
    (-50, "ValueError"),
])
def test_bankaccount_init(initial_balance, expected):
    if expected is None:
        acc = BankAccount(initial_balance)
        assert acc.balance == initial_balance
        assert acc.is_active is True
    else:
        with pytest.raises(ValueError):
            BankAccount(initial_balance)

def test_bankaccount_deposit_ok():
    acc = BankAccount(100)
    result = acc.deposit(50)
    assert result == 150

def test_bankaccount_deposit_err_nonpositive():
    acc = BankAccount(100)
    with pytest.raises(ValueError):
        acc.deposit(0)

def test_bankaccount_deposit_err_frozen():
    acc = BankAccount(100)
    acc.freeze_account()
    with pytest.raises(ValueError):
        acc.deposit(50)

def test_bankaccount_withdraw_ok():
    acc = BankAccount(100)
    result = acc.withdraw(50)
    assert result == 50

def test_bankaccount_withdraw_err_nonpositive():
    acc = BankAccount(100)
    with pytest.raises(ValueError):
        acc.withdraw(0)

def test_bankaccount_withdraw_err_insufficient():
    acc = BankAccount(100)
    with pytest.raises(ValueError):
        acc.withdraw(150)

def test_bankaccount_withdraw_err_frozen():
    acc = BankAccount(100)
    acc.freeze_account()
    with pytest.raises(ValueError):
        acc.withdraw(50)

def test_bankaccount_freeze_ok():
    acc = BankAccount(100)
    acc.freeze_account()
    assert acc.is_active is False

def test_bankaccount_unfreeze_ok():
    acc = BankAccount(100)
    acc.freeze_account()
    acc.unfreeze_account()
    assert acc.is_active is True