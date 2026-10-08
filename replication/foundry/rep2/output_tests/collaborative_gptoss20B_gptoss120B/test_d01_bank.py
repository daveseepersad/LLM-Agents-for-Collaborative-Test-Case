import pytest
from data.input_code.d01_bank import *

@pytest.mark.parametrize('initial_balance, expect_error', [
    (0, None),
    (-10, ValueError)
])
def test_bank_init(initial_balance, expect_error):
    if expect_error is None:
        acc = BankAccount(initial_balance=initial_balance)
        assert acc.balance == initial_balance
        assert acc.is_active is True
    else:
        with pytest.raises(expect_error):
            BankAccount(initial_balance=initial_balance)

@pytest.mark.parametrize('initial_balance, pre_actions, amount, expected', [
    (100, [], 50, 150),
    (100, [], 0, "ValueError"),
    (100, ["freeze_account"], 10, "ValueError"),
])
def test_bank_deposit(initial_balance, pre_actions, amount, expected):
    acc = BankAccount(initial_balance=initial_balance)
    for action in pre_actions:
        if action == "freeze_account":
            acc.freeze_account()
        elif action == "unfreeze_account":
            acc.unfreeze_account()
    if expected == "ValueError":
        with pytest.raises(ValueError):
            acc.deposit(amount)
    else:
        result = acc.deposit(amount)
        assert result == expected

@pytest.mark.parametrize('initial_balance, pre_actions, amount, expected, start_inactive', [
    (200, [], 30, 170, False),
    (200, [], 0, "ValueError", False),
    (50, [], 100, "ValueError", False),
    (100, ["freeze_account"], 10, "ValueError", False),
    (100, ["unfreeze_account"], 20, 80, True),
])
def test_bank_withdraw(initial_balance, pre_actions, amount, expected, start_inactive):
    acc = BankAccount(initial_balance=initial_balance)
    if start_inactive:
        acc.is_active = False
    for action in pre_actions:
        if action == "freeze_account":
            acc.freeze_account()
        elif action == "unfreeze_account":
            acc.unfreeze_account()
    if expected == "ValueError":
        with pytest.raises(ValueError):
            acc.withdraw(amount)
    else:
        result = acc.withdraw(amount)
        assert result == expected