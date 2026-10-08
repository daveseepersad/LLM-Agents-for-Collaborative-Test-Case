import pytest
from data.input_code.d01_bank import BankAccount

class TestBankAccount:
    def test_init_default_balance(self):
        account = BankAccount()
        assert account.balance == 0
        assert account.is_active

    def test_init_positive_balance(self):
        account = BankAccount(100)
        assert account.balance == 100
        assert account.is_active

    def test_init_negative_balance(self):
        with pytest.raises(ValueError):
            BankAccount(-100)

    def test_deposit_positive_amount(self):
        account = BankAccount(100)
        new_balance = account.deposit(50)
        assert new_balance == 150
        assert account.balance == 150

    def test_deposit_zero_amount(self):
        account = BankAccount(100)
        with pytest.raises(ValueError):
            account.deposit(0)

    def test_deposit_negative_amount(self):
        account = BankAccount(100)
        with pytest.raises(ValueError):
            account.deposit(-50)

    def test_deposit_frozen_account(self):
        account = BankAccount(100)
        account.freeze_account()
        with pytest.raises(ValueError):
            account.deposit(50)

    def test_withdraw_positive_amount(self):
        account = BankAccount(100)
        new_balance = account.withdraw(50)
        assert new_balance == 50
        assert account.balance == 50

    def test_withdraw_zero_amount(self):
        account = BankAccount(100)
        with pytest.raises(ValueError):
            account.withdraw(0)

    def test_withdraw_negative_amount(self):
        account = BankAccount(100)
        with pytest.raises(ValueError):
            account.withdraw(-50)

    def test_withdraw_insufficient_funds(self):
        account = BankAccount(100)
        with pytest.raises(ValueError):
            account.withdraw(150)

    def test_withdraw_frozen_account(self):
        account = BankAccount(100)
        account.freeze_account()
        with pytest.raises(ValueError):
            account.withdraw(50)

    def test_freeze_account(self):
        account = BankAccount(100)
        account.freeze_account()
        assert not account.is_active

    def test_unfreeze_account(self):
        account = BankAccount(100)
        account.freeze_account()
        account.unfreeze_account()
        assert account.is_active

def test_init_none_balance():
    with pytest.raises(TypeError):
        BankAccount(None)

def test_deposit_none_amount():
    account = BankAccount(100)
    with pytest.raises(TypeError):
        account.deposit(None)

def test_withdraw_none_amount():
    account = BankAccount(100)
    with pytest.raises(TypeError):
        account.withdraw(None)