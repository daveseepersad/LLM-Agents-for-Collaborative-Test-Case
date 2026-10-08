import pytest
from data.input_code.d01_bank import *

def test_init_success():
    acc = BankAccount(initial_balance=100)
    assert acc.balance == 100
    assert acc.is_active is True

def test_init_error():
    with pytest.raises(ValueError):
        BankAccount(initial_balance=-50)

@pytest.mark.parametrize('amount, expected_balance', [
    (50, 150),
])
def test_deposit_success(amount, expected_balance):
    acc = BankAccount(initial_balance=100)
    assert acc.deposit(amount) == expected_balance
    assert acc.balance == expected_balance

def test_deposit_error_frozen():
    acc = BankAccount(initial_balance=100)
    acc.freeze_account()
    with pytest.raises(ValueError):
        acc.deposit(50)

def test_deposit_error_nonpositive():
    acc = BankAccount(initial_balance=100)
    with pytest.raises(ValueError):
        acc.deposit(0)

@pytest.mark.parametrize('amount, expected_balance', [
    (50, 50),
])
def test_withdraw_success(amount, expected_balance):
    acc = BankAccount(initial_balance=100)
    assert acc.withdraw(amount) == expected_balance
    assert acc.balance == expected_balance

def test_withdraw_error_frozen():
    acc = BankAccount(initial_balance=100)
    acc.freeze_account()
    with pytest.raises(ValueError):
        acc.withdraw(50)

def test_withdraw_error_nonpositive():
    acc = BankAccount(initial_balance=100)
    with pytest.raises(ValueError):
        acc.withdraw(0)

def test_withdraw_error_insufficient():
    acc = BankAccount(initial_balance=100)
    with pytest.raises(ValueError):
        acc.withdraw(150)

def test_freeze_account():
    acc = BankAccount(initial_balance=100)
    acc.freeze_account()
    assert acc.is_active is False

def test_unfreeze_account():
    acc = BankAccount(initial_balance=100)
    acc.freeze_account()
    acc.unfreeze_account()
    assert acc.is_active is True