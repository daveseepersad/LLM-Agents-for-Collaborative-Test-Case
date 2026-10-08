import pytest
from data.input_code.d04_library import *

def test_T1_BOOK_INIT():
    b = Book("Test Book", "Test Author", "1234567890")
    assert b.title == "Test Book"
    assert b.author == "Test Author"
    assert b.isbn == "1234567890"
    assert b.is_available is True

def test_T2_BOOK_STR():
    b = Book("Test Book", "Test Author", "1234567890")
    assert str(b) == "[Available] Test Book by Test Author (ISBN: 1234567890)"

def test_T3_LIB_INIT():
    lm = LibraryManager()
    assert isinstance(lm, LibraryManager)
    assert lm.inventory == {}

def test_T4_ADD_BOOK_OK(capsys):
    lm = LibraryManager()
    lm.add_book("Test Book", "Test Author", "1234567890")
    captured = capsys.readouterr().out
    assert captured == "Success: Added 'Test Book' to the library.\n"
    assert "1234567890" in lm.inventory
    assert isinstance(lm.inventory["1234567890"], Book)

def test_T5_ADD_BOOK_SHORT_ISBN(capsys):
    lm = LibraryManager()
    lm.add_book("Test Book", "Test Author", "12")
    captured = capsys.readouterr().out
    assert captured == "[!] Error: ISBN '12' is too short.\n"

def test_T6_ADD_BOOK_DUPLICATE_ISBN(capsys):
    lm = LibraryManager()
    lm.add_book("Test Book", "Test Author", "1234567890")
    capsys.readouterr()  # clear
    lm.add_book("Test Book 2", "Test Author 2", "1234567890")
    captured = capsys.readouterr().out
    assert captured == "[!] Error: A book with ISBN 1234567890 already exists.\n"

def test_T7_BORROW_BOOK_OK(capsys):
    lm = LibraryManager()
    lm.add_book("Test Book", "Test Author", "1234567890")
    capsys.readouterr()  # clear
    lm.borrow_book("1234567890")
    captured = capsys.readouterr().out
    assert captured == "Success: You have borrowed 'Test Book'.\n"
    assert lm.inventory["1234567890"].is_available is False

def test_T8_BORROW_BOOK_UNAVAILABLE(capsys):
    lm = LibraryManager()
    lm.add_book("Test Book", "Test Author", "1234567890")
    lm.borrow_book("1234567890")
    capsys.readouterr()  # clear
    lm.borrow_book("1234567890")
    captured = capsys.readouterr().out
    assert captured == "[!] Unavailable: 'Test Book' is currently borrowed by someone else.\n"

def test_T9_BORROW_BOOK_NOT_FOUND(capsys):
    lm = LibraryManager()
    lm.add_book("Test Book", "Test Author", "1234567890")  # ensure some data exists
    capsys.readouterr()  # clear
    lm.borrow_book("9876543210")
    captured = capsys.readouterr().out
    assert captured == "[!] Error: Book with ISBN 9876543210 not found.\n"

def test_T10_RETURN_BOOK_OK(capsys):
    lm = LibraryManager()
    lm.add_book("Test Book", "Test Author", "1234567890")
    lm.borrow_book("1234567890")
    capsys.readouterr()  # clear
    lm.return_book("1234567890")
    captured = capsys.readouterr().out
    assert captured == "Success: 'Test Book' has been returned.\n"
    assert lm.inventory["1234567890"].is_available is True

def test_T11_RETURN_BOOK_ALREADY_RETURNED(capsys):
    lm = LibraryManager()
    lm.add_book("Test Book", "Test Author", "1234567890")
    capsys.readouterr()  # clear
    # Do not borrow; try to return
    lm.return_book("1234567890")
    captured = capsys.readouterr().out
    assert captured == "[!] Strange: You are trying to return 'Test Book', but it was already here.\n"

def test_T12_RETURN_BOOK_NOT_FOUND(capsys):
    lm = LibraryManager()
    lm.return_book("9876543210")
    captured = capsys.readouterr().out
    assert captured == "[!] Error: We do not own a book with ISBN 9876543210.\n"

def test_T13_SHOW_INVENTORY_EMPTY(capsys):
    lm = LibraryManager()
    lm.show_inventory()
    captured = capsys.readouterr().out
    assert captured == "\n--- Current Library Inventory ---\nThe library is empty.\n---------------------------------\n\n"

def test_T14_SHOW_INVENTORY_NON_EMPTY(capsys):
    lm = LibraryManager()
    lm.add_book("Test Book", "Test Author", "1234567890")
    capsys.readouterr()  # clear
    lm.show_inventory()
    captured = capsys.readouterr().out
    assert captured == "\n--- Current Library Inventory ---\n[Available] Test Book by Test Author (ISBN: 1234567890)\n---------------------------------\n\n"