import pytest
from data.input_code.d01_bank import BankAccount


def test_init_negative_balance_raises():
    with pytest.raises(ValueError, match="Initial balance cannot be negative"):
        BankAccount(-5)


def test_init_none_raises_type_error():
    with pytest.raises(TypeError):
        BankAccount(None)


def test_zero_balance_flow():
    acc = BankAccount(0)
    assert acc.deposit(10) == 10
    assert acc.balance == 10
    assert acc.withdraw(3) == 7
    assert acc.balance == 7


def test_deposit_inactive_raises():
    acc = BankAccount(10)
    acc.freeze_account()
    with pytest.raises(ValueError, match="Account is frozen"):
        acc.deposit(5)


def test_deposit_non_positive_raises():
    acc = BankAccount(10)
    with pytest.raises(ValueError, match="Deposit amount must be positive"):
        acc.deposit(0)


def test_withdraw_positive_flow():
    acc = BankAccount(50)
    assert acc.withdraw(20) == 30
    assert acc.balance == 30


def test_withdraw_insufficient_funds():
    acc = BankAccount(5)
    with pytest.raises(ValueError, match="Insufficient funds"):
        acc.withdraw(6)


def test_withdraw_non_positive_raises():
    acc = BankAccount(10)
    with pytest.raises(ValueError, match="Withdrawal amount must be positive"):
        acc.withdraw(0)


def test_withdraw_inactive_raises():
    acc = BankAccount(10)
    acc.freeze_account()
    with pytest.raises(ValueError, match="Account is frozen"):
        acc.withdraw(5)


def test_freeze_and_unfreeze_functionality():
    acc = BankAccount(20)
    acc.freeze_account()
    assert acc.is_active is False
    acc.unfreeze_account()
    assert acc.is_active is True
    assert acc.deposit(5) == 25


def test_large_initial_balance_withdraw():
    balance = 2**60
    acc = BankAccount(balance)
    new_balance = acc.withdraw(1)
    assert new_balance == balance - 1
    assert acc.balance == balance - 1


def test_boundary_values_large_initial_balance_and_withdraw():
    # Use a very large initial balance to exercise large-number paths
    large_balance = (1 << 60) + 1
    acc = BankAccount(large_balance)
    assert acc.balance == large_balance
    assert acc.withdraw(1) == large_balance - 1
    assert acc.balance == large_balance - 1