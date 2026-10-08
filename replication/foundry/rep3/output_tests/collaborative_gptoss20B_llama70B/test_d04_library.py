import pytest
from data.input_code.d04_library import Book, LibraryManager

@pytest.mark.parametrize('title, author, isbn, expected', [
    ("Dune", "Frank Herbert", "123", "[Available] Dune by Frank Herbert (ISBN: 123)")
])
def test_book_str(title, author, isbn, expected):
    book = Book(title, author, isbn)
    assert str(book) == expected

@pytest.mark.parametrize('title, author, isbn, expected', [
    ("Dune", "Frank Herbert", "12", "[!] Error: ISBN '12' is too short.")
])
def test_add_book_short_isbn(capsys, title, author, isbn, expected):
    library = LibraryManager()
    library.add_book(title, author, isbn)
    captured = capsys.readouterr()
    assert captured.out.strip() == expected

@pytest.mark.parametrize('title, author, isbn, expected', [
    ("Dune", "Frank Herbert", "12345", "Success: Added 'Dune' to the library.")
])
def test_add_book_success(capsys, title, author, isbn, expected):
    library = LibraryManager()
    library.add_book(title, author, isbn)
    captured = capsys.readouterr()
    assert captured.out.strip() == expected

def test_borrow_non_existent_book(capsys):
    library = LibraryManager()
    library.borrow_book("999")
    captured = capsys.readouterr()
    assert captured.out.strip() == "[!] Error: Book with ISBN 999 not found."

def test_return_non_existent_book(capsys):
    library = LibraryManager()
    library.return_book("999")
    captured = capsys.readouterr()
    assert captured.out.strip() == "[!] Error: We do not own a book with ISBN 999."

@pytest.mark.parametrize('isbn, expected', [
    ("333", "Success: You have borrowed 'Borrowable'.")
])
def test_borrow_book_success(capsys, isbn, expected):
    library = LibraryManager()
    library.add_book("Borrowable", "Author", isbn)
    library.borrow_book(isbn)
    captured = capsys.readouterr()
    assert captured.out.strip().endswith(expected)

@pytest.mark.parametrize('isbn, expected', [
    ("334", "[!] Unavailable: 'Borrowable' is currently borrowed by someone else.")
])
def test_borrow_book_unavailable(capsys, isbn, expected):
    library = LibraryManager()
    library.add_book("Borrowable", "Author", isbn)
    library.borrow_book(isbn)
    library.borrow_book(isbn)
    captured = capsys.readouterr()
    assert captured.out.strip().endswith(expected)

@pytest.mark.parametrize('isbn, expected', [
    ("411", "Success: 'Returnable' has been returned.")
])
def test_return_book_success(capsys, isbn, expected):
    library = LibraryManager()
    library.add_book("Returnable", "Author", isbn)
    library.borrow_book(isbn)
    library.return_book(isbn)
    captured = capsys.readouterr()
    assert captured.out.strip().endswith(expected)

@pytest.mark.parametrize('isbn, expected', [
    ("512", "[!] Strange: You are trying to return 'Again', but it was already here.")
])
def test_return_book_strange_not_borrowed(capsys, isbn, expected):
    library = LibraryManager()
    library.add_book("Again", "Author", isbn)
    library.return_book(isbn)
    captured = capsys.readouterr()
    assert captured.out.strip().endswith(expected)

@pytest.mark.parametrize('title, author, isbn, expected', [
    ("Second", "Author2", "555", "[!] Error: A book with ISBN 555 already exists.")
])
def test_add_book_duplicate_isbn(capsys, title, author, isbn, expected):
    library = LibraryManager()
    library.add_book("First", "Author1", isbn)
    library.add_book(title, author, isbn)
    captured = capsys.readouterr()
    assert captured.out.strip().endswith(expected)

