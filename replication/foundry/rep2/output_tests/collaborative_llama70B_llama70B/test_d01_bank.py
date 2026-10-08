import pytest
from data.input_code.d01_bank import BankAccount

@pytest.mark.parametrize('initial_balance, expected', [
    (100, None)
])
def test_init_success(initial_balance, expected):
    account = BankAccount(initial_balance)
    assert account.balance == initial_balance

def test_init_error():
    with pytest.raises(ValueError):
        BankAccount(-50)

@pytest.mark.parametrize('amount, initial_balance, expected', [
    (50, 100, 150)
])
def test_deposit_success(amount, initial_balance, expected):
    account = BankAccount(initial_balance)
    assert account.deposit(amount) == expected

@pytest.mark.parametrize('amount, initial_balance', [
    (0, 100)
])
def test_deposit_error_nonpos(amount, initial_balance):
    account = BankAccount(initial_balance)
    with pytest.raises(ValueError):
        account.deposit(amount)

def test_deposit_error_frozen():
    account = BankAccount(100)
    account.freeze_account()
    with pytest.raises(ValueError):
        account.deposit(50)

@pytest.mark.parametrize('amount, initial_balance, expected', [
    (50, 100, 50)
])
def test_withdraw_success(amount, initial_balance, expected):
    account = BankAccount(initial_balance)
    assert account.withdraw(amount) == expected

@pytest.mark.parametrize('amount, initial_balance', [
    (0, 100)
])
def test_withdraw_error_nonpos(amount, initial_balance):
    account = BankAccount(initial_balance)
    with pytest.raises(ValueError):
        account.withdraw(amount)

@pytest.mark.parametrize('amount, initial_balance', [
    (150, 100)
])
def test_withdraw_error_insuff(amount, initial_balance):
    account = BankAccount(initial_balance)
    with pytest.raises(ValueError):
        account.withdraw(amount)

def test_withdraw_error_frozen():
    account = BankAccount(100)
    account.freeze_account()
    with pytest.raises(ValueError):
        account.withdraw(50)

def test_freeze_account():
    account = BankAccount(100)
    account.freeze_account()
    assert not account.is_active

def test_unfreeze_account():
    account = BankAccount(100)
    account.freeze_account()
    account.unfreeze_account()
    assert account.is_active