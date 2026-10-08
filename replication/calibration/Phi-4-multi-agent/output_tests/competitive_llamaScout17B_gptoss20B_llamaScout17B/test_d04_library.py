import pytest
from data.input_code.d04_library import *

def test_T1_ADD_SUCCESS(capsys):
    lm = LibraryManager()
    lm.add_book("Book One", "Author A", "12345")
    assert capsys.readouterr().out == "Success: Added 'Book One' to the library.\n"

def test_T2_ADD_SHORT_ISBN(capsys):
    lm = LibraryManager()
    lm.add_book("Book Two", "Author B", "12")
    assert capsys.readouterr().out == "[!] Error: ISBN '12' is too short.\n"

def test_T3_ADD_DUPLICATE(capsys):
    lm = LibraryManager()
    lm.add_book("Book One", "Author A", "12345")
    capsys.readouterr()  # clear prior output
    lm.add_book("Book One Clone", "Author A", "12345")
    out = capsys.readouterr().out
    assert out == "[!] Error: A book with ISBN 12345 already exists.\n"

def test_T4_BORROW_SUCCESS(capsys):
    lm = LibraryManager()
    lm.add_book("Book One", "Author A", "12345")
    capsys.readouterr()  # clear
    lm.borrow_book("12345")
    out = capsys.readouterr().out
    assert out == "Success: You have borrowed 'Book One'.\n"

def test_T5_BORROW_NOT_FOUND(capsys):
    lm = LibraryManager()
    lm.borrow_book("67890")
    out = capsys.readouterr().out
    assert out == "[!] Error: Book with ISBN 67890 not found.\n"

def test_T6_BORROW_UNAVAILABLE(capsys):
    lm = LibraryManager()
    lm.add_book("Book One", "Author A", "12345")
    capsys.readouterr()
    lm.borrow_book("12345")
    capsys.readouterr()  # clear after first borrow
    lm.borrow_book("12345")
    out = capsys.readouterr().out
    assert out == "[!] Unavailable: 'Book One' is currently borrowed by someone else.\n"

def test_T7_RETURN_SUCCESS(capsys):
    lm = LibraryManager()
    lm.add_book("Book One", "Author A", "12345")
    capsys.readouterr()
    lm.borrow_book("12345")
    capsys.readouterr()
    lm.return_book("12345")
    out = capsys.readouterr().out
    assert out == "Success: 'Book One' has been returned.\n"

def test_T8_RETURN_NOT_FOUND(capsys):
    lm = LibraryManager()
    lm.return_book("67890")
    out = capsys.readouterr().out
    assert out == "[!] Error: We do not own a book with ISBN 67890.\n"

def test_T9_RETURN_ALREADY_HERE(capsys):
    lm = LibraryManager()
    lm.add_book("Book One", "Author A", "12345")
    capsys.readouterr()
    lm.return_book("12345")
    out = capsys.readouterr().out
    assert out == "[!] Strange: You are trying to return 'Book One', but it was already here.\n"

def test_T10_SHOW_EMPTY(capsys):
    lm = LibraryManager()
    lm.show_inventory()
    out = capsys.readouterr().out
    assert out == "\n--- Current Library Inventory ---\nThe library is empty.\n---------------------------------\n\n"

def test_T11_SHOW_NON_EMPTY(capsys):
    lm = LibraryManager()
    lm.add_book("Book One", "Author A", "12345")
    capsys.readouterr()
    lm.show_inventory()
    out = capsys.readouterr().out
    assert out == "\n--- Current Library Inventory ---\n[Available] Book One by Author A (ISBN: 12345)\n---------------------------------\n\n"