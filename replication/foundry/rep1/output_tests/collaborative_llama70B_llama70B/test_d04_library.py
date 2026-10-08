import pytest
from library import Book, LibraryManager

@pytest.mark.parametrize('title, author, isbn, expected', [
    ("Test Book", "Test Author", "1234567890", None)
])
def test_book_init(title, author, isbn, expected):
    book = Book(title, author, isbn)
    assert book.title == title
    assert book.author == author
    assert book.isbn == isbn
    assert book.is_available

@pytest.mark.parametrize('title, author, isbn, expected', [
    ("Test Book", "Test Author", "1234567890", "[Available] Test Book by Test Author (ISBN: 1234567890)")
])
def test_book_str(title, author, isbn, expected):
    book = Book(title, author, isbn)
    assert str(book) == expected

def test_library_init():
    library = LibraryManager()
    assert library.inventory == {}

@pytest.mark.parametrize('title, author, isbn, expected', [
    ("Test Book", "Test Author", "1234567890", "Success: Added 'Test Book' to the library.")
])
def test_add_book_ok(capsys, title, author, isbn, expected):
    library = LibraryManager()
    library.add_book(title, author, isbn)
    captured = capsys.readouterr()
    assert captured.out.strip() == expected

@pytest.mark.parametrize('title, author, isbn, expected', [
    ("Test Book", "Test Author", "12", "[!] Error: ISBN '12' is too short.")
])
def test_add_book_short_isbn(capsys, title, author, isbn, expected):
    library = LibraryManager()
    library.add_book(title, author, isbn)
    captured = capsys.readouterr()
    assert captured.out.strip() == expected

@pytest.mark.parametrize('title, author, isbn, expected', [
    ("Test Book 2", "Test Author 2", "1234567890", "[!] Error: A book with ISBN 1234567890 already exists.")
])
def test_add_book_duplicate_isbn(capsys, title, author, isbn, expected):
    library = LibraryManager()
    library.add_book("Test Book", "Test Author", isbn)
    library.add_book(title, author, isbn)
    captured = capsys.readouterr()
    assert captured.out.strip().split('\n')[-1] == expected

@pytest.mark.parametrize('isbn, expected', [
    ("1234567890", "Success: You have borrowed 'Test Book'.")
])
def test_borrow_book_ok(capsys, isbn, expected):
    library = LibraryManager()
    library.add_book("Test Book", "Test Author", isbn)
    library.borrow_book(isbn)
    captured = capsys.readouterr()
    assert captured.out.strip().split('\n')[-1] == expected

@pytest.mark.parametrize('isbn, expected', [
    ("9876543210", "[!] Error: Book with ISBN 9876543210 not found.")
])
def test_borrow_book_not_found(capsys, isbn, expected):
    library = LibraryManager()
    library.borrow_book(isbn)
    captured = capsys.readouterr()
    assert captured.out.strip() == expected

@pytest.mark.parametrize('isbn, expected', [
    ("1234567890", "[!] Unavailable: 'Test Book' is currently borrowed by someone else.")
])
def test_borrow_book_unavailable(capsys, isbn, expected):
    library = LibraryManager()
    library.add_book("Test Book", "Test Author", isbn)
    library.borrow_book(isbn)
    library.borrow_book(isbn)
    captured = capsys.readouterr()
    assert captured.out.strip().split('\n')[-1] == expected

@pytest.mark.parametrize('isbn, expected', [
    ("1234567890", "Success: 'Test Book' has been returned.")
])
def test_return_book_ok(capsys, isbn, expected):
    library = LibraryManager()
    library.add_book("Test Book", "Test Author", isbn)
    library.borrow_book(isbn)
    library.return_book(isbn)
    captured = capsys.readouterr()
    assert captured.out.strip().split('\n')[-1] == expected

@pytest.mark.parametrize('isbn, expected', [
    ("9876543210", "[!] Error: We do not own a book with ISBN 9876543210.")
])
def test_return_book_not_found(capsys, isbn, expected):
    library = LibraryManager()
    library.return_book(isbn)
    captured = capsys.readouterr()
    assert captured.out.strip() == expected

@pytest.mark.parametrize('isbn, expected', [
    ("1234567890", "[!] Strange: You are trying to return 'Test Book', but it was already here.")
])
def test_return_book_already_returned(capsys, isbn, expected):
    library = LibraryManager()
    library.add_book("Test Book", "Test Author", isbn)
    library.return_book(isbn)
    captured = capsys.readouterr()
    assert captured.out.strip() == expected

def test_show_inventory_empty(capsys):
    library = LibraryManager()
    library.show_inventory()
    captured = capsys.readouterr()
    assert captured.out.strip() == "The library is empty."

def test_show_inventory_non_empty(capsys):
    library = LibraryManager()
    library.add_book("Test Book", "Test Author", "1234567890")
    library.show_inventory()
    captured = capsys.readouterr()
    assert captured.out.strip().split('\n')[0] == "The library has the following books:"
    assert captured.out.strip().split('\n')[1] == "[Available] Test Book by Test Author (ISBN: 1234567890)"