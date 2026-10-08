import pytest
from data.input_code.d01_bank import *

@pytest.fixture
def account():
    """Provides a fresh BankAccount with balance 100 and active state."""
    return BankAccount(100)

# ---------- __init__ ----------
def test_init_happy_path():
    acc = BankAccount(100)
    assert acc.balance == 100
    assert acc.is_active is True

def test_init_negative_balance():
    with pytest.raises(ValueError):
        BankAccount(-50)

# ---------- deposit ----------
@pytest.mark.parametrize(
    "freeze, amount, expected_balance, exc",
    [
        (False, 50, 150, None),          # happy path
        (False, 0, None, ValueError),    # zero deposit
        (False, -20, None, ValueError),  # negative deposit
        (True, 50, None, ValueError),    # frozen account
    ],
)
def test_deposit_variants(account, freeze, amount, expected_balance, exc):
    if freeze:
        account.freeze_account()
    if exc:
        with pytest.raises(exc):
            account.deposit(amount)
    else:
        result = account.deposit(amount)
        assert result == expected_balance
        assert account.balance == expected_balance

# ---------- withdraw ----------
@pytest.mark.parametrize(
    "freeze, amount, expected_balance, exc",
    [
        (False, 20, 80, None),           # happy path
        (False, 0, None, ValueError),    # zero withdrawal
        (False, -30, None, ValueError),  # negative withdrawal
        (False, 150, None, ValueError),  # insufficient funds
        (True, 20, None, ValueError),    # frozen account
    ],
)
def test_withdraw_variants(account, freeze, amount, expected_balance, exc):
    if freeze:
        account.freeze_account()
    if exc:
        with pytest.raises(exc):
            account.withdraw(amount)
    else:
        result = account.withdraw(amount)
        assert result == expected_balance
        assert account.balance == expected_balance

# ---------- freeze_account ----------
def test_freeze_account(account):
    account.freeze_account()
    assert account.is_active is False

# ---------- unfreeze_account ----------
def test_unfreeze_account(account):
    account.freeze_account()
    account.unfreeze_account()
    assert account.is_active is True