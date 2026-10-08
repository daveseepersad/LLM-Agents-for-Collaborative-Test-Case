import pytest
from data.input_code.d04_library import *


@pytest.mark.parametrize('title, author, isbn, should_exist', [
    ("1984", "George Orwell", "123", True),
    ("Hello", "A", "12", False),
    ("Sample", "B", "", False),
])
def test_add_book_cases(title, author, isbn, should_exist):
    lm = LibraryManager()
    lm.add_book(title, author, isbn)

    if should_exist:
        assert isbn in lm.inventory
        assert lm.inventory[isbn].title == title
        assert lm.inventory[isbn].author == author
        assert lm.inventory[isbn].isbn == isbn
        assert lm.inventory[isbn].is_available is True
    else:
        assert isbn not in lm.inventory


def test_add_book_none_isbn_raises():
    lm = LibraryManager()
    with pytest.raises(TypeError):
        lm.add_book("Sample", "C", None)


def test_borrow_nonexistent_inventory():
    lm = LibraryManager()
    lm.borrow_book("999999")
    assert "999999" not in lm.inventory


def test_return_nonexistent_inventory():
    lm = LibraryManager()
    lm.return_book("999999")
    assert "999999" not in lm.inventory


def test_show_inventory_empty(capsys):
    lm = LibraryManager()
    lm.show_inventory()
    captured = capsys.readouterr()
    assert "The library is empty." in captured.out

import pytest
from data.input_code.d04_library import *

@pytest.mark.parametrize('title, author, isbn, is_available, expected', [
    ("1984", "George Orwell", "123", True, "[Available] 1984 by George Orwell (ISBN: 123)"),
    ("1984", "George Orwell", "123", False, "[Borrowed] 1984 by George Orwell (ISBN: 123)"),
])
def test_book_str_variants(title, author, isbn, is_available, expected):
    b = Book(title, author, isbn)
    b.is_available = is_available
    assert str(b) == expected

import pytest
from data.input_code.d04_library import *

def test_duplicate_add_book(capsys):
    lm = LibraryManager()
    lm.add_book("Dune", "Frank Herbert", "555")
    lm.add_book("Dune", "Frank Herbert", "555")
    captured = capsys.readouterr()
    assert "A book with ISBN 555 already exists." in captured.out

def test_borrow_success(capsys):
    lm = LibraryManager()
    lm.add_book("1984", "George Orwell", "123")
    lm.borrow_book("123")
    captured = capsys.readouterr()
    assert "Success: You have borrowed '1984'." in captured.out

def test_return_not_borrowed(capsys):
    lm = LibraryManager()
    lm.add_book("1984", "George Orwell", "123")
    lm.return_book("123")
    captured = capsys.readouterr()
    assert "Strange: You are trying to return '1984', but it was already here." in captured.out

def test_show_inventory_nonempty(capsys):
    lm = LibraryManager()
    lm.add_book("1984", "George Orwell", "123")
    lm.show_inventory()
    captured = capsys.readouterr()
    assert "[Available] 1984 by George Orwell (ISBN: 123)" in captured.out

def test_borrow_already_borrowed(capsys):
    lm = LibraryManager()
    lm.add_book("1984", "George Orwell", "123")
    lm.borrow_book("123")
    lm.borrow_book("123")
    captured = capsys.readouterr()
    assert "Unavailable: '1984' is currently borrowed by someone else." in captured.out

import pytest
from data.input_code.d04_library import *

def test_return_success_from_borrowed(capsys):
    lm = LibraryManager()
    lm.add_book("Dune", "Frank Herbert", "777")
    # Simulate the book being borrowed before return
    lm.inventory["777"].is_available = False

    lm.return_book("777")
    captured = capsys.readouterr()
    assert "Success: 'Dune' has been returned." in captured.out