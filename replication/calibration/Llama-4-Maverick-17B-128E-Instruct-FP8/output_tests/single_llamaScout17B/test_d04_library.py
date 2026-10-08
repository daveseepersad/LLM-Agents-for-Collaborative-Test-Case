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
    library = LibraryManager()
    assert library.inventory == {}

def test_add_book_valid():
    library = LibraryManager()
    library.add_book("Title", "Author", "1234567890")
    assert "1234567890" in library.inventory

def test_add_book_isbn_too_short(capsys):
    library = LibraryManager()
    library.add_book("Title", "Author", "12")
    captured = capsys.readouterr()
    assert "[!] Error: ISBN '12' is too short." in captured.out

def test_add_book_duplicate_isbn(capsys):
    library = LibraryManager()
    library.add_book("Title", "Author", "1234567890")
    library.add_book("Another Title", "Another Author", "1234567890")
    captured = capsys.readouterr()
    assert "[!] Error: A book with ISBN 1234567890 already exists." in captured.out

def test_borrow_book_not_found(capsys):
    library = LibraryManager()
    library.borrow_book("1234567890")
    captured = capsys.readouterr()
    assert "[!] Error: Book with ISBN 1234567890 not found." in captured.out

def test_borrow_book_already_borrowed(capsys):
    library = LibraryManager()
    library.add_book("Title", "Author", "1234567890")
    library.borrow_book("1234567890")
    library.borrow_book("1234567890")
    captured = capsys.readouterr()
    assert "[!] Unavailable: 'Title' is currently borrowed by someone else." in captured.out

def test_borrow_book_success(capsys):
    library = LibraryManager()
    library.add_book("Title", "Author", "1234567890")
    library.borrow_book("1234567890")
    captured = capsys.readouterr()
    assert "Success: You have borrowed 'Title'." in captured.out

def test_return_book_not_found(capsys):
    library = LibraryManager()
    library.return_book("1234567890")
    captured = capsys.readouterr()
    assert "[!] Error: We do not own a book with ISBN 1234567890." in captured.out

def test_return_book_not_borrowed(capsys):
    library = LibraryManager()
    library.add_book("Title", "Author", "1234567890")
    library.return_book("1234567890")
    captured = capsys.readouterr()
    assert "[!] Strange: You are trying to return 'Title', but it was already here." in captured.out

def test_return_book_success(capsys):
    library = LibraryManager()
    library.add_book("Title", "Author", "1234567890")
    library.borrow_book("1234567890")
    library.return_book("1234567890")
    captured = capsys.readouterr()
    assert "Success: 'Title' has been returned." in captured.out

def test_show_inventory_empty(capsys):
    library = LibraryManager()
    library.show_inventory()
    captured = capsys.readouterr()
    assert "The library is empty." in captured.out

def test_show_inventory_not_empty(capsys):
    library = LibraryManager()
    library.add_book("Title", "Author", "1234567890")
    library.show_inventory()
    captured = capsys.readouterr()
    assert "[Available] Title by Author (ISBN: 1234567890)" in captured.out