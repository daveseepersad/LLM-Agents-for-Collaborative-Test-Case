import pytest
from data.input_code.d04_library import *

@pytest.mark.parametrize('title, author, isbn, expected', [
    ("Intro", "A", "12", None),
    ("Python 101", "Guido", "123", None),
    ("Another Python", "Guido", "123", None)
])
def test_add_book(capsys, title, author, isbn, expected):
    library = LibraryManager()
    library.add_book(title, author, isbn)
    captured = capsys.readouterr()
    assert captured.out is not None

def test_add_book_valid(capsys):
    library = LibraryManager()
    library.add_book("Python 101", "Guido", "123")
    captured = capsys.readouterr()
    assert "Success: Added 'Python 101' to the library." in captured.out

def test_add_book_duplicate(capsys):
    library = LibraryManager()
    library.add_book("Python 101", "Guido", "123")
    library.add_book("Another Python", "Guido", "123")
    captured = capsys.readouterr()
    assert "[!] Error: A book with ISBN 123 already exists." in captured.out

@pytest.mark.parametrize('isbn, expected', [
    ("999", None),
    ("123", None)
])
def test_borrow_book(capsys, isbn, expected):
    library = LibraryManager()
    library.add_book("Python 101", "Guido", "123")
    library.borrow_book(isbn)
    captured = capsys.readouterr()
    assert captured.out is not None

def test_borrow_book_not_found(capsys):
    library = LibraryManager()
    library.borrow_book("999")
    captured = capsys.readouterr()
    assert "[!] Error: Book with ISBN 999 not found." in captured.out

def test_borrow_book_available(capsys):
    library = LibraryManager()
    library.add_book("Python 101", "Guido", "123")
    library.borrow_book("123")
    captured = capsys.readouterr()
    assert "Success: You have borrowed 'Python 101'." in captured.out

def test_borrow_book_already_borrowed(capsys):
    library = LibraryManager()
    library.add_book("Python 101", "Guido", "123")
    library.borrow_book("123")
    library.borrow_book("123")
    captured = capsys.readouterr()
    assert "[!] Unavailable: 'Python 101' is currently borrowed by someone else." in captured.out

@pytest.mark.parametrize('isbn, expected', [
    ("888", None),
    ("123", None)
])
def test_return_book(capsys, isbn, expected):
    library = LibraryManager()
    library.add_book("Python 101", "Guido", "123")
    library.borrow_book("123")
    library.return_book(isbn)
    captured = capsys.readouterr()
    assert captured.out is not None

def test_return_book_not_found(capsys):
    library = LibraryManager()
    library.return_book("888")
    captured = capsys.readouterr()
    assert "[!] Error: We do not own a book with ISBN 888." in captured.out

def test_return_book_existing_borrowed(capsys):
    library = LibraryManager()
    library.add_book("Python 101", "Guido", "123")
    library.borrow_book("123")
    library.return_book("123")
    captured = capsys.readouterr()
    assert "Success: 'Python 101' has been returned." in captured.out

def test_return_book_already_available(capsys):
    library = LibraryManager()
    library.add_book("Python 101", "Guido", "123")
    library.return_book("123")
    captured = capsys.readouterr()
    assert "[!] Strange: You are trying to return 'Python 101', but it was already here." in captured.out

def test_show_inventory(capsys):
    library = LibraryManager()
    library.show_inventory()
    captured = capsys.readouterr()
    assert "The library is empty." in captured.out

def test_show_inventory_with_books(capsys):
    library = LibraryManager()
    library.add_book("Python 101", "Guido", "123")
    library.show_inventory()
    captured = capsys.readouterr()
    assert "[Available] Python 101 by Guido (ISBN: 123)" in captured.out