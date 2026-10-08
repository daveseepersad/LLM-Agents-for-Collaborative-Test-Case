import pytest
from data.input_code.d04_library import Book, LibraryManager

def test_book_init():
    book = Book("Test Title", "Test Author", "1234567890")
    assert book.title == "Test Title"
    assert book.author == "Test Author"
    assert book.isbn == "1234567890"
    assert book.is_available == True

def test_book_str():
    book = Book("Test Title", "Test Author", "1234567890")
    assert str(book) == "[Available] Test Title by Test Author (ISBN: 1234567890)"

def test_library_manager_init():
    library = LibraryManager()
    assert library.inventory == {}

def test_add_book_success(capsys):
    library = LibraryManager()
    library.add_book("Test Title", "Test Author", "1234567890")
    captured = capsys.readouterr()
    assert "Success: Added 'Test Title' to the library." in captured.out
    assert len(library.inventory) == 1

def test_add_book_isbn_too_short(capsys):
    library = LibraryManager()
    library.add_book("Test Title", "Test Author", "12")
    captured = capsys.readouterr()
    assert "[!] Error: ISBN '12' is too short." in captured.out
    assert len(library.inventory) == 0

def test_add_book_duplicate_isbn(capsys):
    library = LibraryManager()
    library.add_book("Test Title", "Test Author", "1234567890")
    library.add_book("Test Title 2", "Test Author 2", "1234567890")
    captured = capsys.readouterr()
    assert "[!] Error: A book with ISBN 1234567890 already exists." in captured.out
    assert len(library.inventory) == 1

def test_borrow_book_success(capsys):
    library = LibraryManager()
    library.add_book("Test Title", "Test Author", "1234567890")
    library.borrow_book("1234567890")
    captured = capsys.readouterr()
    assert "Success: You have borrowed 'Test Title'." in captured.out
    assert not library.inventory["1234567890"].is_available

def test_borrow_book_not_found(capsys):
    library = LibraryManager()
    library.borrow_book("1234567890")
    captured = capsys.readouterr()
    assert "[!] Error: Book with ISBN 1234567890 not found." in captured.out

def test_borrow_book_already_borrowed(capsys):
    library = LibraryManager()
    library.add_book("Test Title", "Test Author", "1234567890")
    library.borrow_book("1234567890")
    library.borrow_book("1234567890")
    captured = capsys.readouterr()
    assert "[!] Unavailable: 'Test Title' is currently borrowed by someone else." in captured.out

def test_return_book_success(capsys):
    library = LibraryManager()
    library.add_book("Test Title", "Test Author", "1234567890")
    library.borrow_book("1234567890")
    library.return_book("1234567890")
    captured = capsys.readouterr()
    assert "Success: 'Test Title' has been returned." in captured.out
    assert library.inventory["1234567890"].is_available

def test_return_book_not_found(capsys):
    library = LibraryManager()
    library.return_book("1234567890")
    captured = capsys.readouterr()
    assert "[!] Error: We do not own a book with ISBN 1234567890." in captured.out

def test_return_book_already_returned(capsys):
    library = LibraryManager()
    library.add_book("Test Title", "Test Author", "1234567890")
    library.return_book("1234567890")
    captured = capsys.readouterr()
    assert "[!] Strange: You are trying to return 'Test Title', but it was already here." in captured.out

def test_show_inventory_empty(capsys):
    library = LibraryManager()
    library.show_inventory()
    captured = capsys.readouterr()
    assert "The library is empty." in captured.out

def test_show_inventory_not_empty(capsys):
    library = LibraryManager()
    library.add_book("Test Title", "Test Author", "1234567890")
    library.show_inventory()
    captured = capsys.readouterr()
    assert "[Available] Test Title by Test Author (ISBN: 1234567890)" in captured.out