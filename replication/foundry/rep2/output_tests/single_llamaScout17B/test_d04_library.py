import pytest
from data.input_code.d04_library import Book, LibraryManager

def test_book_initialization():
    book = Book("Title", "Author", "1234567890")
    assert book.title == "Title"
    assert book.author == "Author"
    assert book.isbn == "1234567890"
    assert book.is_available

def test_book_str_representation():
    book = Book("Title", "Author", "1234567890")
    assert str(book) == "[Available] Title by Author (ISBN: 1234567890)"
    book.is_available = False
    assert str(book) == "[Borrowed] Title by Author (ISBN: 1234567890)"

def test_library_manager_initialization():
    manager = LibraryManager()
    assert manager.inventory == {}

def test_add_book_valid():
    manager = LibraryManager()
    manager.add_book("Title", "Author", "1234567890")
    assert "1234567890" in manager.inventory

def test_add_book_isbn_too_short(capsys):
    manager = LibraryManager()
    manager.add_book("Title", "Author", "12")
    captured = capsys.readouterr()
    assert "[!] Error: ISBN '12' is too short." in captured.out

def test_add_book_duplicate(capsys):
    manager = LibraryManager()
    manager.add_book("Title", "Author", "1234567890")
    manager.add_book("Title2", "Author2", "1234567890")
    captured = capsys.readouterr()
    assert "[!] Error: A book with ISBN 1234567890 already exists." in captured.out

def test_borrow_book_not_found(capsys):
    manager = LibraryManager()
    manager.borrow_book("1234567890")
    captured = capsys.readouterr()
    assert "[!] Error: Book with ISBN 1234567890 not found." in captured.out

def test_borrow_book_already_borrowed(capsys):
    manager = LibraryManager()
    manager.add_book("Title", "Author", "1234567890")
    manager.borrow_book("1234567890")
    manager.borrow_book("1234567890")
    captured = capsys.readouterr()
    assert "[!] Unavailable: 'Title' is currently borrowed by someone else." in captured.out

def test_borrow_book_success(capsys):
    manager = LibraryManager()
    manager.add_book("Title", "Author", "1234567890")
    manager.borrow_book("1234567890")
    captured = capsys.readouterr()
    assert "Success: You have borrowed 'Title'." in captured.out

def test_return_book_not_found(capsys):
    manager = LibraryManager()
    manager.return_book("1234567890")
    captured = capsys.readouterr()
    assert "[!] Error: We do not own a book with ISBN 1234567890." in captured.out

def test_return_book_not_borrowed(capsys):
    manager = LibraryManager()
    manager.add_book("Title", "Author", "1234567890")
    manager.return_book("1234567890")
    captured = capsys.readouterr()
    assert "[!] Strange: You are trying to return 'Title', but it was already here." in captured.out

def test_return_book_success(capsys):
    manager = LibraryManager()
    manager.add_book("Title", "Author", "1234567890")
    manager.borrow_book("1234567890")
    manager.return_book("1234567890")
    captured = capsys.readouterr()
    assert "Success: 'Title' has been returned." in captured.out

def test_show_inventory_empty(capsys):
    manager = LibraryManager()
    manager.show_inventory()
    captured = capsys.readouterr()
    assert "The library is empty." in captured.out

def test_show_inventory_not_empty(capsys):
    manager = LibraryManager()
    manager.add_book("Title", "Author", "1234567890")
    manager.show_inventory()
    captured = capsys.readouterr()
    assert "[Available] Title by Author (ISBN: 1234567890)" in captured.out