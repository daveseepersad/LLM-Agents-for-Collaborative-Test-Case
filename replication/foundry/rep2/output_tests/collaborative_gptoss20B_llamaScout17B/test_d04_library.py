import pytest
from data.input_code.d04_library import *

@pytest.fixture
def library_manager():
    return LibraryManager()

def test_add_book_valid(library_manager, capsys):
    library_manager.add_book("The Alchemist", "Paulo Coelho", "123")
    captured = capsys.readouterr()
    assert "Success: Added 'The Alchemist' to the library." in captured.out

def test_add_book_isbn_too_short(library_manager, capsys):
    library_manager.add_book("Short ISBN", "Author", "ab")
    captured = capsys.readouterr()
    assert "[!] Error: ISBN 'ab' is too short." in captured.out

def test_borrow_book_not_found(library_manager, capsys):
    library_manager.borrow_book("999")
    captured = capsys.readouterr()
    assert "[!] Error: Book with ISBN 999 not found." in captured.out

def test_return_book_not_found(library_manager, capsys):
    library_manager.return_book("999")
    captured = capsys.readouterr()
    assert "[!] Error: We do not own a book with ISBN 999." in captured.out

def test_show_inventory_empty(library_manager, capsys):
    library_manager.show_inventory()
    captured = capsys.readouterr()
    assert "The library is empty." in captured.out

import pytest
from data.input_code.d04_library import *

@pytest.fixture
def library_manager():
    return LibraryManager()

def test_borrow_book_success(library_manager, capsys):
    library_manager.add_book("Dune", "Frank Herbert", "999")
    library_manager.borrow_book("999")
    captured = capsys.readouterr()
    assert "Success: You have borrowed 'Dune'." in captured.out

def test_borrow_book_unavailable(library_manager, capsys):
    library_manager.add_book("Dune", "Frank Herbert", "888")
    library_manager.borrow_book("888")
    library_manager.borrow_book("888")
    captured = capsys.readouterr()
    assert "[!] Unavailable: 'Dune' is currently borrowed by someone else." in captured.out

def test_return_book_success(library_manager, capsys):
    library_manager.add_book("The Hobbit", "J.R.R. Tolkien", "777")
    library_manager.borrow_book("777")
    library_manager.return_book("777")
    captured = capsys.readouterr()
    assert "Success: 'The Hobbit' has been returned." in captured.out

def test_show_inventory_nonempty(library_manager, capsys):
    library_manager.add_book("The Hobbit", "J.R.R. Tolkien", "777")
    library_manager.show_inventory()
    captured = capsys.readouterr()
    assert "[Available] The Hobbit by J.R.R. Tolkien (ISBN: 777)" in captured.out

import pytest
from data.input_code.d04_library import *

def test_add_book_duplicate_isbn(library_manager, capsys):
    library_manager.add_book("Book One", "Author", "123")
    library_manager.add_book("Book Two", "Author", "123")
    captured = capsys.readouterr()
    assert "[!] Error: A book with ISBN 123 already exists." in captured.out

def test_return_book_already_here(library_manager, capsys):
    library_manager.add_book("Orphan", "Anon", "555")
    library_manager.return_book("555")
    captured = capsys.readouterr()
    assert "[!] Strange: You are trying to return 'Orphan', but it was already here." in captured.out

def test_show_inventory_borrowed_state(library_manager, capsys):
    library_manager.add_book("Available", "A", "111")
    library_manager.add_book("Borrowed", "B", "222")
    library_manager.borrow_book("222")
    library_manager.show_inventory()
    captured = capsys.readouterr()
    assert "[Available] Available by A (ISBN: 111)" in captured.out
    assert "[Borrowed] Borrowed by B (ISBN: 222)" in captured.out