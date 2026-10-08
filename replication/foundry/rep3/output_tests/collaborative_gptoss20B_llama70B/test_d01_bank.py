import pytest
from data.input_code.d01_bank import BankAccount

@pytest.mark.parametrize('initial_balance, expected', [
    (0, None),
])
def test_init_success(initial_balance, expected):
    account = BankAccount(initial_balance)
    assert account.balance == initial_balance

def test_init_error():
    with pytest.raises(ValueError):
        BankAccount(-1)

@pytest.mark.parametrize('initial_balance, amount, expected', [
    (100, 50, 150),
])
def test_deposit_success(initial_balance, amount, expected):
    account = BankAccount(initial_balance)
    assert account.deposit(amount) == expected

@pytest.mark.parametrize('amount, expected', [
    (-10, 'ValueError'),
    (0, 'ValueError'),
])
def test_deposit_error(amount, expected):
    account = BankAccount(100)
    if expected == 'ValueError':
        with pytest.raises(ValueError):
            account.deposit(amount)
    else:
        assert account.deposit(amount) == expected

@pytest.mark.parametrize('initial_balance, amount, expected', [
    (100, 40, 60),
])
def test_withdraw_success(initial_balance, amount, expected):
    account = BankAccount(initial_balance)
    assert account.withdraw(amount) == expected

@pytest.mark.parametrize('initial_balance, amount, expected', [
    (100, 0, 'ValueError'),
    (20, 30, 'ValueError'),
])
def test_withdraw_error(initial_balance, amount, expected):
    account = BankAccount(initial_balance)
    if expected == 'ValueError':
        with pytest.raises(ValueError):
            account.withdraw(amount)
    else:
        assert account.withdraw(amount) == expected

def test_freeze_account():
    account = BankAccount(100)
    account.freeze_account()
    assert not account.is_active

def test_unfreeze_account():
    account = BankAccount(100)
    account.freeze_account()
    account.unfreeze_account()
    assert account.is_active

@pytest.mark.parametrize('initial_balance, amount, expected', [
    (100, 50, 'ValueError'),
])
def test_deposit_on_frozen_account(initial_balance, amount, expected):
    account = BankAccount(initial_balance)
    account.freeze_account()
    if expected == 'ValueError':
        with pytest.raises(ValueError):
            account.deposit(amount)
    else:
        assert account.deposit(amount) == expected

@pytest.mark.parametrize('initial_balance, amount, expected', [
    (100, 10, 'ValueError'),
])
def test_withdraw_on_frozen_account(initial_balance, amount, expected):
    account = BankAccount(initial_balance)
    account.freeze_account()
    if expected == 'ValueError':
        with pytest.raises(ValueError):
            account.withdraw(amount)
    else:
        assert account.withdraw(amount) == expected