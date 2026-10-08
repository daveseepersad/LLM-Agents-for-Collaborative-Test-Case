import pytest
from data.input_code.d04_library import *

@pytest.fixture
def manager():
    """Provides a fresh LibraryManager instance."""
    return LibraryManager()

@pytest.fixture
def filled_manager(manager):
    """LibraryManager with one book added (ISBN: 1234567890)."""
    manager.add_book("Test Book", "Test Author", "1234567890")
    return manager

def test_book_init():
    """T1_BOOK_INIT: Ensure Book can be instantiated without error."""
    book = Book("Test Book", "Test Author", "1234567890")
    assert isinstance(book, Book)

@pytest.mark.parametrize(
    "title, author, isbn, expected_str",
    [
        ("Test Book", "Test Author", "1234567890",
         "[Available] Test Book by Test Author (ISBN: 1234567890)"),
    ],
)
def test_book_str(title, author, isbn, expected_str):
    """T2_BOOK_STR: Verify __str__ output."""
    book = Book(title, author, isbn)
    assert str(book) == expected_str

def test_library_manager_init():
    """T3_LIB_INIT: LibraryManager starts with empty inventory."""
    lib = LibraryManager()
    assert lib.inventory == {}

@pytest.mark.parametrize(
    "title, author, isbn, expected_output",
    [
        ("Test Book", "Test Author", "1234567890",
         "Success: Added 'Test Book' to the library.\n"),
        ("Test Book", "Test Author", "12",
         "[!] Error: ISBN '12' is too short.\n"),
    ],
)
def test_add_book_cases(manager, title, author, isbn, expected_output, capsys):
    """T4_ADD_BOOK_OK and T5_ADD_BOOK_SHORT_ISBN."""
    manager.add_book(title, author, isbn)
    captured = capsys.readouterr()
    assert captured.out == expected_output

def test_add_book_duplicate_isbn(filled_manager, capsys):
    """T6_ADD_BOOK_DUPLICATE_ISBN."""
    filled_manager.add_book("Test Book 2", "Test Author 2", "1234567890")
    captured = capsys.readouterr()
    assert captured.out == "[!] Error: A book with ISBN 1234567890 already exists.\n"

@pytest.mark.parametrize(
    "isbn, expected_output",
    [
        ("1234567890", "Success: You have borrowed 'Test Book'.\n"),
    ],
)
def test_borrow_book_success(filled_manager, isbn, expected_output, capsys):
    """T7_BORROW_BOOK_OK."""
    filled_manager.borrow_book(isbn)
    captured = capsys.readouterr()
    assert captured.out == expected_output

def test_borrow_book_unavailable(filled_manager, capsys):
    """T8_BORROW_BOOK_UNAVAILABLE."""
    # Borrow first to make it unavailable
    filled_manager.borrow_book("1234567890")
    capsys.readouterr()  # clear previous output
    # Attempt second borrow
    filled_manager.borrow_book("1234567890")
    captured = capsys.readouterr()
    assert captured.out == "[!] Unavailable: 'Test Book' is currently borrowed by someone else.\n"

def test_borrow_book_not_found(manager, capsys):
    """T9_BORROW_BOOK_NOT_FOUND."""
    manager.borrow_book("9876543210")
    captured = capsys.readouterr()
    assert captured.out == "[!] Error: Book with ISBN 9876543210 not found.\n"

def test_return_book_success(filled_manager, capsys):
    """T10_RETURN_BOOK_OK."""
    # Borrow first so it can be returned
    filled_manager.borrow_book("1234567890")
    capsys.readouterr()  # clear output
    filled_manager.return_book("1234567890")
    captured = capsys.readouterr()
    assert captured.out == "Success: 'Test Book' has been returned.\n"

def test_return_book_already_returned(filled_manager, capsys):
    """T11_RETURN_BOOK_ALREADY_RETURNED."""
    # Ensure book is in returned state
    filled_manager.return_book("1234567890")  # first call will print error because it's already available
    captured = capsys.readouterr()
    assert captured.out == "[!] Strange: You are trying to return 'Test Book', but it was already here.\n"

def test_return_book_not_found(manager, capsys):
    """T12_RETURN_BOOK_NOT_FOUND."""
    manager.return_book("9876543210")
    captured = capsys.readouterr()
    assert captured.out == "[!] Error: We do not own a book with ISBN 9876543210.\n"

def test_show_inventory_empty(manager, capsys):
    """T13_SHOW_INVENTORY_EMPTY."""
    manager.show_inventory()
    captured = capsys.readouterr()
    expected = "\n--- Current Library Inventory ---\nThe library is empty.\n---------------------------------\n\n"
    assert captured.out == expected

def test_show_inventory_non_empty(filled_manager, capsys):
    """T14_SHOW_INVENTORY_NON_EMPTY."""
    filled_manager.show_inventory()
    captured = capsys.readouterr()
    expected_start = "\n--- Current Library Inventory ---\n"
    expected_book_line = "[Available] Test Book by Test Author (ISBN: 1234567890)\n"
    expected_end = "---------------------------------\n\n"
    assert captured.out.startswith(expected_start)
    assert expected_book_line in captured.out
    assert captured.out.endswith(expected_end)