import pytest
from data.input_code.d01_bank import BankAccount

# ---------- __init__ tests ----------
@pytest.mark.parametrize(
    "initial_balance, expected",
    [
        (-5, ValueError),
        (0, 0),
        (100, 100),
    ],
)
def test_bankaccount_init(initial_balance, expected):
    if isinstance(expected, type) and issubclass(expected, Exception):
        with pytest.raises(expected):
            BankAccount(initial_balance=initial_balance)
    else:
        account = BankAccount(initial_balance=initial_balance)
        assert account.balance == expected
        assert account.is_active is True

# ---------- deposit tests ----------
@pytest.mark.parametrize(
    "initial_balance, amount, freeze_before, expected",
    [
        (10, 5, False, 15),          # T4
        (10, 0, False, ValueError),  # T5
        (10, -3, False, ValueError), # T6
        (10, 5, True, ValueError),   # T7
    ],
)
def test_bankaccount_deposit(initial_balance, amount, freeze_before, expected):
    account = BankAccount(initial_balance=initial_balance)
    if freeze_before:
        account.freeze_account()
    if isinstance(expected, type) and issubclass(expected, Exception):
        with pytest.raises(expected):
            account.deposit(amount)
    else:
        result = account.deposit(amount)
        assert result == expected
        assert account.balance == expected

# ---------- withdraw tests ----------
@pytest.mark.parametrize(
    "initial_balance, amount, freeze_before, expected",
    [
        (10, 4, False, 6),          # T8
        (10, 0, False, ValueError), # T9
        (10, -2, False, ValueError),# T10
        (5, 10, False, ValueError), # T11
        (10, 3, True, ValueError),  # T12
    ],
)
def test_bankaccount_withdraw(initial_balance, amount, freeze_before, expected):
    account = BankAccount(initial_balance=initial_balance)
    if freeze_before:
        account.freeze_account()
    if isinstance(expected, type) and issubclass(expected, Exception):
        with pytest.raises(expected):
            account.withdraw(amount)
    else:
        result = account.withdraw(amount)
        assert result == expected
        assert account.balance == expected

# ---------- freeze_account test ----------
def test_bankaccount_freeze_account():
    account = BankAccount(initial_balance=0)
    account.freeze_account()
    assert account.is_active is False

# ---------- unfreeze_account test ----------
def test_bankaccount_unfreeze_account():
    account = BankAccount(initial_balance=0)
    account.freeze_account()
    account.unfreeze_account()
    assert account.is_active is True