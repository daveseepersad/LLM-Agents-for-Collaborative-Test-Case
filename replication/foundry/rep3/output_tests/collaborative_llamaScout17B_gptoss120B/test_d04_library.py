import pytest
from data.input_code.d04_library import *

def test_init_inventory():
    manager = LibraryManager()
    assert manager.inventory == {}

def test_add_book_success(capsys):
    manager = LibraryManager()
    manager.add_book(title="Book1", author="Author1", isbn="1234567890")
    captured = capsys.readouterr()
    assert "Success: Added 'Book1' to the library." in captured.out
    assert "1234567890" in manager.inventory
    assert isinstance(manager.inventory["1234567890"], Book)

def test_add_book_duplicate(capsys):
    manager = LibraryManager()
    manager.add_book(title="Book1", author="Author1", isbn="1234567890")
    manager.add_book(title="Book1", author="Author1", isbn="1234567890")
    captured = capsys.readouterr()
    assert "[!] Error: A book with ISBN 1234567890 already exists." in captured.out

def test_add_book_short_isbn(capsys):
    manager = LibraryManager()
    manager.add_book(title="Book1", author="Author1", isbn="12")
    captured = capsys.readouterr()
    assert "[!] Error: ISBN '12' is too short." in captured.out

def test_borrow_book_success(capsys):
    manager = LibraryManager()
    manager.add_book(title="Book1", author="Author1", isbn="1234567890")
    manager.borrow_book(isbn="1234567890")
    captured = capsys.readouterr()
    assert "Success: You have borrowed 'Book1'." in captured.out
    assert not manager.inventory["1234567890"].is_available

def test_borrow_book_not_found(capsys):
    manager = LibraryManager()
    manager.borrow_book(isbn="9999999999")
    captured = capsys.readouterr()
    assert "[!] Error: Book with ISBN 9999999999 not found." in captured.out

def test_borrow_book_already_borrowed(capsys):
    manager = LibraryManager()
    manager.add_book(title="Book1", author="Author1", isbn="1234567890")
    manager.borrow_book(isbn="1234567890")  # first borrow
    manager.borrow_book(isbn="1234567890")  # second attempt
    captured = capsys.readouterr()
    assert "[!] Unavailable: 'Book1' is currently borrowed by someone else." in captured.out

def test_return_book_success(capsys):
    manager = LibraryManager()
    manager.add_book(title="Book1", author="Author1", isbn="1234567890")
    manager.borrow_book(isbn="1234567890")
    manager.return_book(isbn="1234567890")
    captured = capsys.readouterr()
    assert "Success: 'Book1' has been returned." in captured.out
    assert manager.inventory["1234567890"].is_available

def test_return_book_not_found(capsys):
    manager = LibraryManager()
    manager.return_book(isbn="9999999999")
    captured = capsys.readouterr()
    assert "[!] Error: We do not own a book with ISBN 9999999999." in captured.out

def test_return_book_already_available(capsys):
    manager = LibraryManager()
    manager.add_book(title="Book1", author="Author1", isbn="1234567890")
    manager.return_book(isbn="1234567890")
    captured = capsys.readouterr()
    assert "[!] Strange: You are trying to return 'Book1', but it was already here." in captured.out

def test_show_inventory_empty(capsys):
    manager = LibraryManager()
    manager.show_inventory()
    captured = capsys.readouterr()
    assert "The library is empty." in captured.out

def test_show_inventory_not_empty(capsys):
    manager = LibraryManager()
    manager.add_book(title="Book1", author="Author1", isbn="1234567890")
    manager.show_inventory()
    captured = capsys.readouterr()
    assert "[Available] Book1 by Author1 (ISBN: 1234567890)" in captured.out