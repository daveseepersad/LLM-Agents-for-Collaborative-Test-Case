import pytest
from data.input_code.d01_bank import *

@pytest.mark.parametrize('initial_balance, expected_balance, expected_active', [
    (100, 100, True),
    (0, 0, True),
])
def test_init_success(initial_balance, expected_balance, expected_active):
    acc = BankAccount(initial_balance)
    assert acc.balance == expected_balance
    assert acc.is_active == expected_active

def test_init_negative():
    with pytest.raises(ValueError):
        BankAccount(-10)

@pytest.mark.parametrize('initial_balance, amount, freeze_before, expected', [
    (50, 25, False, 75),
    (30, 0, False, "ValueError"),
    (40, 10, True, "ValueError"),
])
def test_deposit(initial_balance, amount, freeze_before, expected):
    acc = BankAccount(initial_balance)
    if freeze_before:
        acc.freeze_account()
    if isinstance(expected, str) and expected == "ValueError":
        with pytest.raises(ValueError):
            acc.deposit(amount)
    else:
        assert acc.deposit(amount) == expected

@pytest.mark.parametrize('initial_balance, amount, freeze_before, expected', [
    (100, 40, False, 60),
    (60, 60, False, 0),
    (50, 0, False, "ValueError"),
    (30, 50, False, "ValueError"),
    (70, 10, True, "ValueError"),
])
def test_withdraw(initial_balance, amount, freeze_before, expected):
    acc = BankAccount(initial_balance)
    if freeze_before:
        acc.freeze_account()
    if isinstance(expected, str) and expected == "ValueError":
        with pytest.raises(ValueError):
            acc.withdraw(amount)
    else:
        assert acc.withdraw(amount) == expected

def test_freeze_account():
    acc = BankAccount(20)
    acc.freeze_account()
    assert acc.is_active is False

def test_unfreeze_account():
    acc = BankAccount(20)
    acc.freeze_account()
    acc.unfreeze_account()
    assert acc.is_active is True