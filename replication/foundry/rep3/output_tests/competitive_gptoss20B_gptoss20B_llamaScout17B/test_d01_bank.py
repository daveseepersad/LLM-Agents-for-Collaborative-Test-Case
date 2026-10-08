import pytest
from data.input_code.d01_bank import *

@pytest.mark.parametrize('initial_balance, expected', [
    (0, 0),
    (1000000000000000000, 1000000000000000000)
])
def test_init_balance_sets_balance(initial_balance, expected):
    acc = BankAccount(initial_balance)
    assert acc.balance == expected

def test_init_negative_raises_value_error():
    with pytest.raises(ValueError):
        BankAccount(-1)

def test_init_none_raises_type_error():
    with pytest.raises(TypeError):
        BankAccount(None)

@pytest.mark.parametrize('amount, expected', [
    (50, 50),
    (-5, 'ValueError'),
    (0, 'ValueError')
])
def test_deposit(amount, expected):
    acc = BankAccount(0)
    if isinstance(expected, str):
        with pytest.raises(ValueError):
            acc.deposit(amount)
    else:
        assert acc.deposit(amount) == expected

@pytest.mark.parametrize('amount, expected', [
    (1, 'ValueError'),
    (-3, 'ValueError'),
    (0, 'ValueError')
])
def test_withdraw(amount, expected):
    acc = BankAccount(0)
    if isinstance(expected, str):
        with pytest.raises(ValueError):
            acc.withdraw(amount)
    else:
        assert acc.withdraw(amount) == expected

def test_freeze_account_no_error():
    acc = BankAccount(0)
    result = acc.freeze_account()
    assert result is None
    assert acc.is_active is False

def test_unfreeze_account_no_error():
    acc = BankAccount(0)
    acc.freeze_account()
    result = acc.unfreeze_account()
    assert result is None
    assert acc.is_active is True

import pytest

@pytest.mark.parametrize("method_name", ["deposit", "withdraw"])
def test_frozen_raises_for_operations(method_name):
    acc = BankAccount(100)
    acc.freeze_account()
    amount = 50
    with pytest.raises(ValueError):
        getattr(acc, method_name)(amount)

def test_withdraw_updates_balance():
    acc = BankAccount(100)
    result = acc.withdraw(30)
    assert result == 70
    assert acc.balance == 70