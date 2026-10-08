import pytest
from data.input_code.d04_library import *

def test_TC01_add_book_short_isbn(capsys):
    manager = LibraryManager()
    manager.add_book(title="Short ISBN", author="A", isbn="12")
    out = capsys.readouterr().out
    assert "[!] Error: ISBN '12' is too short." in out
    assert manager.inventory == {}

def test_TC02_add_book_valid(capsys):
    manager = LibraryManager()
    manager.add_book(title="Valid Book", author="B", isbn="123")
    out = capsys.readouterr().out
    assert "Success: Added 'Valid Book' to the library." in out
    assert "123" in manager.inventory
    assert manager.inventory["123"].title == "Valid Book"
    assert manager.inventory["123"].is_available

def test_TC03_add_book_duplicate(capsys):
    manager = LibraryManager()
    manager.add_book(title="First", author="A", isbn="123")
    cap = capsys.readouterr().out  # clear previous output
    manager.add_book(title="Second", author="B", isbn="123")
    out = capsys.readouterr().out
    assert "[!] Error: A book with ISBN 123 already exists." in out
    assert len(manager.inventory) == 1
    assert "123" in manager.inventory

def test_TC04_borrow_non_existent(capsys):
    manager = LibraryManager()
    manager.borrow_book(isbn="999")
    out = capsys.readouterr().out
    assert "[!] Error: Book with ISBN 999 not found." in out
    assert manager.inventory == {}

def test_TC05_borrow_success(capsys):
    manager = LibraryManager()
    manager.add_book(title="Valid Book", author="B", isbn="123")
    capsys.readouterr()  # clear
    manager.borrow_book(isbn="123")
    out = capsys.readouterr().out
    assert "Success: You have borrowed 'Valid Book'." in out
    assert not manager.inventory["123"].is_available

def test_TC06_borrow_already_borrowed(capsys):
    manager = LibraryManager()
    manager.add_book(title="Valid Book", author="B", isbn="123")
    capsys.readouterr()
    manager.borrow_book(isbn="123")
    capsys.readouterr()
    manager.borrow_book(isbn="123")
    out = capsys.readouterr().out
    assert "[!] Unavailable: 'Valid Book' is currently borrowed by someone else." in out
    assert manager.inventory["123"].is_available is False

def test_TC07_return_non_existent(capsys):
    manager = LibraryManager()
    manager.return_book(isbn="999")
    out = capsys.readouterr().out
    assert "[!] Error: We do not own a book with ISBN 999." in out
    assert manager.inventory == {}

def test_TC08_return_borrowed(capsys):
    manager = LibraryManager()
    manager.add_book(title="Valid Book", author="B", isbn="123")
    capsys.readouterr()
    manager.borrow_book(isbn="123")
    capsys.readouterr()
    manager.return_book(isbn="123")
    out = capsys.readouterr().out
    assert "Success: 'Valid Book' has been returned." in out
    assert manager.inventory["123"].is_available

def test_TC09_return_already_available(capsys):
    manager = LibraryManager()
    manager.add_book(title="Valid Book", author="B", isbn="123")
    capsys.readouterr()
    manager.return_book(isbn="123")
    out = capsys.readouterr().out
    assert "[!] Strange: You are trying to return 'Valid Book', but it was already here." in out
    assert manager.inventory["123"].is_available

def test_TC10_show_inventory_empty(capsys):
    manager = LibraryManager()
    manager.show_inventory()
    out = capsys.readouterr().out
    assert "The library is empty." in out

def test_TC11_show_inventory_available(capsys):
    manager = LibraryManager()
    manager.add_book(title="Valid Book", author="B", isbn="123")
    capsys.readouterr()
    manager.show_inventory()
    out = capsys.readouterr().out
    assert "[Available] Valid Book by B (ISBN: 123)" in out

def test_TC12_show_inventory_borrowed(capsys):
    manager = LibraryManager()
    manager.add_book(title="Valid Book", author="B", isbn="123")
    capsys.readouterr()
    manager.borrow_book(isbn="123")
    capsys.readouterr()
    manager.show_inventory()
    out = capsys.readouterr().out
    assert "[Borrowed] Valid Book by B (ISBN: 123)" in out