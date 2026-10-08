import pytest
from data.input_code.d01_bank import *

# -------------------- Init Tests --------------------
@pytest.mark.parametrize(
    "init_balance, expected_balance, expected_active, expect_exc",
    [
        (None, 0, True, None),          # T1_init_default
        (50, 50, True, None),           # T2_init_positive
        (-10, None, None, ValueError),  # T3_init_negative
    ],
)
def test_bankaccount_init(init_balance, expected_balance, expected_active, expect_exc):
    if expect_exc:
        with pytest.raises(expect_exc):
            BankAccount(initial_balance=init_balance) if init_balance is not None else BankAccount()
    else:
        acct = BankAccount(initial_balance=init_balance) if init_balance is not None else BankAccount()
        assert acct.balance == expected_balance
        assert acct.is_active == expected_active


# -------------------- Deposit Tests --------------------
@pytest.mark.parametrize(
    "init_balance, amount, freeze_before, unfreeze_before, expected_balance, expect_exc",
    [
        (100, 25, False, False, 125, None),          # T4_deposit_success
        (0, 0, False, False, None, ValueError),     # T5_deposit_invalid_amount
        (0, 10, True, False, None, ValueError),     # T6_deposit_frozen
        (0, 10, True, True, 10, None),               # T11_unfreeze_deposit
    ],
)
def test_bankaccount_deposit(
    init_balance, amount, freeze_before, unfreeze_before, expected_balance, expect_exc
):
    acct = BankAccount(initial_balance=init_balance)
    if freeze_before:
        acct.freeze_account()
    if unfreeze_before:
        acct.unfreeze_account()
    if expect_exc:
        with pytest.raises(expect_exc):
            acct.deposit(amount)
    else:
        result = acct.deposit(amount)
        assert result == expected_balance
        assert acct.balance == expected_balance


# -------------------- Withdraw Tests --------------------
@pytest.mark.parametrize(
    "init_balance, amount, freeze_before, expected_balance, expect_exc",
    [
        (100, 40, False, 60, None),          # T7_withdraw_success
        (10, 0, False, None, ValueError),    # T8_withdraw_invalid_amount
        (10, 20, False, None, ValueError),   # T9_withdraw_insufficient
        (10, 5, True, None, ValueError),     # T10_withdraw_frozen
    ],
)
def test_bankaccount_withdraw(
    init_balance, amount, freeze_before, expected_balance, expect_exc
):
    acct = BankAccount(initial_balance=init_balance)
    if freeze_before:
        acct.freeze_account()
    if expect_exc:
        with pytest.raises(expect_exc):
            acct.withdraw(amount)
    else:
        result = acct.withdraw(amount)
        assert result == expected_balance
        assert acct.balance == expected_balance