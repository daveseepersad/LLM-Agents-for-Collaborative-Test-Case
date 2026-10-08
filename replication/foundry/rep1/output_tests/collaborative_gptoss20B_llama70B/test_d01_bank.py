import pytest
from data.input_code.d01_bank import *

@pytest.mark.parametrize('initial_balance, expected', [
    (-1, 'ValueError')
])
def test_init_negative(initial_balance, expected):
    if expected == 'ValueError':
        with pytest.raises(ValueError):
            BankAccount(initial_balance)
    else:
        BankAccount(initial_balance)

@pytest.mark.parametrize('initial_balance, amount, expected', [
    (100, 0, 'ValueError'),
    (100, -50, 'ValueError')
])
def test_deposit_leq_zero(initial_balance, amount, expected):
    account = BankAccount(initial_balance)
    if expected == 'ValueError':
        with pytest.raises(ValueError):
            account.deposit(amount)
    else:
        account.deposit(amount)

@pytest.mark.parametrize('initial_balance, amount, expected', [
    (100, 50, 150)
])
def test_deposit_valid(initial_balance, amount, expected):
    account = BankAccount(initial_balance)
    assert account.deposit(amount) == expected

@pytest.mark.parametrize('initial_balance, amount, expected', [
    (100, 0, 'ValueError'),
    (100, -50, 'ValueError')
])
def test_withdraw_leq_zero(initial_balance, amount, expected):
    account = BankAccount(initial_balance)
    if expected == 'ValueError':
        with pytest.raises(ValueError):
            account.withdraw(amount)
    else:
        account.withdraw(amount)

@pytest.mark.parametrize('initial_balance, amount, expected', [
    (100, 150, 'ValueError')
])
def test_withdraw_insufficient_funds(initial_balance, amount, expected):
    account = BankAccount(initial_balance)
    if expected == 'ValueError':
        with pytest.raises(ValueError):
            account.withdraw(amount)
    else:
        account.withdraw(amount)

@pytest.mark.parametrize('initial_balance, amount, expected', [
    (100, 40, 60)
])
def test_withdraw_valid(initial_balance, amount, expected):
    account = BankAccount(initial_balance)
    assert account.withdraw(amount) == expected

def test_freeze_unfreeze():
    account = BankAccount(10)
    account.freeze_account()
    assert account.is_active == False
    account.unfreeze_account()
    assert account.is_active == True

def test_deposit_when_frozen():
    account = BankAccount(100)
    account.freeze_account()
    with pytest.raises(ValueError):
        account.deposit(50)

def test_withdraw_when_frozen():
    account = BankAccount(100)
    account.freeze_account()
    with pytest.raises(ValueError):
        account.withdraw(10)