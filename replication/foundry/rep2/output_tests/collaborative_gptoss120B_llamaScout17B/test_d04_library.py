import pytest
from data.input_code.d04_library import *
from io import StringIO
import sys

@pytest.fixture
def library_manager():
    return LibraryManager()

def setup_library(library_manager, pre_inventory):
    for book_data in pre_inventory:
        library_manager.add_book(book_data['title'], book_data['author'], book_data['isbn'])
        if not book_data['is_available']:
            library_manager.borrow_book(book_data['isbn'])

@pytest.mark.parametrize('title, author, isbn, expected', [
    ('Short ISBN', 'Author', '12', "[!] Error: ISBN '12' is too short."),
    ('Valid Book', 'Author', '123', "Success: Added 'Valid Book' to the library."),
])
def test_add_book(library_manager, title, author, isbn, expected, capsys):
    library_manager.add_book(title, author, isbn)
    captured = capsys.readouterr()
    assert expected in captured.out.strip()

def test_add_book_duplicate(library_manager, capsys):
    library_manager.add_book('Existing Book', 'Author', '123',)
    library_manager.add_book('New Attempt', 'Author', '123')
    captured = capsys.readouterr()
    assert "[!] Error: A book with ISBN 123 already exists." in captured.out.strip()

@pytest.mark.parametrize('isbn, pre_inventory, expected', [
    ('999', [], "[!] Error: Book with ISBN 999 not found."),
    ('456', [{'title': 'Borrowed Book', 'author': 'Author', 'isbn': '456', 'is_available': False}], "[!] Unavailable: 'Borrowed Book' is currently borrowed by someone else."),
    ('789', [{'title': 'Available Book', 'author': 'Author', 'isbn': '789', 'is_available': True}], "Success: You have borrowed 'Available Book'."),
])
def test_borrow_book(library_manager, isbn, pre_inventory, expected, capsys):
    setup_library(library_manager, pre_inventory)
    library_manager.borrow_book(isbn)
    captured = capsys.readouterr()
    assert expected in captured.out.strip()

@pytest.mark.parametrize('isbn, pre_inventory, expected', [
    ('111', [], "[!] Error: We do not own a book with ISBN 111."),
    ('222', [{'title': 'Never Borrowed', 'author': 'Author', 'isbn': '222', 'is_available': True}], "[!] Strange: You are trying to return 'Never Borrowed', but it was already here."),
    ('333', [{'title': 'Returned Book', 'author': 'Author', 'isbn': '333', 'is_available': False}], "Success: 'Returned Book' has been returned."),
])
def test_return_book(library_manager, isbn, pre_inventory, expected, capsys):
    setup_library(library_manager, pre_inventory)
    library_manager.return_book(isbn)
    captured = capsys.readouterr()
    assert expected in captured.out.strip()

@pytest.mark.parametrize('pre_inventory, expected', [
    ([], "\n--- Current Library Inventory ---"),
    ([{'title': 'Available Book', 'author': 'Author A', 'isbn': '444', 'is_available': True}, {'title': 'Borrowed Book', 'author': 'Author B', 'isbn': '555', 'is_available': False}], "\n--- Current Library Inventory ---"),
])
def test_show_inventory(library_manager, pre_inventory, expected, capsys):
    setup_library(library_manager, pre_inventory)
    library_manager.show_inventory()
    captured = capsys.readouterr()
    assert expected in captured.out