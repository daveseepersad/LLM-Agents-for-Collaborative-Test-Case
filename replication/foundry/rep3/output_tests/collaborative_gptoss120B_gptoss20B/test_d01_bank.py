import pytest
from data.input_code.d01_bank import *

# ---------- __init__ ----------
@pytest.mark.parametrize('initial_balance, exc', [
    (-5, ValueError),
    (None, TypeError),
])
def test_bankaccount_init_errors(initial_balance, exc):
    with pytest.raises(exc):
        BankAccount(initial_balance)

@pytest.mark.parametrize('initial_balance, expected_balance', [
    (0, 0),
])
def test_bankaccount_init_success(initial_balance, expected_balance):
    acct = BankAccount(initial_balance)
    assert acct.balance == expected_balance
    assert acct.is_active is True

# ---------- deposit ----------
@pytest.mark.parametrize('initial_balance, amount, expected_balance', [
    (10, 5, 15),
])
def test_bankaccount_deposit_success(initial_balance, amount, expected_balance):
    acct = BankAccount(initial_balance)
    result = acct.deposit(amount)
    assert result == expected_balance
    assert acct.balance == expected_balance

@pytest.mark.parametrize('initial_balance, amount, exc', [
    (10, -3, ValueError),
    (10, 0, ValueError),
])
def test_bankaccount_deposit_errors(initial_balance, amount, exc):
    acct = BankAccount(initial_balance)
    with pytest.raises(exc):
        acct.deposit(amount)

# ---------- withdraw ----------
@pytest.mark.parametrize('initial_balance, amount, expected_balance', [
    (50, 20, 30),
])
def test_bankaccount_withdraw_success(initial_balance, amount, expected_balance):
    acct = BankAccount(initial_balance)
    result = acct.withdraw(amount)
    assert result == expected_balance
    assert acct.balance == expected_balance

@pytest.mark.parametrize('initial_balance, amount, exc', [
    (10, -5, ValueError),
    (10, 0, ValueError),
    (5, 10, ValueError),
])
def test_bankaccount_withdraw_errors(initial_balance, amount, exc):
    acct = BankAccount(initial_balance)
    with pytest.raises(exc):
        acct.withdraw(amount)

# ---------- freeze / unfreeze ----------
def test_bankaccount_freeze_account():
    acct = BankAccount(0)
    acct.freeze_account()
    assert acct.is_active is False

def test_bankaccount_unfreeze_account():
    acct = BankAccount(0)
    acct.freeze_account()  # first freeze
    acct.unfreeze_account()
    assert acct.is_active is True

import pytest
from data.input_code.d01_bank import *

# ---------- frozen deposit ----------
@pytest.mark.parametrize('initial_balance, amount', [
    (100, 50),
])
def test_bankaccount_deposit_frozen(initial_balance, amount):
    acct = BankAccount(initial_balance)
    acct.freeze_account()
    with pytest.raises(ValueError):
        acct.deposit(amount)

# ---------- frozen withdraw ----------
@pytest.mark.parametrize('initial_balance, amount', [
    (100, 10),
])
def test_bankaccount_withdraw_frozen(initial_balance, amount):
    acct = BankAccount(initial_balance)
    acct.freeze_account()
    with pytest.raises(ValueError):
        acct.withdraw(amount)