import pytest
from data.input_code.d01_bank import *

# -------------------- Initialization --------------------

def test_init_success():
    acc = BankAccount(initial_balance=100)
    assert acc.balance == 100
    assert acc.is_active is True

@pytest.mark.parametrize('initial_balance', [-50])
def test_init_error(initial_balance):
    with pytest.raises(ValueError):
        BankAccount(initial_balance=initial_balance)

# -------------------- Deposit --------------------

@pytest.mark.parametrize(
    'initial, amount, expected_balance',
    [
        (100, 50, 150),   # normal deposit
    ]
)
def test_deposit_success(initial, amount, expected_balance):
    acc = BankAccount(initial_balance=initial)
    result = acc.deposit(amount)
    assert result == expected_balance
    assert acc.balance == expected_balance

@pytest.mark.parametrize(
    'initial, amount, freeze, expected_exception',
    [
        (100, 50, True, ValueError),   # deposit on frozen account
        (100, 0, False, ValueError),   # non‑positive deposit amount
    ]
)
def test_deposit_error(initial, amount, freeze, expected_exception):
    acc = BankAccount(initial_balance=initial)
    if freeze:
        acc.freeze_account()
    with pytest.raises(expected_exception):
        acc.deposit(amount)

# -------------------- Withdraw --------------------

@pytest.mark.parametrize(
    'initial, amount, expected_balance',
    [
        (100, 50, 50),   # normal withdrawal
    ]
)
def test_withdraw_success(initial, amount, expected_balance):
    acc = BankAccount(initial_balance=initial)
    result = acc.withdraw(amount)
    assert result == expected_balance
    assert acc.balance == expected_balance

@pytest.mark.parametrize(
    'initial, amount, freeze, expected_exception',
    [
        (100, 50, True, ValueError),    # withdrawal on frozen account
        (100, 0, False, ValueError),    # non‑positive withdrawal amount
        (100, 150, False, ValueError),  # insufficient funds
    ]
)
def test_withdraw_error(initial, amount, freeze, expected_exception):
    acc = BankAccount(initial_balance=initial)
    if freeze:
        acc.freeze_account()
    with pytest.raises(expected_exception):
        acc.withdraw(amount)

# -------------------- Freeze / Unfreeze --------------------

def test_freeze_account():
    acc = BankAccount(initial_balance=100)
    acc.freeze_account()
    assert acc.is_active is False

def test_unfreeze_account():
    acc = BankAccount(initial_balance=100)
    acc.freeze_account()
    assert acc.is_active is False
    acc.unfreeze_account()
    assert acc.is_active is True