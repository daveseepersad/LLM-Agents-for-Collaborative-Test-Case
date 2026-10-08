import pytest
from data.input_code.d04_library import *

# ---------- Book tests ----------
def test_book_initialization():
    book = Book(title="Test", author="Author", isbn="123")
    assert book.title == "Test"
    assert book.author == "Author"
    assert book.isbn == "123"
    assert book.is_available is True

@pytest.mark.parametrize(
    "available, expected_str",
    [
        (True, "[Available] Test by Author (ISBN: 123)"),
        (False, "[Borrowed] Test by Author (ISBN: 123)"),
    ],
)
def test_book_str_representation(available, expected_str):
    book = Book(title="Test", author="Author", isbn="123")
    book.is_available = available
    assert str(book) == expected_str

# ---------- LibraryManager add_book ----------
def test_add_book_success(capsys):
    lib = LibraryManager()
    lib.add_book(title="Test Book", author="Test Author", isbn="123")
    captured = capsys.readouterr()
    assert "Success: Added 'Test Book' to the library." in captured.out
    assert "123" in lib.inventory
    book = lib.inventory["123"]
    assert book.title == "Test Book"
    assert book.author == "Test Author"
    assert book.is_available is True

def test_add_book_short_isbn(capsys):
    lib = LibraryManager()
    lib.add_book(title="Test Book", author="Test Author", isbn="12")
    captured = capsys.readouterr()
    assert "[!] Error: ISBN '12' is too short." in captured.out
    assert "12" not in lib.inventory

def test_add_book_duplicate_isbn(capsys):
    lib = LibraryManager()
    lib.add_book(title="First", author="A", isbn="123")
    lib.add_book(title="Second", author="B", isbn="123")
    captured = capsys.readouterr()
    # First call prints success, second prints duplicate error
    assert "Success: Added 'First' to the library." in captured.out
    assert "[!] Error: A book with ISBN 123 already exists." in captured.out
    # Inventory should still contain only the first book
    assert len(lib.inventory) == 1
    assert lib.inventory["123"].title == "First"

# ---------- LibraryManager borrow_book ----------
def test_borrow_book_success(capsys):
    lib = LibraryManager()
    lib.add_book(title="BorrowMe", author="A", isbn="123")
    lib.borrow_book(isbn="123")
    captured = capsys.readouterr()
    assert "Success: You have borrowed 'BorrowMe'." in captured.out
    assert lib.inventory["123"].is_available is False

def test_borrow_book_nonexistent(capsys):
    lib = LibraryManager()
    lib.borrow_book(isbn="999")
    captured = capsys.readouterr()
    assert "[!] Error: Book with ISBN 999 not found." in captured.out

def test_borrow_book_unavailable(capsys):
    lib = LibraryManager()
    lib.add_book(title="BorrowMe", author="A", isbn="123")
    lib.borrow_book(isbn="123")  # first borrow, makes it unavailable
    lib.borrow_book(isbn="123")  # second attempt
    captured = capsys.readouterr()
    # The second call should print the unavailable message
    assert "[!] Unavailable: 'BorrowMe' is currently borrowed by someone else." in captured.out
    # Status remains False
    assert lib.inventory["123"].is_available is False

# ---------- LibraryManager return_book ----------
def test_return_book_nonexistent(capsys):
    lib = LibraryManager()
    lib.return_book(isbn="999")
    captured = capsys.readouterr()
    assert "[!] Error: We do not own a book with ISBN 999." in captured.out

def test_return_book_success(capsys):
    lib = LibraryManager()
    lib.add_book(title="ReturnMe", author="A", isbn="123")
    lib.borrow_book(isbn="123")
    lib.return_book(isbn="123")
    captured = capsys.readouterr()
    assert "Success: 'ReturnMe' has been returned." in captured.out
    assert lib.inventory["123"].is_available is True

def test_return_book_already_available(capsys):
    lib = LibraryManager()
    lib.add_book(title="ReturnMe", author="A", isbn="123")
    lib.return_book(isbn="123")
    captured = capsys.readouterr()
    assert "[!] Strange: You are trying to return 'ReturnMe', but it was already here." in captured.out
    assert lib.inventory["123"].is_available is True

# ---------- LibraryManager show_inventory ----------
def test_show_inventory_empty(capsys):
    lib = LibraryManager()
    lib.show_inventory()
    captured = capsys.readouterr()
    assert "The library is empty." in captured.out

def test_show_inventory_nonempty(capsys):
    lib = LibraryManager()
    lib.add_book(title="Visible", author="A", isbn="123")
    lib.show_inventory()
    captured = capsys.readouterr()
    # Should contain the header and the book string representation
    assert "--- Current Library Inventory ---" in captured.out
    assert "[Available] Visible by A (ISBN: 123)" in captured.out