import pytest
from data.input_code.d01_bank import *

@pytest.mark.parametrize("initial_balance", [0, 100])
def test_init_default_and_positive(initial_balance):
    acct = BankAccount(initial_balance)
    assert acct.balance == initial_balance
    assert acct.is_active is True

def test_init_negative_raises():
    with pytest.raises(ValueError):
        BankAccount(-10)

def test_deposit_happy():
    acct = BankAccount(0)
    result = acct.deposit(50)
    assert result == 50
    assert acct.balance == 50

def test_deposit_zero_raises():
    acct = BankAccount(0)
    with pytest.raises(ValueError):
        acct.deposit(0)

def test_deposit_frozen_raises():
    acct = BankAccount(0)
    acct.freeze_account()
    with pytest.raises(ValueError):
        acct.deposit(10)

def test_unfreeze_deposit():
    acct = BankAccount(0)
    acct.freeze_account()
    acct.unfreeze_account()
    result = acct.deposit(10)
    assert result == 10
    assert acct.balance == 10

def test_withdraw_happy():
    acct = BankAccount(50)
    result = acct.withdraw(20)
    assert result == 30
    assert acct.balance == 30

def test_withdraw_zero_raises():
    acct = BankAccount(30)
    with pytest.raises(ValueError):
        acct.withdraw(0)

def test_withdraw_insufficient_raises():
    acct = BankAccount(30)
    with pytest.raises(ValueError):
        acct.withdraw(40)

def test_withdraw_frozen_raises():
    acct = BankAccount(30)
    acct.freeze_account()
    with pytest.raises(ValueError):
        acct.withdraw(10)