import pytest
from data.input_code.d04_library import *

@pytest.fixture
def empty_library():
    return LibraryManager()

@pytest.fixture
def library_with_book():
    lib = LibraryManager()
    lib.add_book("Test Book", "Test Author", "1234567890")
    return lib

def test_book_init():
    book = Book("Test Book", "Test Author", "1234567890")
    assert book.title == "Test Book"
    assert book.author == "Test Author"
    assert book.isbn == "1234567890"
    assert book.is_available is True

def test_book_str():
    book = Book("Test Book", "Test Author", "1234567890")
    expected = "[Available] Test Book by Test Author (ISBN: 1234567890)"
    assert str(book) == expected

def test_library_manager_init(empty_library):
    assert isinstance(empty_library.inventory, dict)
    assert not empty_library.inventory  # should be empty

def test_add_book_success(empty_library, capsys):
    empty_library.add_book("Test Book", "Test Author", "1234567890")
    captured = capsys.readouterr()
    assert "Success: Added 'Test Book' to the library." in captured.out
    assert "1234567890" in empty_library.inventory
    book = empty_library.inventory["1234567890"]
    assert isinstance(book, Book)
    assert book.title == "Test Book"

def test_add_book_short_isbn(empty_library, capsys):
    empty_library.add_book("Test Book", "Test Author", "12")
    captured = capsys.readouterr()
    assert "[!] Error: ISBN '12' is too short." in captured.out
    assert not empty_library.inventory  # still empty

def test_add_book_duplicate_isbn(library_with_book, capsys):
    library_with_book.add_book("Another Title", "Another Author", "1234567890")
    captured = capsys.readouterr()
    assert "[!] Error: A book with ISBN 1234567890 already exists." in captured.out
    # inventory should still contain only the original book
    assert len(library_with_book.inventory) == 1
    assert library_with_book.inventory["1234567890"].title == "Test Book"

def test_borrow_book_success(library_with_book, capsys):
    library_with_book.borrow_book("1234567890")
    captured = capsys.readouterr()
    assert "Success: You have borrowed 'Test Book'." in captured.out
    assert library_with_book.inventory["1234567890"].is_available is False

def test_borrow_book_unavailable(library_with_book, capsys):
    # first borrow to make it unavailable
    library_with_book.borrow_book("1234567890")
    capsys.readouterr()  # clear previous output
    # second attempt
    library_with_book.borrow_book("1234567890")
    captured = capsys.readouterr()
    assert "[!] Unavailable: 'Test Book' is currently borrowed by someone else." in captured.out
    assert library_with_book.inventory["1234567890"].is_available is False

def test_borrow_book_not_found(empty_library, capsys):
    empty_library.borrow_book("9876543210")
    captured = capsys.readouterr()
    assert "[!] Error: Book with ISBN 9876543210 not found." in captured.out

def test_return_book_success(library_with_book, capsys):
    # borrow first
    library_with_book.borrow_book("1234567890")
    capsys.readouterr()
    # now return
    library_with_book.return_book("1234567890")
    captured = capsys.readouterr()
    assert "Success: 'Test Book' has been returned." in captured.out
    assert library_with_book.inventory["1234567890"].is_available is True

def test_return_book_already_returned(library_with_book, capsys):
    # ensure book is in initial available state
    library_with_book.return_book("1234567890")
    captured = capsys.readouterr()
    assert "[!] Strange: You are trying to return 'Test Book', but it was already here." in captured.out
    assert library_with_book.inventory["1234567890"].is_available is True

def test_return_book_not_found(empty_library, capsys):
    empty_library.return_book("9876543210")
    captured = capsys.readouterr()
    assert "[!] Error: We do not own a book with ISBN 9876543210." in captured.out

def test_show_inventory_empty(empty_library, capsys):
    empty_library.show_inventory()
    captured = capsys.readouterr()
    assert "The library is empty." in captured.out

def test_show_inventory_non_empty(library_with_book, capsys):
    library_with_book.show_inventory()
    captured = capsys.readouterr()
    expected_line = "[Available] Test Book by Test Author (ISBN: 1234567890)"
    assert expected_line in captured.out