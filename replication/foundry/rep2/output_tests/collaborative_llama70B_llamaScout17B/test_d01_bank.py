import pytest
from data.input_code.d01_bank import *

@pytest.mark.parametrize('initial_balance, expected_exception', [
    (100, None),
    (-50, ValueError)
])
def test_bank_account_init(initial_balance, expected_exception):
    if expected_exception:
        with pytest.raises(expected_exception):
            BankAccount(initial_balance)
    else:
        account = BankAccount(initial_balance)
        assert account.balance == initial_balance

@pytest.mark.parametrize('initial_balance, amount, expected_balance, expected_exception, freeze_account', [
    (100, 50, 150, None, False),
    (100, 0, None, ValueError, False),
    (100, 50, None, ValueError, True)
])
def test_bank_account_deposit(initial_balance, amount, expected_balance, expected_exception, freeze_account):
    account = BankAccount(initial_balance)
    if freeze_account:
        account.freeze_account()
    if expected_exception:
        with pytest.raises(expected_exception):
            account.deposit(amount)
    else:
        assert account.deposit(amount) == expected_balance

@pytest.mark.parametrize('initial_balance, amount, expected_balance, expected_exception, freeze_account', [
    (100, 50, 50, None, False),
    (100, 0, None, ValueError, False),
    (100, 50, None, ValueError, True),
    (100, 200, None, ValueError, False)
])
def test_bank_account_withdraw(initial_balance, amount, expected_balance, expected_exception, freeze_account):
    account = BankAccount(initial_balance)
    if freeze_account:
        account.freeze_account()
    if expected_exception:
        with pytest.raises(expected_exception):
            account.withdraw(amount)
    else:
        assert account.withdraw(amount) == expected_balance

@pytest.mark.parametrize('initial_balance, freeze_account, expected_is_active', [
    (100, False, False),
    (100, True, False)
])
def test_bank_account_freeze(initial_balance, freeze_account, expected_is_active):
    account = BankAccount(initial_balance)
    if freeze_account:
        account.freeze_account()
    account.freeze_account()
    assert not account.is_active

@pytest.mark.parametrize('initial_balance, freeze_account, expected_is_active', [
    (100, True, True),
    (100, False, True)
])
def test_bank_account_unfreeze(initial_balance, freeze_account, expected_is_active):
    account = BankAccount(initial_balance)
    if freeze_account:
        account.freeze_account()
    account.unfreeze_account()
    assert account.is_active