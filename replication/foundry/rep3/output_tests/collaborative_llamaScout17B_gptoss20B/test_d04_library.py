import pytest
from data.input_code.d04_library import *

def test_T1_init():
    lib = LibraryManager()
    assert lib.inventory == {}

def test_T2_add_ok():
    lib = LibraryManager()
    lib.add_book(title="Book1", author="Author1", isbn="1234567890")
    actual = {
        isbn: {
            "title": b.title,
            "author": b.author,
            "isbn": b.isbn,
            "is_available": b.is_available
        } for isbn, b in lib.inventory.items()
    }
    expected = {
        "1234567890": {
            "title": "Book1",
            "author": "Author1",
            "isbn": "1234567890",
            "is_available": True
        }
    }
    assert actual == expected

def test_T3_add_dup():
    lib = LibraryManager()
    lib.add_book(title="Book1", author="Author1", isbn="1234567890")
    lib.add_book(title="Book1", author="Author1", isbn="1234567890")  # duplicate
    actual = {
        isbn: {
            "title": b.title,
            "author": b.author,
            "isbn": b.isbn,
            "is_available": b.is_available
        } for isbn, b in lib.inventory.items()
    }
    expected = {
        "1234567890": {
            "title": "Book1",
            "author": "Author1",
            "isbn": "1234567890",
            "is_available": True
        }
    }
    assert actual == expected

def test_T4_add_short_isbn():
    lib = LibraryManager()
    lib.add_book(title="Book1", author="Author1", isbn="12")
    assert lib.inventory == {}

def test_T5_borrow_ok():
    lib = LibraryManager()
    lib.add_book(title="Book1", author="Author1", isbn="1234567890")
    lib.borrow_book(isbn="1234567890")
    actual = {
        isbn: {
            "title": b.title,
            "author": b.author,
            "isbn": b.isbn,
            "is_available": b.is_available
        } for isbn, b in lib.inventory.items()
    }
    expected = {
        "1234567890": {
            "title": "Book1",
            "author": "Author1",
            "isbn": "1234567890",
            "is_available": False
        }
    }
    assert actual == expected

def test_T6_borrow_not_found():
    lib = LibraryManager()
    lib.add_book(title="Book1", author="Author1", isbn="1234567890")
    lib.borrow_book(isbn="1234567890")  # borrow existing to set borrowed state
    lib.borrow_book(isbn="9999999999")  # non-existent
    actual = {
        isbn: {
            "title": b.title,
            "author": b.author,
            "isbn": b.isbn,
            "is_available": b.is_available
        } for isbn, b in lib.inventory.items()
    }
    expected = {
        "1234567890": {
            "title": "Book1",
            "author": "Author1",
            "isbn": "1234567890",
            "is_available": False
        }
    }
    assert actual == expected

def test_T7_borrow_already_borrowed():
    lib = LibraryManager()
    lib.add_book(title="Book1", author="Author1", isbn="1234567890")
    lib.borrow_book(isbn="1234567890")  # first borrow
    lib.borrow_book(isbn="1234567890")  # borrow again
    actual = {
        isbn: {
            "title": b.title,
            "author": b.author,
            "isbn": b.isbn,
            "is_available": b.is_available
        } for isbn, b in lib.inventory.items()
    }
    expected = {
        "1234567890": {
            "title": "Book1",
            "author": "Author1",
            "isbn": "1234567890",
            "is_available": False
        }
    }
    assert actual == expected

def test_T8_return_ok():
    lib = LibraryManager()
    lib.add_book(title="Book1", author="Author1", isbn="1234567890")
    lib.borrow_book(isbn="1234567890")
    lib.return_book(isbn="1234567890")
    actual = {
        isbn: {
            "title": b.title,
            "author": b.author,
            "isbn": b.isbn,
            "is_available": b.is_available
        } for isbn, b in lib.inventory.items()
    }
    expected = {
        "1234567890": {
            "title": "Book1",
            "author": "Author1",
            "isbn": "1234567890",
            "is_available": True
        }
    }
    assert actual == expected

def test_T9_return_not_found():
    lib = LibraryManager()
    lib.add_book(title="Book1", author="Author1", isbn="1234567890")
    lib.borrow_book(isbn="1234567890")
    lib.return_book(isbn="9999999999")  # non-existent
    actual = {
        isbn: {
            "title": b.title,
            "author": b.author,
            "isbn": b.isbn,
            "is_available": b.is_available
        } for isbn, b in lib.inventory.items()
    }
    expected = {
        "1234567890": {
            "title": "Book1",
            "author": "Author1",
            "isbn": "1234567890",
            "is_available": False
        }
    }
    assert actual == expected

def test_T10_return_already_returned():
    lib = LibraryManager()
    lib.add_book(title="Book1", author="Author1", isbn="1234567890")
    # Do not borrow; return should indicate it's already returned
    lib.return_book(isbn="1234567890")
    actual = {
        isbn: {
            "title": b.title,
            "author": b.author,
            "isbn": b.isbn,
            "is_available": b.is_available
        } for isbn, b in lib.inventory.items()
    }
    expected = {
        "1234567890": {
            "title": "Book1",
            "author": "Author1",
            "isbn": "1234567890",
            "is_available": True
        }
    }
    assert actual == expected

def test_T11_show_empty(capsys):
    lib = LibraryManager()
    lib.show_inventory()
    captured = capsys.readouterr()
    assert "The library is empty." in captured.out

def test_T12_show_not_empty(capsys):
    lib = LibraryManager()
    lib.add_book(title="Book1", author="Author1", isbn="1234567890")
    lib.show_inventory()
    captured = capsys.readouterr()
    assert "Current Library Inventory" in captured.out
    assert "Book1" in captured.out
    assert "ISBN: 1234567890" in captured.out