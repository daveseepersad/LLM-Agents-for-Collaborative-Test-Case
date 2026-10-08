import pytest
from data.input_code.d04_library import *

@pytest.mark.parametrize('title, author, isbn, should_exist', [
    ('Short ISBN Book', 'Author', '12', False),
    ('Clean Code', 'Robert C. Martin', '9780132350884', True),
])
def test_add_book(title, author, isbn, should_exist):
    lm = LibraryManager()
    lm.add_book(title, author, isbn)
    if should_exist:
        assert isbn in lm.inventory
        book = lm.inventory[isbn]
        assert isinstance(book, Book)
        assert book.title == title
        assert book.author == author
        assert book.isbn == isbn
    else:
        assert isbn not in lm.inventory

@pytest.mark.parametrize('method', ['borrow', 'return'])
def test_borrow_return_not_found(method, capsys):
    lm = LibraryManager()
    isbn = '0000'
    if method == 'borrow':
        lm.borrow_book(isbn)
        out = capsys.readouterr().out
        assert "[!] Error: Book with ISBN 0000 not found." in out
    else:
        lm.return_book(isbn)
        out = capsys.readouterr().out
        assert "[!] Error: We do not own a book with ISBN 0000." in out

def test_show_inventory_empty(capsys):
    lm = LibraryManager()
    lm.show_inventory()
    out = capsys.readouterr().out
    assert "The library is empty." in out

import pytest
from data.input_code.d04_library import *

def test_add_book_duplicate(capsys):
    lm = LibraryManager()
    lm.add_book("First Title", "Author", "9780132350884")
    lm.add_book("Duplicate ISBN Book", "Author", "9780132350884")
    out = capsys.readouterr().out
    assert "[!] Error: A book with ISBN 9780132350884 already exists." in out

def test_borrow_and_return_success(capsys):
    isbn = "9780132350884"
    lm = LibraryManager()
    lm.add_book("Clean Code", "Robert C. Martin", isbn)
    lm.borrow_book(isbn)
    out1 = capsys.readouterr().out
    assert "Success: You have borrowed" in out1

    lm.return_book(isbn)
    out2 = capsys.readouterr().out
    assert "has been returned" in out2

def test_borrow_unavailable(capsys):
    isbn = "9780132350884"
    lm = LibraryManager()
    lm.add_book("Clean Code", "Robert C. Martin", isbn)
    lm.borrow_book(isbn)
    _ = capsys.readouterr()  # clear

    lm.borrow_book(isbn)
    out = capsys.readouterr().out
    assert "Unavailable" in out

def test_return_strange(capsys):
    isbn = "9780132350884"
    lm = LibraryManager()
    lm.add_book("Clean Code", "Robert C. Martin", isbn)
    lm.return_book(isbn)
    out = capsys.readouterr().out
    assert "Strange: You are trying to return" in out

def test_show_inventory_non_empty(capsys):
    isbn = "9780132350884"
    lm = LibraryManager()
    lm.add_book("Clean Code", "Robert C. Martin", isbn)
    lm.show_inventory()
    out = capsys.readouterr().out
    assert "Current Library Inventory" in out