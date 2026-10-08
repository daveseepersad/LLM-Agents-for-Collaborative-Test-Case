import pytest
from data.input_code.d01_bank import *

def test_init_negative():
    with pytest.raises(ValueError):
        BankAccount(initial_balance=-1)

def test_init_success():
    acc = BankAccount(initial_balance=0)
    assert acc.balance == 0
    assert acc.is_active is True

@pytest.mark.parametrize('amount', [-5, 0])
def test_deposit_invalid_amount(amount):
    acc = BankAccount()
    with pytest.raises(ValueError):
        acc.deposit(amount)

@pytest.mark.parametrize('amount', [-5, 0, 1])
def test_withdraw_invalid_amount(amount):
    acc = BankAccount()
    with pytest.raises(ValueError):
        acc.withdraw(amount)

def test_freeze_account():
    acc = BankAccount()
    acc.freeze_account()
    assert acc.is_active is False

def test_unfreeze_account():
    acc = BankAccount()
    acc.freeze_account()
    acc.unfreeze_account()
    assert acc.is_active is True

import pytest
from data.input_code.d01_bank import *

def test_init_positive():
    acc = BankAccount(initial_balance=10)
    assert acc.balance == 10
    assert acc.is_active is True

def test_deposit_success():
    acc = BankAccount(initial_balance=10)
    result = acc.deposit(5)
    assert result == 15
    assert acc.balance == 15

def test_withdraw_success():
    acc = BankAccount(initial_balance=20)
    result = acc.withdraw(5)
    assert result == 15
    assert acc.balance == 15

def test_deposit_frozen_account_raises():
    acc = BankAccount(initial_balance=10)
    acc.freeze_account()
    with pytest.raises(ValueError):
        acc.deposit(5)

def test_withdraw_insufficient_funds_raises():
    acc = BankAccount(initial_balance=5)
    with pytest.raises(ValueError):
        acc.withdraw(10)

import pytest
from data.input_code.d01_bank import *

def test_withdraw_frozen_account_raises():
    acc = BankAccount(initial_balance=10)
    acc.freeze_account()
    with pytest.raises(ValueError):
        acc.withdraw(5)

def test_withdraw_exact_balance_success():
    acc = BankAccount(initial_balance=10)
    result = acc.withdraw(10)
    assert result == 0
    assert acc.balance == 0