import pytest
from data.input_code.d01_bank import *

@pytest.mark.parametrize("initial_balance", [
    100,
])
def test_init_success(initial_balance):
    acc = BankAccount(initial_balance)
    assert acc.balance == initial_balance
    assert acc.is_active is True

def test_init_negative_balance():
    with pytest.raises(ValueError):
        BankAccount(-50)

@pytest.mark.parametrize("start_balance, deposit_amount, expected_balance", [
    (100, 50, 150),
])
def test_deposit_success(start_balance, deposit_amount, expected_balance):
    acc = BankAccount(start_balance)
    result = acc.deposit(deposit_amount)
    assert result == expected_balance
    assert acc.balance == expected_balance

def test_deposit_on_frozen_account():
    acc = BankAccount(100)
    acc.freeze_account()
    with pytest.raises(ValueError):
        acc.deposit(50)

def test_deposit_nonpositive_amount():
    acc = BankAccount(100)
    with pytest.raises(ValueError):
        acc.deposit(0)

@pytest.mark.parametrize("start_balance, withdraw_amount, expected_balance", [
    (100, 50, 50),
])
def test_withdraw_success(start_balance, withdraw_amount, expected_balance):
    acc = BankAccount(start_balance)
    result = acc.withdraw(withdraw_amount)
    assert result == expected_balance
    assert acc.balance == expected_balance

def test_withdraw_on_frozen_account():
    acc = BankAccount(100)
    acc.freeze_account()
    with pytest.raises(ValueError):
        acc.withdraw(50)

def test_withdraw_nonpositive_amount():
    acc = BankAccount(100)
    with pytest.raises(ValueError):
        acc.withdraw(0)

def test_withdraw_insufficient_funds():
    acc = BankAccount(100)
    with pytest.raises(ValueError):
        acc.withdraw(150)

def test_freeze_account():
    acc = BankAccount(100)
    acc.freeze_account()
    assert acc.is_active is False

def test_unfreeze_account():
    acc = BankAccount(100)
    acc.freeze_account()
    acc.unfreeze_account()
    assert acc.is_active is True