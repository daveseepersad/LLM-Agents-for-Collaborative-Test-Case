import pytest
from data.input_code.d01_bank import *

# -------------------- __init__ --------------------
@pytest.mark.parametrize(
    "initial_balance, expected_exception",
    [
        (100, None),          # valid positive balance
        (-10, ValueError),    # negative balance raises
    ],
)
def test_bankaccount_init(initial_balance, expected_exception):
    if expected_exception:
        with pytest.raises(expected_exception):
            BankAccount(initial_balance)
    else:
        acc = BankAccount(initial_balance)
        assert acc.balance == initial_balance
        assert acc.is_active is True

# -------------------- deposit --------------------
@pytest.mark.parametrize(
    "balance, is_active, amount, expected, expected_exception",
    [
        (100, True, 50, 150, None),               # normal deposit
        (100, False, 50, None, ValueError),       # frozen account
        (100, True, 0, None, ValueError),         # zero amount
        (100, True, -50, None, ValueError),       # negative amount
    ],
)
def test_bankaccount_deposit(balance, is_active, amount, expected, expected_exception):
    acc = BankAccount()
    acc.balance = balance
    acc.is_active = is_active

    if expected_exception:
        with pytest.raises(expected_exception):
            acc.deposit(amount)
    else:
        result = acc.deposit(amount)
        assert result == expected
        assert acc.balance == expected

# -------------------- withdraw --------------------
@pytest.mark.parametrize(
    "balance, is_active, amount, expected, expected_exception",
    [
        (100, True, 50, 50, None),                # normal withdrawal
        (100, False, 50, None, ValueError),       # frozen account
        (100, True, 0, None, ValueError),         # zero amount
        (100, True, -50, None, ValueError),       # negative amount
        (100, True, 150, None, ValueError),       # insufficient funds
    ],
)
def test_bankaccount_withdraw(balance, is_active, amount, expected, expected_exception):
    acc = BankAccount()
    acc.balance = balance
    acc.is_active = is_active

    if expected_exception:
        with pytest.raises(expected_exception):
            acc.withdraw(amount)
    else:
        result = acc.withdraw(amount)
        assert result == expected
        assert acc.balance == expected

# -------------------- freeze_account --------------------
def test_bankaccount_freeze_account():
    acc = BankAccount()
    acc.is_active = True
    acc.freeze_account()
    assert acc.is_active is False

# -------------------- unfreeze_account --------------------
def test_bankaccount_unfreeze_account():
    acc = BankAccount()
    acc.is_active = False
    acc.unfreeze_account()
    assert acc.is_active is True