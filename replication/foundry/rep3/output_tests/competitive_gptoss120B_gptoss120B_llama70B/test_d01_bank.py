import pytest
from data.input_code.d01_bank import *

@pytest.mark.parametrize(
    "initial_balance, expected_exception",
    [
        (-10, ValueError),
        (0, None),
    ],
)
def test_bankaccount_init(initial_balance, expected_exception):
    if expected_exception:
        with pytest.raises(expected_exception):
            BankAccount(initial_balance)
    else:
        acct = BankAccount(initial_balance)
        assert acct.balance == 0
        assert acct.is_active is True


@pytest.mark.parametrize(
    "initial_balance, amount, freeze_before, expected, expect_exception",
    [
        (0, 100, False, 100, None),          # T3_DEPOSIT_OK
        (0, 0, False, None, ValueError),    # T4_DEPOSIT_ZERO
        (0, 50, True, None, ValueError),    # T5_DEPOSIT_FROZEN
    ],
)
def test_deposit(initial_balance, amount, freeze_before, expected, expect_exception):
    acct = BankAccount(initial_balance)
    if freeze_before:
        acct.freeze_account()
    if expect_exception:
        with pytest.raises(expect_exception):
            acct.deposit(amount)
    else:
        result = acct.deposit(amount)
        assert result == expected
        assert acct.balance == expected


@pytest.mark.parametrize(
    "initial_balance, amount, freeze_before, expected, expect_exception",
    [
        (100, 40, False, 60, None),          # T6_WITHDRAW_OK
        (100, 0, False, None, ValueError),  # T7_WITHDRAW_ZERO
        (100, 150, False, None, ValueError),# T8_WITHDRAW_INSUFFICIENT
        (100, 20, True, None, ValueError),  # T9_WITHDRAW_FROZEN
    ],
)
def test_withdraw(initial_balance, amount, freeze_before, expected, expect_exception):
    acct = BankAccount(initial_balance)
    if freeze_before:
        acct.freeze_account()
    if expect_exception:
        with pytest.raises(expect_exception):
            acct.withdraw(amount)
    else:
        result = acct.withdraw(amount)
        assert result == expected
        assert acct.balance == expected

import pytest

@pytest.mark.parametrize(
    "initial_balance, expected_balance, expected_active",
    [
        (50, 50, True),
    ],
)
def test_init_positive_balance(initial_balance, expected_balance, expected_active):
    acct = BankAccount(initial_balance)
    assert acct.balance == expected_balance
    assert acct.is_active is expected_active


@pytest.mark.parametrize(
    "initial_balance, amount, expected_exception",
    [
        (0, -10, ValueError),
    ],
)
def test_deposit_negative_amount(initial_balance, amount, expected_exception):
    acct = BankAccount(initial_balance)
    with pytest.raises(expected_exception):
        acct.deposit(amount)


@pytest.mark.parametrize(
    "initial_balance, amount, expected_exception",
    [
        (100, -5, ValueError),
    ],
)
def test_withdraw_negative_amount(initial_balance, amount, expected_exception):
    acct = BankAccount(initial_balance)
    with pytest.raises(expected_exception):
        acct.withdraw(amount)


@pytest.mark.parametrize(
    "initial_balance, amount, expected_balance",
    [
        (100, 100, 0),
    ],
)
def test_withdraw_exact_amount(initial_balance, amount, expected_balance):
    acct = BankAccount(initial_balance)
    result = acct.withdraw(amount)
    assert result == expected_balance
    assert acct.balance == expected_balance


def test_unfreeze_account_allows_deposit():
    acct = BankAccount(0)
    acct.freeze_account()
    acct.unfreeze_account()
    result = acct.deposit(25)
    assert result == 25
    assert acct.balance == 25