import pytest
from data.input_code.d01_bank import *

@pytest.mark.parametrize('initial_balance, expected_exception', [
    (-1, ValueError),
    (0, None),
    (100, None)
])
def test_bankaccount_init(initial_balance, expected_exception):
    if expected_exception:
        with pytest.raises(expected_exception):
            BankAccount(initial_balance)
    else:
        account = BankAccount(initial_balance)
        assert account.balance == initial_balance
        assert account.is_active is True

import pytest

@pytest.mark.parametrize(
    "initial_balance, amount, expected",
    [
        (100, 50, 150),          # valid deposit
        (50, 0, ValueError),     # non-positive deposit
    ],
)
def test_bankaccount_deposit(initial_balance, amount, expected):
    account = BankAccount(initial_balance)
    if isinstance(expected, type) and issubclass(expected, Exception):
        with pytest.raises(expected):
            account.deposit(amount)
    else:
        result = account.deposit(amount)
        assert result == expected
        assert account.balance == expected


@pytest.mark.parametrize(
    "initial_balance, amount, expected",
    [
        (100, 40, 60),               # valid withdraw
        (50, -5, ValueError),        # non-positive withdraw
        (20, 30, ValueError),        # insufficient funds
    ],
)
def test_bankaccount_withdraw(initial_balance, amount, expected):
    account = BankAccount(initial_balance)
    if isinstance(expected, type) and issubclass(expected, Exception):
        with pytest.raises(expected):
            account.withdraw(amount)
    else:
        result = account.withdraw(amount)
        assert result == expected
        assert account.balance == expected


def test_bankaccount_freeze_account():
    account = BankAccount(100)
    # Should not raise any exception
    account.freeze_account()
    assert account.is_active is False


def test_bankaccount_unfreeze_account():
    account = BankAccount(100)
    account.freeze_account()
    # Should reactivate the account without error
    account.unfreeze_account()
    assert account.is_active is True

import pytest

@pytest.mark.parametrize(
    "initial_balance, amount, freeze_before, expected",
    [
        (100, 10, True, ValueError),  # deposit should fail when account is frozen
    ],
)
def test_bankaccount_deposit_frozen(initial_balance, amount, freeze_before, expected):
    account = BankAccount(initial_balance)
    if freeze_before:
        account.freeze_account()
    with pytest.raises(expected):
        account.deposit(amount)


@pytest.mark.parametrize(
    "initial_balance, amount, freeze_before, expected",
    [
        (100, 10, True, ValueError),  # withdraw should fail when account is frozen
    ],
)
def test_bankaccount_withdraw_frozen(initial_balance, amount, freeze_before, expected):
    account = BankAccount(initial_balance)
    if freeze_before:
        account.freeze_account()
    with pytest.raises(expected):
        account.withdraw(amount)


@pytest.mark.parametrize(
    "initial_balance, amount, expected",
    [
        (100, 0, ValueError),  # withdrawal with zero amount should be rejected
    ],
)
def test_bankaccount_withdraw_zero_amount(initial_balance, amount, expected):
    account = BankAccount(initial_balance)
    with pytest.raises(expected):
        account.withdraw(amount)