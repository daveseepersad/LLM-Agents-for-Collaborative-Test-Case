import pytest
from data.input_code.d04_library import *

def test_library_plan_execution(capsys):
    # T1_OK: Book.__init__
    book = Book(title="Test Book", author="Test Author", isbn="1234567890")
    assert book.title == "Test Book"
    assert book.author == "Test Author"
    assert book.isbn == "1234567890"
    assert book.is_available is True

    # T2_OK: Book.__str__
    assert str(book) == "[Available] Test Book by Test Author (ISBN: 1234567890)"

    # T3_OK: LibraryManager.__init__
    manager = LibraryManager()
    assert isinstance(manager.inventory, dict)
    assert manager.inventory == {}

    # T4_OK: LibraryManager.add_book
    manager.add_book(title="Test Book", author="Test Author", isbn="1234567890")
    out = capsys.readouterr().out
    assert "Success: Added 'Test Book' to the library." in out
    assert "1234567890" in manager.inventory
    assert manager.inventory["1234567890"].title == "Test Book"

    # T5_ERR: ISBN too short
    manager.add_book(title="Test Book", author="Test Author", isbn="12")
    out = capsys.readouterr().out
    assert "[!] Error: ISBN '12' is too short." in out
    assert len(manager.inventory) == 1  # No new book added

    # T6_ERR: Duplicate ISBN
    manager.add_book(title="Test Book", author="Test Author", isbn="1234567890")
    out = capsys.readouterr().out
    assert "[!] Error: A book with ISBN 1234567890 already exists." in out
    assert len(manager.inventory) == 1

    # T7_OK: borrow_book
    manager.borrow_book(isbn="1234567890")
    out = capsys.readouterr().out
    assert "Success: You have borrowed 'Test Book'." in out
    assert manager.inventory["1234567890"].is_available is False

    # T8_ERR: borrow non-existent ISBN
    manager.borrow_book(isbn="9876543210")
    out = capsys.readouterr().out
    assert "[!] Error: Book with ISBN 9876543210 not found." in out

    # T9_ERR: borrow already borrowed
    manager.borrow_book(isbn="1234567890")
    out = capsys.readouterr().out
    assert "[!] Unavailable: 'Test Book' is currently borrowed by someone else." in out

    # T10_OK: return_book
    manager.return_book(isbn="1234567890")
    out = capsys.readouterr().out
    assert "Success: 'Test Book' has been returned." in out
    assert manager.inventory["1234567890"].is_available is True

    # T11_ERR: return non-existent ISBN
    manager.return_book(isbn="9876543210")
    out = capsys.readouterr().out
    assert "[!] Error: We do not own a book with ISBN 9876543210." in out

    # T12_ERR: return already here
    manager.return_book(isbn="1234567890")
    out = capsys.readouterr().out
    assert "[!] Strange: You are trying to return 'Test Book', but it was already here." in out

    # T13_OK: show_inventory (should print current inventory)
    manager.show_inventory()
    out = capsys.readouterr().out
    assert "Current Library Inventory" in out or "Test Book" in out

    # T14_OK: show_inventory on empty library (new instance)
    empty_manager = LibraryManager()
    empty_manager.show_inventory()
    out = capsys.readouterr().out
    assert "The library is empty." in out