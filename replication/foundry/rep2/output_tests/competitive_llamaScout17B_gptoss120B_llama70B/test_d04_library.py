import pytest
from data.input_code.d04_library import *

@pytest.mark.parametrize('title, author, isbn, expected', [
    ('Book1', 'Author1', '1234567890', {'1234567890': {'title': 'Book1', 'author': 'Author1', 'isbn': '1234567890', 'is_available': True}}),
])
def test_add_book_success(title, author, isbn, expected):
    library = LibraryManager()
    library.add_book(title, author, isbn)
    assert len(library.inventory) == 1
    assert library.inventory[isbn].title == expected[isbn]['title']
    assert library.inventory[isbn].author == expected[isbn]['author']
    assert library.inventory[isbn].isbn == expected[isbn]['isbn']
    assert library.inventory[isbn].is_available == expected[isbn]['is_available']

def test_add_book_duplicate():
    library = LibraryManager()
    library.add_book('Book1', 'Author1', '1234567890')
    library.add_book('Book1', 'Author1', '1234567890')
    assert len(library.inventory) == 1

def test_add_book_short_isbn():
    library = LibraryManager()
    library.add_book('Book1', 'Author1', '12')
    assert len(library.inventory) == 0

@pytest.mark.parametrize('isbn, expected', [
    ('1234567890', {'title': 'Book1', 'author': 'Author1', 'isbn': '1234567890', 'is_available': False}),
])
def test_borrow_book_success(isbn, expected):
    library = LibraryManager()
    library.add_book('Book1', 'Author1', isbn)
    library.borrow_book(isbn)
    assert len(library.inventory) == 1
    assert library.inventory[isbn].title == expected['title']
    assert library.inventory[isbn].author == expected['author']
    assert library.inventory[isbn].isbn == expected['isbn']
    assert library.inventory[isbn].is_available == expected['is_available']

def test_borrow_book_not_found():
    library = LibraryManager()
    library.borrow_book('9999999999')
    assert len(library.inventory) == 0

def test_borrow_book_already_borrowed():
    library = LibraryManager()
    library.add_book('Book1', 'Author1', '1234567890')
    library.borrow_book('1234567890')
    library.borrow_book('1234567890')
    assert len(library.inventory) == 1

@pytest.mark.parametrize('isbn, expected', [
    ('1234567890', {'title': 'Book1', 'author': 'Author1', 'isbn': '1234567890', 'is_available': True}),
])
def test_return_book_success(isbn, expected):
    library = LibraryManager()
    library.add_book('Book1', 'Author1', isbn)
    library.borrow_book(isbn)
    library.return_book(isbn)
    assert len(library.inventory) == 1
    assert library.inventory[isbn].title == expected['title']
    assert library.inventory[isbn].author == expected['author']
    assert library.inventory[isbn].isbn == expected['isbn']
    assert library.inventory[isbn].is_available == expected['is_available']

def test_return_book_not_found():
    library = LibraryManager()
    library.return_book('9999999999')
    assert len(library.inventory) == 0

def test_return_book_already_returned():
    library = LibraryManager()
    library.add_book('Book1', 'Author1', '1234567890')
    library.return_book('1234567890')
    assert len(library.inventory) == 1

def test_show_inventory_empty(capsys):
    library = LibraryManager()
    library.show_inventory()
    captured = capsys.readouterr()
    assert captured.out == "\n--- Current Library Inventory ---\nThe library is empty.\n---------------------------------\n\n"

def test_show_inventory_not_empty(capsys):
    library = LibraryManager()
    library.add_book('Book1', 'Author1', '1234567890')
    library.show_inventory()
    captured = capsys.readouterr()
    # Header should be present somewhere in the output
    assert "\n--- Current Library Inventory ---\n" in captured.out
    # The added book should be listed as available
    assert "[Available] Book1 by Author1 (ISBN: 1234567890)" in captured.out
    # Output should end with the separator line followed by two newlines
    assert captured.out.endswith("---------------------------------\n\n")