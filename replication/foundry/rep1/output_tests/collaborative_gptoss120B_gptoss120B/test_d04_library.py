import pytest
from data.input_code.d04_library import *

@pytest.fixture
def manager():
    """Provide a fresh LibraryManager for each test."""
    return LibraryManager()

def test_add_book_short_isbn(manager, capsys):
    manager.add_book(title="Short ISBN", author="Author A", isbn="12")
    captured = capsys.readouterr().out.strip().splitlines()
    assert captured == ["[!] Error: ISBN '12' is too short."]

@pytest.mark.parametrize(
    "title,author,isbn,expected",
    [
        ("Valid Book", "Author C", "XYZ789",
         ["Success: Added 'Valid Book' to the library."]),
    ]
)
def test_add_book_success(manager, title, author, isbn, expected, capsys):
    manager.add_book(title=title, author=author, isbn=isbn)
    captured = capsys.readouterr().out.strip().splitlines()
    assert captured == expected

def test_add_book_duplicate(manager, capsys):
    # First addition (should succeed)
    manager.add_book(title="First Book", author="Author B", isbn="ABC123")
    # Duplicate addition (should error)
    manager.add_book(title="First Book", author="Author B", isbn="ABC123")
    captured = capsys.readouterr().out.strip().splitlines()
    assert captured == [
        "Success: Added 'First Book' to the library.",
        "[!] Error: A book with ISBN ABC123 already exists."
    ]

def test_borrow_not_found(manager, capsys):
    manager.borrow_book(isbn="NONEXIST")
    captured = capsys.readouterr().out.strip().splitlines()
    assert captured == ["[!] Error: Book with ISBN NONEXIST not found."]

def test_borrow_unavailable(manager, capsys):
    # Add a book and borrow it once
    manager.add_book(title="Already Borrowed", author="Author X", isbn="BORROWED1")
    manager.borrow_book(isbn="BORROWED1")
    # Attempt to borrow again
    manager.borrow_book(isbn="BORROWED1")
    captured = capsys.readouterr().out.strip().splitlines()
    assert captured == [
        "Success: Added 'Already Borrowed' to the library.",
        "Success: You have borrowed 'Already Borrowed'.",
        "[!] Unavailable: 'Already Borrowed' is currently borrowed by someone else."
    ]

def test_borrow_success(manager, capsys):
    manager.add_book(title="Available Book", author="Author Y", isbn="AVAIL123")
    manager.borrow_book(isbn="AVAIL123")
    captured = capsys.readouterr().out.strip().splitlines()
    assert captured == [
        "Success: Added 'Available Book' to the library.",
        "Success: You have borrowed 'Available Book'."
    ]

def test_return_not_found(manager, capsys):
    manager.return_book(isbn="MISSING")
    captured = capsys.readouterr().out.strip().splitlines()
    assert captured == ["[!] Error: We do not own a book with ISBN MISSING."]

def test_return_already_available(manager, capsys):
    manager.add_book(title="Free Book", author="Author Z", isbn="FREE001")
    manager.return_book(isbn="FREE001")
    captured = capsys.readouterr().out.strip().splitlines()
    assert captured == [
        "Success: Added 'Free Book' to the library.",
        "[!] Strange: You are trying to return 'Free Book', but it was already here."
    ]

def test_return_success(manager, capsys):
    manager.add_book(title="To Return", author="Author W", isbn="BORROWED2")
    manager.borrow_book(isbn="BORROWED2")
    manager.return_book(isbn="BORROWED2")
    captured = capsys.readouterr().out.strip().splitlines()
    assert captured == [
        "Success: Added 'To Return' to the library.",
        "Success: You have borrowed 'To Return'.",
        "Success: 'To Return' has been returned."
    ]

def test_show_inventory_empty(manager, capsys):
    manager.show_inventory()
    captured = capsys.readouterr().out.strip().splitlines()
    assert captured == [
        "--- Current Library Inventory ---",
        "The library is empty.",
        "---------------------------------"
    ]

def test_show_inventory_nonempty(manager, capsys):
    manager.add_book(title="Sample Book", author="Sample Author", isbn="SAMPLE123")
    # Clear output from add_book before capturing inventory display
    capsys.readouterr()
    manager.show_inventory()
    captured = capsys.readouterr().out.strip().splitlines()
    assert captured == [
        "--- Current Library Inventory ---",
        "[Available] Sample Book by Sample Author (ISBN: SAMPLE123)",
        "---------------------------------"
    ]

def test_book_str_available():
    book = Book(title="Open Book", author="Writer X", isbn="OPEN001")
    assert str(book) == "[Available] Open Book by Writer X (ISBN: OPEN001)"

def test_book_str_borrowed():
    book = Book(title="Closed Book", author="Writer Y", isbn="CLOSED002")
    book.is_available = False
    assert str(book) == "[Borrowed] Closed Book by Writer Y (ISBN: CLOSED002)"