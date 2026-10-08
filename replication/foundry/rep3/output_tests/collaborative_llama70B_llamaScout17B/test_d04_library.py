import pytest
from data.input_code.d04_library import *

@pytest.mark.parametrize('title, author, isbn, expected', [
    ("Test Book", "Test Author", "1234567890", None)
])
def test_book_init(title, author, isbn, expected, capsys):
    book = Book(title, author, isbn)
    assert book.title == title
    assert book.author == author
    assert book.isbn == isbn
    assert book.is_available == True

@pytest.mark.parametrize('title, author, isbn, expected', [
    ("Test Book", "Test Author", "1234567890", "[Available] Test Book by Test Author (ISBN: 1234567890)")
])
def test_book_str(title, author, isbn, expected):
    book = Book(title, author, isbn)
    assert str(book) == expected

def test_library_manager_init():
    library_manager = LibraryManager()
    assert library_manager.inventory == {}

@pytest.mark.parametrize('title, author, isbn, expected', [
    ("Test Book", "Test Author", "1234567890", "Success: Added 'Test Book' to the library."),
    ("Test Book", "Test Author", "12", "[!] Error: ISBN '12' is too short."),
])
def test_library_manager_add_book(title, author, isbn, expected, capsys):
    library_manager = LibraryManager()
    library_manager.add_book(title, author, isbn)
    captured = capsys.readouterr()
    assert captured.out.strip() == expected

def test_library_manager_add_book_duplicate_isbn(capsys):
    library_manager = LibraryManager()
    library_manager.add_book("Test Book", "Test Author", "1234567890")
    library_manager.add_book("Test Book 2", "Test Author 2", "1234567890")
    captured = capsys.readouterr()
    assert captured.out.strip() == "Success: Added 'Test Book' to the library.\n[!] Error: A book with ISBN 1234567890 already exists."

@pytest.mark.parametrize('isbn, expected', [
    ("1234567890", "Success: You have borrowed 'Test Book'."),
    ("9876543210", "[!] Error: Book with ISBN 9876543210 not found."),
])
def test_library_manager_borrow_book(isbn, expected, capsys):
    library_manager = LibraryManager()
    library_manager.add_book("Test Book", "Test Author", "1234567890")
    library_manager.borrow_book(isbn)
    captured = capsys.readouterr()
    assert captured.out.strip() == "Success: Added 'Test Book' to the library.\n" + expected

def test_library_manager_borrow_book_unavailable(capsys):
    library_manager = LibraryManager()
    library_manager.add_book("Test Book", "Test Author", "1234567890")
    library_manager.borrow_book("1234567890")
    library_manager.borrow_book("1234567890")
    captured = capsys.readouterr()
    assert captured.out.strip() == "Success: Added 'Test Book' to the library.\nSuccess: You have borrowed 'Test Book'.\n[!] Unavailable: 'Test Book' is currently borrowed by someone else."

@pytest.mark.parametrize('isbn, expected', [
    ("1234567890", "Success: 'Test Book' has been returned."),
    ("9876543210", "[!] Error: We do not own a book with ISBN 9876543210."),
])
def test_library_manager_return_book(isbn, expected, capsys):
    library_manager = LibraryManager()
    library_manager.add_book("Test Book", "Test Author", "1234567890")
    library_manager.borrow_book("1234567890")
    library_manager.return_book(isbn)
    captured = capsys.readouterr()
    assert captured.out.strip() == "Success: Added 'Test Book' to the library.\nSuccess: You have borrowed 'Test Book'.\n" + expected

def test_library_manager_return_book_already_returned(capsys):
    library_manager = LibraryManager()
    library_manager.add_book("Test Book", "Test Author", "1234567890")
    library_manager.return_book("1234567890")
    captured = capsys.readouterr()
    assert captured.out.strip() == "Success: Added 'Test Book' to the library.\n[!] Strange: You are trying to return 'Test Book', but it was already here."

def test_library_manager_show_inventory_empty(capsys):
    library_manager = LibraryManager()
    library_manager.show_inventory()
    captured = capsys.readouterr()
    assert "The library is empty." in captured.out

def test_library_manager_show_inventory_non_empty(capsys):
    library_manager = LibraryManager()
    library_manager.add_book("Test Book", "Test Author", "1234567890")
    library_manager.show_inventory()
    captured = capsys.readouterr()
    assert "[Available] Test Book by Test Author (ISBN: 1234567890)" in captured.out