import pytest
from data.input_code.d01_bank import *

# Helper to create account with optional frozen state
def make_account(initial_balance=0, freeze=False):
    acct = BankAccount(initial_balance)
    if freeze:
        acct.freeze_account()
    return acct

# ---------- __init__ ----------
@pytest.mark.parametrize(
    "initial_balance, expect_exception",
    [
        (100, None),          # T1_OK_INIT
        (-50, ValueError),    # T2_ERR_INIT_NEG
    ],
)
def test_bankaccount_init(initial_balance, expect_exception):
    if expect_exception:
        with pytest.raises(expect_exception):
            BankAccount(initial_balance)
    else:
        acct = BankAccount(initial_balance)
        assert acct.balance == initial_balance
        assert acct.is_active is True

# ---------- deposit ----------
@pytest.mark.parametrize(
    "setup, amount, expected, expect_exception",
    [
        ({"initial_balance": 100}, 50, 150, None),                     # T3_OK_DEPOSIT
        ({"initial_balance": 100, "freeze": True}, 50, None, ValueError),  # T4_ERR_DEPOSIT_FROZEN
        ({"initial_balance": 100}, 0, None, ValueError),              # T5_ERR_DEPOSIT_NONPOS
        ({"initial_balance": 100}, -50, None, ValueError),            # T6_ERR_DEPOSIT_NEG
    ],
)
def test_bankaccount_deposit(setup, amount, expected, expect_exception):
    acct = make_account(setup.get("initial_balance", 0), setup.get("freeze", False))
    if expect_exception:
        with pytest.raises(expect_exception):
            acct.deposit(amount)
    else:
        result = acct.deposit(amount)
        assert result == expected
        assert acct.balance == expected

# ---------- withdraw ----------
@pytest.mark.parametrize(
    "setup, amount, expected, expect_exception",
    [
        ({"initial_balance": 100}, 50, 50, None),                     # T7_OK_WITHDRAW
        ({"initial_balance": 100, "freeze": True}, 50, None, ValueError),  # T8_ERR_WITHDRAW_FROZEN
        ({"initial_balance": 100}, 0, None, ValueError),              # T9_ERR_WITHDRAW_NONPOS
        ({"initial_balance": 100}, -50, None, ValueError),            # T10_ERR_WITHDRAW_NEG
        ({"initial_balance": 100}, 150, None, ValueError),            # T11_ERR_WITHDRAW_INSUFF
    ],
)
def test_bankaccount_withdraw(setup, amount, expected, expect_exception):
    acct = make_account(setup.get("initial_balance", 0), setup.get("freeze", False))
    if expect_exception:
        with pytest.raises(expect_exception):
            acct.withdraw(amount)
    else:
        result = acct.withdraw(amount)
        assert result == expected
        assert acct.balance == expected

# ---------- freeze_account ----------
def test_bankaccount_freeze():
    acct = make_account(initial_balance=100)
    acct.freeze_account()
    assert acct.is_active is False

# ---------- unfreeze_account ----------
def test_bankaccount_unfreeze():
    acct = make_account(initial_balance=100, freeze=True)
    acct.unfreeze_account()
    assert acct.is_active is True