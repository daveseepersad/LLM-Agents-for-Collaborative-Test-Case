import pytest
from data.input_code.d01_bank import *

@pytest.mark.parametrize('initial_balance, expected_balance, expected_is_active', [
    (0, 0, True),
    (100, 100, True)
])
def test_bank_account_init_success(initial_balance, expected_balance, expected_is_active):
    account = BankAccount(initial_balance)
    assert account.balance == expected_balance
    assert account.is_active == expected_is_active

def test_bank_account_init_error():
    with pytest.raises(ValueError):
        BankAccount(-10)

@pytest.mark.parametrize('initial_balance, amount, expected', [
    (50, 25, 75)
])
def test_bank_account_deposit_success(initial_balance, amount, expected):
    account = BankAccount(initial_balance)
    assert account.deposit(amount) == expected

@pytest.mark.parametrize('initial_balance, amount, expected_exception', [
    (50, 0, ValueError),
    (50, -5, ValueError)
])
def test_bank_account_deposit_error_amount(initial_balance, amount, expected_exception):
    account = BankAccount(initial_balance)
    with pytest.raises(expected_exception):
        account.deposit(amount)

def test_bank_account_deposit_error_frozen():
    account = BankAccount(50)
    account.freeze_account()
    with pytest.raises(ValueError):
        account.deposit(10)

@pytest.mark.parametrize('initial_balance, amount, expected', [
    (80, 30, 50),
    (40, 40, 0)
])
def test_bank_account_withdraw_success(initial_balance, amount, expected):
    account = BankAccount(initial_balance)
    assert account.withdraw(amount) == expected

@pytest.mark.parametrize('initial_balance, amount, expected_exception', [
    (50, 0, ValueError),
    (50, -10, ValueError),
    (30, 50, ValueError)
])
def test_bank_account_withdraw_error(initial_balance, amount, expected_exception):
    account = BankAccount(initial_balance)
    with pytest.raises(expected_exception):
        account.withdraw(amount)

def test_bank_account_withdraw_error_frozen():
    account = BankAccount(60)
    account.freeze_account()
    with pytest.raises(ValueError):
        account.withdraw(20)

def test_bank_account_freeze_account():
    account = BankAccount(10)
    account.freeze_account()
    assert account.is_active == False

def test_bank_account_unfreeze_account():
    account = BankAccount(10)
    account.freeze_account()
    account.unfreeze_account()
    assert account.is_active == True