import pytest
from data.input_code.d04_library import *

@pytest.fixture
def manager():
    return LibraryManager()

def test_book_initialization():
    b = Book(title="Test", author="Test Author", isbn="12345")
    assert b.title == "Test"
    assert b.author == "Test Author"
    assert b.isbn == "12345"
    assert b.is_available is True

@pytest.mark.parametrize(
    "is_available, expected_str",
    [
        (True, "[Available] Test by Test Author (ISBN: 12345)"),
        (False, "[Borrowed] Test by Test Author (ISBN: 12345)"),
    ],
)
def test_book_str(is_available, expected_str):
    b = Book(title="Test", author="Test Author", isbn="12345")
    b.is_available = is_available
    assert str(b) == expected_str

def test_add_book_success(manager, capsys):
    manager.add_book(title="1984", author="George Orwell", isbn="1234567890")
    captured = capsys.readouterr()
    assert "Success: Added '1984' to the library." in captured.out
    assert "1234567890" in manager.inventory
    assert isinstance(manager.inventory["1234567890"], Book)

def test_add_book_short_isbn(manager, capsys):
    manager.add_book(title="Short ISBN", author="Author", isbn="12")
    captured = capsys.readouterr()
    assert "Error: ISBN '12' is too short." in captured.out
    assert "12" not in manager.inventory

def test_add_book_duplicate_isbn(manager, capsys):
    manager.add_book(title="First", author="A", isbn="111")
    manager.add_book(title="Duplicate", author="B", isbn="111")
    captured = capsys.readouterr()
    # The second call should produce duplicate error
    assert "Error: A book with ISBN 111 already exists." in captured.out
    # Inventory should still have only one entry with original title
    assert manager.inventory["111"].title == "First"

@pytest.mark.parametrize(
    "setup, action, expected_msg, final_status",
    [
        # borrow existing book
        (
            lambda m: m.add_book("1984", "George Orwell", "1234567890"),
            lambda m: m.borrow_book("1234567890"),
            "Success: You have borrowed '1984'.",
            False,
        ),
        # borrow non‑existent book
        (
            lambda m: None,
            lambda m: m.borrow_book("notfound"),
            "Error: Book with ISBN notfound not found.",
            None,
        ),
        # borrow already borrowed book
        (
            lambda m: (m.add_book("1984", "George Orwell", "1234567890"), m.borrow_book("1234567890")),
            lambda m: m.borrow_book("1234567890"),
            "Unavailable: '1984' is currently borrowed by someone else.",
            False,
        ),
    ],
)
def test_borrow_book(manager, capsys, setup, action, expected_msg, final_status):
    if setup:
        setup(manager)
    action(manager)
    captured = capsys.readouterr()
    assert expected_msg in captured.out
    if final_status is not None:
        assert manager.inventory["1234567890"].is_available is final_status

@pytest.mark.parametrize(
    "setup, action, expected_msg, final_status",
    [
        # return borrowed book
        (
            lambda m: (m.add_book("1984", "George Orwell", "1234567890"), m.borrow_book("1234567890")),
            lambda m: m.return_book("1234567890"),
            "Success: '1984' has been returned.",
            True,
        ),
        # return non‑existent book
        (
            lambda m: None,
            lambda m: m.return_book("notfound"),
            "Error: We do not own a book with ISBN notfound.",
            None,
        ),
        # return already returned book
        (
            lambda m: m.add_book("1984", "George Orwell", "1234567890"),
            lambda m: m.return_book("1234567890"),
            "Strange: You are trying to return '1984', but it was already here.",
            True,
        ),
    ],
)
def test_return_book(manager, capsys, setup, action, expected_msg, final_status):
    if setup:
        setup(manager)
    action(manager)
    captured = capsys.readouterr()
    assert expected_msg in captured.out
    if final_status is not None:
        assert manager.inventory["1234567890"].is_available is final_status

def test_show_inventory_empty(manager, capsys):
    manager.show_inventory()
    captured = capsys.readouterr()
    assert "The library is empty." in captured.out

def test_show_inventory_non_empty(manager, capsys):
    manager.add_book("1984", "George Orwell", "1234567890")
    manager.show_inventory()
    captured = capsys.readouterr()
    # Should contain the header and the book string representation
    assert "--- Current Library Inventory ---" in captured.out
    assert "[Available] 1984 by George Orwell (ISBN: 1234567890)" in captured.out