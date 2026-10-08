import pytest
from data.input_code.d01_bank import BankAccount


def test_init_negative_raises():
    with pytest.raises(ValueError, match="Initial balance cannot be negative"):
        BankAccount(-1)


def test_deposit_and_withdraw_success():
    acc = BankAccount(100)
    # deposit positive amount
    assert acc.deposit(50) == 150
    # withdraw less than balance
    assert acc.withdraw(30) == 120
    # withdraw exact remaining balance
    assert acc.withdraw(120) == 0
    # account remains active after operations
    assert acc.is_active is True


def test_deposit_invalid_amount():
    acc = BankAccount()
    for amt in (0, -10):
        with pytest.raises(ValueError, match="Deposit amount must be positive"):
            acc.deposit(amt)


def test_withdraw_invalid_amount_and_insufficient():
    acc = BankAccount(50)
    for amt in (0, -5):
        with pytest.raises(ValueError, match="Withdrawal amount must be positive"):
            acc.withdraw(amt)
    with pytest.raises(ValueError, match="Insufficient funds"):
        acc.withdraw(100)


def test_account_freeze_and_unfreeze_behavior():
    acc = BankAccount(10)
    acc.freeze_account()
    assert acc.is_active is False
    with pytest.raises(ValueError, match="Account is frozen"):
        acc.deposit(5)
    with pytest.raises(ValueError, match="Account is frozen"):
        acc.withdraw(5)
    acc.unfreeze_account()
    assert acc.is_active is True
    # operations succeed after unfreeze
    assert acc.deposit(5) == 15
    assert acc.withdraw(5) == 10