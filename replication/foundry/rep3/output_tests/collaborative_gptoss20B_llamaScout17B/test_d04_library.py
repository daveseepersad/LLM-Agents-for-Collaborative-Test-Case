import pytest
from data.input_code.d04_library import *

@pytest.fixture
def library_manager():
    return LibraryManager()

def test_add_valid_book(library_manager, capsys):
    library_manager.add_book("Dune", "Frank Herbert", "9780441013593")
    captured = capsys.readouterr()
    assert "Success: Added 'Dune' to the library." in captured.out

def test_add_short_isbn(library_manager, capsys):
    library_manager.add_book("Test Book", "Author", "12")
    captured = capsys.readouterr()
    assert "[!] Error: ISBN '12' is too short." in captured.out

def test_borrow_not_exist(library_manager, capsys):
    library_manager.borrow_book("0000000000")
    captured = capsys.readouterr()
    assert "[!] Error: Book with ISBN 0000000000 not found." in captured.out

def test_return_not_exist(library_manager, capsys):
    library_manager.return_book("0000000000")
    captured = capsys.readouterr()
    assert "[!] Error: We do not own a book with ISBN 0000000000." in captured.out

def test_show_empty(library_manager, capsys):
    library_manager.show_inventory()
    captured = capsys.readouterr()
    assert "The library is empty." in captured.out

import pytest
from data.input_code.d04_library import *

def test_add_duplicate_isbn(library_manager, capsys):
    library_manager.add_book("Dune", "Frank Herbert", "9780441013593")
    library_manager.add_book("Dune Duplicate", "Frank Herbert", "9780441013593")
    captured = capsys.readouterr()
    assert "[!] Error: A book with ISBN 9780441013593 already exists." in captured.out

import pytest
from data.input_code.d04_library import *

def test_borrow_success(library_manager, capsys):
    library_manager.add_book("Dune", "Frank Herbert", "9780441013593")
    library_manager.borrow_book("9780441013593")
    captured = capsys.readouterr()
    assert "Success: You have borrowed 'Dune'." in captured.out

def test_borrow_unavailable(library_manager, capsys):
    library_manager.add_book("Dune", "Frank Herbert", "9780441013593")
    library_manager.borrow_book("9780441013593")
    library_manager.borrow_book("9780441013593")
    captured = capsys.readouterr()
    assert "[!] Unavailable: 'Dune' is currently borrowed by someone else." in captured.out

def test_return_success(library_manager, capsys):
    library_manager.add_book("Dune", "Frank Herbert", "9780441013593")
    library_manager.borrow_book("9780441013593")
    library_manager.return_book("9780441013593")
    captured = capsys.readouterr()
    assert "Success: 'Dune' has been returned." in captured.out

import pytest
from data.input_code.d04_library import *

def test_return_already_available(library_manager, capsys):
    library_manager.add_book("Dune", "Frank Herbert", "9780441013593")
    library_manager.return_book("9780441013593")
    captured = capsys.readouterr()
    assert "[!] Strange: You are trying to return 'Dune', but it was already here." in captured.out

def test_show_inventory_nonempty(library_manager, capsys):
    library_manager.add_book("Dune", "Frank Herbert", "9780441013593")
    library_manager.show_inventory()
    captured = capsys.readouterr()
    assert "[Available] Dune by Frank Herbert (ISBN: 9780441013593)" in captured.out