import pytest
from data.input_code.d04_library import *

@pytest.mark.parametrize('title, author, isbn', [
    ("Test Book", "Test Author", "1234567890")
])
def test_book_init(title, author, isbn):
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
    library = LibraryManager()
    assert library.inventory == {}

@pytest.mark.parametrize('title, author, isbn, expected', [
    ("Test Book", "Test Author", "1234567890", "Success: Added 'Test Book' to the library."),
    ("Test Book", "Test Author", "12", "[!] Error: ISBN '12' is too short."),
])
def test_library_manager_add_book(capsys, title, author, isbn, expected):
    library = LibraryManager()
    library.add_book(title, author, isbn)
    captured = capsys.readouterr()
    assert captured.out.strip() == expected

def test_library_manager_add_duplicate_book(capsys):
    library = LibraryManager()
    library.add_book("Test Book", "Test Author", "1234567890")
    library.add_book("Test Book", "Test Author", "1234567890")
    captured = capsys.readouterr()
    assert captured.out.strip() == "Success: Added 'Test Book' to the library.\n[!] Error: A book with ISBN 1234567890 already exists."

@pytest.mark.parametrize('isbn, expected', [
    ("1234567890", "Success: Added 'Test Book' to the library.\nSuccess: You have borrowed 'Test Book'."),
    ("9876543210", "Success: Added 'Test Book' to the library.\n[!] Error: Book with ISBN 9876543210 not found."),
])
def test_library_manager_borrow_book(capsys, isbn, expected):
    library = LibraryManager()
    library.add_book("Test Book", "Test Author", "1234567890")
    library.borrow_book(isbn)
    captured = capsys.readouterr()
    assert captured.out.strip() == expected

def test_library_manager_borrow_unavailable_book(capsys):
    library = LibraryManager()
    library.add_book("Test Book", "Test Author", "1234567890")
    library.borrow_book("1234567890")
    library.borrow_book("1234567890")
    captured = capsys.readouterr()
    assert captured.out.strip() == "Success: Added 'Test Book' to the library.\nSuccess: You have borrowed 'Test Book'.\n[!] Unavailable: 'Test Book' is currently borrowed by someone else."

@pytest.mark.parametrize('isbn, expected', [
    ("1234567890", "Success: Added 'Test Book' to the library.\nSuccess: You have borrowed 'Test Book'.\nSuccess: 'Test Book' has been returned."),
    ("9876543210", "Success: Added 'Test Book' to the library.\nSuccess: You have borrowed 'Test Book'.\n[!] Error: We do not own a book with ISBN 9876543210."),
])
def test_library_manager_return_book(capsys, isbn, expected):
    library = LibraryManager()
    library.add_book("Test Book", "Test Author", "1234567890")
    library.borrow_book("1234567890")
    library.return_book(isbn)
    captured = capsys.readouterr()
    assert captured.out.strip() == expected

def test_library_manager_return_already_returned_book(capsys):
    library = LibraryManager()
    library.add_book("Test Book", "Test Author", "1234567890")
    library.borrow_book("1234567890")
    library.return_book("1234567890")
    library.return_book("1234567890")
    captured = capsys.readouterr()
    assert captured.out.strip() == "Success: Added 'Test Book' to the library.\nSuccess: You have borrowed 'Test Book'.\nSuccess: 'Test Book' has been returned.\n[!] Strange: You are trying to return 'Test Book', but it was already here."

def test_library_manager_show_inventory(capsys):
    library = LibraryManager()
    library.add_book("Test Book", "Test Author", "1234567890")
    library.show_inventory()
    captured = capsys.readouterr()
    assert "[Available] Test Book by Test Author (ISBN: 1234567890)" in captured.out

import pytest
from data.input_code.d04_library import *

def test_library_manager_show_empty_inventory(capsys):
    library = LibraryManager()
    library.show_inventory()
    captured = capsys.readouterr()
    assert "The library is empty." in captured.out

def test_library_manager_borrow_non_existent_book(capsys):
    library = LibraryManager()
    library.borrow_book("1234567890")
    captured = capsys.readouterr()
    assert captured.out.strip() == "[!] Error: Book with ISBN 1234567890 not found."

def test_library_manager_return_non_existent_book(capsys):
    library = LibraryManager()
    library.return_book("1234567890")
    captured = capsys.readouterr()
    assert captured.out.strip() == "[!] Error: We do not own a book with ISBN 1234567890."

def test_library_manager_show_inventory_after_borrow_return(capsys):
    library = LibraryManager()
    library.add_book("Test Book", "Test Author", "1234567890")
    library.borrow_book("1234567890")
    library.return_book("1234567890")
    library.show_inventory()
    captured = capsys.readouterr()
    assert "[Available] Test Book by Test Author (ISBN: 1234567890)" in captured.out