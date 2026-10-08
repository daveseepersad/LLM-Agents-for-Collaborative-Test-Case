import pytest
from data.input_code.d01_bank import *

def test_T1_init_pos():
    acct = BankAccount(100)
    assert acct.balance == 100
    assert acct.is_active is True

def test_T2_init_neg():
    with pytest.raises(ValueError):
        BankAccount(-10)

def test_T3_deposit_ok():
    acct = BankAccount(0)
    new_balance = acct.deposit(50)
    assert new_balance == 50
    assert acct.balance == 50

def test_T4_deposit_bad_amount():
    acct = BankAccount(0)
    with pytest.raises(ValueError):
        acct.deposit(0)

def test_T5_freeze_account():
    acct = BankAccount(0)
    acct.freeze_account()
    assert acct.is_active is False

def test_T6_deposit_frozen():
    acct = BankAccount(0)
    acct.freeze_account()
    with pytest.raises(ValueError):
        acct.deposit(10)

def test_T7_withdraw_ok():
    acct = BankAccount(100)
    new_balance = acct.withdraw(40)
    assert new_balance == 60
    assert acct.balance == 60

def test_T8_withdraw_bad_amount():
    acct = BankAccount(100)
    with pytest.raises(ValueError):
        acct.withdraw(0)

def test_T9_withdraw_insufficient():
    acct = BankAccount(30)
    with pytest.raises(ValueError):
        acct.withdraw(50)

def test_T10_withdraw_frozen():
    acct = BankAccount(100)
    acct.freeze_account()
    with pytest.raises(ValueError):
        acct.withdraw(10)

def test_T11_unfreeze_account():
    acct = BankAccount(0)
    acct.freeze_account()
    acct.unfreeze_account()
    assert acct.is_active is True

def test_T12_deposit_after_unfreeze():
    acct = BankAccount(0)
    new_balance = acct.deposit(25)
    assert new_balance == 25
    assert acct.balance == 25