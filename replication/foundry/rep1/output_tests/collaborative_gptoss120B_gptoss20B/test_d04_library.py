import pytest
from data.input_code.d04_library import *

# -------------------- add_book --------------------
@pytest.mark.parametrize(
    "title, author, isbn, expected_msg",
    [
        # Normal addition
        ("1984", "George Orwell", "9780451524935", "Success: Added '1984' to the library."),
        # Short ISBN validation
        ("Test Book", "Anon", "12", "[!] Error: ISBN '12' is too short."),
        # Duplicate ISBN validation
        ("Duplicate", "Writer", "dup123", "[!] Error: A book with ISBN dup123 already exists."),
    ],
)
def test_add_book(title, author, isbn, expected_msg, capsys):
    lib = LibraryManager()
    # Pre‑populate for duplicate case
    if expected_msg.startswith("[!] Error: A book with ISBN"):
        lib.add_book("First", "Author", isbn)

    lib.add_book(title, author, isbn)
    captured = capsys.readouterr().out.strip().splitlines()[-1]
    assert expected_msg in captured

# -------------------- borrow_book --------------------
@pytest.mark.parametrize(
    "setup_isbn, borrow_isbn, expected_msg",
    [
        # Borrow non‑existent book
        (None, "000-000-000", "[!] Error: Book with ISBN 000-000-000 not found."),
        # Borrow already borrowed book
        ("avail123", "avail123", "[!] Unavailable: 'Available Book' is currently borrowed by someone else."),
        # Successful borrow
        ("avail456", "avail456", "Success: You have borrowed 'Borrowable Book'."),
    ],
)
def test_borrow_book(setup_isbn, borrow_isbn, expected_msg, capsys):
    lib = LibraryManager()
    if setup_isbn:
        # Add a book that will be borrowed
        title = "Available Book" if setup_isbn == "avail123" else "Borrowable Book"
        lib.add_book(title, "Author", setup_isbn)
        # For the already borrowed scenario, mark it as borrowed first
        if expected_msg.startswith("[!] Unavailable"):
            lib.borrow_book(setup_isbn)

    lib.borrow_book(borrow_isbn)
    captured = capsys.readouterr().out.strip().splitlines()[-1]
    assert expected_msg in captured

# -------------------- return_book --------------------
@pytest.mark.parametrize(
    "setup_isbn, return_isbn, expected_msg",
    [
        # Return non‑existent book
        (None, "999-999-999", "[!] Error: We do not own a book with ISBN 999-999-999."),
        # Return a book that is already available
        ("avail789", "avail789", "[!] Strange: You are trying to return 'Already Here', but it was already here."),
        # Successful return
        ("borrowed101", "borrowed101", "Success: 'Returned Book' has been returned."),
    ],
)
def test_return_book(setup_isbn, return_isbn, expected_msg, capsys):
    lib = LibraryManager()
    if setup_isbn:
        title = "Already Here" if setup_isbn == "avail789" else "Returned Book"
        lib.add_book(title, "Author", setup_isbn)
        # For successful return, borrow first
        if expected_msg.startswith("Success:"):
            lib.borrow_book(setup_isbn)

    lib.return_book(return_isbn)
    captured = capsys.readouterr().out.strip().splitlines()[-1]
    assert expected_msg in captured

# -------------------- show_inventory --------------------
def test_show_inventory_empty(capsys):
    lib = LibraryManager()
    lib.show_inventory()
    out = capsys.readouterr().out
    assert "The library is empty." in out

def test_show_inventory_non_empty(capsys):
    lib = LibraryManager()
    lib.add_book("Dune", "Frank Herbert", "isbn001")
    lib.show_inventory()
    out = capsys.readouterr().out
    assert "[Available] Dune by Frank Herbert (ISBN: isbn001)" in out