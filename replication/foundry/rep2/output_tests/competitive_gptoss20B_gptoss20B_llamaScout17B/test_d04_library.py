import pytest
from data.input_code.d04_library import *

@pytest.fixture(scope="module")
def lib():
    return LibraryManager()

def test_library_plan_workflow(lib, capsys):
    # T1_ADD_OK
    lib.add_book("1984", "George Orwell", "9780451524935")
    out = capsys.readouterr().out
    assert out == "Success: Added '1984' to the library.\n"

    # T2_BORROW_OK
    lib.borrow_book("9780451524935")
    out = capsys.readouterr().out
    assert out == "Success: You have borrowed '1984'.\n"

    # T3_BORROW_UNAVAILABLE
    lib.borrow_book("9780451524935")
    out = capsys.readouterr().out
    assert out == "[!] Unavailable: '1984' is currently borrowed by someone else.\n"

    # T4_RETURN_OK
    lib.return_book("9780451524935")
    out = capsys.readouterr().out
    assert out == "Success: '1984' has been returned.\n"

    # T5_RETURN_ALREADY_AVAILABLE
    lib.return_book("9780451524935")
    out = capsys.readouterr().out
    assert out == "[!] Strange: You are trying to return '1984', but it was already here.\n"

    # T6_ADD_SHORT_ISBN
    lib.add_book("Brave New World", "Aldous Huxley", "12")
    out = capsys.readouterr().out
    assert out == "[!] Error: ISBN '12' is too short.\n"

    # T7_ADD_DUPLICATE
    lib.add_book("Animal Farm", "George Orwell", "9780451524935")
    out = capsys.readouterr().out
    assert out == "[!] Error: A book with ISBN 9780451524935 already exists.\n"

    # T8_BORROW_NOT_FOUND
    lib.borrow_book("0000000000")
    out = capsys.readouterr().out
    assert out == "[!] Error: Book with ISBN 0000000000 not found.\n"

    # T9_RETURN_NOT_FOUND
    lib.return_book("0000000000")
    out = capsys.readouterr().out
    assert out == "[!] Error: We do not own a book with ISBN 0000000000.\n"

    # T10_SHOW_INV_NONEMPTY
    lib.show_inventory()
    out = capsys.readouterr().out
    assert out == "\n--- Current Library Inventory ---\n[Available] 1984 by George Orwell (ISBN: 9780451524935)\n---------------------------------\n\n"

def test_show_inv_empty(capsys):
    lib = LibraryManager()
    lib.show_inventory()
    out = capsys.readouterr().out
    assert out == "\n--- Current Library Inventory ---\nThe library is empty.\n---------------------------------\n\n"

@pytest.mark.parametrize("title, author, isbn, is_available, expected", [
    ("Dune", "Frank Herbert", "9780441013593", False, "[Borrowed] Dune by Frank Herbert (ISBN: 9780441013593)"),
])
def test_book_str(title, author, isbn, is_available, expected):
    book = Book(title, author, isbn)
    book.is_available = is_available
    assert str(book) == expected