import pytest
from data.input_code.d01_bank import *

# -------------------- __init__ --------------------

@pytest.mark.parametrize(
    "initial_balance, expected_balance, expected_active",
    [
        (100, 100, True),
    ],
    ids=["TC01_INIT_POSITIVE"]
)
def test_bankaccount_init_success(initial_balance, expected_balance, expected_active):
    account = BankAccount(initial_balance)
    assert account.balance == expected_balance
    assert account.is_active == expected_active


def test_bankaccount_init_negative():
    with pytest.raises(ValueError):
        BankAccount(-10)


# -------------------- deposit --------------------

@pytest.mark.parametrize(
    "setup_balance, setup_active, amount, expected_balance, expect_exception",
    [
        (50, True, 25, 75, None),                     # TC03_DEPOSIT_SUCCESS
        (30, True, 0, None, ValueError),             # TC04_DEPOSIT_NONPOSITIVE
        (20, False, 10, None, ValueError),           # TC05_DEPOSIT_FROZEN
    ],
    ids=[
        "TC03_DEPOSIT_SUCCESS",
        "TC04_DEPOSIT_NONPOSITIVE",
        "TC05_DEPOSIT_FROZEN",
    ]
)
def test_bankaccount_deposit(setup_balance, setup_active, amount, expected_balance, expect_exception):
    account = BankAccount(setup_balance)
    account.is_active = setup_active
    if expect_exception:
        with pytest.raises(expect_exception):
            account.deposit(amount)
    else:
        result = account.deposit(amount)
        assert result == expected_balance
        assert account.balance == expected_balance


# -------------------- withdraw --------------------

@pytest.mark.parametrize(
    "setup_balance, setup_active, amount, expected_balance, expect_exception",
    [
        (100, True, 40, 60, None),                    # TC06_WITHDRAW_SUCCESS
        (80, True, 0, None, ValueError),             # TC07_WITHDRAW_NONPOSITIVE
        (30, True, 50, None, ValueError),            # TC08_WITHDRAW_INSUFFICIENT
        (70, False, 20, None, ValueError),           # TC09_WITHDRAW_FROZEN
    ],
    ids=[
        "TC06_WITHDRAW_SUCCESS",
        "TC07_WITHDRAW_NONPOSITIVE",
        "TC08_WITHDRAW_INSUFFICIENT",
        "TC09_WITHDRAW_FROZEN",
    ]
)
def test_bankaccount_withdraw(setup_balance, setup_active, amount, expected_balance, expect_exception):
    account = BankAccount(setup_balance)
    account.is_active = setup_active
    if expect_exception:
        with pytest.raises(expect_exception):
            account.withdraw(amount)
    else:
        result = account.withdraw(amount)
        assert result == expected_balance
        assert account.balance == expected_balance


# -------------------- freeze_account --------------------

def test_bankaccount_freeze_account():
    account = BankAccount(0)          # starts active
    account.freeze_account()
    assert account.is_active is False


# -------------------- unfreeze_account --------------------

def test_bankaccount_unfreeze_account():
    account = BankAccount(0)
    account.is_active = False        # manually freeze for setup
    account.unfreeze_account()
    assert account.is_active is True