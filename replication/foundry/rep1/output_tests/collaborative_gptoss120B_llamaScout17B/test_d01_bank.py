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

def test_bank_account_init_negative():
    with pytest.raises(ValueError):
        BankAccount(-10)

@pytest.mark.parametrize('initial_balance, is_active, amount, expected', [
    (100, True, 50, 150)
])
def test_bank_account_deposit_success(initial_balance, is_active, amount, expected):
    account = BankAccount(initial_balance)
    if not is_active:
        account.freeze_account()
    if is_active:
        assert account.deposit(amount) == expected
    else:
        with pytest.raises(ValueError):
            account.deposit(amount)

@pytest.mark.parametrize('initial_balance, is_active, amount', [
    (100, True, 0),
    (100, False, 20)
])
def test_bank_account_deposit_error(initial_balance, is_active, amount):
    account = BankAccount(initial_balance)
    if not is_active:
        account.freeze_account()
    with pytest.raises(ValueError):
        account.deposit(amount)

@pytest.mark.parametrize('initial_balance, is_active, amount, expected', [
    (150, True, 30, 120)
])
def test_bank_account_withdraw_success(initial_balance, is_active, amount, expected):
    account = BankAccount(initial_balance)
    if not is_active:
        account.freeze_account()
    if is_active:
        assert account.withdraw(amount) == expected
    else:
        with pytest.raises(ValueError):
            account.withdraw(amount)

@pytest.mark.parametrize('initial_balance, is_active, amount', [
    (150, True, 0),
    (50, True, 100),
    (100, False, 20)
])
def test_bank_account_withdraw_error(initial_balance, is_active, amount):
    account = BankAccount(initial_balance)
    if not is_active:
        account.freeze_account()
    with pytest.raises(ValueError):
        account.withdraw(amount)

def test_bank_account_freeze_unfreeze():
    account = BankAccount(0)
    account.freeze_account()
    assert account.is_active == False
    account.unfreeze_account()
    assert account.is_active == True