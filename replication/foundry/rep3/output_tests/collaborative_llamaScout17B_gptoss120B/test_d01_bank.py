import pytest
from data.input_code.d01_bank import *

# ---------- Initialization ----------
@pytest.mark.parametrize('initial_balance, expected_exception', [
    (100, None),          # valid initialization
    (-50, ValueError),    # negative initial balance
])
def test_bankaccount_init(initial_balance, expected_exception):
    if expected_exception:
        with pytest.raises(expected_exception):
            BankAccount(initial_balance)
    else:
        acct = BankAccount(initial_balance)
        assert acct.balance == initial_balance
        assert acct.is_active is True

# ---------- Deposit ----------
@pytest.mark.parametrize(
    'initial_balance, freeze_before, amount, expected_balance, expected_exception',
    [
        (100, False, 50, 150, None),          # valid deposit
        (100, True, 50, None, ValueError),    # deposit on frozen account
        (100, False, 0, None, ValueError),    # non‑positive deposit amount
    ]
)
def test_bankaccount_deposit(initial_balance, freeze_before, amount,
                             expected_balance, expected_exception):
    acct = BankAccount(initial_balance)
    if freeze_before:
        acct.freeze_account()
    if expected_exception:
        with pytest.raises(expected_exception):
            acct.deposit(amount)
    else:
        result = acct.deposit(amount)
        assert result == expected_balance
        assert acct.balance == expected_balance

# ---------- Withdraw ----------
@pytest.mark.parametrize(
    'initial_balance, freeze_before, amount, expected_balance, expected_exception',
    [
        (100, False, 50, 50, None),           # valid withdrawal
        (100, True, 50, None, ValueError),    # withdrawal on frozen account
        (100, False, 0, None, ValueError),    # non‑positive withdrawal amount
        (100, False, 150, None, ValueError),  # insufficient funds
    ]
)
def test_bankaccount_withdraw(initial_balance, freeze_before, amount,
                              expected_balance, expected_exception):
    acct = BankAccount(initial_balance)
    if freeze_before:
        acct.freeze_account()
    if expected_exception:
        with pytest.raises(expected_exception):
            acct.withdraw(amount)
    else:
        result = acct.withdraw(amount)
        assert result == expected_balance
        assert acct.balance == expected_balance

# ---------- Freeze / Unfreeze ----------
def test_bankaccount_freeze_and_unfreeze():
    acct = BankAccount(100)
    # Freeze
    acct.freeze_account()
    assert acct.is_active is False
    # Unfreeze
    acct.unfreeze_account()
    assert acct.is_active is True