import pytest
from data.input_code.d01_bank import *

@pytest.mark.parametrize('initial_balance, expected', [
    (100, None)
])
def test_bank_account_init_success(initial_balance, expected):
    account = BankAccount(initial_balance)
    assert account.balance == initial_balance
    assert account.is_active == True

def test_bank_account_init_error():
    with pytest.raises(ValueError):
        BankAccount(-50)

@pytest.mark.parametrize('initial_balance, amount, expected', [
    (100, 50, 150)
])
def test_bank_account_deposit_success(initial_balance, amount, expected):
    account = BankAccount(initial_balance)
    assert account.deposit(amount) == expected

def test_bank_account_deposit_error_frozen():
    account = BankAccount(100)
    account.freeze_account()
    with pytest.raises(ValueError):
        account.deposit(50)

def test_bank_account_deposit_error_nonpositive():
    account = BankAccount(100)
    with pytest.raises(ValueError):
        account.deposit(0)

@pytest.mark.parametrize('initial_balance, amount, expected', [
    (100, 50, 50)
])
def test_bank_account_withdraw_success(initial_balance, amount, expected):
    account = BankAccount(initial_balance)
    assert account.withdraw(amount) == expected

def test_bank_account_withdraw_error_frozen():
    account = BankAccount(100)
    account.freeze_account()
    with pytest.raises(ValueError):
        account.withdraw(50)

def test_bank_account_withdraw_error_nonpositive():
    account = BankAccount(100)
    with pytest.raises(ValueError):
        account.withdraw(0)

def test_bank_account_withdraw_error_insufficient():
    account = BankAccount(100)
    with pytest.raises(ValueError):
        account.withdraw(150)

def test_bank_account_freeze_ok():
    account = BankAccount(100)
    account.freeze_account()
    assert account.is_active == False

def test_bank_account_unfreeze_ok():
    account = BankAccount(100)
    account.freeze_account()
    account.unfreeze_account()
    assert account.is_active == True