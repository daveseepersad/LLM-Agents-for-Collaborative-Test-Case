import pytest
from data.input_code.d01_bank import *

def test_init_negative_raises_ValueError():
    with pytest.raises(ValueError):
        BankAccount(-1)

@pytest.mark.parametrize('initial_balance, deposit_amount, expected', [
    (0, 50, 50.0),                   # T2
    (0, 0, 'ValueError'),            # T3
    (0, None, 'TypeError'),          # T9
    (0, 9223372036854775807, 9223372036854775807),  # T10
    (0, 9223372036854775808, 9223372036854775808),  # T11
    (0, -1, 'ValueError'),           # T12
])
def test_bankaccount_deposit_variants(initial_balance, deposit_amount, expected):
    acc = BankAccount(initial_balance)
    if isinstance(expected, str):
        exc_map = {'ValueError': ValueError, 'TypeError': TypeError}
        with pytest.raises(exc_map[expected]):
            acc.deposit(deposit_amount)
    else:
        assert acc.deposit(deposit_amount) == expected

@pytest.mark.parametrize('initial_balance, withdraw_amount, expected', [
    (10, 5, 5.0),       # T4
    (10, 0, 'ValueError'),  # T5
    (5, 10, 'ValueError'),  # T6
])
def test_bankaccount_withdraw_variants(initial_balance, withdraw_amount, expected):
    acc = BankAccount(initial_balance)
    if isinstance(expected, str):
        exc_map = {'ValueError': ValueError}
        with pytest.raises(exc_map[expected]):
            acc.withdraw(withdraw_amount)
    else:
        assert acc.withdraw(withdraw_amount) == expected

def test_freeze_account_sets_inactive_and_returns_none():
    acc = BankAccount(0)
    result = acc.freeze_account()
    assert result is None
    assert acc.is_active is False

def test_unfreeze_account_sets_active_and_returns_none():
    acc = BankAccount(0)
    acc.freeze_account()
    result = acc.unfreeze_account()
    assert result is None
    assert acc.is_active is True

import pytest
from data.input_code.d01_bank import *

def test_withdraw_exact_balance_results_in_zero():
    acc = BankAccount(5)
    result = acc.withdraw(5)
    assert result == 0

@pytest.mark.parametrize('initial_balance, withdraw_amount, expected', [
    (20, -3, 'ValueError')
])
def test_withdraw_negative_amount_raises(initial_balance, withdraw_amount, expected):
    acc = BankAccount(initial_balance)
    if isinstance(expected, str):
        exc_map = {'ValueError': ValueError}
        with pytest.raises(exc_map[expected]):
            acc.withdraw(withdraw_amount)
    else:
        assert acc.withdraw(withdraw_amount) == expected

import pytest
from data.input_code.d01_bank import *

@pytest.mark.parametrize('initial_balance, amount', [
    (10, 5),
])
def test_bankaccount_deposit_raises_when_frozen(initial_balance, amount):
    acc = BankAccount(initial_balance)
    acc.freeze_account()
    with pytest.raises(ValueError):
        acc.deposit(amount)

@pytest.mark.parametrize('initial_balance, amount', [
    (10, 5),
])
def test_bankaccount_withdraw_raises_when_frozen(initial_balance, amount):
    acc = BankAccount(initial_balance)
    acc.freeze_account()
    with pytest.raises(ValueError):
        acc.withdraw(amount)