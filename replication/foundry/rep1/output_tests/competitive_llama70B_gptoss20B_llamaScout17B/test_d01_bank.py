import pytest
from data.input_code.d01_bank import *

def test_T1_OK_INIT():
    acct = BankAccount(initial_balance=100)
    assert acct.balance == 100
    assert acct.is_active is True

def test_T2_ERR_INIT_NEG():
    with pytest.raises(ValueError):
        BankAccount(initial_balance=-50)

def test_T3_OK_DEPOSIT():
    acct = BankAccount(initial_balance=100)
    result = acct.deposit(50)
    assert result == 150
    assert acct.balance == 150

def test_T4_ERR_DEPOSIT_NONPOS():
    acct = BankAccount(initial_balance=100)
    with pytest.raises(ValueError):
        acct.deposit(0)

def test_T5_ERR_DEPOSIT_FROZEN():
    acct = BankAccount(initial_balance=100)
    acct.freeze_account()
    with pytest.raises(ValueError):
        acct.deposit(50)

def test_T6_OK_WITHDRAW():
    acct = BankAccount(initial_balance=100)
    result = acct.withdraw(50)
    assert result == 50
    assert acct.balance == 50

def test_T7_ERR_WITHDRAW_NONPOS():
    acct = BankAccount(initial_balance=100)
    with pytest.raises(ValueError):
        acct.withdraw(0)

def test_T8_ERR_WITHDRAW_INSUFF():
    acct = BankAccount(initial_balance=100)
    with pytest.raises(ValueError):
        acct.withdraw(150)

def test_T9_ERR_WITHDRAW_FROZEN():
    acct = BankAccount(initial_balance=100)
    acct.freeze_account()
    with pytest.raises(ValueError):
        acct.withdraw(50)

def test_T10_OK_FREEZE():
    acct = BankAccount(initial_balance=100)
    acct.freeze_account()
    assert acct.is_active is False

def test_T11_OK_UNFREEZE():
    acct = BankAccount(initial_balance=100)
    acct.freeze_account()
    acct.unfreeze_account()
    assert acct.is_active is True