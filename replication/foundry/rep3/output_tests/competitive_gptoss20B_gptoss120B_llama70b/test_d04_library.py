import pytest
from data.input_code.d04_library import *

@pytest.fixture
def manager():
    """Provides a fresh LibraryManager for each test."""
    return LibraryManager()

@pytest.mark.parametrize(
    "title, author, isbn, should_add",
    [
        ("Book A", "Author A", "12", False),   # ISBN too short
        ("1984", "George Orwell", "123", True)  # Valid ISBN
    ]
)
def test_add_book(manager, title, author, isbn, should_add, capsys):
    """
    Verify that add_book respects ISBN length validation and adds a book when valid.
    """
    manager.add_book(title, author, isbn)
    # Check inventory state
    assert (isbn in manager.inventory) is should_add
    # Optional: verify printed messages contain expected hints
    captured = capsys.readouterr().out
    if not should_add:
        assert "Error: ISBN" in captured
    else:
        assert "Success: Added" in captured

def test_borrow_nonexistent_book(manager, capsys):
    """
    Borrowing a book that does not exist should not raise and leave inventory unchanged.
    """
    manager.borrow_book("9999")
    # Inventory should still be empty
    assert manager.inventory == {}
    # Verify appropriate error message is printed
    captured = capsys.readouterr().out
    assert "Error: Book with ISBN 9999 not found." in captured

def test_return_nonexistent_book(manager, capsys):
    """
    Returning a book that does not exist should not raise and leave inventory unchanged.
    """
    manager.return_book("9999")
    # Inventory should still be empty
    assert manager.inventory == {}
    # Verify appropriate error message is printed
    captured = capsys.readouterr().out
    assert "Error: We do not own a book with ISBN 9999." in captured

def test_show_inventory_empty(manager, capsys):
    """
    show_inventory should handle an empty library gracefully.
    """
    manager.show_inventory()
    captured = capsys.readouterr().out
    assert "The library is empty." in captured

def test_duplicate_book(manager, capsys):
    # First addition should succeed
    manager.add_book("Dune", "Frank Herbert", "123")
    # Second addition should trigger duplicate error
    manager.add_book("Dune", "Frank Herbert", "123")
    captured = capsys.readouterr().out
    assert "[!] Error: A book with ISBN 123 already exists." in captured
    # Inventory must contain only one entry for the ISBN
    assert list(manager.inventory.keys()) == ["123"]


def test_borrow_success(manager, capsys):
    manager.add_book("The Hobbit", "J.R.R. Tolkien", "111")
    manager.borrow_book("111")
    captured = capsys.readouterr().out
    assert "Success: You have borrowed 'The Hobbit'." in captured
    # Book should now be marked as not available
    assert not manager.inventory["111"].is_available


def test_borrow_already_borrowed(manager, capsys):
    manager.add_book("Test", "Author", "222")
    manager.borrow_book("222")   # first borrow succeeds
    manager.borrow_book("222")   # second attempt should fail
    captured = capsys.readouterr().out
    assert "Unavailable: 'Test' is currently borrowed by someone else." in captured
    # Book remains not available
    assert not manager.inventory["222"].is_available


def test_return_after_borrow(manager, capsys):
    manager.add_book("Clean Code", "Robert C. Martin", "333")
    manager.borrow_book("333")
    manager.return_book("333")
    captured = capsys.readouterr().out
    assert "Success: 'Clean Code' has been returned." in captured
    # Book should be available again
    assert manager.inventory["333"].is_available


def test_return_not_borrowed(manager, capsys):
    manager.add_book("Orphan", "Someone", "444")
    manager.return_book("444")
    captured = capsys.readouterr().out
    assert "Strange: You are trying to return 'Orphan', but it was already here." in captured
    # Book should still be available
    assert manager.inventory["444"].is_available


def test_show_inventory_nonempty(manager, capsys):
    manager.add_book("Alpha", "A", "AAA")
    manager.add_book("Beta", "B", "BBB")
    manager.show_inventory()
    captured = capsys.readouterr().out
    assert "[Available] Alpha by A (ISBN: AAA)" in captured
    assert "[Available] Beta by B (ISBN: BBB)" in captured