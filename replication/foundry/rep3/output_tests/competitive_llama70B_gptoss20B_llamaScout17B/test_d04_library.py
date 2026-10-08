import pytest
from data.input_code.d04_library import *

def test_book_init():
    b = Book("Test Book", "Test Author", "1234567890")
    assert b.title == "Test Book"
    assert b.author == "Test Author"
    assert b.isbn == "1234567890"
    assert b.is_available is True

def test_book_str():
    b = Book("Test Book", "Test Author", "1234567890")
    assert str(b) == "[Available] Test Book by Test Author (ISBN: 1234567890)"

def test_library_init_empty():
    lm = LibraryManager()
    assert isinstance(lm.inventory, dict)
    assert lm.inventory == {}

def test_add_book_ok(capsys):
    lm = LibraryManager()
    lm.add_book("Test Book", "Test Author", "1234567890")
    captured_out = capsys.readouterr().out
    assert "Success: Added 'Test Book' to the library." in captured_out

def test_add_book_short_isbn(capsys):
    lm = LibraryManager()
    lm.add_book("Test Book", "Test Author", "12")
    captured_out = capsys.readouterr().out
    assert "[!] Error: ISBN '12' is too short." in captured_out

def test_add_book_duplicate_isbn(capsys):
    lm = LibraryManager()
    lm.add_book("Test Book", "Test Author", "1234567890")
    capsys.readouterr()  # clear prior output
    lm.add_book("Test Book 2", "Test Author 2", "1234567890")
    captured_out = capsys.readouterr().out
    assert "[!] Error: A book with ISBN 1234567890 already exists." in captured_out

def test_borrow_book_ok(capsys):
    lm = LibraryManager()
    lm.add_book("Test Book", "Test Author", "1234567890")
    lm.borrow_book("1234567890")
    captured_out = capsys.readouterr().out
    assert "Success: You have borrowed 'Test Book'." in captured_out

def test_borrow_book_unavailable(capsys):
    lm = LibraryManager()
    lm.add_book("Test Book", "Test Author", "1234567890")
    lm.borrow_book("1234567890")
    capsys.readouterr()  # clear
    lm.borrow_book("1234567890")
    captured_out = capsys.readouterr().out
    assert "[!] Unavailable: 'Test Book' is currently borrowed by someone else." in captured_out

def test_borrow_book_not_found(capsys):
    lm = LibraryManager()
    lm.borrow_book("9876543210")
    captured_out = capsys.readouterr().out
    assert "[!] Error: Book with ISBN 9876543210 not found." in captured_out

def test_return_book_ok(capsys):
    lm = LibraryManager()
    lm.add_book("Test Book", "Test Author", "1234567890")
    lm.borrow_book("1234567890")
    capsys.readouterr()  # clear
    lm.return_book("1234567890")
    captured_out = capsys.readouterr().out
    assert "Success: 'Test Book' has been returned." in captured_out

def test_return_book_already_returned(capsys):
    lm = LibraryManager()
    lm.add_book("Test Book", "Test Author", "1234567890")
    # Initially the book is available; borrow then return
    lm.borrow_book("1234567890")
    capsys.readouterr()
    lm.return_book("1234567890")
    capsys.readouterr()  # clear after return
    lm.return_book("1234567890")
    captured_out = capsys.readouterr().out
    assert "[!] Strange: You are trying to return 'Test Book', but it was already here." in captured_out

def test_return_book_not_found(capsys):
    lm = LibraryManager()
    lm.return_book("9876543210")
    captured_out = capsys.readouterr().out
    assert "[!] Error: We do not own a book with ISBN 9876543210." in captured_out

def test_show_inventory_empty(capsys):
    lm = LibraryManager()
    lm.show_inventory()
    captured_out = capsys.readouterr().out
    assert "The library is empty." in captured_out

def test_show_inventory_non_empty(capsys):
    lm = LibraryManager()
    lm.add_book("Test Book", "Test Author", "1234567890")
    capsys.readouterr()  # clear
    lm.show_inventory()
    captured_out = capsys.readouterr().out
    assert "[Available] Test Book by Test Author (ISBN: 1234567890)" in captured_out