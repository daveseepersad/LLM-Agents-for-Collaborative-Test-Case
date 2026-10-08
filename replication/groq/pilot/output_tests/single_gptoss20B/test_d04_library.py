import pytest
from data.input_code.d04_library import Book, LibraryManager


def test_book_initial_is_available():
    book = Book("Title", "Author", "12345")
    assert book.is_available is True
    assert book.title == "Title"
    assert book.author == "Author"
    assert book.isbn == "12345"


def test_book_str_available_and_borrowed():
    book = Book("The Great Gatsby", "F. Scott Fitzgerald", "9780743273565")
    # Available state
    assert str(book) == "[Available] The Great Gatsby by F. Scott Fitzgerald (ISBN: 9780743273565)"
    # Borrow the book
    book.is_available = False
    assert str(book) == "[Borrowed] The Great Gatsby by F. Scott Fitzgerald (ISBN: 9780743273565)"


def test_add_book_invalid_isbn(capsys):
    manager = LibraryManager()
    result = manager.add_book("Book", "Author", "12")  # ISBN too short
    captured = capsys.readouterr()
    assert result is None
    assert "[!] Error: ISBN '12' is too short." in captured.out
    assert manager.inventory == {}


def test_add_book_duplicate(capsys):
    manager = LibraryManager()
    manager.add_book("First Book", "Author1", "ISBN123")
    captured1 = capsys.readouterr()
    assert "Success: Added 'First Book' to the library." in captured1.out
    # Attempt to add duplicate
    result = manager.add_book("Duplicate Book", "Author2", "ISBN123")
    captured2 = capsys.readouterr()
    assert result is None
    assert "[!] Error: A book with ISBN ISBN123 already exists." in captured2.out
    # Inventory should still contain only the first book
    assert len(manager.inventory) == 1
    assert "ISBN123" in manager.inventory
    assert manager.inventory["ISBN123"].title == "First Book"


def test_add_book_success(capsys):
    manager = LibraryManager()
    result = manager.add_book("New Book", "New Author", "ISBN456")
    captured = capsys.readouterr()
    assert result is None
    assert "Success: Added 'New Book' to the library." in captured.out
    assert "ISBN456" in manager.inventory
    assert manager.inventory["ISBN456"].title == "New Book"


def test_borrow_book_nonexistent(capsys):
    manager = LibraryManager()
    result = manager.borrow_book("NONEXISTENT")
    captured = capsys.readouterr()
    assert result is None
    assert "[!] Error: Book with ISBN NONEXISTENT not found." in captured.out


def test_borrow_book_success_and_already_borrowed(capsys):
    manager = LibraryManager()
    manager.add_book("Borrowable", "Author", "ISBN789")
    capsys.readouterr()  # clear output
    # Borrow the book
    result1 = manager.borrow_book("ISBN789")
    out1 = capsys.readouterr().out
    assert result1 is None
    assert "Success: You have borrowed 'Borrowable'." in out1
    assert manager.inventory["ISBN789"].is_available is False
    # Attempt to borrow again
    result2 = manager.borrow_book("ISBN789")
    out2 = capsys.readouterr().out
    assert result2 is None
    assert "[!] Unavailable: 'Borrowable' is currently borrowed by someone else." in out2
    # Status remains borrowed
    assert manager.inventory["ISBN789"].is_available is False


def test_return_book_nonexistent(capsys):
    manager = LibraryManager()
    result = manager.return_book("NONEXISTENT")
    captured = capsys.readouterr()
    assert result is None
    assert "[!] Error: We do not own a book with ISBN NONEXISTENT." in captured.out


def test_return_book_already_available(capsys):
    manager = LibraryManager()
    manager.add_book("Returnable", "Author", "ISBN321")
    capsys.readouterr()  # clear output
    # Return without borrowing
    result = manager.return_book("ISBN321")
    captured = capsys.readouterr()
    assert result is None
    assert "[!] Strange: You are trying to return 'Returnable', but it was already here." in captured.out
    assert manager.inventory["ISBN321"].is_available is True


def test_return_book_success(capsys):
    manager = LibraryManager()
    manager.add_book("Returnable", "Author", "ISBN321")
    capsys.readouterr()  # clear output
    # Borrow first
    manager.borrow_book("ISBN321")
    capsys.readouterr()  # clear output
    # Now return
    result = manager.return_book("ISBN321")
    captured = capsys.readouterr()
    assert result is None
    assert "Success: 'Returnable' has been returned." in captured.out
    assert manager.inventory["ISBN321"].is_available is True


def test_show_inventory_empty(capsys):
    manager = LibraryManager()
    manager.show_inventory()
    captured = capsys.readouterr()
    assert "\n--- Current Library Inventory ---" in captured.out
    assert "The library is empty." in captured.out
    assert "---------------------------------" in captured.out


def test_show_inventory_non_empty(capsys):
    manager = LibraryManager()
    manager.add_book("Book One", "Author A", "ISBN001")
    manager.add_book("Book Two", "Author B", "ISBN002")
    capsys.readouterr()  # clear output
    manager.show_inventory()
    captured = capsys.readouterr()
    # Header and footer
    assert "\n--- Current Library Inventory ---" in captured.out
    assert "---------------------------------" in captured.out
    # Each book string should appear
    assert "[Available] Book One by Author A (ISBN: ISBN001)" in captured.out
    assert "[Available] Book Two by Author B (ISBN: ISBN002)" in captured.out
    # No empty library message
    assert "The library is empty." not in captured.out


def test_inventory_contains_book_and_isbn_key():
    manager = LibraryManager()
    manager.add_book("Unique Book", "Unique Author", "UNIQUEISBN")
    assert "UNIQUEISBN" in manager.inventory
    assert manager.inventory["UNIQUEISBN"].title == "Unique Book"
    assert manager.inventory["UNIQUEISBN"].author == "Unique Author"
    assert manager.inventory["UNIQUEISBN"].isbn == "UNIQUEISBN"
    assert manager.inventory["UNIQUEISBN"].is_available is True
    # Borrow and check status
    manager.borrow_book("UNIQUEISBN")
    assert manager.inventory["UNIQUEISBN"].is_available is False
    # Return and check status
    manager.return_book("UNIQUEISBN")
    assert manager.inventory["UNIQUEISBN"].is_available is True