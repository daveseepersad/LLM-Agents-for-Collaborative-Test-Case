import pytest
from data.input_code.d01_bank import *

@pytest.mark.parametrize('initial_balance', [0, 150])
def test_init_default_and_positive(initial_balance):
    acc = BankAccount(initial_balance)
    assert acc.balance == initial_balance
    assert acc.is_active is True

def test_init_negative_raises():
    with pytest.raises(ValueError):
        BankAccount(-10)

@pytest.mark.parametrize('initial_balance, amount, expected', [
    (50, 25, 75),
])
def test_deposit_success(initial_balance, amount, expected):
    acc = BankAccount(initial_balance)
    result = acc.deposit(amount)
    assert result == expected
    assert acc.balance == expected

def test_deposit_invalid_amount_raises():
    acc = BankAccount(30)
    with pytest.raises(ValueError):
        acc.deposit(0)

def test_deposit_frozen_raises():
    acc = BankAccount(40)
    acc.freeze_account()
    with pytest.raises(ValueError):
        acc.deposit(10)

def test_freeze_unfreeze_deposit():
    acc = BankAccount(20)
    acc.freeze_account()
    acc.unfreeze_account()
    result = acc.deposit(15)
    assert result == 35

@pytest.mark.parametrize('initial_balance, amount, expected', [
    (100, 40, 60),
])
def test_withdraw_success(initial_balance, amount, expected):
    acc = BankAccount(initial_balance)
    result = acc.withdraw(amount)
    assert result == expected
    assert acc.balance == expected

def test_withdraw_invalid_amount_raises():
    acc = BankAccount(80)
    with pytest.raises(ValueError):
        acc.withdraw(-5)

def test_withdraw_insufficient_funds_raises():
    acc = BankAccount(30)
    with pytest.raises(ValueError):
        acc.withdraw(50)

def test_withdraw_frozen_raises():
    acc = BankAccount(70)
    acc.freeze_account()
    with pytest.raises(ValueError):
        acc.withdraw(20)