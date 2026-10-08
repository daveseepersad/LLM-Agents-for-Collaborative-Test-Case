import pytest
from data.input_code.d01_bank import *

def make_account(initial_balance: int, freeze: bool = False) -> BankAccount:
    """Helper to create a BankAccount with optional frozen state."""
    acct = BankAccount(initial_balance)
    if freeze:
        acct.freeze_account()
    return acct

# -------------------- __init__ --------------------
@pytest.mark.parametrize(
    "initial_balance, expected_exception",
    [
        (100, None),          # happy path
        (-50, ValueError),    # negative balance
    ],
)
def test_bankaccount_init(initial_balance, expected_exception):
    if expected_exception:
        with pytest.raises(expected_exception):
            BankAccount(initial_balance)
    else:
        acct = BankAccount(initial_balance)
        assert acct.balance == initial_balance
        assert acct.is_active is True

# -------------------- deposit --------------------
@pytest.mark.parametrize(
    "setup_balance, freeze, amount, expected, expected_exception",
    [
        (100, False, 50, 150, None),               # OK deposit
        (100, True, 50, None, ValueError),         # frozen account
        (100, False, 0, None, ValueError),         # non‑positive amount
        (100, False, -50, None, ValueError),       # negative amount
    ],
)
def test_bankaccount_deposit(setup_balance, freeze, amount, expected, expected_exception):
    acct = make_account(setup_balance, freeze)
    if expected_exception:
        with pytest.raises(expected_exception):
            acct.deposit(amount)
    else:
        result = acct.deposit(amount)
        assert result == expected
        assert acct.balance == expected

# -------------------- withdraw --------------------
@pytest.mark.parametrize(
    "setup_balance, freeze, amount, expected, expected_exception",
    [
        (100, False, 50, 50, None),                # OK withdraw
        (100, True, 50, None, ValueError),         # frozen account
        (100, False, 0, None, ValueError),         # non‑positive amount
        (100, False, -50, None, ValueError),       # negative amount
        (100, False, 150, None, ValueError),       # insufficient funds
    ],
)
def test_bankaccount_withdraw(setup_balance, freeze, amount, expected, expected_exception):
    acct = make_account(setup_balance, freeze)
    if expected_exception:
        with pytest.raises(expected_exception):
            acct.withdraw(amount)
    else:
        result = acct.withdraw(amount)
        assert result == expected
        assert acct.balance == expected

# -------------------- freeze_account --------------------
def test_bankaccount_freeze():
    acct = make_account(100)
    acct.freeze_account()
    assert acct.is_active is False

# -------------------- unfreeze_account --------------------
def test_bankaccount_unfreeze():
    acct = make_account(100, freeze=True)
    acct.unfreeze_account()
    assert acct.is_active is True