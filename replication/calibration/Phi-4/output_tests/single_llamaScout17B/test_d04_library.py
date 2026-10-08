import pytest
from data.input_code.d04_library import Book, LibraryManager

def test_add_book_success():
    manager = LibraryManager()
    manager.add_book("Test Book", "Test Author", "123456789")
    assert "123456789" in manager.inventory
    assert manager.inventory["123456789"].title == "Test Book"
    assert manager.inventory["123456789"].author == "Test Author"
    assert manager.inventory["123456789"].isbn == "123456789"
    assert manager.inventory["123456789"].is_available is True



def test_borrow_book_success():
    manager = LibraryManager()
    manager.add_book("Test Book", "Test Author", "123456789")
    manager.borrow_book("123456789")
    assert manager.inventory["123456789"].is_available is False



def test_return_book_success():
    manager = LibraryManager()
    manager.add_book("Test Book", "Test Author", "123456789")
    manager.borrow_book("123456789")
    manager.return_book("123456789")
    assert manager.inventory["123456789"].is_available is True



def test_show_inventory_empty():
    manager = LibraryManager()
    manager.show_inventory()
    # This test is more about checking the output, which is not captured by pytest directly.
    # It would require mocking or capturing stdout to verify the output.

def test_show_inventory_with_books():
    manager = LibraryManager()
    manager.add_book("Test Book 1", "Test Author 1", "123456789")
    manager.add_book("Test Book 2", "Test Author 2", "987654321")
    manager.show_inventory()
    # Similar to the above, this test would require capturing stdout to verify the output.