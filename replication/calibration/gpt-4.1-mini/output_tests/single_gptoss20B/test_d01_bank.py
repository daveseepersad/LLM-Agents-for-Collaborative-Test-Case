import pytest
from data.input_code.d01_bank import BankAccount

def test_init_positive_and_zero_balance():
    acc = BankAccount(0)
    assert acc.balance == 0
    assert acc.is_active is True
    acc2 = BankAccount(100)
    assert acc2.balance == 100
    assert acc2.is_active is True

def test_init_negative_balance_raises():
    with pytest.raises(ValueError, match="Initial balance cannot be negative"):
        BankAccount(-1)

def test_deposit_success():
    acc = BankAccount(10)
    new_balance = acc.deposit(5)
    assert new_balance == 15
    assert acc.balance == 15

def test_deposit_zero_or_negative_raises():
    acc = BankAccount(10)
    with pytest.raises(ValueError, match="Deposit amount must be positive"):
        acc.deposit(0)
    with pytest.raises(ValueError, match="Deposit amount must be positive"):
        acc.deposit(-10)

def test_deposit_frozen_account_raises():
    acc = BankAccount(10)
    acc.freeze_account()
    with pytest.raises(ValueError, match="Account is frozen"):
        acc.deposit(10)

def test_withdraw_success():
    acc = BankAccount(20)
    new_balance = acc.withdraw(10)
    assert new_balance == 10
    assert acc.balance == 10

def test_withdraw_zero_or_negative_raises():
    acc = BankAccount(20)
    with pytest.raises(ValueError, match="Withdrawal amount must be positive"):
        acc.withdraw(0)
    with pytest.raises(ValueError, match="Withdrawal amount must be positive"):
        acc.withdraw(-5)

def test_withdraw_insufficient_funds_raises():
    acc = BankAccount(10)
    with pytest.raises(ValueError, match="Insufficient funds"):
        acc.withdraw(11)

def test_withdraw_frozen_account_raises():
    acc = BankAccount(10)
    acc.freeze_account()
    with pytest.raises(ValueError, match="Account is frozen"):
        acc.withdraw(5)

def test_freeze_and_unfreeze_account():
    acc = BankAccount(10)
    acc.freeze_account()
    assert acc.is_active is False
    acc.unfreeze_account()
    assert acc.is_active is True