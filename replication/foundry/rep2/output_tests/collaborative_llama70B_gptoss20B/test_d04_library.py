import pytest
from data.input_code.d04_library import *

def test_T1_BOOK_INIT():
    b = Book("Test Book", "Test Author", "1234567890")
    assert isinstance(b, Book)
    assert b.title == "Test Book"
    assert b.author == "Test Author"
    assert b.isbn == "1234567890"
    assert b.is_available is True

def test_T2_BOOK_STR():
    b = Book("Test Book", "Test Author", "1234567890")
    assert str(b) == "[Available] Test Book by Test Author (ISBN: 1234567890)"

def test_T3_LIB_INIT():
    lib = LibraryManager()
    assert isinstance(lib, LibraryManager)

def test_T4_ADD_BOOK_OK(capsys):
    lib = LibraryManager()
    lib.add_book("Test Book", "Test Author", "1234567890")
    captured = capsys.readouterr()
    assert "Success: Added 'Test Book' to the library." in captured.out

def test_T5_ADD_BOOK_SHORT_ISBN(capsys):
    lib = LibraryManager()
    lib.add_book("Test Book", "Test Author", "12")
    captured = capsys.readouterr()
    assert "[!] Error: ISBN '12' is too short." in captured.out

def test_T6_ADD_BOOK_DUPLICATE_ISBN(capsys):
    lib = LibraryManager()
    lib.add_book("Test Book", "Test Author", "1234567890")
    lib.add_book("Test Book 2", "Test Author 2", "1234567890")
    captured = capsys.readouterr()
    assert "[!] Error: A book with ISBN 1234567890 already exists." in captured.out

def test_T7_BORROW_BOOK_OK(capsys):
    lib = LibraryManager()
    lib.add_book("Test Book", "Test Author", "1234567890")
    lib.borrow_book("1234567890")
    captured = capsys.readouterr()
    assert "Success: You have borrowed 'Test Book'." in captured.out

def test_T8_BORROW_BOOK_NOT_FOUND(capsys):
    lib = LibraryManager()
    lib.borrow_book("9876543210")
    captured = capsys.readouterr()
    assert "[!] Error: Book with ISBN 9876543210 not found." in captured.out

def test_T9_BORROW_BOOK_UNAVAILABLE(capsys):
    lib = LibraryManager()
    lib.add_book("Test Book", "Test Author", "1234567890")
    lib.borrow_book("1234567890")
    lib.borrow_book("1234567890")
    captured = capsys.readouterr()
    assert "[!] Unavailable: 'Test Book' is currently borrowed by someone else." in captured.out

def test_T10_RETURN_BOOK_OK(capsys):
    lib = LibraryManager()
    lib.add_book("Test Book", "Test Author", "1234567890")
    lib.borrow_book("1234567890")
    lib.return_book("1234567890")
    captured = capsys.readouterr()
    assert "Success: 'Test Book' has been returned." in captured.out

def test_T11_RETURN_BOOK_NOT_FOUND(capsys):
    lib = LibraryManager()
    lib.return_book("9876543210")
    captured = capsys.readouterr()
    assert "[!] Error: We do not own a book with ISBN 9876543210." in captured.out

def test_T12_RETURN_BOOK_ALREADY_RETURNED(capsys):
    lib = LibraryManager()
    lib.add_book("Test Book", "Test Author", "1234567890")
    lib.return_book("1234567890")
    captured = capsys.readouterr()
    assert "[!] Strange: You are trying to return 'Test Book', but it was already here." in captured.out

def test_T13_SHOW_INVENTORY_EMPTY(capsys):
    lib = LibraryManager()
    lib.show_inventory()
    captured = capsys.readouterr()
    assert "The library is empty." in captured.out

def test_T14_SHOW_INVENTORY_NON_EMPTY(capsys):
    lib = LibraryManager()
    lib.add_book("Test Book", "Test Author", "1234567890")
    lib.show_inventory()
    captured = capsys.readouterr()
    assert "[Available] Test Book by Test Author (ISBN: 1234567890)" in captured.out