import pytest
from data.input_code.d04_library import *


# TC01-03: Add book variations
@pytest.mark.parametrize("title, author, isbn, expected, preadd", [
    ("Short ISBN", "A", "12", "[!] Error: ISBN '12' is too short.", False),
    ("First Book", "B", "12345", "Success: Added 'First Book' to the library.", False),
    ("Duplicate Book", "C", "12345", "Success: Added 'First Book' to the library.\n[!] Error: A book with ISBN 12345 already exists.", True),
])
def test_add_book_variants(title, author, isbn, expected, preadd, capsys):
    lm = LibraryManager()
    if preadd:
        lm.add_book("First Book", "B", "12345")
    lm.add_book(title, author, isbn)
    out = capsys.readouterr().out.strip()
    assert out == expected


# TC04-09: Borrow/Return scenarios
def test_borrow_nonexistent(capsys):
    lm = LibraryManager()
    lm.borrow_book("99999")
    out = capsys.readouterr().out.strip()
    assert out == "[!] Error: Book with ISBN 99999 not found."


def test_borrow_success(capsys):
    lm = LibraryManager()
    lm.add_book("First Book", "B", "12345")
    lm.borrow_book("12345")
    out = capsys.readouterr().out.strip()
    assert out == "Success: Added 'First Book' to the library.\nSuccess: You have borrowed 'First Book'."


def test_borrow_already_borrowed(capsys):
    lm = LibraryManager()
    lm.add_book("First Book", "B", "12345")
    lm.borrow_book("12345")
    lm.borrow_book("12345")
    out = capsys.readouterr().out.strip()
    expected = "Success: Added 'First Book' to the library.\nSuccess: You have borrowed 'First Book'.\n[!] Unavailable: 'First Book' is currently borrowed by someone else."
    assert out == expected


def test_return_nonexistent(capsys):
    lm = LibraryManager()
    lm.return_book("88888")
    out = capsys.readouterr().out.strip()
    assert out == "[!] Error: We do not own a book with ISBN 88888."


def test_return_already_here(capsys):
    lm = LibraryManager()
    lm.add_book("First Book", "B", "12345")
    lm.return_book("12345")
    out = capsys.readouterr().out.strip()
    assert out == "Success: Added 'First Book' to the library.\n[!] Strange: You are trying to return 'First Book', but it was already here."


def test_return_success(capsys):
    lm = LibraryManager()
    lm.add_book("First Book", "B", "12345")
    lm.borrow_book("12345")
    lm.return_book("12345")
    out = capsys.readouterr().out.strip()
    assert out == "Success: Added 'First Book' to the library.\nSuccess: You have borrowed 'First Book'.\nSuccess: 'First Book' has been returned."


def test_show_inventory_empty(capsys):
    lm = LibraryManager()
    lm.show_inventory()
    expected = "\n--- Current Library Inventory ---\nThe library is empty.\n---------------------------------\n\n"
    out = capsys.readouterr().out
    assert out == expected


def test_show_inventory_nonempty(capsys):
    lm = LibraryManager()
    lm.add_book("First Book", "B", "12345")
    lm.show_inventory()
    expected = "Success: Added 'First Book' to the library.\n\n--- Current Library Inventory ---\n[Available] First Book by B (ISBN: 12345)\n---------------------------------\n\n"
    out = capsys.readouterr().out
    assert out == expected


def test_book_str_borrowed():
    b = Book("Hidden", "D", "777")
    b.is_available = False
    assert str(b) == "[Borrowed] Hidden by D (ISBN: 777)"