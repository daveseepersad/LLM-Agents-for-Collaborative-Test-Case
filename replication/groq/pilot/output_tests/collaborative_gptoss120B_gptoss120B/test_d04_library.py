import pytest
from data.input_code.d04_library import *

def test_library_manager_workflow(capsys):
    manager = LibraryManager()

    # T1: ISBN too short
    manager.add_book(title="Short ISBN", author="A", isbn="12")
    out = capsys.readouterr().out.strip().splitlines()
    assert out == ["[!] Error: ISBN '12' is too short."]

    # T2: Add first valid book
    manager.add_book(title="First Book", author="B", isbn="ABC")
    out = capsys.readouterr().out.strip().splitlines()
    assert out == ["Success: Added 'First Book' to the library."]

    # T3: Duplicate ISBN detection
    manager.add_book(title="Duplicate Book", author="C", isbn="ABC")
    out = capsys.readouterr().out.strip().splitlines()
    assert out == ["[!] Error: A book with ISBN ABC already exists."]

    # T4: Borrow non‑existent ISBN
    manager.borrow_book(isbn="XYZ")
    out = capsys.readouterr().out.strip().splitlines()
    assert out == ["[!] Error: Book with ISBN XYZ not found."]

    # T5: Successful borrow
    manager.borrow_book(isbn="ABC")
    out = capsys.readouterr().out.strip().splitlines()
    assert out == ["Success: You have borrowed 'First Book'."]

    # T6: Attempt to borrow already borrowed book
    manager.borrow_book(isbn="ABC")
    out = capsys.readouterr().out.strip().splitlines()
    assert out == ["[!] Unavailable: 'First Book' is currently borrowed by someone else."]

    # T7: Return non‑existent ISBN
    manager.return_book(isbn="XYZ")
    out = capsys.readouterr().out.strip().splitlines()
    assert out == ["[!] Error: We do not own a book with ISBN XYZ."]

    # T8: Successful return
    manager.return_book(isbn="ABC")
    out = capsys.readouterr().out.strip().splitlines()
    assert out == ["Success: 'First Book' has been returned."]

    # T9: Return a book that is already available
    manager.return_book(isbn="ABC")
    out = capsys.readouterr().out.strip().splitlines()
    assert out == ["[!] Strange: You are trying to return 'First Book', but it was already here."]

    # T10: Show inventory representation
    manager.show_inventory()
    out = capsys.readouterr().out.strip().splitlines()
    # Remove possible empty lines caused by leading/trailing newlines
    filtered = [line for line in out if line]
    assert filtered == [
        "--- Current Library Inventory ---",
        "[Available] First Book by B (ISBN: ABC)",
        "---------------------------------"
    ]

import pytest
from data.input_code.d04_library import *

def test_show_inventory_empty(capsys):
    manager = LibraryManager()
    manager.show_inventory()
    out = capsys.readouterr().out.strip().splitlines()
    filtered = [line for line in out if line]
    assert filtered == [
        "--- Current Library Inventory ---",
        "The library is empty.",
        "---------------------------------"
    ]

@pytest.mark.parametrize(
    "title,author,isbn,available,expected",
    [
        (
            "Mystery Novel",
            "Jane Doe",
            "XYZ123",
            False,
            "[Borrowed] Mystery Novel by Jane Doe (ISBN: XYZ123)"
        ),
    ],
)
def test_book_str_borrowed(title, author, isbn, available, expected):
    book = Book(title, author, isbn)
    book.is_available = available
    assert str(book) == expected