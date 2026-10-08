import pytest
from data.input_code.d01_bank import *

@pytest.mark.parametrize("initial_balance", [100])
def test_init_success(initial_balance):
    acc = BankAccount(initial_balance)
    assert acc.balance == initial_balance
    assert acc.is_active is True

@pytest.mark.parametrize("initial_balance", [-50])
def test_init_error(initial_balance):
    with pytest.raises(ValueError):
        BankAccount(initial_balance)

@pytest.mark.parametrize("initial, amount, expected", [
    (100, 50, 150),
])
def test_deposit_success(initial, amount, expected):
    acc = BankAccount(initial)
    assert acc.deposit(amount) == expected

def test_deposit_error_frozen():
    acc = BankAccount(100)
    acc.freeze_account()
    with pytest.raises(ValueError):
        acc.deposit(50)

@pytest.mark.parametrize("initial, amount", [
    (100, 0),
    (100, -10),
])
def test_deposit_error_nonpositive(initial, amount):
    acc = BankAccount(initial)
    with pytest.raises(ValueError):
        acc.deposit(amount)

@pytest.mark.parametrize("initial, amount, expected", [
    (100, 50, 50),
])
def test_withdraw_success(initial, amount, expected):
    acc = BankAccount(initial)
    assert acc.withdraw(amount) == expected

def test_withdraw_error_frozen():
    acc = BankAccount(100)
    acc.freeze_account()
    with pytest.raises(ValueError):
        acc.withdraw(50)

@pytest.mark.parametrize("initial, amount", [
    (100, 0),
    (100, -5),
])
def test_withdraw_error_nonpositive(initial, amount):
    acc = BankAccount(initial)
    with pytest.raises(ValueError):
        acc.withdraw(amount)

def test_withdraw_error_insufficient():
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