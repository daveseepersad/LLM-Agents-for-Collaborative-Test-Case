import pytest
from data.input_code.d04_library import LibraryManager, Book

@pytest.mark.parametrize('title, author, isbn, expected', [
    ("Short ISBN", "Author A", "12", ["[!] Error: ISBN '12' is too short."]),
])
def test_add_book_short_isbn(capsys, title, author, isbn, expected):
    library = LibraryManager()
    library.add_book(title, author, isbn)
    captured = capsys.readouterr()
    assert captured.out.strip().split('\n') == expected

@pytest.mark.parametrize('title, author, isbn, expected', [
    ("First Book", "Author B", "ABC123", ["Success: Added 'First Book' to the library.", "[!] Error: A book with ISBN ABC123 already exists."]),
])
def test_add_book_duplicate_isbn(capsys, title, author, isbn, expected):
    library = LibraryManager()
    library.add_book(title, author, isbn)
    library.add_book(title, author, isbn)
    captured = capsys.readouterr()
    assert captured.out.strip().split('\n') == expected

@pytest.mark.parametrize('title, author, isbn, expected', [
    ("Normal Book", "Author C", "XYZ789", ["Success: Added 'Normal Book' to the library."]),
])
def test_add_book_normal(capsys, title, author, isbn, expected):
    library = LibraryManager()
    library.add_book(title, author, isbn)
    captured = capsys.readouterr()
    assert captured.out.strip().split('\n') == expected

@pytest.mark.parametrize('isbn, expected', [
    ("NONEXIST", ["[!] Error: Book with ISBN NONEXIST not found."]),
])
def test_borrow_book_not_exist(capsys, isbn, expected):
    library = LibraryManager()
    library.borrow_book(isbn)
    captured = capsys.readouterr()
    assert captured.out.strip().split('\n') == expected

@pytest.mark.parametrize('isbn, expected', [
    ("XYZ789", ["Success: Added 'Normal Book' to the library.", "Success: You have borrowed 'Normal Book'.", "[!] Unavailable: 'Normal Book' is currently borrowed by someone else."]),
])
def test_borrow_book_unavailable(capsys, isbn, expected):
    library = LibraryManager()
    library.add_book("Normal Book", "Author C", isbn)
    library.borrow_book(isbn)
    library.borrow_book(isbn)
    captured = capsys.readouterr()
    assert captured.out.strip().split('\n') == expected

@pytest.mark.parametrize('isbn, expected', [
    ("UNKNOWN", ["[!] Error: We do not own a book with ISBN UNKNOWN."]),
])
def test_return_book_not_exist(capsys, isbn, expected):
    library = LibraryManager()
    library.return_book(isbn)
    captured = capsys.readouterr()
    assert captured.out.strip().split('\n') == expected

@pytest.mark.parametrize('isbn, expected', [
    ("ABC123", ["Success: Added 'First Book' to the library.", "[!] Strange: You are trying to return 'First Book', but it was already here."]),
])
def test_return_book_already_available(capsys, isbn, expected):
    library = LibraryManager()
    library.add_book("First Book", "Author B", isbn)
    library.return_book(isbn)
    captured = capsys.readouterr()
    assert captured.out.strip().split('\n') == expected

@pytest.mark.parametrize('isbn, expected', [
    ("XYZ789", ["Success: Added 'Normal Book' to the library.", "Success: You have borrowed 'Normal Book'.", "Success: 'Normal Book' has been returned."]),
])
def test_return_book_success(capsys, isbn, expected):
    library = LibraryManager()
    library.add_book("Normal Book", "Author C", isbn)
    library.borrow_book(isbn)
    library.return_book(isbn)
    captured = capsys.readouterr()
    assert captured.out.strip().split('\n') == expected

def test_show_inventory_empty(capsys):
    library = LibraryManager()
    library.show_inventory()
    captured = capsys.readouterr()
    expected = [
        "\n--- Current Library Inventory ---",
        "The library is empty.",
        "---------------------------------\n"
    ]
    assert captured.out.strip().split('\n') == [line.strip() for line in expected]

def test_show_inventory_non_empty(capsys):
    library = LibraryManager()
    library.add_book("First Book", "Author B", "ABC123")
    library.add_book("Normal Book", "Author C", "XYZ789")
    captured = capsys.readouterr()
    library.show_inventory()
    captured = capsys.readouterr()
    expected = [
        "\n--- Current Library Inventory ---",
        "[Available] First Book by Author B (ISBN: ABC123)",
        "[Available] Normal Book by Author C (ISBN: XYZ789)",
        "---------------------------------\n"
    ]
    assert captured.out.strip().split('\n') == [line.strip() for line in expected]