import pytest
from data.input_code.d04_library import *

@pytest.fixture
def library_manager():
    return LibraryManager()

def test_book_init():
    book = Book("Test", "Author", "123")
    assert book.title == "Test"
    assert book.author == "Author"
    assert book.isbn == "123"
    assert book.is_available == True

@pytest.mark.parametrize('is_available, expected', [
    (True, "[Available] Test by Author (ISBN: 123)"),
    (False, "[Borrowed] Test by Author (ISBN: 123)")
])
def test_book_str(is_available, expected):
    book = Book("Test", "Author", "123")
    book.is_available = is_available
    assert str(book) == expected

def test_library_manager_add_book(library_manager):
    library_manager.add_book("Test Book", "Test Author", "1234567890")
    assert "1234567890" in library_manager.inventory

def test_library_manager_add_book_isbn_too_short(library_manager, capsys):
    library_manager.add_book("Short ISBN", "Test Author", "12")
    captured = capsys.readouterr()
    assert "[!] Error: ISBN '12' is too short." in captured.out

def test_library_manager_add_book_duplicate_isbn(library_manager, capsys):
    library_manager.add_book("Test Book", "Test Author", "1234567890")
    library_manager.add_book("Duplicate ISBN", "Test Author", "1234567890")
    captured = capsys.readouterr()
    assert "[!] Error: A book with ISBN 1234567890 already exists." in captured.out

def test_library_manager_borrow_book(library_manager):
    library_manager.add_book("Test Book", "Test Author", "1234567890")
    library_manager.borrow_book("1234567890")
    assert library_manager.inventory["1234567890"].is_available == False

def test_library_manager_borrow_nonexistent_book(library_manager, capsys):
    library_manager.borrow_book("nonexistent")
    captured = capsys.readouterr()
    assert "[!] Error: Book with ISBN nonexistent not found." in captured.out

def test_library_manager_borrow_already_borrowed_book(library_manager, capsys):
    library_manager.add_book("Test Book", "Test Author", "1234567890")
    library_manager.borrow_book("1234567890")
    library_manager.borrow_book("1234567890")
    captured = capsys.readouterr()
    assert "[!] Unavailable: 'Test Book' is currently borrowed by someone else." in captured.out

def test_library_manager_return_book(library_manager):
    library_manager.add_book("Test Book", "Test Author", "1234567890")
    library_manager.borrow_book("1234567890")
    library_manager.return_book("1234567890")
    assert library_manager.inventory["1234567890"].is_available == True

def test_library_manager_return_nonexistent_book(library_manager, capsys):
    library_manager.return_book("nonexistent")
    captured = capsys.readouterr()
    assert "[!] Error: We do not own a book with ISBN nonexistent." in captured.out

def test_library_manager_return_already_returned_book(library_manager, capsys):
    library_manager.add_book("Test Book", "Test Author", "1234567890")
    library_manager.return_book("1234567890")
    captured = capsys.readouterr()
    assert "[!] Strange: You are trying to return 'Test Book', but it was already here." in captured.out

def test_library_manager_show_inventory_empty(library_manager, capsys):
    library_manager.show_inventory()
    captured = capsys.readouterr()
    assert "The library is empty." in captured.out

def test_library_manager_show_inventory_non_empty(library_manager, capsys):
    library_manager.add_book("Test Book", "Test Author", "1234567890")
    library_manager.show_inventory()
    captured = capsys.readouterr()
    assert "[Available] Test Book by Test Author (ISBN: 1234567890)" in captured.out