import pytest
from data.input_code.d01_bank import *

# T1 & T2: __init__
@pytest.mark.parametrize("initial_balance, expected_exception", [
    (100, None),
    (-50, "ValueError"),
])
def test_bankaccount_init_case(initial_balance, expected_exception):
    if expected_exception:
        with pytest.raises(ValueError):
            BankAccount(initial_balance)
    else:
        acct = BankAccount(initial_balance)
        assert isinstance(acct, BankAccount)
        assert acct.balance == initial_balance
        assert acct.is_active is True

# T3, T4, T5: deposit
@pytest.mark.parametrize("initial_balance, amount, freeze_before, expected", [
    (100, 50, False, 150),          # T3
    (100, 0, False, "ValueError"),  # T4
    (100, 50, True, "ValueError"),  # T5
])
def test_bankaccount_deposit(initial_balance, amount, freeze_before, expected):
    acct = BankAccount(initial_balance)
    if freeze_before:
        acct.freeze_account()
    if isinstance(expected, str):
        with pytest.raises(ValueError):
            acct.deposit(amount)
    else:
        result = acct.deposit(amount)
        assert result == expected
        assert acct.balance == expected

# T6, T7, T8, T9: withdraw
@pytest.mark.parametrize("initial_balance, amount, freeze_before, expected", [
    (100, 50, False, 50),           # T6
    (100, 0, False, "ValueError"),  # T7
    (100, 50, True, "ValueError"),  # T8
    (100, 200, False, "ValueError"),# T9
])
def test_bankaccount_withdraw(initial_balance, amount, freeze_before, expected):
    acct = BankAccount(initial_balance)
    if freeze_before:
        acct.freeze_account()
    if isinstance(expected, str):
        with pytest.raises(ValueError):
            acct.withdraw(amount)
    else:
        result = acct.withdraw(amount)
        assert result == expected
        assert acct.balance == expected

# T10: freeze_account
def test_bankaccount_freeze():
    acct = BankAccount(100)
    acct.freeze_account()
    assert acct.is_active is False

# T11: unfreeze_account
def test_bankaccount_unfreeze():
    acct = BankAccount(100)
    acct.freeze_account()
    acct.unfreeze_account()
    assert acct.is_active is True