import pytest
from data.input_code.d01_bank import *

# Helper to create an account with optional frozen state
def make_account(initial_balance=0, freeze=False):
    acct = BankAccount(initial_balance)
    if freeze:
        acct.freeze_account()
    return acct

def test_init_success():
    acct = BankAccount(100)
    assert acct.balance == 100
    assert acct.is_active is True

def test_init_negative_balance():
    with pytest.raises(ValueError):
        BankAccount(-50)

@pytest.mark.parametrize(
    "initial, amount, expected_balance",
    [
        (100, 50, 150),
    ],
)
def test_deposit_success(initial, amount, expected_balance):
    acct = make_account(initial)
    assert acct.deposit(amount) == expected_balance
    assert acct.balance == expected_balance

@pytest.mark.parametrize(
    "initial, amount, freeze, exc",
    [
        (100, 0, False, ValueError),      # zero deposit
        (100, -20, False, ValueError),    # negative deposit
        (100, 50, True, ValueError),      # deposit on frozen account
    ],
)
def test_deposit_errors(initial, amount, freeze, exc):
    acct = make_account(initial, freeze)
    with pytest.raises(exc):
        acct.deposit(amount)

@pytest.mark.parametrize(
    "initial, amount, expected_balance",
    [
        (100, 20, 80),
    ],
)
def test_withdraw_success(initial, amount, expected_balance):
    acct = make_account(initial)
    assert acct.withdraw(amount) == expected_balance
    assert acct.balance == expected_balance

@pytest.mark.parametrize(
    "initial, amount, freeze, exc",
    [
        (100, 0, False, ValueError),       # zero withdrawal
        (100, -20, False, ValueError),     # negative withdrawal
        (100, 200, False, ValueError),     # insufficient funds
        (100, 20, True, ValueError),       # withdrawal on frozen account
    ],
)
def test_withdraw_errors(initial, amount, freeze, exc):
    acct = make_account(initial, freeze)
    with pytest.raises(exc):
        acct.withdraw(amount)

def test_freeze_account():
    acct = make_account(100)
    acct.freeze_account()
    assert acct.is_active is False

def test_unfreeze_account():
    acct = make_account(100, freeze=True)
    acct.unfreeze_account()
    assert acct.is_active is True