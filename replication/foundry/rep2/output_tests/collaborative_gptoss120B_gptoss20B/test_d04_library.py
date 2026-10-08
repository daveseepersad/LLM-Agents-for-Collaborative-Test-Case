import pytest
from data.input_code.d04_library import *

@pytest.fixture
def manager():
    """Provides a fresh LibraryManager for each test."""
    return LibraryManager()


def test_add_short_isbn(manager, capsys):
    """T1: ISBN shorter than 3 characters should be rejected."""
    manager.add_book(title="A", author="A", isbn="12")
    captured = capsys.readouterr()
    assert "[!] Error: ISBN '12' is too short." in captured.out
    assert "12" not in manager.inventory


def test_add_valid_and_duplicate(manager, capsys):
    """T2: Add a valid book, then attempt to add a duplicate ISBN."""
    # Add first book (valid)
    manager.add_book(title="Python 101", author="Guido van Rossum", isbn="123")
    out1 = capsys.readouterr().out
    assert "Success: Added 'Python 101' to the library." in out1
    assert "123" in manager.inventory
    assert isinstance(manager.inventory["123"], Book)

    # Attempt duplicate addition
    manager.add_book(title="Python 101 - Duplicate", author="Guido", isbn="123")
    out2 = capsys.readouterr().out
    assert "[!] Error: A book with ISBN 123 already exists." in out2
    # Inventory should still contain only one entry for ISBN 123
    assert len(manager.inventory) == 1
    assert manager.inventory["123"].title == "Python 101"


def test_borrow_nonexistent(manager, capsys):
    """T4: Borrowing a book that does not exist should report an error."""
    manager.borrow_book(isbn="999")
    captured = capsys.readouterr()
    assert "[!] Error: Book with ISBN 999 not found." in captured.out


def test_borrow_success_and_already_borrowed(manager, capsys):
    """T5 & T6: Borrow an available book, then attempt to borrow it again."""
    # Setup: add a valid book
    manager.add_book(title="Python 101", author="Guido van Rossum", isbn="123")
    capsys.readouterr()  # clear previous output

    # First borrow – should succeed
    manager.borrow_book(isbn="123")
    out_success = capsys.readouterr().out
    assert "Success: You have borrowed 'Python 101'." in out_success
    assert not manager.inventory["123"].is_available

    # Second borrow – should report unavailable
    manager.borrow_book(isbn="123")
    out_unavailable = capsys.readouterr().out
    assert "[!] Unavailable: 'Python 101' is currently borrowed by someone else." in out_unavailable
    # Status must remain borrowed
    assert not manager.inventory["123"].is_available


def test_return_nonexistent(manager, capsys):
    """T7: Returning a non‑existent book should report an error."""
    manager.return_book(isbn="999")
    captured = capsys.readouterr()
    assert "[!] Error: We do not own a book with ISBN 999." in captured.out


def test_show_inventory(manager, capsys):
    """T8: Show inventory prints each book using its __str__ representation."""
    # Add and borrow a book so its status is 'Borrowed'
    manager.add_book(title="Python 101", author="Guido van Rossum", isbn="123")
    capsys.readouterr()  # clear output
    manager.borrow_book(isbn="123")
    capsys.readouterr()  # clear output

    manager.show_inventory()
    out = capsys.readouterr().out
    # Header and footer should be present
    assert "--- Current Library Inventory ---" in out
    assert "---------------------------------" in out
    # Book line should reflect borrowed status
    expected_line = "[Borrowed] Python 101 by Guido van Rossum (ISBN: 123)"
    assert expected_line in out


def test_return_success(manager, capsys):
    """T9: Returning a borrowed book should make it available again."""
    # Add and borrow the book first
    manager.add_book(title="Python 101", author="Guido van Rossum", isbn="123")
    capsys.readouterr()
    manager.borrow_book(isbn="123")
    capsys.readouterr()

    # Return the book
    manager.return_book(isbn="123")
    out = capsys.readouterr().out
    assert "Success: 'Python 101' has been returned." in out
    assert manager.inventory["123"].is_available

import pytest
from data.input_code.d04_library import *

def test_show_inventory_empty(manager, capsys):
    """T_MISSING_EMPTY_INVENTORY: Verify show_inventory behavior when the library is empty."""
    manager.show_inventory()
    out = capsys.readouterr().out
    assert "The library is empty." in out

def test_return_already_available(manager, capsys):
    """T_MISSING_RETURN_ALREADY_AVAILABLE: Returning a book that has not been borrowed should trigger the Strange message."""
    manager.add_book(title="The Pragmatic Programmer", author="Andrew Hunt", isbn="555")
    capsys.readouterr()  # clear add_book output
    manager.return_book(isbn="555")
    out = capsys.readouterr().out
    assert "[!] Strange: You are trying to return 'The Pragmatic Programmer', but it was already here." in out

def test_show_inventory_available_book(manager, capsys):
    """T_MISSING_SHOW_AVAILABLE_BOOK: Show_inventory should reflect an available book's status."""
    manager.add_book(title="Clean Code", author="Robert C. Martin", isbn="555")
    capsys.readouterr()  # clear add_book output
    manager.show_inventory()
    out = capsys.readouterr().out
    expected_line = "[Available] Clean Code by Robert C. Martin (ISBN: 555)"
    assert expected_line in out