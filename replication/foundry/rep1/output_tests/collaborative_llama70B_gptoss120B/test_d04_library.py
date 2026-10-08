import pytest
from data.input_code.d04_library import *

@pytest.fixture
def fresh_manager():
    """Provides a new LibraryManager for each test."""
    return LibraryManager()

def test_book_init():
    """T1_OK – ensure Book can be instantiated without error."""
    book = Book(title="Test Book", author="Test Author", isbn="1234567890")
    assert book.title == "Test Book"
    assert book.author == "Test Author"
    assert book.isbn == "1234567890"
    assert book.is_available is True

def test_book_str():
    """T2_OK – string representation reflects availability."""
    book = Book(title="Test Book", author="Test Author", isbn="1234567890")
    expected = "[Available] Test Book by Test Author (ISBN: 1234567890)"
    assert str(book) == expected

def test_library_manager_init():
    """T3_OK – LibraryManager starts with empty inventory."""
    manager = LibraryManager()
    assert isinstance(manager.inventory, dict)
    assert not manager.inventory

@pytest.mark.parametrize(
    "title,author,isbn,expected_output",
    [
        (
            "Test Book",
            "Test Author",
            "1234567890",
            "Success: Added 'Test Book' to the library.\n",
        ),
    ],
)
def test_add_book_success(fresh_manager, title, author, isbn, expected_output, capsys):
    """T4_OK – adding a valid book prints success and stores it."""
    fresh_manager.add_book(title, author, isbn)
    captured = capsys.readouterr()
    assert captured.out == expected_output
    # verify inventory
    assert isbn in fresh_manager.inventory
    book = fresh_manager.inventory[isbn]
    assert book.title == title
    assert book.author == author
    assert book.isbn == isbn

@pytest.mark.parametrize(
    "title,author,isbn,expected_output",
    [
        (
            "Test Book",
            "Test Author",
            "12",
            "[!] Error: ISBN '12' is too short.\n",
        ),
    ],
)
def test_add_book_isbn_too_short(fresh_manager, title, author, isbn, expected_output, capsys):
    """T5_ERR – short ISBN triggers error message."""
    fresh_manager.add_book(title, author, isbn)
    captured = capsys.readouterr()
    assert captured.out == expected_output
    assert isbn not in fresh_manager.inventory

def test_add_book_duplicate_isbn(fresh_manager, capsys):
    """T6_ERR – adding a book with an existing ISBN prints duplicate error."""
    # first addition
    fresh_manager.add_book("Test Book", "Test Author", "1234567890")
    capsys.readouterr()  # clear previous output
    # duplicate addition
    fresh_manager.add_book("Another Book", "Another Author", "1234567890")
    captured = capsys.readouterr()
    assert captured.out == "[!] Error: A book with ISBN 1234567890 already exists.\n"
    # inventory should still contain only the first book
    assert len(fresh_manager.inventory) == 1
    assert fresh_manager.inventory["1234567890"].title == "Test Book"

def test_borrow_book_success(fresh_manager, capsys):
    """T7_OK – borrowing an available book prints success."""
    fresh_manager.add_book("Test Book", "Test Author", "1234567890")
    capsys.readouterr()  # clear add_book output
    fresh_manager.borrow_book("1234567890")
    captured = capsys.readouterr()
    assert captured.out == "Success: You have borrowed 'Test Book'.\n"
    assert fresh_manager.inventory["1234567890"].is_available is False

@pytest.mark.parametrize(
    "isbn,expected_output",
    [
        ("9876543210", "[!] Error: Book with ISBN 9876543210 not found.\n"),
    ],
)
def test_borrow_book_not_found(fresh_manager, isbn, expected_output, capsys):
    """T8_ERR – borrowing a non‑existent ISBN prints error."""
    fresh_manager.borrow_book(isbn)
    captured = capsys.readouterr()
    assert captured.out == expected_output

def test_borrow_book_already_borrowed(fresh_manager, capsys):
    """T9_ERR – borrowing a book that is already borrowed prints unavailable."""
    fresh_manager.add_book("Test Book", "Test Author", "1234567890")
    capsys.readouterr()
    # first borrow succeeds
    fresh_manager.borrow_book("1234567890")
    capsys.readouterr()
    # second borrow should fail
    fresh_manager.borrow_book("1234567890")
    captured = capsys.readouterr()
    assert captured.out == "[!] Unavailable: 'Test Book' is currently borrowed by someone else.\n"

def test_return_book_success(fresh_manager, capsys):
    """T10_OK – returning a borrowed book prints success."""
    fresh_manager.add_book("Test Book", "Test Author", "1234567890")
    capsys.readouterr()
    fresh_manager.borrow_book("1234567890")
    capsys.readouterr()
    fresh_manager.return_book("1234567890")
    captured = capsys.readouterr()
    assert captured.out == "Success: 'Test Book' has been returned.\n"
    assert fresh_manager.inventory["1234567890"].is_available is True

@pytest.mark.parametrize(
    "isbn,expected_output",
    [
        ("9876543210", "[!] Error: We do not own a book with ISBN 9876543210.\n"),
    ],
)
def test_return_book_not_found(fresh_manager, isbn, expected_output, capsys):
    """T11_ERR – returning a non‑existent ISBN prints error."""
    fresh_manager.return_book(isbn)
    captured = capsys.readouterr()
    assert captured.out == expected_output

def test_return_book_already_returned(fresh_manager, capsys):
    """T12_ERR – returning a book that is already available prints strange message."""
    fresh_manager.add_book("Test Book", "Test Author", "1234567890")
    capsys.readouterr()
    fresh_manager.return_book("1234567890")
    captured = capsys.readouterr()
    assert captured.out == "[!] Strange: You are trying to return 'Test Book', but it was already here.\n"

def test_show_inventory_output(fresh_manager, capsys):
    """T13_OK – show_inventory prints header/footer and book lines."""
    fresh_manager.add_book("Test Book", "Test Author", "1234567890")
    capsys.readouterr()
    fresh_manager.show_inventory()
    captured = capsys.readouterr()
    # Expected lines (order matters)
    expected_lines = [
        "\n--- Current Library Inventory ---\n",
        "[Available] Test Book by Test Author (ISBN: 1234567890)\n",
        "---------------------------------\n\n",
    ]
    assert captured.out == "".join(expected_lines)

import pytest
from data.input_code.d04_library import *

def test_show_inventory_empty(fresh_manager, capsys):
    """T_MISSING_EMPTY_INVENTORY – show inventory when library is empty."""
    fresh_manager.show_inventory()
    captured = capsys.readouterr()
    expected = "\n--- Current Library Inventory ---\nThe library is empty.\n---------------------------------\n\n"
    assert captured.out == expected

def test_show_inventory_multiple_books(fresh_manager, capsys):
    """T_MISSING_MULTIPLE_BOOKS – show inventory with multiple books."""
    fresh_manager.add_book("Book1", "Author1", "1234567890")
    fresh_manager.add_book("Book2", "Author2", "9876543210")
    capsys.readouterr()  # clear add_book output
    fresh_manager.show_inventory()
    captured = capsys.readouterr()
    expected = (
        "\n--- Current Library Inventory ---\n"
        "[Available] Book1 by Author1 (ISBN: 1234567890)\n"
        "[Available] Book2 by Author2 (ISBN: 9876543210)\n"
        "---------------------------------\n\n"
    )
    assert captured.out == expected

def test_show_inventory_borrowed_and_available(fresh_manager, capsys):
    """T_MISSING_BORROWED_BOOKS – show inventory with borrowed and available books."""
    fresh_manager.add_book("Book1", "Author1", "1234567890")
    fresh_manager.add_book("Book2", "Author2", "9876543210")
    capsys.readouterr()
    fresh_manager.borrow_book("1234567890")
    capsys.readouterr()
    fresh_manager.show_inventory()
    captured = capsys.readouterr()
    expected = (
        "\n--- Current Library Inventory ---\n"
        "[Borrowed] Book1 by Author1 (ISBN: 1234567890)\n"
        "[Available] Book2 by Author2 (ISBN: 9876543210)\n"
        "---------------------------------\n\n"
    )
    assert captured.out == expected

@pytest.mark.parametrize(
    "title,author,isbn",
    [
        ("Test Book", "Test Author", "123"),               # exact 3‑char ISBN
        ("", "Test Author", "1234567890"),                # empty title
        ("Test Book", "", "1234567890"),                  # empty author
    ],
)
def test_book_edge_cases(title, author, isbn):
    """T_MISSING_EDGE_CASE_* – ensure Book can be instantiated with edge‑case values."""
    book = Book(title=title, author=author, isbn=isbn)
    assert book.title == title
    assert book.author == author
    assert book.isbn == isbn
    assert book.is_available is True