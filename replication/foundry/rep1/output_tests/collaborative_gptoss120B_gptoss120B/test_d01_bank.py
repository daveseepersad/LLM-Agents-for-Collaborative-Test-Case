import pytest
from data.input_code.d01_bank import *

# ---------- __init__ ----------
@pytest.mark.parametrize(
    "initial_balance, expected",
    [
        (-10, ValueError),          # T1_INIT_NEG
        (0, {"balance": 0, "is_active": True}),  # T2_INIT_ZERO
    ],
)
def test_bankaccount_init(initial_balance, expected):
    if isinstance(expected, type) and issubclass(expected, Exception):
        with pytest.raises(expected):
            BankAccount(initial_balance)
    else:
        acct = BankAccount(initial_balance)
        assert acct.balance == expected["balance"]
        assert acct.is_active == expected["is_active"]

# ---------- deposit ----------
@pytest.mark.parametrize(
    "initial_balance, freeze, amount, expected",
    [
        (100, False, 50, 150),               # T3_DEPOSIT_OK
        (100, False, 0, ValueError),        # T4_DEPOSIT_BAD_AMOUNT
        (100, True, 10, ValueError),        # T5_DEPOSIT_FROZEN
    ],
)
def test_bankaccount_deposit(initial_balance, freeze, amount, expected):
    acct = BankAccount(initial_balance)
    if freeze:
        acct.freeze_account()
    if isinstance(expected, type) and issubclass(expected, Exception):
        with pytest.raises(expected):
            acct.deposit(amount)
    else:
        result = acct.deposit(amount)
        assert result == expected
        assert acct.balance == expected

# ---------- withdraw ----------
@pytest.mark.parametrize(
    "initial_balance, freeze, amount, expected",
    [
        (100, False, 40, 60),                # T6_WITHDRAW_OK
        (100, False, -5, ValueError),       # T7_WITHDRAW_BAD_AMOUNT
        (100, False, 150, ValueError),      # T8_WITHDRAW_INSUFFICIENT
        (100, True, 10, ValueError),        # T9_WITHDRAW_FROZEN
    ],
)
def test_bankaccount_withdraw(initial_balance, freeze, amount, expected):
    acct = BankAccount(initial_balance)
    if freeze:
        acct.freeze_account()
    if isinstance(expected, type) and issubclass(expected, Exception):
        with pytest.raises(expected):
            acct.withdraw(amount)
    else:
        result = acct.withdraw(amount)
        assert result == expected
        assert acct.balance == expected

# ---------- freeze / unfreeze ----------
def test_bankaccount_freeze_unfreeze():
    acct = BankAccount(100)          # T10_FREEZE_UNFREEZE
    acct.freeze_account()
    assert acct.is_active is False
    acct.unfreeze_account()
    assert acct.is_active is True