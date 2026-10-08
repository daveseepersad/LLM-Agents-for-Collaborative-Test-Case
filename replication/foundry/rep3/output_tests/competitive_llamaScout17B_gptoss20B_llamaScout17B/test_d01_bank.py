import pytest
from data.input_code.d01_bank import *

def test_T1_INIT_OK():
    acc = BankAccount(100)
    assert acc.balance == 100
    assert acc.is_active is True

def test_T2_INIT_ERR():
    with pytest.raises(ValueError):
        BankAccount(-50)

def test_T3_DEPOSIT_OK():
    acc = BankAccount(100)
    result = acc.deposit(50)
    assert result == 150

def test_T4_DEPOSIT_ERR_FROZEN():
    acc = BankAccount(100)
    acc.freeze_account()
    with pytest.raises(ValueError):
        acc.deposit(50)

def test_T5_DEPOSIT_ERR_NONPOSITIVE():
    acc = BankAccount(100)
    with pytest.raises(ValueError):
        acc.deposit(0)

def test_T6_WITHDRAW_OK():
    acc = BankAccount(100)
    result = acc.withdraw(50)
    assert result == 50

def test_T7_WITHDRAW_ERR_FROZEN():
    acc = BankAccount(100)
    acc.freeze_account()
    with pytest.raises(ValueError):
        acc.withdraw(50)

def test_T8_WITHDRAW_ERR_NONPOSITIVE():
    acc = BankAccount(100)
    with pytest.raises(ValueError):
        acc.withdraw(0)

def test_T9_WITHDRAW_ERR_INSUFFICIENT():
    acc = BankAccount(100)
    with pytest.raises(ValueError):
        acc.withdraw(150)

def test_T10_FREEZE_OK():
    acc = BankAccount(100)
    acc.freeze_account()
    assert acc.is_active is False

def test_T11_UNFREEZE_OK():
    acc = BankAccount(100)
    acc.freeze_account()
    acc.unfreeze_account()
    assert acc.is_active is True