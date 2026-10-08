import pytest
from data.input_code.d04_library import *

def test_TC1_AddBook_ShortISBN(capsys):
    lm = LibraryManager()
    lm.add_book(title="Tiny", author="A", isbn="12")
    out = capsys.readouterr().out
    assert "[!] Error: ISBN '12' is too short." in out

def test_TC2_AddBook_DuplicateISBN(capsys):
    lm = LibraryManager()
    lm.add_book(title="First", author="B", isbn="12345")
    lm.add_book(title="Second", author="B", isbn="12345")
    out = capsys.readouterr().out
    assert "[!] Error: A book with ISBN 12345 already exists." in out
    # Ensure inventory unchanged for the duplicate attempt
    assert "12345" in lm.inventory
    assert lm.inventory["12345"].title == "First"

def test_TC3_AddBook_Success(capsys):
    lm = LibraryManager()
    lm.add_book(title="Python 101", author="Guido", isbn="98765")
    out = capsys.readouterr().out
    assert "Success: Added 'Python 101' to the library." in out
    assert "98765" in lm.inventory
    assert lm.inventory["98765"].title == "Python 101"
    assert lm.inventory["98765"].is_available is True

def test_TC4_BorrowBook_NotFound(capsys):
    lm = LibraryManager()
    lm.borrow_book(isbn="00000")
    out = capsys.readouterr().out
    assert "[!] Error: Book with ISBN 00000 not found." in out

def test_TC5_BorrowBook_AlreadyBorrowed(capsys):
    lm = LibraryManager()
    lm.add_book(title="Python 101", author="Guido", isbn="98765")
    # Mark as already borrowed
    lm.inventory["98765"].is_available = False
    lm.borrow_book(isbn="98765")
    out = capsys.readouterr().out
    assert "[!] Unavailable: 'Python 101' is currently borrowed by someone else." in out
    # Ensure status did not change to borrowed again
    assert lm.inventory["98765"].is_available is False

def test_TC6_BorrowBook_Success(capsys):
    lm = LibraryManager()
    lm.add_book(title="Python 101", author="Guido", isbn="98765")
    lm.borrow_book(isbn="98765")
    out = capsys.readouterr().out
    assert "Success: You have borrowed 'Python 101'." in out
    assert lm.inventory["98765"].is_available is False

def test_TC7_ReturnBook_NotFound(capsys):
    lm = LibraryManager()
    lm.return_book(isbn="11111")
    out = capsys.readouterr().out
    assert "[!] Error: We do not own a book with ISBN 11111." in out

def test_TC8_ReturnBook_AlreadyAvailable(capsys):
    lm = LibraryManager()
    lm.add_book(title="First", author="B", isbn="12345")
    # Do not borrow; book remains available
    lm.return_book(isbn="12345")
    out = capsys.readouterr().out
    assert "[!] Strange: You are trying to return 'First', but it was already here." in out

def test_TC9_ReturnBook_Success(capsys):
    lm = LibraryManager()
    lm.add_book(title="Python 101", author="Guido", isbn="98765")
    # Simulate borrowed
    lm.inventory["98765"].is_available = False
    lm.return_book(isbn="98765")
    out = capsys.readouterr().out
    assert "Success: 'Python 101' has been returned." in out
    assert lm.inventory["98765"].is_available is True

def test_TC10_ShowInventory_Empty(capsys):
    lm = LibraryManager()
    lm.show_inventory()
    out = capsys.readouterr().out
    assert "\n--- Current Library Inventory ---" in out
    assert "The library is empty." in out

def test_TC11_ShowInventory_NonEmpty(capsys):
    lm = LibraryManager()
    lm.add_book(title="Python 101", author="Guido", isbn="98765")
    lm.show_inventory()
    out = capsys.readouterr().out
    assert "\n--- Current Library Inventory ---" in out
    assert "[Available] Python 101 by Guido (ISBN: 98765)" in out

def test_TC12_BookStr_Available():
    bk = Book(title="Clean Code", author="Robert", isbn="55555")
    assert str(bk) == "[Available] Clean Code by Robert (ISBN: 55555)"

def test_TC13_BookStr_Borrowed():
    bk = Book(title="Clean Code", author="Robert", isbn="55555")
    bk.is_available = False
    assert str(bk) == "[Borrowed] Clean Code by Robert (ISBN: 55555)"