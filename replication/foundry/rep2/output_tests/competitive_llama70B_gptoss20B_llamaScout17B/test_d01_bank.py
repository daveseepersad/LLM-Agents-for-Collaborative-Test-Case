import pytest
from data.input_code.d01_bank import *

cases = [
    {"id": "T1_OK_INIT", "target": "BankAccount.__init__", "input": {"initial_balance": 100}, "setup": {}, "expected": None},
    {"id": "T2_ERR_INIT_NEG", "target": "BankAccount.__init__", "input": {"initial_balance": -50}, "setup": {}, "expected": "ValueError"},
    {"id": "T3_OK_DEPOSIT", "target": "BankAccount.deposit", "input": {"amount": 50}, "setup": {"initial_balance": 100}, "expected": 150},
    {"id": "T4_ERR_DEPOSIT_NONPOS", "target": "BankAccount.deposit", "input": {"amount": 0}, "setup": {"initial_balance": 100}, "expected": "ValueError"},
    {"id": "T5_ERR_DEPOSIT_FROZEN", "target": "BankAccount.deposit", "input": {"amount": 50}, "setup": {"initial_balance": 100, "freeze": True}, "expected": "ValueError"},
    {"id": "T6_OK_WITHDRAW", "target": "BankAccount.withdraw", "input": {"amount": 50}, "setup": {"initial_balance": 100}, "expected": 50},
    {"id": "T7_ERR_WITHDRAW_NONPOS", "target": "BankAccount.withdraw", "input": {"amount": 0}, "setup": {"initial_balance": 100}, "expected": "ValueError"},
    {"id": "T8_ERR_WITHDRAW_FROZEN", "target": "BankAccount.withdraw", "input": {"amount": 50}, "setup": {"initial_balance": 100, "freeze": True}, "expected": "ValueError"},
    {"id": "T9_ERR_WITHDRAW_INSUFF", "target": "BankAccount.withdraw", "input": {"amount": 150}, "setup": {"initial_balance": 100}, "expected": "ValueError"},
    {"id": "T10_OK_FREEZE", "target": "BankAccount.freeze_account", "input": {}, "setup": {"initial_balance": 100}, "expected": None},
    {"id": "T11_OK_UNFREEZE", "target": "BankAccount.unfreeze_account", "input": {}, "setup": {"initial_balance": 100, "freeze": True}, "expected": None},
]

@pytest.mark.parametrize("case", cases, ids=[c["id"] for c in cases])
def test_bank_account_plan(case):
    target = case["target"]
    input_data = case.get("input", {})
    setup = case.get("setup", {})
    expected = case.get("expected")

    if target == "BankAccount.__init__":
        # Initialize and validate or expect exception
        if expected is None:
            acc = BankAccount(**input_data)
            balance = input_data.get("initial_balance", 0)
            assert acc.balance == balance
            assert acc.is_active is True
        else:
            with pytest.raises(eval(expected)):
                BankAccount(**input_data)
        return

    # For other methods, create account with setup initial_balance
    init_balance = setup.get("initial_balance", 0)
    acc = BankAccount(initial_balance=init_balance)
    if setup.get("freeze"):
        acc.freeze_account()

    if target == "BankAccount.deposit":
        amount = input_data["amount"]
        if isinstance(expected, str):
            with pytest.raises(eval(expected)):
                acc.deposit(amount)
        else:
            ret = acc.deposit(amount)
            assert ret == expected
            assert acc.balance == expected
    elif target == "BankAccount.withdraw":
        amount = input_data["amount"]
        if isinstance(expected, str):
            with pytest.raises(eval(expected)):
                acc.withdraw(amount)
        else:
            ret = acc.withdraw(amount)
            assert ret == expected
            assert acc.balance == expected
    elif target == "BankAccount.freeze_account":
        acc.freeze_account()
        assert acc.is_active is False
    elif target == "BankAccount.unfreeze_account":
        acc.unfreeze_account()
        assert acc.is_active is True