import pytest
from data.input_code.d04_library import *

# ------------------------------------------------------------------
# add_book tests
# ------------------------------------------------------------------
def test_add_book_short_isbn():
    manager = LibraryManager()
    manager.add_book(title="Book1", author="Author1", isbn="12")
    assert len(manager.inventory) == 0

def test_add_book_duplicate_isbn():
    manager = LibraryManager()
    manager.add_book(title="Book1", author="Author1", isbn="123")
    manager.add_book(title="Book2", author="Author2", isbn="123")
    assert len(manager.inventory) == 1
    book = manager.inventory["123"]
    assert book.title == "Book1"
    assert book.author == "Author1"
    assert book.isbn == "123"
    assert book.is_available is True

def test_add_book_normal():
    manager = LibraryManager()
    manager.add_book(title="Book1", author="Author1", isbn="123")
    assert len(manager.inventory) == 1
    book = manager.inventory["123"]
    assert book.is_available is True
    assert book.title == "Book1"
    assert book.author == "Author1"
    assert book.isbn == "123"

# ------------------------------------------------------------------
# borrow_book tests
# ------------------------------------------------------------------
def test_borrow_book_nonexistent_isbn():
    manager = LibraryManager()
    manager.borrow_book(isbn="999")
    assert len(manager.inventory) == 0

def test_borrow_book_normal():
    manager = LibraryManager()
    manager.add_book(title="Book1", author="Author1", isbn="123")
    manager.borrow_book(isbn="123")
    assert len(manager.inventory) == 1
    book = manager.inventory["123"]
    assert book.is_available is False

def test_borrow_book_already_borrowed():
    manager = LibraryManager()
    manager.add_book(title="Book1", author="Author1", isbn="123")
    manager.borrow_book(isbn="123")
    manager.borrow_book(isbn="123")  # second attempt
    book = manager.inventory["123"]
    assert book.is_available is False

# ------------------------------------------------------------------
# return_book tests
# ------------------------------------------------------------------
def test_return_book_nonexistent_isbn():
    manager = LibraryManager()
    manager.return_book(isbn="999")
    assert len(manager.inventory) == 0

def test_return_book_already_available():
    manager = LibraryManager()
    manager.add_book(title="Book1", author="Author1", isbn="123")
    manager.return_book(isbn="123")
    book = manager.inventory["123"]
    assert book.is_available is True

def test_return_book_normal():
    manager = LibraryManager()
    manager.add_book(title="Book1", author="Author1", isbn="123")
    manager.borrow_book(isbn="123")
    manager.return_book(isbn="123")
    book = manager.inventory["123"]
    assert book.is_available is True

# ------------------------------------------------------------------
# show_inventory tests
# ------------------------------------------------------------------
def test_show_inventory_empty():
    manager = LibraryManager()
    # Should not raise any exception
    manager.show_inventory()

def test_show_inventory_non_empty():
    manager = LibraryManager()
    manager.add_book(title="Book1", author="Author1", isbn="123")
    manager.show_inventory()

# ------------------------------------------------------------------
# Book.__str__ test
# ------------------------------------------------------------------
def test_book_str_available():
    book = Book(title="Book1", author="Author1", isbn="123")
    assert str(book) == "[Available] Book1 by Author1 (ISBN: 123)"