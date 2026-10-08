import pytest
from data.input_code.d04_library import *

@pytest.mark.parametrize('title, author, isbn', [
    ("Book1", "Author1", "123"),
    ("Book2", "Author2", "12"),
    ("Book3", "Author3", "123")
])
def test_LibraryManager_add_book(title, author, isbn, capsys):
    manager = LibraryManager()
    if isbn == "123":
        manager.add_book("ExistingBook", "ExistingAuthor", isbn)
    manager.add_book(title, author, isbn)
    captured = capsys.readouterr()
    if isbn == "12":
        assert "[!] Error: ISBN '12' is too short." in captured.out
    elif isbn == "123":
        assert "[!] Error: A book with ISBN 123 already exists." in captured.out
    else:
        assert f"Success: Added '{title}' to the library." in captured.out

@pytest.mark.parametrize('isbn, expected_output', [
    ("1234", "[!] Error: Book with ISBN 1234 not found."),
    ("123", "Success: You have borrowed 'ExistingBook'."),
    ("123", "[!] Unavailable: 'ExistingBook' is currently borrowed by someone else.")
])
def test_LibraryManager_borrow_book(isbn, expected_output, capsys):
    manager = LibraryManager()
    manager.add_book("ExistingBook", "ExistingAuthor", "123")
    if expected_output != "[!] Error: Book with ISBN 1234 not found.":
        if expected_output == "Success: You have borrowed 'ExistingBook'.":
            manager.borrow_book(isbn)
        else:
            manager.borrow_book("123")
            manager.borrow_book(isbn)
    else:
        manager.borrow_book(isbn)
    captured = capsys.readouterr()
    assert expected_output in captured.out

@pytest.mark.parametrize('isbn, expected_output', [
    ("1234", "[!] Error: We do not own a book with ISBN 1234."),
    ("123", "[!] Strange: You are trying to return 'ExistingBook', but it was already here."),
    ("123", "Success: 'ExistingBook' has been returned.")
])
def test_LibraryManager_return_book(isbn, expected_output, capsys):
    manager = LibraryManager()
    manager.add_book("ExistingBook", "ExistingAuthor", "123")
    if expected_output != "[!] Error: We do not own a book with ISBN 1234.":
        if expected_output == "[!] Strange: You are trying to return 'ExistingBook', but it was already here.":
            manager.return_book(isbn)
        else:
            manager.borrow_book("123")
            manager.return_book(isbn)
    else:
        manager.return_book(isbn)
    captured = capsys.readouterr()
    assert expected_output in captured.out

def test_LibraryManager_show_inventory(capsys):
    manager = LibraryManager()
    manager.show_inventory()
    captured = capsys.readouterr()
    assert "The library is empty." in captured.out

    manager.add_book("Book1", "Author1", "123")
    manager.show_inventory()
    captured = capsys.readouterr()
    assert "[Available] Book1 by Author1 (ISBN: 123)" in captured.out

@pytest.mark.parametrize('title, author, isbn', [
    ("Test", "Test", "123")
])
def test_Book_init(title, author, isbn):
    book = Book(title, author, isbn)
    assert book.title == title
    assert book.author == author
    assert book.isbn == isbn
    assert book.is_available == True

@pytest.mark.parametrize('is_available, expected', [
    (True, "[Available] Test by Test (ISBN: 123)"),
    (False, "[Borrowed] Test by Test (ISBN: 123)")
])
def test_Book_str(is_available, expected):
    book = Book("Test", "Test", "123")
    book.is_available = is_available
    assert str(book) == expected