import pytest
from data.input_code.d01_bank import *

@pytest.mark.parametrize('initial_balance, expected_balance, expected_active', [
    (0, 0, True),
])
def test_T1_INIT_DEFAULT(initial_balance, expected_balance, expected_active):
    acc = BankAccount(initial_balance=initial_balance)
    assert acc.balance == expected_balance
    assert acc.is_active == expected_active

@pytest.mark.parametrize('initial_balance', [-10])
def test_T2_INIT_NEGATIVE(initial_balance):
    with pytest.raises(ValueError):
        BankAccount(initial_balance=initial_balance)

@pytest.mark.parametrize('initial_balance, amount, expected', [
    (50, 25, 75),
])
def test_T3_DEPOSIT_SUCCESS(initial_balance, amount, expected):
    acc = BankAccount(initial_balance=initial_balance)
    result = acc.deposit(amount)
    assert result == expected

@pytest.mark.parametrize('initial_balance, amount', [
    (30, 0),
])
def test_T4_DEPOSIT_ZERO(initial_balance, amount):
    acc = BankAccount(initial_balance=initial_balance)
    with pytest.raises(ValueError):
        acc.deposit(amount)

@pytest.mark.parametrize('initial_balance, amount, freeze_before', [
    (20, 10, True),
])
def test_T5_DEPOSIT_FROZEN(initial_balance, amount, freeze_before):
    acc = BankAccount(initial_balance=initial_balance)
    if freeze_before:
        acc.freeze_account()
    with pytest.raises(ValueError):
        acc.deposit(amount)

@pytest.mark.parametrize('initial_balance, amount, expected', [
    (100, 40, 60),
])
def test_T6_WITHDRAW_SUCCESS(initial_balance, amount, expected):
    acc = BankAccount(initial_balance=initial_balance)
    result = acc.withdraw(amount)
    assert result == expected

@pytest.mark.parametrize('initial_balance, amount', [
    (50, 0),
])
def test_T7_WITHDRAW_ZERO(initial_balance, amount):
    acc = BankAccount(initial_balance=initial_balance)
    with pytest.raises(ValueError):
        acc.withdraw(amount)

@pytest.mark.parametrize('initial_balance, amount', [
    (30, 50),
])
def test_T8_WITHDRAW_INSUFFICIENT(initial_balance, amount):
    acc = BankAccount(initial_balance=initial_balance)
    with pytest.raises(ValueError):
        acc.withdraw(amount)

@pytest.mark.parametrize('initial_balance, amount, freeze_before', [
    (70, 20, True),
])
def test_T9_WITHDRAW_FROZEN(initial_balance, amount, freeze_before):
    acc = BankAccount(initial_balance=initial_balance)
    if freeze_before:
        acc.freeze_account()
    with pytest.raises(ValueError):
        acc.withdraw(amount)

def test_T10_FREEZE_ACCOUNT():
    acc = BankAccount(initial_balance=10)
    acc.freeze_account()
    assert acc.is_active is False

def test_T11_UNFREEZE_ACCOUNT():
    acc = BankAccount(initial_balance=10)
    acc.freeze_account()
    acc.unfreeze_account()
    assert acc.is_active is True