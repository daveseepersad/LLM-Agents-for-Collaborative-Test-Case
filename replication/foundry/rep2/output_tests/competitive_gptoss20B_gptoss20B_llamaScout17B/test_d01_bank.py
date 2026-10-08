import pytest
import builtins
from data.input_code.d01_bank import *

# BankAccount.__init__ tests
@pytest.mark.parametrize('initial_balance, exc_name, expected_attrs', [
    (-5, 'ValueError', None),
    (None, 'TypeError', None),
    (0, None, {'balance': 0, 'is_active': True}),
    (1000000000, None, {'balance': 1000000000, 'is_active': True}),
])
def test_bank_account_init(initial_balance, exc_name, expected_attrs):
    if exc_name is not None:
        with pytest.raises(getattr(builtins, exc_name)):
            BankAccount(initial_balance=initial_balance)
    else:
        acc = BankAccount(initial_balance=initial_balance)
        assert acc.balance == expected_attrs['balance']
        assert acc.is_active == expected_attrs['is_active']

# BankAccount.deposit tests
@pytest.mark.parametrize('state, amount, expected', [
    ({'balance': 100, 'is_active': True}, 50, 150),
    ({'balance': 100, 'is_active': False}, 50, 'ValueError'),
    ({'balance': 10, 'is_active': True}, 0, 'ValueError'),
])
def test_bank_account_deposit(state, amount, expected):
    acc = BankAccount(initial_balance=0)
    acc.balance = state['balance']
    acc.is_active = state['is_active']
    if isinstance(expected, int):
        assert acc.deposit(amount) == expected
    else:
        with pytest.raises(getattr(builtins, expected)):
            acc.deposit(amount)

# BankAccount.withdraw tests
@pytest.mark.parametrize('state, amount, expected', [
    ({'balance': 100, 'is_active': True}, 40, 60),
    ({'balance': 100, 'is_active': False}, 40, 'ValueError'),
    ({'balance': 50, 'is_active': True}, -5, 'ValueError'),
    ({'balance': 30, 'is_active': True}, 40, 'ValueError'),
])
def test_bank_account_withdraw(state, amount, expected):
    acc = BankAccount(initial_balance=0)
    acc.balance = state['balance']
    acc.is_active = state['is_active']
    if isinstance(expected, int):
        assert acc.withdraw(amount) == expected
    else:
        with pytest.raises(getattr(builtins, expected)):
            acc.withdraw(amount)

# BankAccount.freeze_account / unfreeze_account tests
@pytest.mark.parametrize('start_is_active, action, final_is_active', [
    (True, 'freeze', False),
    (False, 'unfreeze', True),
])
def test_bank_account_freeze_unfreeze(start_is_active, action, final_is_active):
    acc = BankAccount(initial_balance=0)
    acc.is_active = start_is_active
    if action == 'freeze':
        acc.freeze_account()
    else:
        acc.unfreeze_account()
    assert acc.is_active == final_is_active