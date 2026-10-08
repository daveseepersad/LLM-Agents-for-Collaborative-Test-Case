import pytest
from data.input_code.d04_library import *

@pytest.fixture
def library_manager():
    return LibraryManager()

def test_add_book_valid(library_manager, capsys):
    library_manager.add_book("Dune", "Frank Herbert", "9780441013593")
    captured = capsys.readouterr()
    assert "Success: Added 'Dune' to the library." in captured.out

def test_add_book_short_isbn(library_manager, capsys):
    library_manager.add_book("Test", "Anon", "12")
    captured = capsys.readouterr()
    assert "[!] Error: ISBN '12' is too short." in captured.out

def test_add_book_duplicate_isbn(library_manager, capsys):
    library_manager.add_book("Existing Book", "Author", "111")
    library_manager.add_book("New Book", "Author", "111")
    captured = capsys.readouterr()
    assert "[!] Error: A book with ISBN 111 already exists." in captured.out

def test_borrow_book_existing_available(library_manager, capsys):
    library_manager.add_book("Existing Book", "Author", "111")
    library_manager.borrow_book("111")
    captured = capsys.readouterr()
    assert "Success: You have borrowed 'Existing Book'." in captured.out

def test_borrow_book_nonexistent(library_manager, capsys):
    library_manager.borrow_book("9999")
    captured = capsys.readouterr()
    assert "[!] Error: Book with ISBN 9999 not found." in captured.out

def test_return_book_not_existing(library_manager, capsys):
    library_manager.return_book("8888")
    captured = capsys.readouterr()
    assert "[!] Error: We do not own a book with ISBN 8888." in captured.out

def test_show_inventory_empty(library_manager, capsys):
    library_manager.show_inventory()
    captured = capsys.readouterr()
    assert "The library is empty." in captured.out

def test_show_inventory_non_empty(library_manager, capsys):
    library_manager.add_book("Existing Book", "Author", "111")
    library_manager.show_inventory()
    captured = capsys.readouterr()
    assert "[Available] Existing Book by Author (ISBN: 111)" in captured.out

import pytest
from data.input_code.d04_library import *

@pytest.mark.parametrize("is_available, expected_status", [
    (True, "[Available] Dune by Frank Herbert (ISBN: 9780441013593)"),
    (False, "[Borrowed] Dune by Frank Herbert (ISBN: 9780441013593)"),
])
def test_book_str(is_available, expected_status):
    book = Book("Dune", "Frank Herbert", "9780441013593")
    book.is_available = is_available
    assert str(book) == expected_status

import pytest
from data.input_code.d04_library import *

def test_borrow_unavailable_book(library_manager, capsys):
    library_manager.add_book("Book A", "Author", "222")
    library_manager.borrow_book("222")
    library_manager.borrow_book("222")
    captured = capsys.readouterr()
    assert "[!] Unavailable: 'Book A' is currently borrowed by someone else." in captured.out

def test_return_success(library_manager, capsys):
    library_manager.add_book("Returnable", "Author", "333")
    library_manager.borrow_book("333")
    library_manager.return_book("333")
    captured = capsys.readouterr()
    assert "Success: 'Returnable' has been returned." in captured.out

def test_return_already_available(library_manager, capsys):
    library_manager.add_book("AvailableAgain", "Author", "444")
    library_manager.return_book("444")
    captured = capsys.readouterr()
    assert "[!] Strange: You are trying to return 'AvailableAgain', but it was already here." in captured.out