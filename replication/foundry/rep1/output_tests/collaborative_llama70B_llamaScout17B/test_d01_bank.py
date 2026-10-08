import pytest
from data.input_code.d01_bank import *

@pytest.mark.parametrize('initial_balance, expected_balance', [
    (100, 100)
])
def test_bank_account_init(initial_balance, expected_balance):
    account = BankAccount(initial_balance)
    assert account.balance == expected_balance

def test_bank_account_init_negative():
    with pytest.raises(ValueError):
        BankAccount(-50)

@pytest.mark.parametrize('initial_balance, amount, expected_balance', [
    (100, 50, 150)
])
def test_bank_account_deposit(initial_balance, amount, expected_balance):
    account = BankAccount(initial_balance)
    assert account.deposit(amount) == expected_balance

def test_bank_account_deposit_frozen():
    account = BankAccount(100)
    account.freeze_account()
    with pytest.raises(ValueError):
        account.deposit(50)

@pytest.mark.parametrize('initial_balance, amount', [
    (100, 0),
    (100, -50)
])
def test_bank_account_deposit_invalid_amount(initial_balance, amount):
    account = BankAccount(initial_balance)
    with pytest.raises(ValueError):
        account.deposit(amount)

@pytest.mark.parametrize('initial_balance, amount, expected_balance', [
    (100, 50, 50)
])
def test_bank_account_withdraw(initial_balance, amount, expected_balance):
    account = BankAccount(initial_balance)
    assert account.withdraw(amount) == expected_balance

def test_bank_account_withdraw_frozen():
    account = BankAccount(100)
    account.freeze_account()
    with pytest.raises(ValueError):
        account.withdraw(50)

@pytest.mark.parametrize('initial_balance, amount', [
    (100, 0),
    (100, -50),
    (100, 150)
])
def test_bank_account_withdraw_invalid_amount(initial_balance, amount):
    account = BankAccount(initial_balance)
    with pytest.raises(ValueError):
        account.withdraw(amount)

def test_bank_account_freeze():
    account = BankAccount(100)
    account.freeze_account()
    assert not account.is_active

def test_bank_account_unfreeze():
    account = BankAccount(100)
    account.freeze_account()
    account.unfreeze_account()
    assert account.is_active