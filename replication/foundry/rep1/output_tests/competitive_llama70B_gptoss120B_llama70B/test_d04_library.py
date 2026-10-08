import pytest
from data.input_code.d04_library import *

@pytest.fixture
def empty_manager():
    """Provides a fresh LibraryManager with no books."""
    return LibraryManager()

@pytest.fixture
def manager_with_book():
    """Provides a LibraryManager with a single book added."""
    mgr = LibraryManager()
    mgr.add_book("Test Book", "Test Author", "1234567890")
    return mgr

def test_book_init():
    b = Book("Test Book", "Test Author", "1234567890")
    assert b.title == "Test Book"
    assert b.author == "Test Author"
    assert b.isbn == "1234567890"
    assert b.is_available is True

def test_book_str():
    b = Book("Test Book", "Test Author", "1234567890")
    expected = "[Available] Test Book by Test Author (ISBN: 1234567890)"
    assert str(b) == expected

def test_library_manager_init(empty_manager):
    assert isinstance(empty_manager.inventory, dict)
    assert not empty_manager.inventory  # should be empty

@pytest.mark.parametrize(
    "title,author,isbn,expected_output",
    [
        ("Test Book", "Test Author", "1234567890",
         "Success: Added 'Test Book' to the library.\n"),
        ("Test Book", "Test Author", "12",
         "[!] Error: ISBN '12' is too short.\n"),
    ]
)
def test_add_book_various(empty_manager, title, author, isbn, expected_output, capsys):
    empty_manager.add_book(title, author, isbn)
    captured = capsys.readouterr()
    assert captured.out == expected_output

def test_add_book_duplicate_isbn(manager_with_book, capsys):
    # Attempt to add another book with the same ISBN
    manager_with_book.add_book("Test Book 2", "Test Author 2", "1234567890")
    captured = capsys.readouterr()
    assert captured.out == "[!] Error: A book with ISBN 1234567890 already exists.\n"

def test_borrow_book_success(manager_with_book, capsys):
    manager_with_book.borrow_book("1234567890")
    captured = capsys.readouterr()
    assert captured.out == "Success: You have borrowed 'Test Book'.\n"
    # Verify status changed
    assert not manager_with_book.inventory["1234567890"].is_available

def test_borrow_book_unavailable(manager_with_book, capsys):
    # Borrow first to make it unavailable
    manager_with_book.borrow_book("1234567890")
    capsys.readouterr()  # clear previous output
    # Attempt to borrow again
    manager_with_book.borrow_book("1234567890")
    captured = capsys.readouterr()
    assert captured.out == "[!] Unavailable: 'Test Book' is currently borrowed by someone else.\n"

def test_borrow_book_not_found(empty_manager, capsys):
    empty_manager.borrow_book("9876543210")
    captured = capsys.readouterr()
    assert captured.out == "[!] Error: Book with ISBN 9876543210 not found.\n"

def test_return_book_success(manager_with_book, capsys):
    # Borrow first so it can be returned
    manager_with_book.borrow_book("1234567890")
    capsys.readouterr()
    manager_with_book.return_book("1234567890")
    captured = capsys.readouterr()
    assert captured.out == "Success: 'Test Book' has been returned.\n"
    assert manager_with_book.inventory["1234567890"].is_available

def test_return_book_already_returned(manager_with_book, capsys):
    # Ensure book is in returned state
    manager_with_book.return_book("1234567890")
    captured = capsys.readouterr()
    assert captured.out == "[!] Strange: You are trying to return 'Test Book', but it was already here.\n"

def test_return_book_not_found(empty_manager, capsys):
    empty_manager.return_book("9876543210")
    captured = capsys.readouterr()
    assert captured.out == "[!] Error: We do not own a book with ISBN 9876543210.\n"

def test_show_inventory_empty(empty_manager, capsys):
    empty_manager.show_inventory()
    captured = capsys.readouterr()
    expected = "\n--- Current Library Inventory ---\nThe library is empty.\n---------------------------------\n\n"
    assert captured.out == expected

def test_show_inventory_non_empty(manager_with_book, capsys):
    manager_with_book.show_inventory()
    captured = capsys.readouterr()
    # Build expected output dynamically to avoid hard‑coding line endings
    header = "\n--- Current Library Inventory ---\n"
    book_line = str(manager_with_book.inventory["1234567890"]) + "\n"
    footer = "---------------------------------\n\n"
    expected = header + book_line + footer
    assert captured.out == expected