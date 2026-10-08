import pytest
from data.input_code.d04_library import *

def test_T1_SHORT_ISBN(capsys):
    lib = LibraryManager()
    lib.add_book(title="Tiny", author="A", isbn="12")
    captured = capsys.readouterr()
    assert "[!] Error: ISBN '12' is too short." in captured.out
    assert lib.inventory == {}

@pytest.mark.parametrize(
    "title, author, isbn, expected_msg",
    [
        ("Python 101", "Guido", "12345", "Success: Added 'Python 101' to the library."),
    ],
)
def test_T2_SUCCESS_ADD(capsys, title, author, isbn, expected_msg):
    lib = LibraryManager()
    lib.add_book(title=title, author=author, isbn=isbn)
    captured = capsys.readouterr()
    assert expected_msg in captured.out
    assert isbn in lib.inventory
    assert lib.inventory[isbn].is_available is True

def test_T3_DUPLICATE_ISBN(capsys):
    lib = LibraryManager()
    lib.add_book(title="Python 101", author="Guido", isbn="12345")
    lib.add_book(title="Duplicate", author="Someone", isbn="12345")
    captured = capsys.readouterr()
    assert "[!] Error: A book with ISBN 12345 already exists." in captured.out
    # inventory should still contain only the first book
    assert list(lib.inventory.keys()) == ["12345"]
    assert lib.inventory["12345"].title == "Python 101"

def test_T4_BORROW_NONEXISTENT(capsys):
    lib = LibraryManager()
    lib.borrow_book(isbn="99999")
    captured = capsys.readouterr()
    assert "[!] Error: Book with ISBN 99999 not found." in captured.out

def test_T5_BORROW_SUCCESS(capsys):
    lib = LibraryManager()
    lib.add_book(title="Python 101", author="Guido", isbn="12345")
    lib.borrow_book(isbn="12345")
    captured = capsys.readouterr()
    assert "Success: You have borrowed 'Python 101'." in captured.out
    assert lib.inventory["12345"].is_available is False

def test_T6_BORROW_ALREADY_BORROWED(capsys):
    lib = LibraryManager()
    lib.add_book(title="Python 101", author="Guido", isbn="12345")
    # first borrow to make it unavailable
    lib.borrow_book(isbn="12345")
    # second attempt
    lib.borrow_book(isbn="12345")
    captured = capsys.readouterr()
    assert "[!] Unavailable: 'Python 101' is currently borrowed by someone else." in captured.out
    assert lib.inventory["12345"].is_available is False

def test_T7_RETURN_NONEXISTENT(capsys):
    lib = LibraryManager()
    lib.return_book(isbn="88888")
    captured = capsys.readouterr()
    assert "[!] Error: We do not own a book with ISBN 88888." in captured.out

def test_T8_RETURN_ALREADY_AVAILABLE(capsys):
    lib = LibraryManager()
    lib.add_book(title="Python 101", author="Guido", isbn="12345")
    # Ensure the book is marked as available
    lib.inventory["12345"].is_available = True
    lib.return_book(isbn="12345")
    captured = capsys.readouterr()
    assert "[!] Strange: You are trying to return 'Python 101', but it was already here." in captured.out
    assert lib.inventory["12345"].is_available is True

def test_T9_RETURN_SUCCESS(capsys):
    lib = LibraryManager()
    lib.add_book(title="Python 101", author="Guido", isbn="12345")
    lib.borrow_book(isbn="12345")   # make it borrowed
    lib.return_book(isbn="12345")   # now return
    captured = capsys.readouterr()
    assert "Success: 'Python 101' has been returned." in captured.out
    assert lib.inventory["12345"].is_available is True

def test_T10_STR_REPRESENTATION():
    book = Book(title="Meta", author="Author", isbn="ABC")
    assert str(book) == "[Available] Meta by Author (ISBN: ABC)"

def test_T11_STR_BORROWED():
    book = Book(title="Meta", author="Author", isbn="ABC")
    book.is_available = False
    assert str(book) == "[Borrowed] Meta by Author (ISBN: ABC)"

def test_T12_SHOW_EMPTY_INVENTORY(capsys):
    lib = LibraryManager()
    lib.show_inventory()
    captured = capsys.readouterr()
    assert "The library is empty." in captured.out


def test_T13_SHOW_INVENTORY_WITH_BOOK(capsys):
    lib = LibraryManager()
    lib.add_book(title="Test Book", author="Author", isbn="123")
    lib.show_inventory()
    captured = capsys.readouterr()
    assert "[Available] Test Book by Author (ISBN: 123)" in captured.out