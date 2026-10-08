import pytest
from data.input_code.d01_bank import *

@pytest.mark.parametrize('initial_balance, expected', [
    (0, {'balance': 0, 'is_active': True}),
    (100, {'balance': 100, 'is_active': True}),
])
def test_bank_account_init_ok(initial_balance, expected):
    acc = BankAccount(initial_balance)
    assert acc.balance == expected['balance']
    assert acc.is_active == expected['is_active']

def test_bank_account_init_negative():
    with pytest.raises(ValueError):
        BankAccount(-5)

@pytest.mark.parametrize('initial_balance, deposit_amount, expected', [
    (50, 25, 75),
])
def test_bank_account_deposit_ok(initial_balance, deposit_amount, expected):
    acc = BankAccount(initial_balance)
    assert acc.deposit(deposit_amount) == expected

def test_bank_account_deposit_negative():
    acc = BankAccount(50)
    with pytest.raises(ValueError):
        acc.deposit(0)

@pytest.mark.parametrize('initial_balance, withdraw_amount, expected', [
    (100, 40, 60),
])
def test_bank_account_withdraw_ok(initial_balance, withdraw_amount, expected):
    acc = BankAccount(initial_balance)
    assert acc.withdraw(withdraw_amount) == expected

def test_bank_account_withdraw_negative():
    acc = BankAccount(100)
    with pytest.raises(ValueError):
        acc.withdraw(-5)

@pytest.mark.parametrize('initial_balance, withdraw_amount', [
    (30, 50),
])
def test_bank_account_withdraw_no_funds(initial_balance, withdraw_amount):
    acc = BankAccount(initial_balance)
    with pytest.raises(ValueError):
        acc.withdraw(withdraw_amount)

def test_bank_account_freeze_account():
    acc = BankAccount(80)
    acc.freeze_account()
    assert acc.is_active is False

def test_bank_account_unfreeze_account():
    acc = BankAccount(0)
    acc.unfreeze_account()
    assert acc.is_active is True

import pytest

@pytest.mark.parametrize("initial_balance, withdraw_amount, expected", [
    (50, 50, 0),
    (20, 0, "ValueError"),
])
def test_bank_account_withdraw_cases(initial_balance, withdraw_amount, expected):
    acc = BankAccount(initial_balance)
    if isinstance(expected, str) and expected == "ValueError":
        with pytest.raises(ValueError):
            acc.withdraw(withdraw_amount)
    else:
        result = acc.withdraw(withdraw_amount)
        assert result == expected

def test_bank_account_deposit_negative():
    acc = BankAccount(30)
    with pytest.raises(ValueError):
        acc.deposit(-5)

@pytest.mark.parametrize("method", ["deposit", "withdraw"])
def test_bank_account_frozen_raises_for_method(method, initial_balance=100, amount=10):
    acc = BankAccount(initial_balance)
    acc.freeze_account()
    if method == "deposit":
        with pytest.raises(ValueError):
            acc.deposit(amount)
    else:
        with pytest.raises(ValueError):
            acc.withdraw(amount)