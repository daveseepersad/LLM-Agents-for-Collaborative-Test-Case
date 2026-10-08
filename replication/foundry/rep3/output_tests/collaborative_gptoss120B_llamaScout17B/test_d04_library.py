import pytest
from io import StringIO
from contextlib import redirect_stdout
from data.input_code.d04_library import *

@pytest.fixture
def library_manager():
    return LibraryManager()

def test_add_book_short_isbn(library_manager, capsys):
    library_manager.add_book("Tiny Book", "A. Writer", "12")
    captured = capsys.readouterr()
    assert captured.out.strip() == "[!] Error: ISBN '12' is too short."

def test_add_book_success(library_manager, capsys):
    library_manager.add_book("Python 101", "Guido", "12345")
    captured = capsys.readouterr()
    assert captured.out.strip() == "Success: Added 'Python 101' to the library."

def test_add_book_duplicate(library_manager, capsys):
    library_manager.add_book("Python 101", "Guido", "12345")
    captured = capsys.readouterr()
    library_manager.add_book("Python 101", "Guido", "12345")
    captured = capsys.readouterr()
    assert captured.out.strip() == "[!] Error: A book with ISBN 12345 already exists."

def test_borrow_book_nonexistent(library_manager, capsys):
    library_manager.borrow_book("99999")
    captured = capsys.readouterr()
    assert captured.out.strip() == "[!] Error: Book with ISBN 99999 not found."

def test_borrow_book_success(library_manager, capsys):
    library_manager.add_book("Python 101", "Guido", "12345")
    captured = capsys.readouterr()
    library_manager.borrow_book("12345")
    captured = capsys.readouterr()
    assert captured.out.strip() == "Success: You have borrowed 'Python 101'."

def test_borrow_book_unavailable(library_manager, capsys):
    library_manager.add_book("Python 101", "Guido", "12345")
    library_manager.borrow_book("12345")
    captured = capsys.readouterr()
    library_manager.borrow_book("12345")
    captured = capsys.readouterr()
    assert captured.out.strip() == "[!] Unavailable: 'Python 101' is currently borrowed by someone else."

def test_return_book_nonexistent(library_manager, capsys):
    library_manager.return_book("88888")
    captured = capsys.readouterr()
    assert captured.out.strip() == "[!] Error: We do not own a book with ISBN 88888."

def test_return_book_not_borrowed(library_manager, capsys):
    library_manager.add_book("Python 101", "Guido", "12345")
    captured = capsys.readouterr()
    library_manager.return_book("12345")
    captured = capsys.readouterr()
    assert captured.out.strip() == "[!] Strange: You are trying to return 'Python 101', but it was already here."

def test_return_book_success(library_manager, capsys):
    library_manager.add_book("Python 101", "Guido", "12345")
    library_manager.borrow_book("12345")
    captured = capsys.readouterr()
    library_manager.return_book("12345")
    captured = capsys.readouterr()
    assert captured.out.strip() == "Success: 'Python 101' has been returned."

def test_show_inventory_empty(library_manager, capsys):
    library_manager.show_inventory()
    captured = capsys.readouterr()
    expected_output = "\n--- Current Library Inventory ---\nThe library is empty.\n---------------------------------\n\n"
    assert captured.out == expected_output

def test_show_inventory_nonempty(library_manager, capsys):
    library_manager.add_book("Python 101", "Guido", "12345")
    captured = capsys.readouterr()
    library_manager.show_inventory()
    captured = capsys.readouterr()
    expected_output = "\n--- Current Library Inventory ---\n[Available] Python 101 by Guido (ISBN: 12345)\n---------------------------------\n\n"
    assert captured.out == expected_output

def test_add_book_duplicate(library_manager, capsys):
    library_manager.add_book("Python 101", "Guido", "12345")
    captured = capsys.readouterr()
    assert captured.out.strip() == "Success: Added 'Python 101' to the library."
    library_manager.add_book("Python 101", "Guido", "12345")
    captured = capsys.readouterr()
    assert captured.out.strip() == "[!] Error: A book with ISBN 12345 already exists."

def test_return_book_not_borrowed(library_manager, capsys):
    library_manager.add_book("Python 101", "Guido", "12345")
    captured = capsys.readouterr()
    assert captured.out.strip() == "Success: Added 'Python 101' to the library."
    library_manager.return_book("12345")
    captured = capsys.readouterr()
    assert captured.out.strip() == "[!] Strange: You are trying to return 'Python 101', but it was already here."