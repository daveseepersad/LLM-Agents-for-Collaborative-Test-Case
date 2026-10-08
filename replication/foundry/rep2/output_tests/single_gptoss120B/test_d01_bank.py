import pytest
from data.input_code.d01_bank import BankAccount

def test_init_negative_balance_raises():
    with pytest.raises(ValueError, match="Initial balance cannot be negative"):
        BankAccount(initial_balance=-1)

def test_init_default_and_positive_balance():
    acc_default = BankAccount()
    assert acc_default.balance == 0
    assert acc_default.is_active is True

    acc_positive = BankAccount(initial_balance=100)
    assert acc_positive.balance == 100
    assert acc_positive.is_active is True

@pytest.mark.parametrize("amount", [0, -10])
def test_deposit_non_positive_raises(amount):
    acc = BankAccount()
    with pytest.raises(ValueError, match="Deposit amount must be positive"):
        acc.deposit(amount)

def test_deposit_frozen_raises():
    acc = BankAccount()
    acc.freeze_account()
    with pytest.raises(ValueError, match="Account is frozen"):
        acc.deposit(50)

def test_deposit_success():
    acc = BankAccount(initial_balance=20)
    new_balance = acc.deposit(30)
    assert new_balance == 50
    assert acc.balance == 50

@pytest.mark.parametrize("amount", [0, -5])
def test_withdraw_non_positive_raises(amount):
    acc = BankAccount(initial_balance=100)
    with pytest.raises(ValueError, match="Withdrawal amount must be positive"):
        acc.withdraw(amount)

def test_withdraw_frozen_raises():
    acc = BankAccount(initial_balance=100)
    acc.freeze_account()
    with pytest.raises(ValueError, match="Account is frozen"):
        acc.withdraw(10)

def test_withdraw_insufficient_funds_raises():
    acc = BankAccount(initial_balance=50)
    with pytest.raises(ValueError, match="Insufficient funds"):
        acc.withdraw(60)

def test_withdraw_success():
    acc = BankAccount(initial_balance=80)
    new_balance = acc.withdraw(30)
    assert new_balance == 50
    assert acc.balance == 50

def test_freeze_and_unfreeze_behavior():
    acc = BankAccount(initial_balance=10)
    acc.freeze_account()
    assert acc.is_active is False
    with pytest.raises(ValueError):
        acc.deposit(5)
    with pytest.raises(ValueError):
        acc.withdraw(5)

    acc.unfreeze_account()
    assert acc.is_active is True
    # operations should now succeed
    assert acc.deposit(5) == 15
    assert acc.withdraw(5) == 10
    assert acc.balance == 10