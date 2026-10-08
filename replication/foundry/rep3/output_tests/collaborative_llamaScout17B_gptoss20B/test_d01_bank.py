import pytest
from data.input_code.d01_bank import *


def test_T1_INIT_OK():
    BankAccount(100)


def test_T2_INIT_ERR():
    with pytest.raises(ValueError):
        BankAccount(-50)


def test_T3_DEPOSIT_OK():
    acct = BankAccount(100)
    assert acct.deposit(50) == 150


def test_T4_DEPOSIT_ERR_FROZEN():
    acct = BankAccount(100)
    acct.freeze_account()
    with pytest.raises(ValueError):
        acct.deposit(50)


def test_T5_DEPOSIT_ERR_NONPOSITIVE():
    acct = BankAccount(100)
    with pytest.raises(ValueError):
        acct.deposit(0)


def test_T6_WITHDRAW_OK():
    acct = BankAccount(100)
    assert acct.withdraw(50) == 50


def test_T7_WITHDRAW_ERR_FROZEN():
    acct = BankAccount(100)
    acct.freeze_account()
    with pytest.raises(ValueError):
        acct.withdraw(50)


def test_T8_WITHDRAW_ERR_NONPOSITIVE():
    acct = BankAccount(100)
    with pytest.raises(ValueError):
        acct.withdraw(0)


def test_T9_WITHDRAW_ERR_INSUFFICIENT():
    acct = BankAccount(100)
    with pytest.raises(ValueError):
        acct.withdraw(150)


def test_T10_FREEZE_OK():
    acct = BankAccount(100)
    acct.freeze_account()
    assert acct.is_active is False


def test_T11_UNFREEZE_OK():
    acct = BankAccount(100)
    acct.freeze_account()
    acct.unfreeze_account()
    assert acct.is_active is True