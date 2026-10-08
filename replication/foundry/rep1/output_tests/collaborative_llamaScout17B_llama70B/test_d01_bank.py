import pytest
from data.input_code.d01_bank import *

@pytest.mark.parametrize('initial_balance, expected', [
    (100, None),
])
def test_init_success(initial_balance, expected):
    account = BankAccount(initial_balance)
    assert account.balance == initial_balance

def test_init_error():
    with pytest.raises(ValueError):
        BankAccount(-50)

@pytest.mark.parametrize('initial_balance, amount, expected', [
    (100, 50, 150),
])
def test_deposit_success(initial_balance, amount, expected):
    account = BankAccount(initial_balance)
    assert account.deposit(amount) == expected

@pytest.mark.parametrize('initial_balance, amount, expected', [
    (100, 0, 'ValueError'),
    (100, -50, 'ValueError'),
])
def test_deposit_error(initial_balance, amount, expected):
    account = BankAccount(initial_balance)
    if expected == 'ValueError':
        with pytest.raises(ValueError):
            account.deposit(amount)
    else:
        assert account.deposit(amount) == expected

def test_deposit_error_frozen():
    account = BankAccount(100)
    account.freeze_account()
    with pytest.raises(ValueError):
        account.deposit(50)

@pytest.mark.parametrize('initial_balance, amount, expected', [
    (100, 50, 50),
])
def test_withdraw_success(initial_balance, amount, expected):
    account = BankAccount(initial_balance)
    assert account.withdraw(amount) == expected

@pytest.mark.parametrize('initial_balance, amount, expected', [
    (100, 0, 'ValueError'),
    (100, -50, 'ValueError'),
    (100, 150, 'ValueError'),
])
def test_withdraw_error(initial_balance, amount, expected):
    account = BankAccount(initial_balance)
    if expected == 'ValueError':
        with pytest.raises(ValueError):
            account.withdraw(amount)
    else:
        assert account.withdraw(amount) == expected

def test_withdraw_error_frozen():
    account = BankAccount(100)
    account.freeze_account()
    with pytest.raises(ValueError):
        account.withdraw(50)

def test_freeze_unfreeze():
    account = BankAccount(100)
    account.freeze_account()
    assert account.is_active == False
    account.unfreeze_account()
    assert account.is_active == True