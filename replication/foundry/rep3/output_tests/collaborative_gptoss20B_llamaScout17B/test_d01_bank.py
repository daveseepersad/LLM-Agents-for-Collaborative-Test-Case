import pytest
from data.input_code.d01_bank import *

@pytest.mark.parametrize('initial_balance, expected_exception', [
    (-1, ValueError),
    (-9223372036854775808, ValueError),
    (None, TypeError),
])
def test_bank_account_init_error(initial_balance, expected_exception):
    with pytest.raises(expected_exception):
        BankAccount(initial_balance)

@pytest.mark.parametrize('initial_balance', [
    0,
    9223372036854775807,
])
def test_bank_account_init_success(initial_balance):
    account = BankAccount(initial_balance)
    assert account.balance == initial_balance

@pytest.mark.parametrize('initial_balance, amount, expected', [
    (100, 50, 150),
])
def test_bank_account_deposit_success(initial_balance, amount, expected):
    account = BankAccount(initial_balance)
    result = account.deposit(amount)
    assert result == expected

@pytest.mark.parametrize('initial_balance, amount, freeze_before, expected_exception', [
    (100, 0, False, ValueError),
    (100, 50, True, ValueError),
])
def test_bank_account_deposit_error(initial_balance, amount, freeze_before, expected_exception):
    account = BankAccount(initial_balance)
    if freeze_before:
        account.freeze_account()
    with pytest.raises(expected_exception):
        account.deposit(amount)

@pytest.mark.parametrize('initial_balance, amount, expected', [
    (100, 40, 60),
])
def test_bank_account_withdraw_success(initial_balance, amount, expected):
    account = BankAccount(initial_balance)
    result = account.withdraw(amount)
    assert result == expected

@pytest.mark.parametrize('initial_balance, amount, freeze_before, expected_exception', [
    (50, 60, False, ValueError),
    (100, 0, False, ValueError),
    (100, 10, True, ValueError),
])
def test_bank_account_withdraw_error(initial_balance, amount, freeze_before, expected_exception):
    account = BankAccount(initial_balance)
    if freeze_before:
        account.freeze_account()
    with pytest.raises(expected_exception):
        account.withdraw(amount)

def test_bank_account_freeze_unfreeze():
    account = BankAccount(100)
    account.freeze_account()
    assert not account.is_active
    account.unfreeze_account()
    assert account.is_active