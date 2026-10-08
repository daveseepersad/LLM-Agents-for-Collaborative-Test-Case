import pytest
from data.input_code.d04_library import *

def test_T1_add_success(capsys):
    lm = LibraryManager()
    lm.add_book("1984", "George Orwell", "12345")
    out = capsys.readouterr().out
    assert out == "Success: Added '1984' to the library.\n"

def test_T2_add_short_isbn(capsys):
    lm = LibraryManager()
    lm.add_book("Short ISBN", "Anon", "12")
    out = capsys.readouterr().out
    assert out == "[!] Error: ISBN '12' is too short.\n"

def test_T3_add_duplicate(capsys):
    lm = LibraryManager()
    lm.add_book("Original", "Author", "12345")
    _ = capsys.readouterr()  # flush first message
    lm.add_book("Duplicate Book", "Author", "12345")
    out = capsys.readouterr().out
    assert out == "[!] Error: A book with ISBN 12345 already exists.\n"

def test_T4_borrow_success(capsys):
    lm = LibraryManager()
    lm.add_book("1984", "George Orwell", "12345")
    _ = capsys.readouterr()
    lm.borrow_book("12345")
    out = capsys.readouterr().out
    assert out == "Success: You have borrowed '1984'.\n"

def test_T5_borrow_nonexistent(capsys):
    lm = LibraryManager()
    lm.borrow_book("99999")
    out = capsys.readouterr().out
    assert out == "[!] Error: Book with ISBN 99999 not found.\n"

def test_T6_borrow_unavailable(capsys):
    lm = LibraryManager()
    lm.add_book("1984", "George Orwell", "12345")
    _ = capsys.readouterr()
    lm.borrow_book("12345")
    _ = capsys.readouterr()
    lm.borrow_book("12345")
    out = capsys.readouterr().out
    assert out == "[!] Unavailable: '1984' is currently borrowed by someone else.\n"

def test_T7_return_success(capsys):
    lm = LibraryManager()
    lm.add_book("1984", "George Orwell", "12345")
    _ = capsys.readouterr()
    lm.borrow_book("12345")
    _ = capsys.readouterr()
    lm.return_book("12345")
    out = capsys.readouterr().out
    assert out == "Success: '1984' has been returned.\n"

def test_T8_return_nonexistent(capsys):
    lm = LibraryManager()
    lm.return_book("88888")
    out = capsys.readouterr().out
    assert out == "[!] Error: We do not own a book with ISBN 88888.\n"

def test_T9_return_already_available(capsys):
    lm = LibraryManager()
    lm.add_book("1984", "George Orwell", "12345")
    _ = capsys.readouterr()
    lm.return_book("12345")
    out = capsys.readouterr().out
    assert out == "[!] Strange: You are trying to return '1984', but it was already here.\n"

def test_T10_show_inventory_empty(capsys):
    lm = LibraryManager()
    lm.show_inventory()
    out = capsys.readouterr().out
    assert out == "\n--- Current Library Inventory ---\nThe library is empty.\n---------------------------------\n\n"

def test_T11_show_inventory_nonempty(capsys):
    lm = LibraryManager()
    lm.add_book("1984", "George Orwell", "12345")
    _ = capsys.readouterr()
    lm.add_book("Brave New World", "Aldous Huxley", "67890")
    _ = capsys.readouterr()
    lm.show_inventory()
    out = capsys.readouterr().out
    expected = "\n--- Current Library Inventory ---\n[Available] 1984 by George Orwell (ISBN: 12345)\n[Available] Brave New World by Aldous Huxley (ISBN: 67890)\n---------------------------------\n\n"
    assert out == expected

def test_T12_book_str_borrowed():
    b = Book("Dune", "Frank Herbert", "55555")
    b.is_available = False
    assert str(b) == "[Borrowed] Dune by Frank Herbert (ISBN: 55555)"