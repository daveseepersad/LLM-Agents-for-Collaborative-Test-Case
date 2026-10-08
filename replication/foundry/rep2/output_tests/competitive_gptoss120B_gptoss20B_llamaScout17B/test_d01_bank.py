import pytest
from data.input_code.d01_bank import *

@pytest.mark.parametrize('initial_balance, expect_exception, expected_balance', [
    (100, None, 100),
    (-10, ValueError, None),
])
def test_T1_T2_INIT(initial_balance, expect_exception, expected_balance):
    if expect_exception:
        with pytest.raises(expect_exception):
            BankAccount(initial_balance)
    else:
        acc = BankAccount(initial_balance)
        assert acc.balance == expected_balance
        assert acc.is_active is True


@pytest.mark.parametrize('initial_balance, amount, freeze_before, expected, expect_exception', [
    (50, 25, False, 75, None),
    (20, 0, False, None, ValueError),
    (30, 10, True, None, ValueError),
])
def test_T3_T4_T5_DEPOSIT(initial_balance, amount, freeze_before, expected, expect_exception):
    acc = BankAccount(initial_balance)
    if freeze_before:
        acc.freeze_account()
    if expect_exception:
        with pytest.raises(expect_exception):
            acc.deposit(amount)
    else:
        result = acc.deposit(amount)
        assert result == expected


@pytest.mark.parametrize('initial_balance, amount, freeze_before, expected, expect_exception', [
    (100, 30, False, 70, None),
    (50, 50, False, 0, None),
    (40, 0, False, None, ValueError),
    (30, 40, False, None, ValueError),
    (20, 10, True, None, ValueError),
])
def test_T6_T7_T8_T9_T10_WITHDRAW(initial_balance, amount, freeze_before, expected, expect_exception):
    acc = BankAccount(initial_balance)
    if freeze_before:
        acc.freeze_account()
    if expect_exception:
        with pytest.raises(expect_exception):
            acc.withdraw(amount)
    else:
        result = acc.withdraw(amount)
        assert result == expected


def test_T11_FREEZE_UNFREEZE():
    acc = BankAccount(15)
    acc.freeze_account()
    acc.unfreeze_account()
    assert acc.is_active is True