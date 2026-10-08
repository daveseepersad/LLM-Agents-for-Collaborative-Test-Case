import pytest
from data.input_code.d01_bank import *

def test_bank_init_ok():
    acc = BankAccount(initial_balance=100)
    assert acc.balance == 100
    assert acc.is_active is True

def test_bank_init_err_negative():
    with pytest.raises(ValueError):
        BankAccount(initial_balance=-50)

def test_bank_deposit_ok():
    acc = BankAccount(100)
    result = acc.deposit(50)
    assert result == 150
    assert acc.balance == 150

def test_bank_deposit_err_frozen():
    acc = BankAccount(100)
    acc.freeze_account()
    with pytest.raises(ValueError):
        acc.deposit(50)

def test_bank_deposit_err_nonpositive():
    acc = BankAccount(100)
    with pytest.raises(ValueError):
        acc.deposit(0)

def test_bank_withdraw_ok():
    acc = BankAccount(100)
    result = acc.withdraw(50)
    assert result == 50
    assert acc.balance == 50

def test_bank_withdraw_err_frozen():
    acc = BankAccount(100)
    acc.freeze_account()
    with pytest.raises(ValueError):
        acc.withdraw(50)

def test_bank_withdraw_err_nonpositive():
    acc = BankAccount(100)
    with pytest.raises(ValueError):
        acc.withdraw(0)

def test_bank_withdraw_err_insufficient():
    acc = BankAccount(100)
    with pytest.raises(ValueError):
        acc.withdraw(150)

def test_bank_freeze_ok():
    acc = BankAccount(100)
    acc.freeze_account()
    assert acc.is_active is False

def test_bank_unfreeze_ok():
    acc = BankAccount(100)
    acc.freeze_account()
    acc.unfreeze_account()
    assert acc.is_active is True