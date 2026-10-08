import pytest
from data.input_code.d01_bank import *

# ---------- __init__ ----------
@pytest.mark.parametrize(
    "initial_balance, expected_balance, expected_active",
    [
        (0, 0, True),
    ],
)
def test_bankaccount_init_success(initial_balance, expected_balance, expected_active):
    account = BankAccount(initial_balance)
    assert account.balance == expected_balance
    assert account.is_active is expected_active


def test_bankaccount_init_negative():
    with pytest.raises(ValueError):
        BankAccount(-10)


# ---------- deposit ----------
@pytest.mark.parametrize(
    "initial_balance, amount, expected_balance",
    [
        (100, 50, 150),
    ],
)
def test_deposit_success(initial_balance, amount, expected_balance):
    acc = BankAccount(initial_balance)
    result = acc.deposit(amount)
    assert result == expected_balance
    assert acc.balance == expected_balance


@pytest.mark.parametrize(
    "initial_balance, is_active, amount, exc",
    [
        (100, True, 0, ValueError),          # zero amount
        (100, False, 10, ValueError),        # frozen account
    ],
)
def test_deposit_errors(initial_balance, is_active, amount, exc):
    acc = BankAccount(initial_balance)
    if not is_active:
        acc.freeze_account()
    with pytest.raises(exc):
        acc.deposit(amount)


def test_deposit_unfreeze_then_success():
    acc = BankAccount(100)
    acc.freeze_account()
    # unfreeze before deposit
    acc.unfreeze_account()
    result = acc.deposit(20)
    assert result == 120
    assert acc.balance == 120
    assert acc.is_active is True


# ---------- withdraw ----------
@pytest.mark.parametrize(
    "initial_balance, amount, expected_balance",
    [
        (100, 30, 70),
    ],
)
def test_withdraw_success(initial_balance, amount, expected_balance):
    acc = BankAccount(initial_balance)
    result = acc.withdraw(amount)
    assert result == expected_balance
    assert acc.balance == expected_balance


@pytest.mark.parametrize(
    "initial_balance, is_active, amount, exc",
    [
        (100, True, 0, ValueError),          # zero amount
        (50, True, 60, ValueError),          # insufficient funds
        (100, False, 10, ValueError),        # frozen account
    ],
)
def test_withdraw_errors(initial_balance, is_active, amount, exc):
    acc = BankAccount(initial_balance)
    if not is_active:
        acc.freeze_account()
    with pytest.raises(exc):
        acc.withdraw(amount)