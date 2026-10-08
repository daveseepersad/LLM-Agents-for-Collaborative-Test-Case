import pytest
from data.input_code.d01_bank import *

# -------------------- Initialization Tests --------------------
@pytest.mark.parametrize(
    "initial_balance, expect_exception, expected_balance, expected_active",
    [
        (-1, ValueError, None, None),          # T_INIT_NEG
        (0, None, 0, True),                    # T_INIT_OK
    ],
)
def test_bankaccount_init(initial_balance, expect_exception, expected_balance, expected_active):
    if expect_exception:
        with pytest.raises(expect_exception):
            BankAccount(initial_balance)
    else:
        acc = BankAccount(initial_balance)
        assert acc.balance == expected_balance
        assert acc.is_active is expected_active


# -------------------- Deposit Tests --------------------
@pytest.mark.parametrize(
    "initial_balance, amount, freeze_before, expect_exception, expected_balance",
    [
        (10, 5, False, None, 15),          # T_DEPOSIT_OK
        (10, 0, False, ValueError, None), # T_DEPOSIT_NEG
        (10, 5, True, ValueError, None),  # T_DEPOSIT_FROZEN
    ],
)
def test_bankaccount_deposit(initial_balance, amount, freeze_before, expect_exception, expected_balance):
    acc = BankAccount(initial_balance)
    if freeze_before:
        acc.freeze_account()
    if expect_exception:
        with pytest.raises(expect_exception):
            acc.deposit(amount)
    else:
        result = acc.deposit(amount)
        assert result == expected_balance
        assert acc.balance == expected_balance


# -------------------- Withdraw Tests --------------------
@pytest.mark.parametrize(
    "initial_balance, amount, freeze_before, expect_exception, expected_balance",
    [
        (100, 40, False, None, 60),          # T_WITHDRAW_OK
        (50, 60, False, ValueError, None),  # T_WITHDRAW_INS
        (50, -5, False, ValueError, None),  # T_WITHDRAW_NEG
        (100, 10, True, ValueError, None),  # T_WITHDRAW_FROZEN
    ],
)
def test_bankaccount_withdraw(initial_balance, amount, freeze_before, expect_exception, expected_balance):
    acc = BankAccount(initial_balance)
    if freeze_before:
        acc.freeze_account()
    if expect_exception:
        with pytest.raises(expect_exception):
            acc.withdraw(amount)
    else:
        result = acc.withdraw(amount)
        assert result == expected_balance
        assert acc.balance == expected_balance


# -------------------- Freeze / Unfreeze Tests --------------------
def test_bankaccount_freeze():
    acc = BankAccount(5)
    acc.freeze_account()
    assert acc.is_active is False


def test_bankaccount_unfreeze():
    acc = BankAccount(5)
    # Ensure we start from a frozen state to truly test unfreeze
    acc.freeze_account()
    acc.unfreeze_account()
    assert acc.is_active is True