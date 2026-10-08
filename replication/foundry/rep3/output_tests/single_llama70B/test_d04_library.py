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
    assert captured.out == "Success: Added 'Test Title' to the library.\n"
    assert len(library.inventory) == 1

def test_add_book_isbn_too_short(capsys):
    library = LibraryManager()
    library.add_book("Test Title", "Test Author", "12")
    captured = capsys.readouterr()
    assert captured.out == "[!] Error: ISBN '12' is too short.\n"
    assert len(library.inventory) == 0

def test_add_book_duplicate_isbn(capsys):
    library = LibraryManager()
    library.add_book("Test Title", "Test Author", "1234567890")
    library.add_book("Test Title 2", "Test Author 2", "1234567890")
    captured = capsys.readouterr()
    assert captured.out == "Success: Added 'Test Title' to the library.\n[!] Error: A book with ISBN 1234567890 already exists.\n"
    assert len(library.inventory) == 1

def test_borrow_book_success(capsys):
    library = LibraryManager()
    library.add_book("Test Title", "Test Author", "1234567890")
    library.borrow_book("1234567890")
    captured = capsys.readouterr()
    assert captured.out == "Success: Added 'Test Title' to the library.\nSuccess: You have borrowed 'Test Title'.\n"
    assert not library.inventory["1234567890"].is_available

def test_borrow_book_not_found(capsys):
    library = LibraryManager()
    library.borrow_book("1234567890")
    captured = capsys.readouterr()
    assert captured.out == "[!] Error: Book with ISBN 1234567890 not found.\n"
    assert len(library.inventory) == 0

def test_borrow_book_already_borrowed(capsys):
    library = LibraryManager()
    library.add_book("Test Title", "Test Author", "1234567890")
    library.borrow_book("1234567890")
    library.borrow_book("1234567890")
    captured = capsys.readouterr()
    assert captured.out == "Success: Added 'Test Title' to the library.\nSuccess: You have borrowed 'Test Title'.\n[!] Unavailable: 'Test Title' is currently borrowed by someone else.\n"
    assert not library.inventory["1234567890"].is_available

def test_return_book_success(capsys):
    library = LibraryManager()
    library.add_book("Test Title", "Test Author", "1234567890")
    library.borrow_book("1234567890")
    library.return_book("1234567890")
    captured = capsys.readouterr()
    assert captured.out == "Success: Added 'Test Title' to the library.\nSuccess: You have borrowed 'Test Title'.\nSuccess: 'Test Title' has been returned.\n"
    assert library.inventory["1234567890"].is_available

def test_return_book_not_found(capsys):
    library = LibraryManager()
    library.return_book("1234567890")
    captured = capsys.readouterr()
    assert captured.out == "[!] Error: We do not own a book with ISBN 1234567890.\n"
    assert len(library.inventory) == 0

def test_return_book_already_returned(capsys):
    library = LibraryManager()
    library.add_book("Test Title", "Test Author", "1234567890")
    library.return_book("1234567890")
    captured = capsys.readouterr()
    assert captured.out == "Success: Added 'Test Title' to the library.\n[!] Strange: You are trying to return 'Test Title', but it was already here.\n"
    assert library.inventory["1234567890"].is_available


