import pytest
from data.input_code.d01_bank import *

@pytest.mark.parametrize('initial_balance, expected', [
    (0, None),
    (100, None)
])
def test_bank_account_init_valid(initial_balance, expected):
    if expected is None:
        BankAccount(initial_balance)
    else:
        assert BankAccount(initial_balance) == expected

def test_bank_account_init_invalid():
    with pytest.raises(ValueError):
        BankAccount(-1)

@pytest.mark.parametrize('amount, expected, is_active', [
    (50, 50, True),
    (-10, 'ValueError', True),
    (10, 'ValueError', False)
])
def test_bank_account_deposit(amount, expected, is_active):
    account = BankAccount(0)
    account.is_active = is_active
    if isinstance(expected, str) and expected == 'ValueError':
        with pytest.raises(ValueError):
            account.deposit(amount)
    else:
        assert account.deposit(amount) == expected

@pytest.mark.parametrize('amount, expected, initial_balance, is_active', [
    (-5, 'ValueError', 100, True),
    (5, 'ValueError', 0, True),
    (10, 'ValueError', 100, False)
])
def test_bank_account_withdraw(amount, expected, initial_balance, is_active):
    account = BankAccount(initial_balance)
    account.is_active = is_active
    if isinstance(expected, str) and expected == 'ValueError':
        with pytest.raises(ValueError):
            account.withdraw(amount)
    else:
        assert account.withdraw(amount) == expected

def test_bank_account_freeze():
    account = BankAccount(100)
    account.freeze_account()
    assert not account.is_active

def test_bank_account_unfreeze():
    account = BankAccount(100)
    account.freeze_account()
    account.unfreeze_account()
    assert account.is_active

import pytest
from data.input_code.d01_bank import *

def test_bank_account_init_default_active():
    account = BankAccount(0)
    assert account.is_active == True

@pytest.mark.parametrize('amount, expected', [
    (0, 'ValueError')
])
def test_bank_account_deposit_zero(amount, expected):
    account = BankAccount(0)
    if isinstance(expected, str) and expected == 'ValueError':
        with pytest.raises(ValueError):
            account.deposit(amount)
    else:
        assert account.deposit(amount) == expected

@pytest.mark.parametrize('amount, expected, initial_balance', [
    (0, 'ValueError', 100)
])
def test_bank_account_withdraw_zero(amount, expected, initial_balance):
    account = BankAccount(initial_balance)
    if isinstance(expected, str) and expected == 'ValueError':
        with pytest.raises(ValueError):
            account.withdraw(amount)
    else:
        assert account.withdraw(amount) == expected

import pytest
from data.input_code.d01_bank import *

def test_bank_account_withdraw_exact_balance():
    account = BankAccount(100)
    account.is_active = True
    assert account.withdraw(100) == 0