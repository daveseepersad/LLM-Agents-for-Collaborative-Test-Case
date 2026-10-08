import pytest
from data.input_code.d01_bank import *

@pytest.mark.parametrize('initial_balance, expected_balance, expected_is_active', [
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
    (100, 50, 150)
])
def test_bank_account_deposit_success(initial_balance, amount, expected):
    account = BankAccount(initial_balance)
    assert account.deposit(amount) == expected

@pytest.mark.parametrize('initial_balance, amount, expected_exception', [
    (100, 0, ValueError),
    (100, -10, ValueError)
])
def test_bank_account_deposit_error_amount(initial_balance, amount, expected_exception):
    account = BankAccount(initial_balance)
    with pytest.raises(expected_exception):
        account.deposit(amount)

def test_bank_account_deposit_error_frozen():
    account = BankAccount(100)
    account.freeze_account()
    with pytest.raises(ValueError):
        account.deposit(10)

@pytest.mark.parametrize('initial_balance, amount, expected', [
    (100, 40, 60)
])
def test_bank_account_withdraw_success(initial_balance, amount, expected):
    account = BankAccount(initial_balance)
    assert account.withdraw(amount) == expected

@pytest.mark.parametrize('initial_balance, amount, expected_exception', [
    (100, 0, ValueError),
    (100, -10, ValueError),
    (100, 200, ValueError)
])
def test_bank_account_withdraw_error(initial_balance, amount, expected_exception):
    account = BankAccount(initial_balance)
    with pytest.raises(expected_exception):
        account.withdraw(amount)

def test_bank_account_withdraw_error_frozen():
    account = BankAccount(100)
    account.freeze_account()
    with pytest.raises(ValueError):
        account.withdraw(10)

def test_bank_account_freeze_unfreeze():
    account = BankAccount(50)
    account.freeze_account()
    assert account.is_active == False
    account.unfreeze_account()
    assert account.is_active == True