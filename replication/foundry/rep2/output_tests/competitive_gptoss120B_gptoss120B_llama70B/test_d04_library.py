import pytest
from data.input_code.d04_library import *

@pytest.mark.parametrize('title, author, isbn, expected', [
    ('Tiny', 'Anon', '12', "[!] Error: ISBN '12' is too short.\n")
])
def test_add_book_short_isbn(capsys, title, author, isbn, expected):
    library = LibraryManager()
    library.add_book(title, author, isbn)
    captured = capsys.readouterr()
    assert captured.out == expected

@pytest.mark.parametrize('title, author, isbn, expected', [
    ('Python 101', 'Guido', '12345', "Success: Added 'Python 101' to the library.\n")
])
def test_add_book_success(capsys, title, author, isbn, expected):
    library = LibraryManager()
    library.add_book(title, author, isbn)
    captured = capsys.readouterr()
    assert captured.out == expected

def test_add_book_duplicate(capsys):
    library = LibraryManager()
    library.add_book('Python 101', 'Guido', '12345')
    library.add_book('Python 101', 'Guido', '12345')
    captured = capsys.readouterr()
    assert captured.out == "Success: Added 'Python 101' to the library.\n[!] Error: A book with ISBN 12345 already exists.\n"

def test_borrow_book_not_found(capsys):
    library = LibraryManager()
    library.borrow_book('99999')
    captured = capsys.readouterr()
    assert captured.out == "[!] Error: Book with ISBN 99999 not found.\n"

def test_borrow_book_success(capsys):
    library = LibraryManager()
    library.add_book('Deep Learning', 'Ian', 'DL001')
    library.borrow_book('DL001')
    captured = capsys.readouterr()
    assert captured.out == "Success: Added 'Deep Learning' to the library.\nSuccess: You have borrowed 'Deep Learning'.\n"

def test_borrow_book_unavailable(capsys):
    library = LibraryManager()
    library.add_book('Deep Learning', 'Ian', 'DL001')
    library.borrow_book('DL001')
    library.borrow_book('DL001')
    captured = capsys.readouterr()
    assert captured.out == "Success: Added 'Deep Learning' to the library.\nSuccess: You have borrowed 'Deep Learning'.\n[!] Unavailable: 'Deep Learning' is currently borrowed by someone else.\n"

def test_return_book_not_found(capsys):
    library = LibraryManager()
    library.return_book('XYZ999')
    captured = capsys.readouterr()
    assert captured.out == "[!] Error: We do not own a book with ISBN XYZ999.\n"

def test_return_book_success(capsys):
    library = LibraryManager()
    library.add_book('Deep Learning', 'Ian', 'DL001')
    library.borrow_book('DL001')
    library.return_book('DL001')
    captured = capsys.readouterr()
    assert captured.out == "Success: Added 'Deep Learning' to the library.\nSuccess: You have borrowed 'Deep Learning'.\nSuccess: 'Deep Learning' has been returned.\n"

def test_return_book_strange(capsys):
    library = LibraryManager()
    library.add_book('Deep Learning', 'Ian', 'DL001')
    library.return_book('DL001')
    captured = capsys.readouterr()
    assert captured.out == "Success: Added 'Deep Learning' to the library.\n[!] Strange: You are trying to return 'Deep Learning', but it was already here.\n"

def test_show_inventory_empty(capsys):
    library = LibraryManager()
    library.show_inventory()
    captured = capsys.readouterr()
    assert captured.out == "\n--- Current Library Inventory ---\nThe library is empty.\n---------------------------------\n\n"

def test_show_inventory_non_empty(capsys):
    library = LibraryManager()
    library.add_book('Deep Learning', 'Ian', 'DL001')
    library.show_inventory()
    captured = capsys.readouterr()
    assert captured.out == "Success: Added 'Deep Learning' to the library.\n\n--- Current Library Inventory ---\n[Available] Deep Learning by Ian (ISBN: DL001)\n---------------------------------\n\n"

def test_show_inventory_borrowed(capsys):
    library = LibraryManager()
    library.add_book('Deep Learning', 'Ian', 'DL001')
    library.borrow_book('DL001')
    library.show_inventory()
    captured = capsys.readouterr()
    assert captured.out == "Success: Added 'Deep Learning' to the library.\nSuccess: You have borrowed 'Deep Learning'.\n\n--- Current Library Inventory ---\n[Borrowed] Deep Learning by Ian (ISBN: DL001)\n---------------------------------\n\n"