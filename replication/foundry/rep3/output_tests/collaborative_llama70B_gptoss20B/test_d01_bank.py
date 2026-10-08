import pytest
from data.input_code.d01_bank import *

# Init tests: T1_OK_INIT, T2_ERR_INIT_NEG
init_tests = [
    ({"initial_balance": 100}, None),
    ({"initial_balance": -50}, "ValueError"),
]

@pytest.mark.parametrize("input_kwargs, expected_exc", init_tests)
def test_bank_account_init(input_kwargs, expected_exc):
    if expected_exc:
        with pytest.raises(ValueError):
            BankAccount(**input_kwargs)
    else:
        acc = BankAccount(**input_kwargs)
        assert isinstance(acc, BankAccount)
        assert acc.balance == input_kwargs["initial_balance"]

# Deposit tests: T3_OK_DEPOSIT, T4_ERR_DEPOSIT_FROZEN, T5_ERR_DEPOSIT_NONPOS, T6_ERR_DEPOSIT_NEG
deposit_tests = [
    ({"initial_balance": 100}, 50, 150, None),
    ({"initial_balance": 100, "freeze_account": True}, 50, None, "ValueError"),
    ({"initial_balance": 100}, 0, None, "ValueError"),
    ({"initial_balance": 100}, -50, None, "ValueError"),
]

@pytest.mark.parametrize("setup, amount, expected, exc_name", deposit_tests)
def test_bank_account_deposit(setup, amount, expected, exc_name):
    acc = BankAccount(setup.get("initial_balance", 0))
    if setup.get("freeze_account"):
        acc.freeze_account()
    if exc_name:
        with pytest.raises(ValueError):
            acc.deposit(amount)
    else:
        result = acc.deposit(amount)
        assert result == expected

# Withdraw tests: T7_OK_WITHDRAW, T8_ERR_WITHDRAW_FROZEN, T9_ERR_WITHDRAW_NONPOS, T10_ERR_WITHDRAW_NEG, T11_ERR_WITHDRAW_INSUFF
withdraw_tests = [
    ({"initial_balance": 100}, 50, 50, None),
    ({"initial_balance": 100, "freeze_account": True}, 50, None, "ValueError"),
    ({"initial_balance": 100}, 0, None, "ValueError"),
    ({"initial_balance": 100}, -50, None, "ValueError"),
    ({"initial_balance": 100}, 150, None, "ValueError"),
]

@pytest.mark.parametrize("setup, amount, expected, exc_name", withdraw_tests)
def test_bank_account_withdraw(setup, amount, expected, exc_name):
    acc = BankAccount(setup.get("initial_balance", 0))
    if setup.get("freeze_account"):
        acc.freeze_account()
    if exc_name:
        with pytest.raises(ValueError):
            acc.withdraw(amount)
    else:
        result = acc.withdraw(amount)
        assert result == expected

# Freeze test: T12_OK_FREEZE
@pytest.mark.parametrize("setup", [
    {"initial_balance": 100},
])
def test_bank_account_freeze(setup):
    acc = BankAccount(setup.get("initial_balance", 0))
    acc.freeze_account()
    assert acc.is_active is False

# Unfreeze test: T13_OK_UNFREEZE
@pytest.mark.parametrize("setup", [
    {"initial_balance": 100, "freeze_account": True},
])
def test_bank_account_unfreeze(setup):
    acc = BankAccount(setup.get("initial_balance", 0))
    if setup.get("freeze_account"):
        acc.freeze_account()
    acc.unfreeze_account()
    assert acc.is_active is True