import pytest
from data.input_code.d01_bank import *

@pytest.mark.parametrize("initial_balance", [100])
def test_init_success(initial_balance):
    acc = BankAccount(initial_balance)
    assert acc.balance == initial_balance
    assert acc.is_active is True

def test_init_negative():
    with pytest.raises(ValueError):
        BankAccount(-50)

@pytest.mark.parametrize("initial_balance, deposit, expected_balance", [
    (100, 50, 150),
])
def test_deposit_success(initial_balance, deposit, expected_balance):
    acc = BankAccount(initial_balance)
    assert acc.deposit(deposit) == expected_balance
    assert acc.balance == expected_balance

@pytest.mark.parametrize("initial_balance, deposit", [
    (100, 0),
    (100, -10),
])
def test_deposit_nonpositive(initial_balance, deposit):
    acc = BankAccount(initial_balance)
    with pytest.raises(ValueError):
        acc.deposit(deposit)

def test_deposit_frozen():
    acc = BankAccount(100)
    acc.freeze_account()
    with pytest.raises(ValueError):
        acc.deposit(50)

@pytest.mark.parametrize("initial_balance, withdraw, expected_balance", [
    (100, 50, 50),
])
def test_withdraw_success(initial_balance, withdraw, expected_balance):
    acc = BankAccount(initial_balance)
    assert acc.withdraw(withdraw) == expected_balance
    assert acc.balance == expected_balance

@pytest.mark.parametrize("initial_balance, withdraw", [
    (100, 0),
    (100, -5),
])
def test_withdraw_nonpositive(initial_balance, withdraw):
    acc = BankAccount(initial_balance)
    with pytest.raises(ValueError):
        acc.withdraw(withdraw)

def test_withdraw_frozen():
    acc = BankAccount(100)
    acc.freeze_account()
    with pytest.raises(ValueError):
        acc.withdraw(50)

def test_withdraw_insufficient():
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