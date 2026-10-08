import pytest
from data.input_code.d04_library import LibraryManager, Book

@pytest.mark.parametrize('title, author, isbn, expected', [
    ("Sample Book", "Author A", "12", None),
    ("1984", "George Orwell", "123", None)
])
def test_add_book(title, author, isbn, expected, capsys):
    library = LibraryManager()
    library.add_book(title, author, isbn)
    captured = capsys.readouterr()
    if len(isbn) < 3:
        assert f"[!] Error: ISBN '{isbn}' is too short." in captured.out
    else:
        assert f"Success: Added '{title}' to the library." in captured.out

def test_borrow_nonexistent(capsys):
    library = LibraryManager()
    library.borrow_book("9999")
    captured = capsys.readouterr()
    assert f"[!] Error: Book with ISBN 9999 not found." in captured.out

def test_return_nonexistent(capsys):
    library = LibraryManager()
    library.return_book("9999")
    captured = capsys.readouterr()
    assert f"[!] Error: We do not own a book with ISBN 9999." in captured.out

def test_show_inventory_empty(capsys):
    library = LibraryManager()
    library.show_inventory()
    captured = capsys.readouterr()
    assert "The library is empty." in captured.out

def test_borrow_and_return(capsys):
    library = LibraryManager()
    library.add_book("1984", "George Orwell", "123")
    library.borrow_book("123")
    captured = capsys.readouterr()
    assert f"Success: You have borrowed '1984'." in captured.out
    library.return_book("123")
    captured = capsys.readouterr()
    assert f"Success: '1984' has been returned." in captured.out

def test_duplicate_add_book(capsys):
    library = LibraryManager()
    library.add_book("First", "Author", "111")
    library.add_book("First Duplicate", "Author", "111")
    captured = capsys.readouterr()
    assert "[!] Error: A book with ISBN 111 already exists." in captured.out


def test_borrow_already_borrowed(capsys):
    library = LibraryManager()
    library.add_book("Book", "Author", "333")
    library.borrow_book("333")
    # first borrow output is not needed for assertion
    library.borrow_book("333")
    captured = capsys.readouterr()
    assert "[!] Unavailable: 'Book' is currently borrowed by someone else." in captured.out


def test_return_already_present(capsys):
    library = LibraryManager()
    library.add_book("BookX", "AuthorX", "444")
    library.return_book("444")
    captured = capsys.readouterr()
    assert "[!] Strange: You are trying to return 'BookX', but it was already here." in captured.out


def test_show_inventory_non_empty(capsys):
    library = LibraryManager()
    library.add_book("BookA", "AuthorA", "111")
    library.add_book("BookB", "AuthorB", "222")
    library.borrow_book("111")
    library.show_inventory()
    captured = capsys.readouterr()
    assert "[Borrowed] BookA by AuthorA (ISBN: 111)" in captured.out