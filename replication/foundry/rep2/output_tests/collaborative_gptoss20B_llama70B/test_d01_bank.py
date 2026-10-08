import pytest
from data.input_code.d01_bank import BankAccount

@pytest.mark.parametrize('initial_balance, expected', [
    (0, 0),
])
def test_init_success(initial_balance, expected):
    account = BankAccount(initial_balance)
    assert account.balance == expected

def test_init_negative():
    with pytest.raises(ValueError):
        BankAccount(-5)

def test_init_none():
    with pytest.raises(TypeError):
        BankAccount(None)

@pytest.mark.parametrize('initial_balance, amount, expected', [
    (10, 5, 15),
])
def test_deposit_success(initial_balance, amount, expected):
    account = BankAccount(initial_balance)
    assert account.deposit(amount) == expected

@pytest.mark.parametrize('amount, expected_exception', [
    (0, ValueError),
    (-1, ValueError),
])
def test_deposit_error(amount, expected_exception):
    account = BankAccount(10)
    with pytest.raises(expected_exception):
        account.deposit(amount)

@pytest.mark.parametrize('initial_balance, amount, expected', [
    (20, 5, 15),
])
def test_withdraw_success(initial_balance, amount, expected):
    account = BankAccount(initial_balance)
    assert account.withdraw(amount) == expected

@pytest.mark.parametrize('initial_balance, amount, expected_exception', [
    (20, 0, ValueError),
    (20, -5, ValueError),
    (20, 25, ValueError),
])
def test_withdraw_error(initial_balance, amount, expected_exception):
    account = BankAccount(initial_balance)
    with pytest.raises(expected_exception):
        account.withdraw(amount)

@pytest.mark.parametrize('initial_balance, amount, expected', [
    (10, 10, 0),
])
def test_withdraw_exact_balance(initial_balance, amount, expected):
    account = BankAccount(initial_balance)
    assert account.withdraw(amount) == expected

@pytest.mark.parametrize('initial_balance, amount, freeze_before, expected_exception', [
    (50, 10, True, ValueError),
])
def test_freeze_deposit_error(initial_balance, amount, freeze_before, expected_exception):
    account = BankAccount(initial_balance)
    if freeze_before:
        account.freeze_account()
    with pytest.raises(expected_exception):
        account.deposit(amount)

@pytest.mark.parametrize('initial_balance, amount, freeze_before, expected_exception', [
    (50, 10, True, ValueError),
])
def test_freeze_withdraw_error(initial_balance, amount, freeze_before, expected_exception):
    account = BankAccount(initial_balance)
    if freeze_before:
        account.freeze_account()
    with pytest.raises(expected_exception):
        account.withdraw(amount)

@pytest.mark.parametrize('initial_balance, amount, unfreeze_before, expected', [
    (10, 5, True, 15),
])
def test_unfreeze_deposit_success(initial_balance, amount, unfreeze_before, expected):
    account = BankAccount(initial_balance)
    account.freeze_account()
    if unfreeze_before:
        account.unfreeze_account()
    assert account.deposit(amount) == expected