import pytest
from data.input_code.d04_library import *

@pytest.mark.parametrize("title, author, isbn, expected", [
    ("1984", "George Orwell", "12345", "Success: Added '1984' to the library."),
    ("Short ISBN", "Anon", "12", "[!] Error: ISBN '12' is too short.")
])
def test_T1_T2_add(title, author, isbn, expected, capfd):
    lib = LibraryManager()
    lib.add_book(title, author, isbn)
    out = capfd.readouterr().out.strip()
    assert out == expected

def test_T3_duplicate(capfd):
    lib = LibraryManager()
    # Pre-populate inventory with an existing ISBN
    lib.inventory["ABC123"] = Book("Existing", "Writer", "ABC123")
    lib.add_book("Duplicate", "Writer2", "ABC123")
    out = capfd.readouterr().out.strip()
    assert out == "[!] Error: A book with ISBN ABC123 already exists."

def test_T4_borrow_success(capfd):
    lib = LibraryManager()
    lib.inventory["DUNE01"] = Book("Dune", "Frank Herbert", "DUNE01")
    lib.borrow_book("DUNE01")
    out = capfd.readouterr().out.strip()
    assert out == "Success: You have borrowed 'Dune'."

def test_T5_borrow_not_found(capfd):
    lib = LibraryManager()
    lib.borrow_book("NONEXIST")
    out = capfd.readouterr().out.strip()
    assert out == "[!] Error: Book with ISBN NONEXIST not found."

def test_T6_borrow_unavailable(capfd):
    lib = LibraryManager()
    b = Book("Locked", "Author", "LOCKED")
    lib.inventory["LOCKED"] = b
    # Simulate that it's already borrowed
    lib.inventory["LOCKED"].is_available = False
    lib.borrow_book("LOCKED")
    out = capfd.readouterr().out.strip()
    assert out == "[!] Unavailable: 'Locked' is currently borrowed by someone else."

def test_T7_return_success(capfd):
    lib = LibraryManager()
    lib.inventory["RET01"] = Book("ReturnMe", "Auth", "RET01")
    # Simulate that it was borrowed
    lib.inventory["RET01"].is_available = False
    lib.return_book("RET01")
    out = capfd.readouterr().out.strip()
    assert out == "Success: 'ReturnMe' has been returned."

def test_T8_return_not_found(capfd):
    lib = LibraryManager()
    lib.return_book("MISSING")
    out = capfd.readouterr().out.strip()
    assert out == "[!] Error: We do not own a book with ISBN MISSING."

def test_T9_return_already_available(capfd):
    lib = LibraryManager()
    lib.inventory["AH01"] = Book("AlreadyHere", "Auth", "AH01")
    # Book is available by default
    lib.return_book("AH01")
    out = capfd.readouterr().out.strip()
    assert out == "[!] Strange: You are trying to return 'AlreadyHere', but it was already here."

@pytest.mark.parametrize("title, author, isbn, is_available, expected", [
    ("Free Book", "Writer", "FREE01", True, "[Available] Free Book by Writer (ISBN: FREE01)"),
    ("Taken Book", "Writer", "TAKE01", False, "[Borrowed] Taken Book by Writer (ISBN: TAKE01)")
])
def test_T10_T11_str_representation(title, author, isbn, is_available, expected):
    b = Book(title, author, isbn)
    b.is_available = is_available
    assert str(b) == expected

def test_T_ADD_BOUNDARY(capfd):
    lib = LibraryManager()
    lib.add_book("Boundary", "Auth", "ABC")
    out = capfd.readouterr().out.strip()
    assert out == "Success: Added 'Boundary' to the library."

def test_T_BORROW_STATE_CHANGE():
    lib = LibraryManager()
    lib.inventory["BORROW1"] = Book("Borrowable", "Author", "BORROW1")
    lib.borrow_book("BORROW1")
    result = lib.inventory["BORROW1"].is_available
    assert result is False

def test_T_RETURN_STATE_CHANGE():
    lib = LibraryManager()
    lib.inventory["RET2"] = Book("Returnable", "Author", "RET2")
    lib.inventory["RET2"].is_available = False
    lib.return_book("RET2")
    result = lib.inventory["RET2"].is_available
    assert result is True

def test_T_SHOW_EMPTY(capfd):
    lib = LibraryManager()
    lib.show_inventory()
    out = capfd.readouterr().out
    assert out == "\n--- Current Library Inventory ---\nThe library is empty.\n---------------------------------\n\n"

def test_T_SHOW_NONEMPTY(capfd):
    lib = LibraryManager()
    lib.inventory["ISBN1"] = Book("A", "B", "ISBN1")
    lib.inventory["ISBN1"].is_available = True
    lib.inventory["ISBN2"] = Book("C", "D", "ISBN2")
    lib.inventory["ISBN2"].is_available = False
    lib.show_inventory()
    out = capfd.readouterr().out
    assert out == "\n--- Current Library Inventory ---\n[Available] A by B (ISBN: ISBN1)\n[Borrowed] C by D (ISBN: ISBN2)\n---------------------------------\n\n"