import pytest
from data.input_code.d01_bank import BankAccount

def test_init_negative_balance_raises():
    with pytest.raises(ValueError, match="Initial balance"):
        BankAccount(-5)

def test_init_zero_balance():
    acct = BankAccount(0)
    assert acct.balance == 0
    assert acct.is_active is True

def test_deposit_positive_updates_balance():
    acct = BankAccount(10)
    new = acct.deposit(5)
    assert new == 15
    assert acct.balance == 15

def test_deposit_zero_raises():
    acct = BankAccount(10)
    with pytest.raises(ValueError, match="Deposit amount must be positive"):
        acct.deposit(0)

def test_deposit_negative_raises():
    acct = BankAccount(10)
    with pytest.raises(ValueError, match="Deposit amount must be positive"):
        acct.deposit(-3)

def test_deposit_when_frozen_raises():
    acct = BankAccount(10)
    acct.freeze_account()
    with pytest.raises(ValueError, match="Account is frozen"):
        acct.deposit(5)

def test_withdraw_positive_updates_balance():
    acct = BankAccount(20)
    new = acct.withdraw(5)
    assert new == 15
    assert acct.balance == 15

def test_withdraw_zero_raises():
    acct = BankAccount(20)
    with pytest.raises(ValueError, match="Withdrawal amount must be positive"):
        acct.withdraw(0)

def test_withdraw_negative_raises():
    acct = BankAccount(20)
    with pytest.raises(ValueError, match="Withdrawal amount must be positive"):
        acct.withdraw(-2)

def test_withdraw_insufficient_funds_raises():
    acct = BankAccount(5)
    with pytest.raises(ValueError, match="Insufficient funds"):
        acct.withdraw(6)

def test_withdraw_when_frozen_raises():
    acct = BankAccount(10)
    acct.freeze_account()
    with pytest.raises(ValueError, match="Account is frozen"):
        acct.withdraw(5)

