import pytest
from data.input_code.d04_library import *

@pytest.fixture
def manager():
    return LibraryManager()

@pytest.mark.parametrize(
    "title, author, isbn, expected",
    [
        ("Tiny", "A", "12", "[!] Error: ISBN '12' is too short."),
        ("First", "B", "123", "Success: Added 'First' to the library."),
    ],
    ids=["short_isbn", "add_success"]
)
def test_add_book_basic(manager, title, author, isbn, expected, capsys):
    manager.add_book(title, author, isbn)
    captured = capsys.readouterr().out.strip().splitlines()[-1]
    assert captured == expected

def test_add_book_duplicate(manager, capsys):
    # first addition (setup)
    manager.add_book("First", "B", "123")
    # duplicate attempt
    manager.add_book("Second", "C", "123")
    captured = capsys.readouterr().out.strip().splitlines()[-1]
    assert captured == "[!] Error: A book with ISBN 123 already exists."

@pytest.mark.parametrize(
    "isbn, expected",
    [
        ("999", "[!] Error: Book with ISBN 999 not found."),
    ],
    ids=["borrow_not_found"]
)
def test_borrow_not_found(manager, isbn, expected, capsys):
    manager.borrow_book(isbn)
    captured = capsys.readouterr().out.strip().splitlines()[-1]
    assert captured == expected

def test_borrow_success(manager, capsys):
    manager.add_book("Guide", "E", "777")
    manager.borrow_book("777")
    captured = capsys.readouterr().out.strip().splitlines()[-1]
    assert captured == "Success: You have borrowed 'Guide'."

def test_borrow_unavailable(manager, capsys):
    manager.add_book("Guide", "E", "777")
    manager.borrow_book("777")  # first borrow makes it unavailable
    manager.borrow_book("777")  # second attempt
    captured = capsys.readouterr().out.strip().splitlines()[-1]
    assert captured == "[!] Unavailable: 'Guide' is currently borrowed by someone else."

@pytest.mark.parametrize(
    "isbn, expected",
    [
        ("888", "[!] Error: We do not own a book with ISBN 888."),
    ],
    ids=["return_not_found"]
)
def test_return_not_found(manager, isbn, expected, capsys):
    manager.return_book(isbn)
    captured = capsys.readouterr().out.strip().splitlines()[-1]
    assert captured == expected

def test_return_strange(manager, capsys):
    manager.add_book("Manual", "F", "555")
    manager.return_book("555")
    captured = capsys.readouterr().out.strip().splitlines()[-1]
    assert captured == "[!] Strange: You are trying to return 'Manual', but it was already here."

def test_return_success(manager, capsys):
    manager.add_book("Manual", "F", "555")
    manager.borrow_book("555")
    manager.return_book("555")
    captured = capsys.readouterr().out.strip().splitlines()[-1]
    assert captured == "Success: 'Manual' has been returned."

def test_show_inventory_empty(manager, capsys):
    manager.show_inventory()
    out = capsys.readouterr().out
    assert "The library is empty." in out

def test_show_inventory_nonempty(manager, capsys):
    manager.add_book("Atlas", "G", "321")
    manager.show_inventory()
    out = capsys.readouterr().out
    assert "[Available] Atlas by G (ISBN: 321)" in out

def test_book_str_available():
    book = Book("Chronicle", "H", "111")
    book.is_available = True
    assert str(book) == "[Available] Chronicle by H (ISBN: 111)"

def test_book_str_borrowed():
    book = Book("Chronicle", "H", "111")
    book.is_available = False
    assert str(book) == "[Borrowed] Chronicle by H (ISBN: 111)"