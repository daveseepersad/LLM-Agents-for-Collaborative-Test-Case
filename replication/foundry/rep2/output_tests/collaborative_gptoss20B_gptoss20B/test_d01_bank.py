import pytest
from data.input_code.d01_bank import *

# T1_INIT_ZERO
def test_init_zero_balance():
    acct = BankAccount(0)
    assert acct.balance == 0
    assert acct.is_active is True

# T2_INIT_NEG
def test_init_negative_raises():
    with pytest.raises(ValueError):
        BankAccount(-5)

# T3_INIT_NONE
def test_init_none_raises():
    with pytest.raises(TypeError):
        BankAccount(None)

# T4_DEPOSIT_OK
def test_deposit_ok():
    acct = BankAccount()
    result = acct.deposit(50)
    assert result == 50
    assert acct.balance == 50

# T5_DEPOSIT_NON_POS
def test_deposit_non_positive():
    acct = BankAccount()
    with pytest.raises(ValueError):
        acct.deposit(0)

# T6_WITHDRAW_INSUFFICIENT
def test_withdraw_insufficient():
    acct = BankAccount()
    with pytest.raises(ValueError):
        acct.withdraw(1)

# T7_WITHDRAW_NON_POS
def test_withdraw_non_positive():
    acct = BankAccount()
    with pytest.raises(ValueError):
        acct.withdraw(0)

# T8_FREEZE_ACCOUNT
def test_freeze_account_returns_none_and_updates_state():
    acct = BankAccount()
    result = acct.freeze_account()
    assert result is None
    assert acct.is_active is False

# T9_UNFREEZE_ACCOUNT
def test_unfreeze_account_updates_state():
    acct = BankAccount()
    acct.freeze_account()
    result = acct.unfreeze_account()
    assert result is None
    assert acct.is_active is True

import pytest
from data.input_code.d01_bank import *

@pytest.mark.parametrize("target, initial_balance, amount, expected", [
    ("BankAccount.deposit", 0, 50, 50),
    ("BankAccount.deposit", 0, -10, "ValueError"),
    ("BankAccount.withdraw", 50, 50, 0),
    ("BankAccount.withdraw", 10, -5, "ValueError"),
])
def test_bank_operations(target, initial_balance, amount, expected):
    if target == "BankAccount.deposit":
        acct = BankAccount(initial_balance)
        if isinstance(expected, str) and expected == "ValueError":
            with pytest.raises(ValueError):
                acct.deposit(amount)
        else:
            result = acct.deposit(amount)
            assert result == expected
            assert acct.balance == expected
    elif target == "BankAccount.withdraw":
        acct = BankAccount(initial_balance)
        if isinstance(expected, str) and expected == "ValueError":
            with pytest.raises(ValueError):
                acct.withdraw(amount)
        else:
            result = acct.withdraw(amount)
            assert result == expected
            assert acct.balance == expected
    else:
        pytest.fail("Unknown target")

import pytest
from data.input_code.d01_bank import *

def test_init_positive_balance():
    acct = BankAccount(100)
    assert acct.balance == 100
    assert acct.is_active is True

def test_withdraw_over_balance():
    acct = BankAccount(50)
    with pytest.raises(ValueError):
        acct.withdraw(60)

import pytest
from data.input_code.d01_bank import *

@pytest.mark.parametrize("target, initial_balance, amount, freeze_before", [
    ("BankAccount.deposit", 0, 5, True),
    ("BankAccount.withdraw", 100, 5, True),
])
def test_operation_when_frozen(target, initial_balance, amount, freeze_before):
    acct = BankAccount(initial_balance)
    if freeze_before:
        acct.freeze_account()
    if target == "BankAccount.deposit":
        with pytest.raises(ValueError):
            acct.deposit(amount)
    elif target == "BankAccount.withdraw":
        with pytest.raises(ValueError):
            acct.withdraw(amount)
    else:
        pytest.fail("Unknown target")