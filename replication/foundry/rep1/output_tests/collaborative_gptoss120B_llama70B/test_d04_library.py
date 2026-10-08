import pytest
from data.input_code.d04_library import LibraryManager, Book

@pytest.mark.parametrize('title, author, isbn, expected_print, expected_inventory_size', [
    ('Tiny', 'A', '12', "[!] Error: ISBN '12' is too short.", 0),
    ('Original', 'B', '12345', "Success: Added 'Original' to the library.", 1),
])
def test_add_book(capsys, title, author, isbn, expected_print, expected_inventory_size):
    library = LibraryManager()
    library.add_book(title, author, isbn)
    captured = capsys.readouterr()
    assert captured.out.strip() == expected_print
    assert len(library.inventory) == expected_inventory_size

def test_add_book_duplicate(capsys):
    library = LibraryManager()
    library.add_book('Original', 'B', '12345')
    library.add_book('Copy', 'C', '12345')
    captured = capsys.readouterr()
    assert captured.out.strip().endswith("[!] Error: A book with ISBN 12345 already exists.")

def test_add_book_success(capsys):
    library = LibraryManager()
    library.add_book('Python 101', 'Guido', '98765')
    captured = capsys.readouterr()
    assert captured.out.strip() == "Success: Added 'Python 101' to the library."
    assert len(library.inventory) == 1
    assert list(library.inventory.values())[0].is_available

@pytest.mark.parametrize('isbn, expected_print, expected_inventory_unchanged', [
    ('00000', "[!] Error: Book with ISBN 00000 not found.", True),
])
def test_borrow_book(capsys, isbn, expected_print, expected_inventory_unchanged):
    library = LibraryManager()
    library.borrow_book(isbn)
    captured = capsys.readouterr()
    assert captured.out.strip() == expected_print
    assert len(library.inventory) == 0

def test_borrow_book_success(capsys):
    library = LibraryManager()
    library.add_book('Effective Java', 'Joshua', '11111')
    library.borrow_book('11111')
    captured = capsys.readouterr()
    assert captured.out.strip().endswith("Success: You have borrowed 'Effective Java'.")
    assert not list(library.inventory.values())[0].is_available

def test_borrow_book_already_borrowed(capsys):
    library = LibraryManager()
    library.add_book('Clean Code', 'Robert', '22222')
    library.borrow_book('22222')
    library.borrow_book('22222')
    captured = capsys.readouterr()
    assert captured.out.strip().endswith("[!] Unavailable: 'Clean Code' is currently borrowed by someone else.")
    assert not list(library.inventory.values())[0].is_available

@pytest.mark.parametrize('isbn, expected_print, expected_inventory_unchanged', [
    ('33333', "[!] Error: We do not own a book with ISBN 33333.", True),
])
def test_return_book(capsys, isbn, expected_print, expected_inventory_unchanged):
    library = LibraryManager()
    library.return_book(isbn)
    captured = capsys.readouterr()
    assert captured.out.strip() == expected_print
    assert len(library.inventory) == 0

def test_return_book_already_available(capsys):
    library = LibraryManager()
    library.add_book('Design Patterns', 'Gamma', '44444')
    library.return_book('44444')
    captured = capsys.readouterr()
    assert captured.out.strip().endswith("[!] Strange: You are trying to return 'Design Patterns', but it was already here.")
    assert list(library.inventory.values())[0].is_available

def test_return_book_success(capsys):
    library = LibraryManager()
    library.add_book('Refactoring', 'Martin', '55555')
    library.borrow_book('55555')
    library.return_book('55555')
    captured = capsys.readouterr()
    assert captured.out.strip().endswith("Success: 'Refactoring' has been returned.")
    assert list(library.inventory.values())[0].is_available


