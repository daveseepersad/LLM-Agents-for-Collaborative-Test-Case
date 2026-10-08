import pytest
from data.input_code.d01_bank import *

# -------------------- __init__ tests --------------------
@pytest.mark.parametrize(
    "initial_balance, expected_balance, expected_is_active, expected_exception",
    [
        (100, 100, True, None),          # positive balance
        (0, 0, True, None),              # zero balance
        (-10, None, None, ValueError),   # negative balance raises
    ],
)
def test_bankaccount_init(
    initial_balance, expected_balance, expected_is_active, expected_exception
):
    if expected_exception:
        with pytest.raises(expected_exception):
            BankAccount(initial_balance)
    else:
        acct = BankAccount(initial_balance)
        assert acct.balance == expected_balance
        assert acct.is_active == expected_is_active


# -------------------- deposit tests --------------------
@pytest.mark.parametrize(
    "initial_balance, freeze, unfreeze, amount, expected_balance, expected_exception",
    [
        (100, False, False, 50, 150, None),          # successful deposit
        (100, False, False, 0, None, ValueError),   # invalid amount
        (100, True, False, 10, None, ValueError),   # deposit into frozen account
        (100, True, True, 10, 110, None),            # freeze then unfreeze then deposit
    ],
)
def test_bankaccount_deposit(
    initial_balance,
    freeze,
    unfreeze,
    amount,
    expected_balance,
    expected_exception,
):
    acct = BankAccount(initial_balance)
    if freeze:
        acct.freeze_account()
    if unfreeze:
        acct.unfreeze_account()

    if expected_exception:
        with pytest.raises(expected_exception):
            acct.deposit(amount)
    else:
        result = acct.deposit(amount)
        assert result == expected_balance
        assert acct.balance == expected_balance


# -------------------- withdraw tests --------------------
@pytest.mark.parametrize(
    "initial_balance, freeze, amount, expected_balance, expected_exception",
    [
        (100, False, 30, 70, None),          # successful withdraw
        (100, False, 100, 0, None),          # withdraw entire balance
        (100, False, 0, None, ValueError),  # invalid amount
        (100, False, 150, None, ValueError),# insufficient funds
        (100, True, 10, None, ValueError),  # withdraw from frozen account
    ],
)
def test_bankaccount_withdraw(
    initial_balance, freeze, amount, expected_balance, expected_exception
):
    acct = BankAccount(initial_balance)
    if freeze:
        acct.freeze_account()

    if expected_exception:
        with pytest.raises(expected_exception):
            acct.withdraw(amount)
    else:
        result = acct.withdraw(amount)
        assert result == expected_balance
        assert acct.balance == expected_balance