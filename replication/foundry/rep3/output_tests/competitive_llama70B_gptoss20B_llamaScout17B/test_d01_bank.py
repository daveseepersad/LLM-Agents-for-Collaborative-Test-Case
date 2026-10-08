import pytest
from data.input_code.d01_bank import *

# Tests for BankAccount.__init__
@pytest.mark.parametrize('initial, expected_exception, expected_balance', [
    (100, None, 100),
    (-50, ValueError, None),
])
def test_bankaccount_init(initial, expected_exception, expected_balance):
    if expected_exception is not None:
        with pytest.raises(expected_exception):
            BankAccount(initial)
    else:
        acct = BankAccount(initial)
        assert acct.balance == expected_balance
        assert acct.is_active is True

# Tests for BankAccount.deposit
@pytest.mark.parametrize('initial, amount, expected, freeze', [
    (100, 50, 150, False),  # T3_OK_DEPOSIT
    (100, 50, ValueError, True),  # T4_ERR_DEPOSIT_FROZEN
    (100, 0, ValueError, False),  # T5_ERR_DEPOSIT_NONPOS
    (100, -50, ValueError, False),  # T6_ERR_DEPOSIT_NEG
])
def test_bankaccount_deposit(initial, amount, expected, freeze):
    acct = BankAccount(initial)
    if freeze:
        acct.freeze_account()
    if isinstance(expected, type) and issubclass(expected, BaseException):
        with pytest.raises(expected):
            acct.deposit(amount)
    else:
        assert acct.deposit(amount) == expected

# Tests for BankAccount.withdraw
@pytest.mark.parametrize('initial, amount, expected, freeze', [
    (100, 50, 50, False),  # T7_OK_WITHDRAW
    (100, 50, ValueError, True),  # T8_ERR_WITHDRAW_FROZEN
    (100, 0, ValueError, False),  # T9_ERR_WITHDRAW_NONPOS
    (100, -50, ValueError, False),  # T10_ERR_WITHDRAW_NEG
    (100, 150, ValueError, False),  # T11_ERR_WITHDRAW_INSUFF
])
def test_bankaccount_withdraw(initial, amount, expected, freeze):
    acct = BankAccount(initial)
    if freeze:
        acct.freeze_account()
    if isinstance(expected, type) and issubclass(expected, BaseException):
        with pytest.raises(expected):
            acct.withdraw(amount)
    else:
        assert acct.withdraw(amount) == expected

# Tests for BankAccount.freeze_account
def test_bankaccount_freeze():
    acct = BankAccount(100)
    acct.freeze_account()
    assert acct.is_active is False

# Tests for BankAccount.unfreeze_account
def test_bankaccount_unfreeze():
    acct = BankAccount(100)
    acct.freeze_account()
    acct.unfreeze_account()
    assert acct.is_active is True