import pytest
from data.input_code.d04_library import *

@pytest.fixture
def manager():
    """Provides a fresh LibraryManager for each test."""
    return LibraryManager()

def test_book_initialization():
    book = Book(title="Test", author="Author", isbn="12345")
    assert book.title == "Test"
    assert book.author == "Author"
    assert book.isbn == "12345"
    assert book.is_available is True

def test_book_str_available():
    book = Book(title="Test", author="Author", isbn="12345")
    assert str(book) == "[Available] Test by Author (ISBN: 12345)"

def test_book_str_borrowed():
    book = Book(title="Test", author="Author", isbn="12345")
    book.is_available = False
    assert str(book) == "[Borrowed] Test by Author (ISBN: 12345)"

@pytest.mark.parametrize(
    "title,author,isbn,expected_msg,inventory_len",
    [
        ("Book1", "Author1", "123", "Success: Added 'Book1' to the library.", 1),   # valid add
        ("Book2", "Author2", "12", "[!]" , 0),                                   # isbn too short
        ("Book3", "Author3", "123", "[!]" , 1),                                   # duplicate isbn (inventory already has one)
    ],
)
def test_add_book(manager, title, author, isbn, expected_msg, inventory_len, capsys):
    # Pre‑populate for duplicate case
    if isbn == "123" and title != "Book1":
        manager.add_book("Existing", "Existing", "123")
    manager.add_book(title, author, isbn)
    captured = capsys.readouterr().out
    # Verify message contains expected fragment
    assert expected_msg in captured
    # Verify inventory size after operation
    assert len(manager.inventory) == inventory_len

def test_borrow_nonexistent_book(manager, capsys):
    manager.borrow_book("999")
    out = capsys.readouterr().out
    assert "[!]" in out and "not found" in out
    assert len(manager.inventory) == 0

def test_borrow_available_book(manager, capsys):
    manager.add_book("BookA", "AuthorA", "111")
    manager.borrow_book("111")
    out = capsys.readouterr().out
    assert "Success: You have borrowed 'BookA'." in out
    assert manager.inventory["111"].is_available is False

def test_borrow_already_borrowed_book(manager, capsys):
    manager.add_book("BookB", "AuthorB", "222")
    manager.borrow_book("222")          # first borrow
    manager.borrow_book("222")          # second attempt
    out = capsys.readouterr().out
    assert "[!]" in out and "currently borrowed" in out
    assert manager.inventory["222"].is_available is False

def test_return_nonexistent_book(manager, capsys):
    manager.return_book("333")
    out = capsys.readouterr().out
    assert "[!]" in out and "do not own a book" in out

def test_return_available_book(manager, capsys):
    manager.add_book("BookC", "AuthorC", "444")
    manager.return_book("444")
    out = capsys.readouterr().out
    assert "[!]" in out and "already here" in out
    assert manager.inventory["444"].is_available is True

def test_return_borrowed_book(manager, capsys):
    manager.add_book("BookD", "AuthorD", "555")
    manager.borrow_book("555")
    manager.return_book("555")
    out = capsys.readouterr().out
    assert "Success: 'BookD' has been returned." in out
    assert manager.inventory["555"].is_available is True

def test_show_inventory_empty(manager, capsys):
    manager.show_inventory()
    out = capsys.readouterr().out
    assert "The library is empty." in out

def test_show_inventory_non_empty(manager, capsys):
    manager.add_book("BookE", "AuthorE", "666")
    manager.show_inventory()
    out = capsys.readouterr().out
    assert "[Available] BookE by AuthorE (ISBN: 666)" in out