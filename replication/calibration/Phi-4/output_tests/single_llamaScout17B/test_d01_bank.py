import pytest
from data.input_code.d01_bank import BankAccount

def test_initial_balance_positive():
    account = BankAccount(100)
    assert account.balance == 100
    assert account.is_active is True

def test_initial_balance_zero():
    account = BankAccount(0)
    assert account.balance == 0
    assert account.is_active is True

def test_initial_balance_negative():
    with pytest.raises(ValueError, match="Initial balance cannot be negative"):
        BankAccount(-10)

def test_deposit_positive_amount():
    account = BankAccount(100)
    new_balance = account.deposit(50)
    assert new_balance == 150

def test_deposit_zero_amount():
    account = BankAccount(100)
    with pytest.raises(ValueError, match="Deposit amount must be positive"):
        account.deposit(0)

def test_deposit_negative_amount():
    account = BankAccount(100)
    with pytest.raises(ValueError, match="Deposit amount must be positive"):
        account.deposit(-50)

def test_deposit_with_frozen_account():
    account = BankAccount(100)
    account.freeze_account()
    with pytest.raises(ValueError, match="Account is frozen"):
        account.deposit(50)

def test_withdraw_positive_amount():
    account = BankAccount(100)
    new_balance = account.withdraw(50)
    assert new_balance == 50

def test_withdraw_zero_amount():
    account = BankAccount(100)
    with pytest.raises(ValueError, match="Withdrawal amount must be positive"):
        account.withdraw(0)

def test_withdraw_negative_amount():
    account = BankAccount(100)
    with pytest.raises(ValueError, match="Withdrawal amount must be positive"):
        account.withdraw(-50)

def test_withdraw_insufficient_funds():
    account = BankAccount(50)
    with pytest.raises(ValueError, match="Insufficient funds"):
        account.withdraw(100)

def test_withdraw_with_frozen_account():
    account = BankAccount(100)
    account.freeze_account()
    with pytest.raises(ValueError, match="Account is frozen"):
        account.withdraw(50)

def test_freeze_account():
    account = BankAccount(100)
    account.freeze_account()
    assert account.is_active is False

def test_unfreeze_account():
    account = BankAccount(100)
    account.freeze_account()
    account.unfreeze_account()
    assert account.is_active is True