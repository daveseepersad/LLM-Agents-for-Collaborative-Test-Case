import pytest
from data.input_code.d01_bank import *

@pytest.mark.parametrize('initial_balance, expected', [
    (100, 100)
])
def test_bank_account_init_success(initial_balance, expected):
    account = BankAccount(initial_balance)
    assert account.balance == expected

def test_bank_account_init_error():
    with pytest.raises(ValueError):
        BankAccount(-5)

@pytest.mark.parametrize('initial_balance, amount, expected', [
    (100, 25, 125)
])
def test_bank_account_deposit_success(initial_balance, amount, expected):
    account = BankAccount(initial_balance)
    result = account.deposit(amount)
    assert result == expected

@pytest.mark.parametrize('initial_balance, amount, expected', [
    (50, 0, 'ValueError'),
    (50, -10, 'ValueError')
])
def test_bank_account_deposit_error(initial_balance, amount, expected):
    account = BankAccount(initial_balance)
    with pytest.raises(ValueError) if expected == 'ValueError' else pytest.fail('Unexpected test case'):
        account.deposit(amount)

def test_bank_account_deposit_frozen():
    account = BankAccount(50)
    account.freeze_account()
    with pytest.raises(ValueError):
        account.deposit(10)

@pytest.mark.parametrize('initial_balance, amount, expected', [
    (100, 30, 70)
])
def test_bank_account_withdraw_success(initial_balance, amount, expected):
    account = BankAccount(initial_balance)
    result = account.withdraw(amount)
    assert result == expected

@pytest.mark.parametrize('initial_balance, amount, expected', [
    (50, 0, 'ValueError'),
    (50, -10, 'ValueError'),
    (60, 100, 'ValueError')
])
def test_bank_account_withdraw_error(initial_balance, amount, expected):
    account = BankAccount(initial_balance)
    with pytest.raises(ValueError) if expected == 'ValueError' else pytest.fail('Unexpected test case'):
        account.withdraw(amount)

def test_bank_account_withdraw_frozen():
    account = BankAccount(60)
    account.freeze_account()
    with pytest.raises(ValueError):
        account.withdraw(10)

def test_bank_account_freeze():
    account = BankAccount(10)
    account.freeze_account()
    assert not account.is_active

def test_bank_account_unfreeze():
    account = BankAccount(0)
    account.freeze_account()
    account.unfreeze_account()
    assert account.is_active