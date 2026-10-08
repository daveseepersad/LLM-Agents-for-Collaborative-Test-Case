import pytest
from data.input_code.d01_bank import *

# -------------------- __init__ --------------------
@pytest.mark.parametrize(
    "initial_balance, expected_attrs, expected_exc",
    [
        (0, {"balance": 0, "is_active": True}, None),                     # default ok
        (100, {"balance": 100, "is_active": True}, None),                 # positive ok
        (-5, None, ValueError),                                           # negative raises
        (None, None, TypeError),                                          # None raises
    ],
)
def test_bankaccount_init(initial_balance, expected_attrs, expected_exc):
    if expected_exc:
        with pytest.raises(expected_exc):
            BankAccount(initial_balance)
    else:
        acc = BankAccount(initial_balance)
        assert acc.balance == expected_attrs["balance"]
        assert acc.is_active == expected_attrs["is_active"]


# -------------------- deposit --------------------
@pytest.mark.parametrize(
    "start_balance, is_active, amount, expected_balance, expected_exc",
    [
        (50, True, 25, 75, None),                # normal deposit
        (50, False, 10, None, ValueError),       # frozen account
        (50, True, 0, None, ValueError),         # non‑positive amount
        (50, True, -5, None, ValueError),        # negative amount
        (50, True, "", None, TypeError),         # invalid type
    ],
)
def test_bankaccount_deposit(start_balance, is_active, amount, expected_balance, expected_exc):
    acc = BankAccount(start_balance)
    acc.is_active = is_active
    if expected_exc:
        with pytest.raises(expected_exc):
            acc.deposit(amount)
    else:
        result = acc.deposit(amount)
        assert result == expected_balance
        assert acc.balance == expected_balance


# -------------------- withdraw --------------------
@pytest.mark.parametrize(
    "start_balance, is_active, amount, expected_balance, expected_exc",
    [
        (100, True, 40, 60, None),               # normal withdraw
        (100, False, 10, None, ValueError),      # frozen account
        (100, True, 0, None, ValueError),        # non‑positive amount
        (100, True, -5, None, ValueError),       # negative amount
        (20, True, 30, None, ValueError),        # insufficient funds
        (50, True, [], None, TypeError),         # invalid type
    ],
)
def test_bankaccount_withdraw(start_balance, is_active, amount, expected_balance, expected_exc):
    acc = BankAccount(start_balance)
    acc.is_active = is_active
    if expected_exc:
        with pytest.raises(expected_exc):
            acc.withdraw(amount)
    else:
        result = acc.withdraw(amount)
        assert result == expected_balance
        assert acc.balance == expected_balance


# -------------------- freeze_account --------------------
def test_freeze_account():
    acc = BankAccount(10)
    acc.freeze_account()
    assert acc.is_active is False
    assert acc.balance == 10


# -------------------- unfreeze_account --------------------
def test_unfreeze_account():
    acc = BankAccount(10)
    acc.is_active = False
    acc.unfreeze_account()
    assert acc.is_active is True
    assert acc.balance == 10