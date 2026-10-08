import pytest
from data.input_code.d01_bank import BankAccount

@pytest.mark.parametrize('initial_balance, expected', [
    (0, {'balance': 0, 'is_active': True}),
    (150, {'balance': 150, 'is_active': True})
])
def test_init_success(initial_balance, expected):
    account = BankAccount(initial_balance)
    assert account.balance == expected['balance']
    assert account.is_active == expected['is_active']

def test_init_error():
    with pytest.raises(ValueError):
        BankAccount(-10)

@pytest.mark.parametrize('amount, expected', [
    (25, 75)
])
def test_deposit_success(amount, expected):
    account = BankAccount(50)
    assert account.deposit(amount) == expected

@pytest.mark.parametrize('amount', [
    0
])
def test_deposit_zero(amount):
    account = BankAccount(30)
    with pytest.raises(ValueError):
        account.deposit(amount)

def test_deposit_frozen():
    account = BankAccount(20)
    account.freeze_account()
    with pytest.raises(ValueError):
        account.deposit(10)

@pytest.mark.parametrize('amount, expected', [
    (40, 60)
])
def test_withdraw_success(amount, expected):
    account = BankAccount(100)
    assert account.withdraw(amount) == expected

@pytest.mark.parametrize('amount', [
    0
])
def test_withdraw_zero(amount):
    account = BankAccount(80)
    with pytest.raises(ValueError):
        account.withdraw(amount)

def test_withdraw_insufficient():
    account = BankAccount(30)
    with pytest.raises(ValueError):
        account.withdraw(50)

def test_withdraw_frozen():
    account = BankAccount(70)
    account.freeze_account()
    with pytest.raises(ValueError):
        account.withdraw(20)

def test_freeze_unfreeze():
    account = BankAccount(0)
    account.freeze_account()
    assert account.is_active == False
    account.unfreeze_account()
    assert account.is_active == True