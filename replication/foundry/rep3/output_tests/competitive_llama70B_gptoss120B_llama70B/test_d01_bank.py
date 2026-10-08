import pytest
from data.input_code.d01_bank import *

def _make_account(initial_balance=0, freeze=False):
    acct = BankAccount(initial_balance)
    if freeze:
        acct.freeze_account()
    return acct

def test_init_happy_path():
    acct = BankAccount(100)
    assert acct.balance == 100
    assert acct.is_active is True

def test_init_negative_balance():
    with pytest.raises(ValueError):
        BankAccount(-50)

@pytest.mark.parametrize(
    "setup, amount, expected_balance",
    [
        ({"initial_balance": 100, "freeze_account": False}, 50, 150),
    ],
)
def test_deposit_success(setup, amount, expected_balance):
    acct = _make_account(setup["initial_balance"], setup.get("freeze_account", False))
    assert acct.deposit(amount) == expected_balance

@pytest.mark.parametrize(
    "setup, amount, exc",
    [
        ({"initial_balance": 100, "freeze_account": True}, 50, ValueError),   # frozen account
        ({"initial_balance": 100, "freeze_account": False}, 0, ValueError),   # non‑positive amount
        ({"initial_balance": 100, "freeze_account": False}, -50, ValueError), # negative amount
    ],
)
def test_deposit_errors(setup, amount, exc):
    acct = _make_account(setup["initial_balance"], setup.get("freeze_account", False))
    with pytest.raises(exc):
        acct.deposit(amount)

@pytest.mark.parametrize(
    "setup, amount, expected_balance",
    [
        ({"initial_balance": 100, "freeze_account": False}, 50, 50),
    ],
)
def test_withdraw_success(setup, amount, expected_balance):
    acct = _make_account(setup["initial_balance"], setup.get("freeze_account", False))
    assert acct.withdraw(amount) == expected_balance

@pytest.mark.parametrize(
    "setup, amount, exc",
    [
        ({"initial_balance": 100, "freeze_account": True}, 50, ValueError),    # frozen account
        ({"initial_balance": 100, "freeze_account": False}, 0, ValueError),    # non‑positive amount
        ({"initial_balance": 100, "freeze_account": False}, -50, ValueError),  # negative amount
        ({"initial_balance": 100, "freeze_account": False}, 150, ValueError),  # insufficient funds
    ],
)
def test_withdraw_errors(setup, amount, exc):
    acct = _make_account(setup["initial_balance"], setup.get("freeze_account", False))
    with pytest.raises(exc):
        acct.withdraw(amount)

def test_freeze_account():
    acct = _make_account(initial_balance=100)
    acct.freeze_account()
    assert acct.is_active is False

def test_unfreeze_account():
    acct = _make_account(initial_balance=100, freeze=True)
    acct.unfreeze_account()
    assert acct.is_active is True