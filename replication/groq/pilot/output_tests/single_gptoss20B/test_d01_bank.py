import pytest
from data.input_code.d01_bank import BankAccount


def test_initial_balance_negative_raises():
    with pytest.raises(ValueError, match="Initial balance cannot be negative"):
        BankAccount(initial_balance=-10)


def test_default_initial_balance():
    account = BankAccount()
    assert account.balance == 0
    assert account.is_active is True


def test_deposit_success():
    account = BankAccount()
    new_balance = account.deposit(100)
    assert new_balance == 100
    assert account.balance == 100


def test_deposit_zero_raises():
    account = BankAccount()
    with pytest.raises(ValueError, match="Deposit amount must be positive"):
        account.deposit(0)


def test_deposit_negative_raises():
    account = BankAccount()
    with pytest.raises(ValueError, match="Deposit amount must be positive"):
        account.deposit(-50)


def test_deposit_when_frozen_raises():
    account = BankAccount()
    account.freeze_account()
    with pytest.raises(ValueError, match="Account is frozen"):
        account.deposit(10)


def test_withdraw_success():
    account = BankAccount(initial_balance=200)
    new_balance = account.withdraw(50)
    assert new_balance == 150
    assert account.balance == 150


def test_withdraw_zero_raises():
    account = BankAccount()
    with pytest.raises(ValueError, match="Withdrawal amount must be positive"):
        account.withdraw(0)


def test_withdraw_negative_raises():
    account = BankAccount()
    with pytest.raises(ValueError, match="Withdrawal amount must be positive"):
        account.withdraw(-30)


def test_withdraw_insufficient_funds_raises():
    account = BankAccount(initial_balance=30)
    with pytest.raises(ValueError, match="Insufficient funds"):
        account.withdraw(50)


def test_withdraw_when_frozen_raises():
    account = BankAccount(initial_balance=100)
    account.freeze_account()
    with pytest.raises(ValueError, match="Account is frozen"):
        account.withdraw(10)


def test_freeze_and_unfreeze():
    account = BankAccount(initial_balance=50)
    # Initially active
    assert account.is_active is True
    # Freeze the account
    account.freeze_account()
    assert account.is_active is False
    # Unfreeze the account
    account.unfreeze_account()
    assert account.is_active is True
    # Ensure balance remains unchanged
    assert account.balance == 50
    # After unfreezing, operations should succeed
    account.deposit(25)
    assert account.balance == 75
    account.withdraw(30)
    assert account.balance == 45
    # Freeze again and confirm operations fail
    account.freeze_account()
    with pytest.raises(ValueError, match="Account is frozen"):
        account.deposit(10)
    with pytest.raises(ValueError, match="Account is frozen"):
        account.withdraw(10)
    # Unfreeze and confirm operations succeed again
    account.unfreeze_account()
    account.deposit(5)
    assert account.balance == 50
    account.withdraw(5)
    assert account.balance == 45