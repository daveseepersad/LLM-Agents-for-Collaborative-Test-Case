import pytest
from data.input_code.d01_bank import *
import builtins

def test_init_ok():
    acct = BankAccount(initial_balance=100)
    assert acct.balance == 100
    assert acct.is_active is True

def test_init_err():
    with pytest.raises(ValueError):
        BankAccount(initial_balance=-10)

@pytest.mark.parametrize('self_state, amount, expected, expected_exception', [
    ({"balance": 100, "is_active": True}, 50, 150, None),     # T3_DEPOSIT_OK
    ({"balance": 100, "is_active": False}, 50, None, "ValueError"),  # T4_DEPOSIT_ERR_FROZEN
    ({"balance": 100, "is_active": True}, -50, None, "ValueError"),   # T5_DEPOSIT_ERR_NEGATIVE
])
def test_deposit_operations(self_state, amount, expected, expected_exception):
    acct = BankAccount(initial_balance=self_state.get('balance', 0))
    acct.is_active = self_state.get('is_active', True)
    if expected_exception:
        with pytest.raises(getattr(builtins, expected_exception)):
            acct.deposit(amount)
    else:
        result = acct.deposit(amount)
        assert result == expected
        assert acct.balance == expected

@pytest.mark.parametrize('self_state, amount, expected, expected_exception', [
    ({"balance": 100, "is_active": True}, 50, 50, None),       # T6_WITHDRAW_OK
    ({"balance": 100, "is_active": False}, 50, None, "ValueError"),  # T7_WITHDRAW_ERR_FROZEN
    ({"balance": 100, "is_active": True}, -50, None, "ValueError"),   # T8_WITHDRAW_ERR_NEGATIVE
    ({"balance": 100, "is_active": True}, 150, None, "ValueError"),   # T9_WITHDRAW_ERR_INSUFFICIENT
])
def test_withdraw_operations(self_state, amount, expected, expected_exception):
    acct = BankAccount(initial_balance=self_state.get('balance', 0))
    acct.is_active = self_state.get('is_active', True)
    if expected_exception:
        with pytest.raises(getattr(builtins, expected_exception)):
            acct.withdraw(amount)
    else:
        result = acct.withdraw(amount)
        assert result == expected
        assert acct.balance == expected

def test_freeze_account():
    acct = BankAccount(initial_balance=100)
    acct.freeze_account()
    assert acct.is_active is False

def test_unfreeze_account():
    acct = BankAccount(initial_balance=100)
    acct.is_active = False
    acct.unfreeze_account()
    assert acct.is_active is True