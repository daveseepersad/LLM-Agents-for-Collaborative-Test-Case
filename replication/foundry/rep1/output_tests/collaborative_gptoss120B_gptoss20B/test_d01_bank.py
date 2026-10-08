import pytest
from data.input_code.d01_bank import *

@pytest.mark.parametrize(
    "initial_balance, expect_exception",
    [
        (-5, True),   # Negative balance should raise
        (0, False),   # Zero balance OK
        (100, False), # Positive balance OK
    ],
)
def test_bankaccount_init(initial_balance, expect_exception):
    if expect_exception:
        with pytest.raises(ValueError):
            BankAccount(initial_balance)
    else:
        acct = BankAccount(initial_balance)
        assert acct.balance == initial_balance
        assert acct.is_active is True


@pytest.mark.parametrize(
    "initial_balance, amount, expected",
    [
        (50, 0, ValueError),      # Non‑positive deposit raises
        (50, 25, 75.0),            # Valid deposit updates balance
    ],
)
def test_bankaccount_deposit(initial_balance, amount, expected):
    acct = BankAccount(initial_balance)
    if isinstance(expected, type) and issubclass(expected, Exception):
        with pytest.raises(expected):
            acct.deposit(amount)
    else:
        result = acct.deposit(amount)
        assert result == expected
        assert acct.balance == expected


@pytest.mark.parametrize(
    "initial_balance, amount, expected",
    [
        (10, 5, 5.0),               # Valid withdrawal
        (10, 20, ValueError),      # Overdraw raises
        (10, -5, ValueError),      # Non‑positive withdrawal raises
    ],
)
def test_bankaccount_withdraw(initial_balance, amount, expected):
    acct = BankAccount(initial_balance)
    if isinstance(expected, type) and issubclass(expected, Exception):
        with pytest.raises(expected):
            acct.withdraw(amount)
    else:
        result = acct.withdraw(amount)
        assert result == expected
        assert acct.balance == expected


def test_bankaccount_freeze():
    acct = BankAccount(10)
    acct.freeze_account()
    assert acct.is_active is False


def test_bankaccount_unfreeze():
    acct = BankAccount(10)
    acct.unfreeze_account()
    assert acct.is_active is True

import pytest
from data.input_code.d01_bank import *

@pytest.mark.parametrize(
    "initial_balance, amount, freeze, expected",
    [
        (50, 10, True, ValueError),   # Deposit when account is frozen
        (50, -5, False, ValueError),  # Deposit with negative amount
    ],
)
def test_bankaccount_deposit_edge_cases(initial_balance, amount, freeze, expected):
    acct = BankAccount(initial_balance)
    if freeze:
        acct.freeze_account()
    with pytest.raises(expected):
        acct.deposit(amount)


@pytest.mark.parametrize(
    "initial_balance, amount, freeze, expected",
    [
        (50, 10, True, ValueError),   # Withdraw when account is frozen
        (10, 10, False, 0),           # Withdraw full balance
    ],
)
def test_bankaccount_withdraw_edge_cases(initial_balance, amount, freeze, expected):
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