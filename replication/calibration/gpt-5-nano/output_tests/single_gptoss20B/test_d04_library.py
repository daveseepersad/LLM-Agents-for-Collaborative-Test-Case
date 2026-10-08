import pytest
from data.input_code.d04_library import Book, LibraryManager

def test_book_str_and_availability():
    b = Book("1984", "George Orwell", "12345")
    assert str(b) == "[Available] 1984 by George Orwell (ISBN: 12345)"
    b.is_available = False
    assert str(b) == "[Borrowed] 1984 by George Orwell (ISBN: 12345)"

def test_add_book_validation_and_duplicate_and_success(capsys):
    mgr = LibraryManager()

    # Short ISBN should trigger error and not add
    mgr.add_book("Title", "Author", "12")
    out = capsys.readouterr().out
    assert "too short" in out
    assert "12" not in mgr.inventory

    # Valid addition
    mgr.add_book("Title", "Author", "123")
    out = capsys.readouterr().out
    assert "Success: Added 'Title' to the library." in out
    assert "123" in mgr.inventory
    assert isinstance(mgr.inventory["123"], Book)

    # Duplicate ISBN should trigger error and not re-add
    mgr.add_book("Another Title", "Another Author", "123")
    out = capsys.readouterr().out
    assert "A book with ISBN 123 already exists." in out

def test_borrow_and_return_flow(capsys):
    mgr = LibraryManager()
    mgr.add_book("BorrowTitle", "Borrower", "456")
    out = capsys.readouterr().out
    assert "Success: Added 'BorrowTitle' to the library." in out

    # Borrow when available
    mgr.borrow_book("456")
    out = capsys.readouterr().out
    assert "Success: You have borrowed 'BorrowTitle'." in out
    assert mgr.inventory["456"].is_available is False

    # Borrow again should be unavailable
    mgr.borrow_book("456")
    out = capsys.readouterr().out
    assert "Unavailable" in out

    # Return the book
    mgr.return_book("456")
    out = capsys.readouterr().out
    assert "'BorrowTitle' has been returned." in out
    assert mgr.inventory["456"].is_available is True

def test_return_not_present_and_strange_branch(capsys):
    mgr = LibraryManager()

    # Returning a non-existent book should trigger an error
    mgr.return_book("999")
    out = capsys.readouterr().out
    assert "We do not own a book with ISBN 999." in out

    # Add a book and attempt to return it while it's not borrowed -> should trigger strange message
    mgr.add_book("Title2", "Author2", "789")
    out = capsys.readouterr().out
    assert "Success: Added 'Title2' to the library." in out

    mgr.return_book("789")
    out = capsys.readouterr().out
    assert "Strange: You are trying to return" in out
    assert mgr.inventory["789"].is_available is True

def test_show_inventory_empty_and_with_books(capsys):
    mgr = LibraryManager()

    # Show inventory when empty
    mgr.show_inventory()
    out = capsys.readouterr().out
    assert "The library is empty." in out

    # Add a book and show inventory again
    mgr.add_book("SomeTitle", "SomeAuthor", "321")
    out = capsys.readouterr().out
    assert "Success: Added 'SomeTitle' to the library." in out

    mgr.show_inventory()
    out = capsys.readouterr().out
    assert "[Available] SomeTitle by SomeAuthor (ISBN: 321)" in out