import pytest
from data.input_code.d01_bank import BankAccount

def test_negative_initial_balance_raises():
    with pytest.raises(ValueError) as excinfo:
        BankAccount(-5)
    assert "Initial balance" in str(excinfo.value)

def test_initial_zero_and_basic_operations_and_insufficient_funds():
    acc = BankAccount(0)
    assert acc.balance == 0
    assert acc.is_active is True

    # Deposit positive amount
    new_balance = acc.deposit(10)
    assert new_balance == 10
    assert acc.balance == 10

    # Withdraw within balance
    new_balance = acc.withdraw(4)
    assert new_balance == 6
    assert acc.balance == 6

    # Withdraw remaining funds to zero
    new_balance = acc.withdraw(6)
    assert new_balance == 0
    assert acc.balance == 0

    # Insufficient funds
    with pytest.raises(ValueError) as excinfo:
        acc.withdraw(1)
    assert "Insufficient funds" in str(excinfo.value)

def test_freeze_and_error_paths_and_unfreeze():
    acc = BankAccount(20)

    # Withdraw with invalid amount (negative/zero)
    with pytest.raises(ValueError) as excinfo:
        acc.withdraw(0)
    assert "Withdrawal amount must be positive" in str(excinfo.value)

    # Deposit with invalid amount (zero)
    with pytest.raises(ValueError) as excinfo:
        acc.deposit(0)
    assert "Deposit amount must be positive" in str(excinfo.value)

    # Freeze account and ensure operations are blocked
    acc.freeze_account()
    with pytest.raises(ValueError) as excinfo:
        acc.deposit(5)
    assert "Account is frozen" in str(excinfo.value)
    with pytest.raises(ValueError) as excinfo:
        acc.withdraw(5)
    assert "Account is frozen" in str(excinfo.value)

    # Unfreeze and perform valid operations
    acc.unfreeze_account()
    assert acc.is_active is True
    new_balance = acc.deposit(5)
    assert new_balance == 25
    new_balance = acc.withdraw(10)
    assert new_balance == 15