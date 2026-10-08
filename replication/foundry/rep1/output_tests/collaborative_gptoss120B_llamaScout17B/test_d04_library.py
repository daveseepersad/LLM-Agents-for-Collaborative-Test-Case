import pytest
from io import StringIO
from unittest.mock import patch
from data.input_code.d04_library import *

@pytest.fixture
def library_manager():
    return LibraryManager()

def execute_setup(library_manager, setup):
    for step in setup:
        method_name = step['method']
        args = step['args']
        getattr(library_manager, method_name)(**args)

@pytest.mark.parametrize('title, author, isbn, expected_stdout, expected_inventory_count', [
    ('Tiny', 'Anon', '12', "[!] Error: ISBN '12' is too short.\n", 0),
    ('Python 101', 'Guido', 'PY001', "Success: Added 'Python 101' to the library.\n", 1)
])
def test_add_book(library_manager, title, author, isbn, expected_stdout, expected_inventory_count):
    with patch('sys.stdout', new=StringIO()) as fake_stdout:
        library_manager.add_book(title, author, isbn)
        assert fake_stdout.getvalue() == expected_stdout
        assert len(library_manager.inventory) == expected_inventory_count

def test_add_duplicate_isbn(library_manager):
    library_manager.add_book('First', 'Author1', 'ABC123')
    with patch('sys.stdout', new=StringIO()) as fake_stdout:
        library_manager.add_book('Second', 'Author2', 'ABC123')
        assert fake_stdout.getvalue() == "[!] Error: A book with ISBN ABC123 already exists.\n"
        assert len(library_manager.inventory) == 1

@pytest.mark.parametrize('isbn, expected_stdout, expected_status_changed', [
    ('NOPE', "[!] Error: Book with ISBN NOPE not found.\n", False),
    ('LCK001', "[!] Unavailable: 'Locked' is currently borrowed by someone else.\n", False),
    ('OPN001', "Success: You have borrowed 'Open'.\n", True)
])
def test_borrow_book(library_manager, isbn, expected_stdout, expected_status_changed):
    if isbn == 'LCK001':
        library_manager.add_book('Locked', 'Writer', 'LCK001')
        library_manager.borrow_book('LCK001')
    elif isbn == 'OPN001':
        library_manager.add_book('Open', 'Writer', 'OPN001')
    with patch('sys.stdout', new=StringIO()) as fake_stdout:
        initial_status = library_manager.inventory.get(isbn).is_available if isbn in library_manager.inventory else None
        library_manager.borrow_book(isbn)
        final_status = library_manager.inventory.get(isbn).is_available if isbn in library_manager.inventory else None
        assert fake_stdout.getvalue() == expected_stdout
        if initial_status is not None and final_status is not None:
            assert (initial_status != final_status) == expected_status_changed

@pytest.mark.parametrize('isbn, expected_stdout, expected_status_changed', [
    ('UNKNOWN', "[!] Error: We do not own a book with ISBN UNKNOWN.\n", False),
    ('IDL001', "[!] Strange: You are trying to return 'Idle', but it was already here.\n", False),
    ('REV001', "Success: 'Reversible' has been returned.\n", True)
])
def test_return_book(library_manager, isbn, expected_stdout, expected_status_changed):
    if isbn == 'IDL001':
        library_manager.add_book('Idle', 'Writer', 'IDL001')
    elif isbn == 'REV001':
        library_manager.add_book('Reversible', 'Writer', 'REV001')
        library_manager.borrow_book('REV001')
    with patch('sys.stdout', new=StringIO()) as fake_stdout:
        initial_status = library_manager.inventory.get(isbn).is_available if isbn in library_manager.inventory else None
        library_manager.return_book(isbn)
        final_status = library_manager.inventory.get(isbn).is_available if isbn in library_manager.inventory else None
        assert fake_stdout.getvalue() == expected_stdout
        if initial_status is not None and final_status is not None:
            assert (initial_status != final_status) == expected_status_changed

def test_show_inventory_empty(library_manager):
    with patch('sys.stdout', new=StringIO()) as fake_stdout:
        library_manager.show_inventory()
        output = fake_stdout.getvalue()
        assert "--- Current Library Inventory ---" in output
        assert "The library is empty." in output
        assert "---------------------------------" in output

def test_show_inventory_nonempty(library_manager):
    library_manager.add_book('Visible', 'AuthorX', 'VIS001')
    library_manager.borrow_book('VIS001')
    with patch('sys.stdout', new=StringIO()) as fake_stdout:
        library_manager.show_inventory()
        output = fake_stdout.getvalue()
        assert "--- Current Library Inventory ---" in output
        assert "[Borrowed] Visible by AuthorX (ISBN: VIS001)" in output
        assert "---------------------------------" in output

@pytest.mark.parametrize('isbn, expected_value', [
    ('FRB001', "[Available] FreeBook by FreeAuthor (ISBN: FRB001)"),
    ('TKB001', "[Borrowed] TakenBook by TakenAuthor (ISBN: TKB001)")
])
def test_book_str_representation(library_manager, isbn, expected_value):
    if isbn == 'FRB001':
        library_manager.add_book('FreeBook', 'FreeAuthor', 'FRB001')
    elif isbn == 'TKB001':
        library_manager.add_book('TakenBook', 'TakenAuthor', 'TKB001')
        library_manager.borrow_book('TKB001')
    book = library_manager.inventory[isbn]
    assert str(book) == expected_value