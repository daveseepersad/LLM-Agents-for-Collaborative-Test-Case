import pytest
from data.input_code.d04_library import Book, LibraryManager

@pytest.fixture
def manager():
    return LibraryManager()

def test_add_book_short_isbn(manager, capsys):
    manager.add_book("Short ISBN", "Author A", "12")
    captured = capsys.readouterr()
    assert "[!] Error: ISBN '12' is too short." in captured.out
    assert "12" not in manager.inventory

def test_add_book_duplicate(manager, capsys):
    isbn = "12345"
    manager.add_book("First Book", "Author A", isbn)
    captured1 = capsys.readouterr()
    assert f"Success: Added 'First Book' to the library." in captured1.out
    manager.add_book("Duplicate Book", "Author B", isbn)
    captured2 = capsys.readouterr()
    assert f"[!] Error: A book with ISBN {isbn} already exists." in captured2.out
    # Ensure original book remains unchanged
    assert manager.inventory[isbn].title == "First Book"

def test_add_book_success(manager, capsys):
    isbn = "ABC"
    manager.add_book("New Book", "Author X", isbn)
    captured = capsys.readouterr()
    assert f"Success: Added 'New Book' to the library." in captured.out
    assert isbn in manager.inventory
    book = manager.inventory[isbn]
    assert isinstance(book, Book)
    assert book.title == "New Book"
    assert book.is_available is True

def test_borrow_book_not_exist(manager, capsys):
    manager.borrow_book("NONEXIST")
    captured = capsys.readouterr()
    assert "[!] Error: Book with ISBN NONEXIST not found." in captured.out

def test_borrow_book_unavailable(manager, capsys):
    isbn = "XYZ"
    manager.add_book("Borrowed Book", "Author Y", isbn)
    capsys.readouterr()  # clear
    manager.borrow_book(isbn)  # first borrow succeeds
    captured1 = capsys.readouterr()
    assert "Success: You have borrowed 'Borrowed Book'." in captured1.out
    manager.borrow_book(isbn)  # second attempt should fail
    captured2 = capsys.readouterr()
    assert "[!] Unavailable: 'Borrowed Book' is currently borrowed by someone else." in captured2.out
    assert manager.inventory[isbn].is_available is False

def test_borrow_book_success(manager, capsys):
    isbn = "LMN"
    manager.add_book("Available Book", "Author Z", isbn)
    capsys.readouterr()
    manager.borrow_book(isbn)
    captured = capsys.readouterr()
    assert "Success: You have borrowed 'Available Book'." in captured.out
    assert manager.inventory[isbn].is_available is False

def test_return_book_not_exist(manager, capsys):
    manager.return_book("UNKNOWN")
    captured = capsys.readouterr()
    assert "[!] Error: We do not own a book with ISBN UNKNOWN." in captured.out

def test_return_book_already_available(manager, capsys):
    isbn = "RET1"
    manager.add_book("Never Borrowed", "Author Q", isbn)
    capsys.readouterr()
    manager.return_book(isbn)
    captured = capsys.readouterr()
    assert "[!] Strange: You are trying to return 'Never Borrowed', but it was already here." in captured.out
    assert manager.inventory[isbn].is_available is True

def test_return_book_success(manager, capsys):
    isbn = "RET2"
    manager.add_book("To Return", "Author R", isbn)
    capsys.readouterr()
    manager.borrow_book(isbn)
    capsys.readouterr()
    manager.return_book(isbn)
    captured = capsys.readouterr()
    assert "Success: 'To Return' has been returned." in captured.out
    assert manager.inventory[isbn].is_available is True

def test_book_str_representation(manager):
    isbn = "STR1"
    manager.add_book("Title", "Writer", isbn)
    book = manager.inventory[isbn]
    # Initially available
    assert str(book) == f"[Available] Title by Writer (ISBN: {isbn})"
    # Borrow and test again
    manager.borrow_book(isbn)
    assert str(book) == f"[Borrowed] Title by Writer (ISBN: {isbn})"

def test_show_inventory_empty(manager, capsys):
    manager.show_inventory()
    captured = capsys.readouterr()
    assert "The library is empty." in captured.out
    assert "--- Current Library Inventory ---" in captured.out

def test_show_inventory_non_empty(manager, capsys):
    isbn = "INV1"
    manager.add_book("Inv Book", "Inv Author", isbn)
    capsys.readouterr()
    manager.show_inventory()
    captured = capsys.readouterr()
    assert "[Available] Inv Book by Inv Author (ISBN: INV1)" in captured.out
    assert "--- Current Library Inventory ---" in captured.out
    assert "---------------------------------" in captured.out