import pytest
from data.input_code.d04_library import *

@pytest.fixture
def manager():
    return LibraryManager()

def test_add_book_short_isbn(manager, capsys):
    # Attempt to add a book with an ISBN shorter than 3 characters
    manager.add_book(title="Sample", author="Author", isbn="12")
    captured = capsys.readouterr()
    # Verify that an error message was printed
    assert "[!] Error: ISBN '12' is too short." in captured.out
    # The book should not be added to the inventory
    assert "12" not in manager.inventory

@pytest.mark.parametrize(
    "title,author,isbn",
    [
        ("1984", "George Orwell", "123"),
    ],
)
def test_add_book_valid(manager, title, author, isbn, capsys):
    # Add a valid book
    manager.add_book(title=title, author=author, isbn=isbn)
    captured = capsys.readouterr()
    # Verify success message
    assert f"Success: Added '{title}' to the library." in captured.out
    # The book should be present in the inventory with correct attributes
    assert isbn in manager.inventory
    book = manager.inventory[isbn]
    assert isinstance(book, Book)
    assert book.title == title
    assert book.author == author
    assert book.isbn == isbn
    assert book.is_available is True

def test_borrow_non_existent(manager, capsys):
    # Attempt to borrow a book that does not exist
    manager.borrow_book(isbn="999")
    captured = capsys.readouterr()
    # Verify appropriate error message
    assert "[!] Error: Book with ISBN 999 not found." in captured.out
    # Inventory should remain unchanged (still empty)
    assert not manager.inventory

def test_return_non_existent(manager, capsys):
    # Attempt to return a book that does not exist
    manager.return_book(isbn="999")
    captured = capsys.readouterr()
    # Verify appropriate error message
    assert "[!] Error: We do not own a book with ISBN 999." in captured.out
    # Inventory should remain unchanged (still empty)
    assert not manager.inventory

def test_show_inventory_empty(manager, capsys):
    # Show inventory when it is empty
    manager.show_inventory()
    captured = capsys.readouterr()
    # Verify that the empty library message is printed
    assert "The library is empty." in captured.out

import pytest
from data.input_code.d04_library import *

def test_add_book_duplicate_isbn(manager, capsys):
    # First add a valid book
    manager.add_book(title="Original", author="Author", isbn="123")
    # Attempt to add another book with the same ISBN
    manager.add_book(title="Duplicate", author="Author", isbn="123")
    captured = capsys.readouterr()
    # Verify duplicate error message
    assert "[!] Error: A book with ISBN 123 already exists." in captured.out
    # Inventory should still contain only the original book
    assert len(manager.inventory) == 1
    assert manager.inventory["123"].title == "Original"

def test_borrow_and_return_flow(manager, capsys):
    # Add a book to borrow and later return
    manager.add_book(title="FlowBook", author="Author", isbn="777")
    # Borrow the book
    manager.borrow_book(isbn="777")
    borrow_out = capsys.readouterr().out
    assert "Success: You have borrowed 'FlowBook'." in borrow_out
    assert not manager.inventory["777"].is_available
    # Return the book
    manager.return_book(isbn="777")
    return_out = capsys.readouterr().out
    assert "Success: 'FlowBook' has been returned." in return_out
    assert manager.inventory["777"].is_available

def test_borrow_already_borrowed(manager, capsys):
    # Add and borrow the book first
    manager.add_book(title="Locked", author="Author", isbn="888")
    manager.borrow_book(isbn="888")
    _ = capsys.readouterr()  # clear previous output
    # Attempt to borrow again
    manager.borrow_book(isbn="888")
    captured = capsys.readouterr()
    assert "[!] Unavailable: 'Locked' is currently borrowed by someone else." in captured.out
    # Status should remain borrowed
    assert not manager.inventory["888"].is_available

def test_return_strange_when_not_borrowed(manager, capsys):
    # Add a book but do not borrow it
    manager.add_book(title="NeverBorrowed", author="Author", isbn="999")
    # Attempt to return it
    manager.return_book(isbn="999")
    captured = capsys.readouterr()
    assert "[!] Strange: You are trying to return 'NeverBorrowed', but it was already here." in captured.out
    # Ensure the book is still marked as available
    assert manager.inventory["999"].is_available

def test_show_inventory_non_empty(manager, capsys):
    # Add multiple books
    manager.add_book(title="BookOne", author="AuthorA", isbn="111")
    manager.add_book(title="BookTwo", author="AuthorB", isbn="222")
    # Show inventory
    manager.show_inventory()
    captured = capsys.readouterr().out
    # Verify header and footer are present
    assert "--- Current Library Inventory ---" in captured
    assert "---------------------------------" in captured
    # Verify each book's string representation appears
    assert "[Available] BookOne by AuthorA (ISBN: 111)" in captured
    assert "[Available] BookTwo by AuthorB (ISBN: 222)" in captured