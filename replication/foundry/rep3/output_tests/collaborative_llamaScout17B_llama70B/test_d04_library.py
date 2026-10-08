import pytest
from data.input_code.d04_library import *


def test_add_book_duplicate(capsys):
    library = LibraryManager()
    library.add_book('Test Book', 'Test Author', '123')
    library.add_book('Test Book', 'Test Author', '123')
    captured = capsys.readouterr()
    assert "[!] Error: A book with ISBN 123 already exists." in captured.out


def test_borrow_book_twice(capsys):
    library = LibraryManager()
    library.add_book('Test Book', 'Test Author', '123')
    library.borrow_book('123')
    library.borrow_book('123')
    captured = capsys.readouterr()
    assert "[!] Unavailable: '{}' is currently borrowed by someone else.".format(library.inventory['123'].title) in captured.out


def test_return_book_twice(capsys):
    library = LibraryManager()
    library.add_book('Test Book', 'Test Author', '123')
    library.borrow_book('123')
    library.return_book('123')
    library.return_book('123')
    captured = capsys.readouterr()
    assert "[!] Strange: You are trying to return '{}', but it was already here.".format(library.inventory['123'].title) in captured.out

def test_show_inventory(capsys):
    library = LibraryManager()
    library.show_inventory()
    captured = capsys.readouterr()
    assert "The library is empty." in captured.out

def test_show_inventory_non_empty(capsys):
    library = LibraryManager()
    library.add_book('Test Book', 'Test Author', '123')
    library.show_inventory()
    captured = capsys.readouterr()
    assert "[Available] Test Book by Test Author (ISBN: 123)" in captured.out

def test_book_init():
    book = Book('Test', 'Author', '123')
    assert book.title == 'Test'
    assert book.author == 'Author'
    assert book.isbn == '123'
    assert book.is_available

def test_book_str_available():
    book = Book('Test', 'Author', '123')
    assert str(book) == "[Available] Test by Author (ISBN: 123)"

def test_book_str_borrowed():
    book = Book('Test', 'Author', '123')
    book.is_available = False
    assert str(book) == "[Borrowed] Test by Author (ISBN: 123)"