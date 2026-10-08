import pytest
from data.input_code.d01_bank import *

@pytest.mark.parametrize('initial_balance', [-5])
def test_BA_T1_INIT_NEG(initial_balance):
    with pytest.raises(ValueError):
        BankAccount(initial_balance)

def test_BA_T2_INIT_HAPPY():
    ac = BankAccount(initial_balance=10)
    assert ac.balance == 10
    assert ac.is_active

def test_BA_T3_DEPOSIT_POS():
    ac = BankAccount()
    result = ac.deposit(5)
    assert result == 5
    assert ac.balance == 5

def test_BA_T4_DEPOSIT_ZERO():
    ac = BankAccount()
    with pytest.raises(ValueError):
        ac.deposit(0)

def test_BA_T5_WITHDRAW_ZERO():
    ac = BankAccount()
    with pytest.raises(ValueError):
        ac.withdraw(0)

def test_BA_T6_WITHDRAW_INSUFFICIENT():
    ac = BankAccount()
    with pytest.raises(ValueError):
        ac.withdraw(1)

def test_BA_T7_FREEZE_ACCOUNT():
    ac = BankAccount()
    ret = ac.freeze_account()
    assert ret is None
    assert ac.is_active is False

def test_BA_T8_UNFREEZE_ACCOUNT():
    ac = BankAccount()
    ac.freeze_account()
    ret = ac.unfreeze_account()
    assert ret is None
    assert ac.is_active is True

import pytest
from data.input_code.d01_bank import *

def test_BA_T9_INIT_ZERO():
    ac = BankAccount(initial_balance=0)
    assert ac.balance == 0
    assert ac.is_active

def test_BA_T10_DEPOSIT_NEG():
    ac = BankAccount(initial_balance=5)
    with pytest.raises(ValueError):
        ac.deposit(-2)

def test_BA_T11_WITHDRAW_NEG():
    ac = BankAccount(initial_balance=5)
    with pytest.raises(ValueError):
        ac.withdraw(-2)

import pytest
from data.input_code.d01_bank import *

def test_BA_T12_DEPOSIT_ON_FROZEN():
    ac = BankAccount(initial_balance=10)
    ac.freeze_account()
    with pytest.raises(ValueError):
        ac.deposit(5)

def test_BA_T13_WITHDRAW_ON_FROZEN():
    ac = BankAccount(initial_balance=10)
    ac.freeze_account()
    with pytest.raises(ValueError):
        ac.withdraw(5)

def test_BA_T14_WITHDRAW_EQUAL_BALANCE():
    ac = BankAccount(initial_balance=5)
    result = ac.withdraw(5)
    assert result == 0
    assert ac.balance == 0