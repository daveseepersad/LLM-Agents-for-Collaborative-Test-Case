import pytest
from data.input_code.d04_library import *

# -------------------- add_book tests --------------------

@pytest.mark.parametrize(
    "title, author, isbn, expected_output",
    [
        ("Tiny", "A", "12", "[!] Error: ISBN '12' is too short."),
        ("Python 101", "Guido", "98765", "Success: Added 'Python 101' to the library."),
    ],
)
def test_add_book_basic(title, author, isbn, expected_output, capsys):
    manager = LibraryManager()
    manager.add_book(title, author, isbn)
    captured = capsys.readouterr().out.strip()
    assert captured == expected_output
    if expected_output.startswith("Success"):
        # postcondition: book is stored and available
        assert isbn in manager.inventory
        assert manager.inventory[isbn].is_available is True


def test_add_book_duplicate_isbn(capsys):
    manager = LibraryManager()
    # precondition: inventory already has a book with ISBN '12345'
    manager.inventory["12345"] = Book("First", "B", "12345")
    manager.add_book("Second", "C", "12345")
    captured = capsys.readouterr().out.strip()
    assert captured == "[!] Error: A book with ISBN 12345 already exists."

# -------------------- borrow_book tests --------------------

@pytest.mark.parametrize(
    "isbn, expected_output",
    [
        ("00000", "[!] Error: Book with ISBN 00000 not found."),
        ("11111", "[!] Unavailable: 'Locked Book' is currently borrowed by someone else."),
        ("22222", "Success: You have borrowed 'Open Book'."),
    ],
)
def test_borrow_book_various(isbn, expected_output, capsys):
    manager = LibraryManager()
    # set up preconditions based on isbn
    if isbn == "11111":
        # duplicate entry, already borrowed
        book = Book("Locked Book", "AuthorX", "11111")
        book.is_available = False
        manager.inventory[isbn] = book
    elif isbn == "22222":
        # available book
        manager.inventory[isbn] = Book("Open Book", "AuthorY", "22222")
    # else isbn not in inventory (00000)

    manager.borrow_book(isbn)
    captured = capsys.readouterr().out.strip()
    assert captured == expected_output

    if expected_output.startswith("Success"):
        # postcondition: book becomes unavailable
        assert manager.inventory[isbn].is_available is False

# -------------------- return_book tests --------------------

@pytest.mark.parametrize(
    "isbn, expected_output",
    [
        ("33333", "[!] Error: We do not own a book with ISBN 33333."),
        ("44444", "[!] Strange: You are trying to return 'Free Book', but it was already here."),
        ("55555", "Success: 'Returned Book' has been returned."),
    ],
)
def test_return_book_various(isbn, expected_output, capsys):
    manager = LibraryManager()
    # set up preconditions based on isbn
    if isbn == "44444":
        # already available book
        manager.inventory[isbn] = Book("Free Book", "AuthorZ", "44444")
    elif isbn == "55555":
        # borrowed book
        book = Book("Returned Book", "AuthorW", "55555")
        book.is_available = False
        manager.inventory[isbn] = book
    # else isbn not in inventory (33333)

    manager.return_book(isbn)
    captured = capsys.readouterr().out.strip()
    assert captured == expected_output

    if expected_output.startswith("Success"):
        # postcondition: book becomes available
        assert manager.inventory[isbn].is_available is True

# -------------------- Book __str__ test --------------------

def test_book_str_representation():
    book = Book("Mystery", "Doe", "99999")
    book.is_available = False
    assert str(book) == "[Borrowed] Mystery by Doe (ISBN: 99999)"

import pytest
from data.input_code.d04_library import *

def test_add_book_edge_isbn_length_3(capsys):
    manager = LibraryManager()
    manager.add_book("Edge", "Auth", "123")
    captured = capsys.readouterr().out.strip()
    assert captured == "Success: Added 'Edge' to the library."
    # postcondition
    assert "123" in manager.inventory
    assert manager.inventory["123"].is_available is True

def test_borrow_book_double_borrow(capsys):
    manager = LibraryManager()
    isbn = "77777"
    manager.inventory[isbn] = Book("First Borrow", "Author", isbn)

    expected_outputs = [
        "Success: You have borrowed 'First Borrow'.",
        "[!] Unavailable: 'First Borrow' is currently borrowed by someone else."
    ]

    for expected in expected_outputs:
        manager.borrow_book(isbn)
        captured = capsys.readouterr().out.strip()
        assert captured == expected

def test_return_book_double_return(capsys):
    manager = LibraryManager()
    isbn = "88888"
    book = Book("Returned Twice", "Auth", isbn)
    book.is_available = False  # initially borrowed
    manager.inventory[isbn] = book

    expected_outputs = [
        "Success: 'Returned Twice' has been returned.",
        "[!] Strange: You are trying to return 'Returned Twice', but it was already here."
    ]

    for expected in expected_outputs:
        manager.return_book(isbn)
        captured = capsys.readouterr().out.strip()
        assert captured == expected

@pytest.mark.parametrize(
    "inventory_state, expected_output",
    [
        (
            "empty",
            "--- Current Library Inventory ---\nThe library is empty.\n---------------------------------"
        ),
        (
            "single",
            "--- Current Library Inventory ---\n[Available] Sample Book by Writer (ISBN: 321)\n---------------------------------"
        ),
    ],
)
def test_show_inventory_variants(inventory_state, expected_output, capsys):
    manager = LibraryManager()
    if inventory_state == "single":
        manager.inventory["321"] = Book("Sample Book", "Writer", "321")
    manager.show_inventory()
    captured = capsys.readouterr().out.strip()
    assert captured == expected_output