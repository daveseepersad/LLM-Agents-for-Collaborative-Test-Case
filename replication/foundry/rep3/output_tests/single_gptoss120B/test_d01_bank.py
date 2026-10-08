import pytest
from data.input_code.d01_bank import BankAccount

def test_init_negative_raises():
    with pytest.raises(ValueError, match="Initial balance cannot be negative"):
        BankAccount(initial_balance=-1)

@pytest.mark.parametrize("initial_balance", [0, 150])
def test_init_valid_balances(initial_balance):
    account = BankAccount(initial_balance=initial_balance)
    assert account.balance == initial_balance
    assert account.is_active is True

@pytest.mark.parametrize("deposit_amount,expected_balance", [
    (50, 150),
    (1, 101),
])
def test_deposit_success(deposit_amount, expected_balance):
    account = BankAccount(initial_balance=100)
    new_balance = account.deposit(deposit_amount)
    assert new_balance == expected_balance
    assert account.balance == expected_balance

@pytest.mark.parametrize("invalid_amount", [0, -10])
def test_deposit_invalid_amount_raises(invalid_amount):
    account = BankAccount(initial_balance=100)
    with pytest.raises(ValueError, match="Deposit amount must be positive"):
        account.deposit(invalid_amount)

def test_deposit_frozen_account_raises():
    account = BankAccount(initial_balance=100)
    account.freeze_account()
    with pytest.raises(ValueError, match="Account is frozen"):
        account.deposit(10)

@pytest.mark.parametrize("withdraw_amount,expected_balance", [
    (30, 70),
    (100, 0),
])
def test_withdraw_success(withdraw_amount, expected_balance):
    account = BankAccount(initial_balance=100)
    new_balance = account.withdraw(withdraw_amount)
    assert new_balance == expected_balance
    assert account.balance == expected_balance

@pytest.mark.parametrize("invalid_amount", [0, -5])
def test_withdraw_invalid_amount_raises(invalid_amount):
    account = BankAccount(initial_balance=100)
    with pytest.raises(ValueError, match="Withdrawal amount must be positive"):
        account.withdraw(invalid_amount)

def test_withdraw_insufficient_funds_raises():
    account = BankAccount(initial_balance=50)
    with pytest.raises(ValueError, match="Insufficient funds"):
        account.withdraw(60)

def test_withdraw_frozen_account_raises():
    account = BankAccount(initial_balance=100)
    account.freeze_account()
    with pytest.raises(ValueError, match="Account is frozen"):
        account.withdraw(10)

def test_freeze_and_unfreeze_account():
    account = BankAccount(initial_balance=100)
    account.freeze_account()
    assert account.is_active is False
    account.unfreeze_account()
    assert account.is_active is True
    # after unfreeze, operations should work again
    account.deposit(10)
    assert account.balance == 110
    account.withdraw(20)
    assert account.balance == 90