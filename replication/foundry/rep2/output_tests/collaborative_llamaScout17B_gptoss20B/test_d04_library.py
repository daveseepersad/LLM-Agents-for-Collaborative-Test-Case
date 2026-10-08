import pytest
from data.input_code.d04_library import *

def test_library_and_book_plan():
    # T1_INIT
    lm = LibraryManager()
    assert lm.inventory == {}

    # T2_ADD_OK
    res = lm.add_book(title="Book1", author="Author1", isbn="1234567890")
    assert res is None
    assert "1234567890" in lm.inventory
    book = lm.inventory["1234567890"]
    assert isinstance(book, Book)
    assert book.title == "Book1"
    assert book.author == "Author1"
    assert book.isbn == "1234567890"
    assert book.is_available is True

    # T3_ADD_DUP
    res = lm.add_book(title="Book1", author="Author1", isbn="1234567890")
    assert res is None
    assert len(lm.inventory) == 1

    # T4_ADD_SHORT_ISBN
    res = lm.add_book(title="Book1", author="Author1", isbn="12")
    assert res is None
    assert len(lm.inventory) == 1

    # T5_BORROW_OK
    res = lm.borrow_book(isbn="1234567890")
    assert res is None
    assert lm.inventory["1234567890"].is_available is False

    # T6_BORROW_NOT_FOUND
    res = lm.borrow_book(isbn="NOT_FOUND")
    assert res is None
    assert "NOT_FOUND" not in lm.inventory

    # T7_BORROW_ALREADY_BORROWED
    res = lm.borrow_book(isbn="1234567890")
    assert res is None
    assert lm.inventory["1234567890"].is_available is False

    # T8_RETURN_OK
    res = lm.return_book(isbn="1234567890")
    assert res is None
    assert lm.inventory["1234567890"].is_available is True

    # T9_RETURN_NOT_FOUND
    res = lm.return_book(isbn="NOT_FOUND")
    assert res is None

    # T10_RETURN_ALREADY_AVAILABLE
    res = lm.return_book(isbn="1234567890")
    assert res is None
    assert lm.inventory["1234567890"].is_available is True

    # T11_SHOW_EMPTY
    lm.show_inventory()

    # T12_SHOW_WITH_BOOKS
    lm.show_inventory()

    # T13_BOOK_INIT
    b = Book(title="Test", author="Author", isbn="123")
    assert b.title == "Test"
    assert b.author == "Author"
    assert b.isbn == "123"
    assert b.is_available is True

    # T14_BOOK_STR_AVAILABLE
    assert str(b) == "[Available] Test by Author (ISBN: 123)"

    # T15_BOOK_STR_BORROWED
    b2 = Book(title="Test", author="Author", isbn="123")
    b2.is_available = False
    assert str(b2) == "[Borrowed] Test by Author (ISBN: 123)"

import pytest
from data.input_code.d04_library import *

@pytest.mark.parametrize("title,author,isbn", [
    ("Edge", "Case", "123"),
    ("", "Author", "1234567890"),
    ("Title", "", "1234567890"),
])
def test_add_book_edge_cases(title, author, isbn):
    lm = LibraryManager()
    res = lm.add_book(title=title, author=author, isbn=isbn)
    assert res is None
    assert isbn in lm.inventory
    book = lm.inventory[isbn]
    assert isinstance(book, Book)
    assert book.title == title
    assert book.author == author
    assert book.isbn == isbn
    assert book.is_available is True

import pytest
from data.input_code.d04_library import *

def test_missing_isbn_boundary():
    lm = LibraryManager()
    res = lm.add_book(title="Boundary", author="Test", isbn="123")
    assert res is None
    assert "123" in lm.inventory
    book = lm.inventory["123"]
    assert isinstance(book, Book)
    assert book.title == "Boundary"
    assert book.author == "Test"
    assert book.isbn == "123"
    assert book.is_available is True

@pytest.mark.parametrize("scenario", ["empty", "multiple"])
def test_show_inventory_scenarios(scenario):
    lm = LibraryManager()
    if scenario == "multiple":
        lm.add_book(title="BookA", author="AuthorA", isbn="111")
        lm.add_book(title="BookB", author="AuthorB", isbn="222")
    res = lm.show_inventory()
    assert res is None

def test_borrow_edge_case_corrupted():
    lm = LibraryManager()
    res = lm.borrow_book(isbn="CORRUPTED")
    assert res is None