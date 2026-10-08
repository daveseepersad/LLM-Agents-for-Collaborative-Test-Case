import pytest
from data.input_code.d01_bank import BankAccount

def test_init_negative():
    with pytest.raises(ValueError):
        BankAccount(-50)

def test_init_default():
    account = BankAccount()
    assert account.balance == 0
    assert account.is_active

@pytest.mark.parametrize('amount, expected', [
    (150, 150)
])
def test_deposit_ok(amount, expected):
    account = BankAccount(0)
    assert account.deposit(amount) == expected

def test_deposit_zero():
    account = BankAccount(0)
    with pytest.raises(ValueError):
        account.deposit(0)

def test_deposit_frozen():
    account = BankAccount(100)
    account.freeze_account()
    with pytest.raises(ValueError):
        account.deposit(50)

@pytest.mark.parametrize('amount, expected', [
    (80, 120)
])
def test_withdraw_ok(amount, expected):
    account = BankAccount(200)
    assert account.withdraw(amount) == expected

def test_withdraw_insufficient():
    account = BankAccount(30)
    with pytest.raises(ValueError):
        account.withdraw(100)

def test_withdraw_zero():
    account = BankAccount(50)
    with pytest.raises(ValueError):
        account.withdraw(0)

def test_withdraw_frozen():
    account = BankAccount(70)
    account.freeze_account()
    with pytest.raises(ValueError):
        account.withdraw(20)

def test_unfreeze_deposit():
    account = BankAccount(0)
    account.freeze_account()
    account.unfreeze_account()
    assert account.deposit(25) == 25