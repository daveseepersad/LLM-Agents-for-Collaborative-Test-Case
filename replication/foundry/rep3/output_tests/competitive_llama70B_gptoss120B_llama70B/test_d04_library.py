import pytest
from data.input_code.d04_library import *

# ---------- Book Tests ----------
def test_book_init():
    b = Book(title="Test Book", author="Test Author", isbn="1234567890")
    assert b.title == "Test Book"
    assert b.author == "Test Author"
    assert b.isbn == "1234567890"
    assert b.is_available is True

def test_book_str():
    b = Book(title="Test Book", author="Test Author", isbn="1234567890")
    expected = "[Available] Test Book by Test Author (ISBN: 1234567890)"
    assert str(b) == expected

# ---------- LibraryManager Init ----------
def test_library_manager_init():
    lib = LibraryManager()
    assert isinstance(lib.inventory, dict)
    assert not lib.inventory  # should be empty

# ---------- Add Book ----------
def test_add_book_success(capsys):
    lib = LibraryManager()
    lib.add_book(title="Test Book", author="Test Author", isbn="1234567890")
    captured = capsys.readouterr().out.strip()
    assert captured == "Success: Added 'Test Book' to the library."
    assert "1234567890" in lib.inventory
    assert isinstance(lib.inventory["1234567890"], Book)

@pytest.mark.parametrize(
    "title,author,isbn,expected_output",
    [
        ("Test Book", "Test Author", "12", "[!] Error: ISBN '12' is too short."),
        ("Test Book 2", "Test Author 2", "1234567890", "[!] Error: A book with ISBN 1234567890 already exists."),
    ],
)
def test_add_book_errors(capsys, title, author, isbn, expected_output):
    lib = LibraryManager()
    # First add a valid book to set up duplicate case
    lib.add_book(title="Test Book", author="Test Author", isbn="1234567890")
    # Clear previous output
    capsys.readouterr()
    # Attempt the error case
    lib.add_book(title=title, author=author, isbn=isbn)
    captured = capsys.readouterr().out.strip()
    assert captured == expected_output

# ---------- Borrow Book ----------
def test_borrow_book_success(capsys):
    lib = LibraryManager()
    lib.add_book(title="Test Book", author="Test Author", isbn="1234567890")
    capsys.readouterr()  # discard add_book output
    lib.borrow_book(isbn="1234567890")
    captured = capsys.readouterr().out.strip()
    assert captured == "Success: You have borrowed 'Test Book'."
    assert lib.inventory["1234567890"].is_available is False

def test_borrow_book_not_found(capsys):
    lib = LibraryManager()
    lib.borrow_book(isbn="9876543210")
    captured = capsys.readouterr().out.strip()
    assert captured == "[!] Error: Book with ISBN 9876543210 not found."

def test_borrow_book_unavailable(capsys):
    lib = LibraryManager()
    lib.add_book(title="Test Book", author="Test Author", isbn="1234567890")
    capsys.readouterr()
    # First borrow succeeds
    lib.borrow_book(isbn="1234567890")
    capsys.readouterr()
    # Second borrow should fail
    lib.borrow_book(isbn="1234567890")
    captured = capsys.readouterr().out.strip()
    assert captured == "[!] Unavailable: 'Test Book' is currently borrowed by someone else."

# ---------- Return Book ----------
def test_return_book_success(capsys):
    lib = LibraryManager()
    lib.add_book(title="Test Book", author="Test Author", isbn="1234567890")
    capsys.readouterr()
    lib.borrow_book(isbn="1234567890")
    capsys.readouterr()
    lib.return_book(isbn="1234567890")
    captured = capsys.readouterr().out.strip()
    assert captured == "Success: 'Test Book' has been returned."
    assert lib.inventory["1234567890"].is_available is True

def test_return_book_not_found(capsys):
    lib = LibraryManager()
    lib.return_book(isbn="9876543210")
    captured = capsys.readouterr().out.strip()
    assert captured == "[!] Error: We do not own a book with ISBN 9876543210."

def test_return_book_already_returned(capsys):
    lib = LibraryManager()
    lib.add_book(title="Test Book", author="Test Author", isbn="1234567890")
    capsys.readouterr()
    # Return without borrowing first
    lib.return_book(isbn="1234567890")
    captured = capsys.readouterr().out.strip()
    assert captured == "[!] Strange: You are trying to return 'Test Book', but it was already here."

# ---------- Show Inventory ----------
def test_show_inventory_empty(capsys):
    lib = LibraryManager()
    lib.show_inventory()
    captured = capsys.readouterr().out
    # The output contains the empty message line
    assert "The library is empty." in captured

def test_show_inventory_non_empty(capsys):
    lib = LibraryManager()
    lib.add_book(title="Test Book", author="Test Author", isbn="1234567890")
    capsys.readouterr()
    lib.show_inventory()
    captured = capsys.readouterr().out
    expected_line = "[Available] Test Book by Test Author (ISBN: 1234567890)"
    assert expected_line in captured