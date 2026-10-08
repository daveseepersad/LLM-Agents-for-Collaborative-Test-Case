import pytest
from data.input_code.d04_library import *

@pytest.fixture
def lib():
    return LibraryManager()

def test_book_initialization():
    b = Book(title="Test", author="Author", isbn="123")
    assert b.title == "Test"
    assert b.author == "Author"
    assert b.isbn == "123"
    assert b.is_available is True

@pytest.mark.parametrize(
    "is_available,expected_str",
    [
        (True, "[Available] Test by Author (ISBN: 123)"),
        (False, "[Borrowed] Test by Author (ISBN: 123)"),
    ],
)
def test_book_str(is_available, expected_str):
    b = Book(title="Test", author="Author", isbn="123")
    b.is_available = is_available
    assert str(b) == expected_str

def test_add_book_success(lib, capsys):
    lib.add_book(title="Test Book", author="Test Author", isbn="123")
    captured = capsys.readouterr()
    assert "Success: Added 'Test Book' to the library." in captured.out
    assert "123" in lib.inventory
    book = lib.inventory["123"]
    assert isinstance(book, Book)
    assert book.title == "Test Book"
    assert book.author == "Test Author"
    assert book.is_available is True

def test_add_book_isbn_too_short(lib, capsys):
    lib.add_book(title="Test Book", author="Test Author", isbn="12")
    captured = capsys.readouterr()
    assert "Error: ISBN '12' is too short." in captured.out
    assert "12" not in lib.inventory

def test_add_book_duplicate_isbn(lib, capsys):
    lib.add_book(title="First", author="A", isbn="123")
    lib.add_book(title="Second", author="B", isbn="123")
    captured = capsys.readouterr()
    # First addition success message
    assert "Success: Added 'First' to the library." in captured.out
    # Duplicate warning
    assert "Error: A book with ISBN 123 already exists." in captured.out
    # Inventory should still have only the first book
    assert len(lib.inventory) == 1
    assert lib.inventory["123"].title == "First"

@pytest.mark.parametrize(
    "setup,action,expected_msg,final_status",
    [
        # Borrow existing available book
        (lambda lib: lib.add_book("B1", "A1", "123"), 
         lambda lib: lib.borrow_book("123"),
         "Success: You have borrowed 'B1'.",
         False),
        # Borrow non‑existent book
        (lambda lib: None,
         lambda lib: lib.borrow_book("999"),
         "Error: Book with ISBN 999 not found.",
         None),
        # Borrow already borrowed book
        (lambda lib: (lib.add_book("B2", "A2", "124"), lib.borrow_book("124")),
         lambda lib: lib.borrow_book("124"),
         "Unavailable: 'B2' is currently borrowed by someone else.",
         False),
    ],
)
def test_borrow_book(lib, capsys, setup, action, expected_msg, final_status):
    if setup:
        setup(lib)
    action(lib)
    captured = capsys.readouterr()
    assert expected_msg in captured.out
    if final_status is not None:
        assert lib.inventory["123" if "123" in lib.inventory else "124"].is_available == final_status

def test_return_book_scenarios(lib, capsys):
    # Return non‑existent book
    lib.return_book("999")
    out = capsys.readouterr().out
    assert "Error: We do not own a book with ISBN 999." in out

    # Return borrowed book
    lib.add_book("B3", "A3", "125")
    lib.borrow_book("125")
    capsys.readouterr()  # clear previous output
    lib.return_book("125")
    out = capsys.readouterr().out
    assert "Success: 'B3' has been returned." in out
    assert lib.inventory["125"].is_available is True

    # Return already available book
    lib.return_book("125")
    out = capsys.readouterr().out
    assert "Strange: You are trying to return 'B3', but it was already here." in out

def test_show_inventory_empty(lib, capsys):
    lib.show_inventory()
    out = capsys.readouterr().out
    assert "The library is empty." in out

def test_show_inventory_non_empty(lib, capsys):
    lib.add_book("B4", "A4", "126")
    capsys.readouterr()  # clear add_book output
    lib.show_inventory()
    out = capsys.readouterr().out
    assert "[Available] B4 by A4 (ISBN: 126)" in out