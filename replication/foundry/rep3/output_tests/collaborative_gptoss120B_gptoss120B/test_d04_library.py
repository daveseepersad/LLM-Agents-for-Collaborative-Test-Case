import pytest
from data.input_code.d04_library import *

@pytest.fixture
def manager():
    return LibraryManager()

def test_add_book_isbn_too_short(manager, capsys):
    manager.add_book(title="Short ISBN", author="A", isbn="12")
    captured = capsys.readouterr().out
    assert captured == "[!] Error: ISBN '12' is too short.\n"

def test_add_book_success(manager, capsys):
    manager.add_book(title="Python 101", author="Guido", isbn="12345")
    captured = capsys.readouterr().out
    assert captured == "Success: Added 'Python 101' to the library.\n"

def test_add_book_duplicate(manager, capsys):
    manager.add_book(title="Python 101", author="Guido", isbn="12345")
    capsys.readouterr()
    manager.add_book(title="Duplicate Book", author="Someone", isbn="12345")
    captured = capsys.readouterr().out
    assert captured == "[!] Error: A book with ISBN 12345 already exists.\n"

def test_borrow_book_nonexistent(manager, capsys):
    manager.borrow_book(isbn="99999")
    captured = capsys.readouterr().out
    assert captured == "[!] Error: Book with ISBN 99999 not found.\n"

def test_borrow_book_success(manager, capsys):
    manager.add_book(title="Python 101", author="Guido", isbn="12345")
    capsys.readouterr()
    manager.borrow_book(isbn="12345")
    captured = capsys.readouterr().out
    assert captured == "Success: You have borrowed 'Python 101'.\n"

def test_borrow_book_already_borrowed(manager, capsys):
    manager.add_book(title="Python 101", author="Guido", isbn="12345")
    capsys.readouterr()
    manager.borrow_book(isbn="12345")
    capsys.readouterr()
    manager.borrow_book(isbn="12345")
    captured = capsys.readouterr().out
    assert captured == "[!] Unavailable: 'Python 101' is currently borrowed by someone else.\n"

def test_return_book_nonexistent(manager, capsys):
    manager.return_book(isbn="88888")
    captured = capsys.readouterr().out
    assert captured == "[!] Error: We do not own a book with ISBN 88888.\n"

def test_return_book_success(manager, capsys):
    manager.add_book(title="Python 101", author="Guido", isbn="12345")
    capsys.readouterr()
    manager.borrow_book(isbn="12345")
    capsys.readouterr()
    manager.return_book(isbn="12345")
    captured = capsys.readouterr().out
    assert captured == "Success: 'Python 101' has been returned.\n"

def test_return_book_already_available(manager, capsys):
    manager.add_book(title="Python 101", author="Guido", isbn="12345")
    capsys.readouterr()
    manager.borrow_book(isbn="12345")
    capsys.readouterr()
    manager.return_book(isbn="12345")
    capsys.readouterr()
    manager.return_book(isbn="12345")
    captured = capsys.readouterr().out
    assert captured == "[!] Strange: You are trying to return 'Python 101', but it was already here.\n"

def test_book_str_available():
    book = Book(title="Free Book", author="Author", isbn="111")
    assert str(book) == "[Available] Free Book by Author (ISBN: 111)"

def test_book_str_borrowed():
    book = Book(title="Taken Book", author="Writer", isbn="222")
    book.is_available = False
    assert str(book) == "[Borrowed] Taken Book by Writer (ISBN: 222)"

def test_show_inventory_empty(manager, capsys):
    manager.show_inventory()
    captured = capsys.readouterr().out
    expected = (
        "\n--- Current Library Inventory ---\n"
        "The library is empty.\n"
        "---------------------------------\n\n"
    )
    assert captured == expected

def test_show_inventory_nonempty(manager, capsys):
    manager.add_book(title="Python 101", author="Guido", isbn="12345")
    capsys.readouterr()
    manager.show_inventory()
    captured = capsys.readouterr().out
    expected = (
        "\n--- Current Library Inventory ---\n"
        "[Available] Python 101 by Guido (ISBN: 12345)\n"
        "---------------------------------\n\n"
    )
    assert captured == expected