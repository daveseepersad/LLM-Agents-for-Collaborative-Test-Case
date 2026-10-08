import pytest
from data.input_code.d01_bank import *

@pytest.mark.parametrize('initial_balance, should_raise', [
    (100, None),
    (-50, ValueError)
])
def test_T1_T2_init(initial_balance, should_raise):
    if should_raise:
        with pytest.raises(should_raise):
            BankAccount(initial_balance)
    else:
        acct = BankAccount(initial_balance)
        assert acct.balance == initial_balance
        assert acct.is_active is True

def test_T3_ok_deposit():
    acct = BankAccount(100)
    result = acct.deposit(50)
    assert result == 150
    assert acct.balance == 150

def test_T4_err_deposit_zero():
    acct = BankAccount(100)
    with pytest.raises(ValueError):
        acct.deposit(0)

def test_T5_err_deposit_negative():
    acct = BankAccount(100)
    with pytest.raises(ValueError):
        acct.deposit(-20)

def test_T6_err_deposit_frozen():
    acct = BankAccount(100)
    acct.freeze_account()
    with pytest.raises(ValueError):
        acct.deposit(50)

def test_T7_ok_withdraw():
    acct = BankAccount(100)
    result = acct.withdraw(20)
    assert result == 80
    assert acct.balance == 80

def test_T8_err_withdraw_zero():
    acct = BankAccount(100)
    with pytest.raises(ValueError):
        acct.withdraw(0)

def test_T9_err_withdraw_negative():
    acct = BankAccount(100)
    with pytest.raises(ValueError):
        acct.withdraw(-30)

def test_T10_err_withdraw_insufficient():
    acct = BankAccount(100)
    with pytest.raises(ValueError):
        acct.withdraw(150)

def test_T11_err_withdraw_frozen():
    acct = BankAccount(100)
    acct.freeze_account()
    with pytest.raises(ValueError):
        acct.withdraw(20)

def test_T12_ok_freeze():
    acct = BankAccount(100)
    acct.freeze_account()
    assert acct.is_active is False

def test_T13_ok_unfreeze():
    acct = BankAccount(100)
    acct.freeze_account()
    acct.unfreeze_account()
    assert acct.is_active is True