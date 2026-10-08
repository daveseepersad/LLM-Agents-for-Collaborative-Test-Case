import pytest
from data.input_code.d01_bank import *

# -------------------- __init__ --------------------
@pytest.mark.parametrize(
    "initial_balance, expected_balance, expected_is_active, expected_exception",
    [
        (0, 0, True, None),          # T1_INIT_DEFAULT
        (150, 150, True, None),      # T2_INIT_POSITIVE
        (-10, None, None, ValueError)  # T3_INIT_NEGATIVE
    ]
)
def test_bankaccount_init(initial_balance, expected_balance, expected_is_active, expected_exception):
    if expected_exception:
        with pytest.raises(expected_exception):
            BankAccount(initial_balance)
    else:
        acc = BankAccount(initial_balance)
        assert acc.balance == expected_balance
        assert acc.is_active == expected_is_active

# -------------------- deposit --------------------
@pytest.mark.parametrize(
    "setup_balance, setup_active, deposit_amount, expected_result, expected_exception",
    [
        (50, True, 25, 75, None),          # T4_DEPOSIT_SUCCESS
        (30, True, 0, None, ValueError),  # T5_DEPOSIT_ZERO
        (40, False, 10, None, ValueError) # T6_DEPOSIT_FROZEN
    ]
)
def test_bankaccount_deposit(setup_balance, setup_active, deposit_amount, expected_result, expected_exception):
    acc = BankAccount(setup_balance)
    acc.is_active = setup_active
    if expected_exception:
        with pytest.raises(expected_exception):
            acc.deposit(deposit_amount)
    else:
        result = acc.deposit(deposit_amount)
        assert result == expected_result
        assert acc.balance == expected_result

# -------------------- withdraw --------------------
@pytest.mark.parametrize(
    "setup_balance, setup_active, withdraw_amount, expected_result, expected_exception",
    [
        (100, True, 40, 60, None),          # T7_WITHDRAW_SUCCESS
        (80, True, 0, None, ValueError),   # T8_WITHDRAW_ZERO
        (50, True, 75, None, ValueError),  # T9_WITHDRAW_OVERDRAFT
        (60, False, 20, None, ValueError)  # T10_WITHDRAW_FROZEN
    ]
)
def test_bankaccount_withdraw(setup_balance, setup_active, withdraw_amount, expected_result, expected_exception):
    acc = BankAccount(setup_balance)
    acc.is_active = setup_active
    if expected_exception:
        with pytest.raises(expected_exception):
            acc.withdraw(withdraw_amount)
    else:
        result = acc.withdraw(withdraw_amount)
        assert result == expected_result
        assert acc.balance == expected_result

# -------------------- freeze / unfreeze --------------------
def test_bankaccount_freeze_unfreeze():
    acc = BankAccount(20)  # setup active account
    # freeze
    acc.freeze_account()
    assert acc.is_active is False
    # unfreeze
    acc.unfreeze_account()
    assert acc.is_active is True