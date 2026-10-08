import pytest
from data.input_code.d04_library import *

@pytest.mark.parametrize('title, author, isbn, expected_print', [
    ('Tiny', 'A', '12', '[!] Error: ISBN \'12\' is too short.'),
    ('Python 101', 'Guido', '12345', 'Success: Added \'Python 101\' to the library.')
])
def test_add_book(capsys, title, author, isbn, expected_print):
    manager = LibraryManager()
    manager.add_book(title, author, isbn)
    captured = capsys.readouterr()
    assert expected_print in captured.out

def test_add_duplicate_book(capsys):
    manager = LibraryManager()
    manager.add_book('Python 101', 'Guido', '12345')
    manager.add_book('Another Book', 'Someone', '12345')
    captured = capsys.readouterr()
    assert '[!] Error: A book with ISBN 12345 already exists.' in captured.out

def test_borrow_nonexistent_book(capsys):
    manager = LibraryManager()
    manager.borrow_book('99999')
    captured = capsys.readouterr()
    assert '[!] Error: Book with ISBN 99999 not found.' in captured.out

def test_borrow_success(capsys):
    manager = LibraryManager()
    manager.add_book('Python 101', 'Guido', '12345')
    manager.borrow_book('12345')
    captured = capsys.readouterr()
    assert 'Success: You have borrowed \'Python 101\'.' in captured.out

def test_borrow_already_borrowed(capsys):
    manager = LibraryManager()
    manager.add_book('Python 101', 'Guido', '12345')
    manager.borrow_book('12345')
    manager.borrow_book('12345')
    captured = capsys.readouterr()
    assert '[!] Unavailable: \'Python 101\' is currently borrowed by someone else.' in captured.out

def test_return_nonexistent_book(capsys):
    manager = LibraryManager()
    manager.return_book('88888')
    captured = capsys.readouterr()
    assert '[!] Error: We do not own a book with ISBN 88888.' in captured.out

def test_return_already_available(capsys):
    manager = LibraryManager()
    manager.add_book('Python 101', 'Guido', '12345')
    manager.return_book('12345')
    captured = capsys.readouterr()
    assert '[!] Strange: You are trying to return \'Python 101\', but it was already here.' in captured.out

def test_return_success(capsys):
    manager = LibraryManager()
    manager.add_book('Python 101', 'Guido', '12345')
    manager.borrow_book('12345')
    manager.return_book('12345')
    captured = capsys.readouterr()
    assert 'Success: \'Python 101\' has been returned.' in captured.out

@pytest.mark.parametrize('is_available, expected_return', [
    (True, '[Available] Deep Learning by Ian Goodfellow (ISBN: DL001)'),
    (False, '[Borrowed] Deep Learning by Ian Goodfellow (ISBN: DL001)')
])
def test_book_str_representation(is_available, expected_return):
    book = Book('Deep Learning', 'Ian Goodfellow', 'DL001')
    book.is_available = is_available
    assert str(book) == expected_return

def test_T_ISBN_BOUNDARY(capsys):
    manager = LibraryManager()
    manager.add_book("EdgeCase", "Author", "123")
    captured = capsys.readouterr()
    assert "Success: Added 'EdgeCase' to the library." in captured.out

def test_T_SHOW_INVENTORY_EMPTY(capsys):
    manager = LibraryManager()
    manager.show_inventory()
    captured = capsys.readouterr()
    assert "The library is empty." in captured.out

def test_T_SHOW_INVENTORY_NONEMPTY(capsys):
    manager = LibraryManager()
    manager.add_book("EdgeCase", "Author", "123")
    manager.show_inventory()
    captured = capsys.readouterr()
    assert "[Available] EdgeCase by Author (ISBN: 123)" in captured.out

def test_T_BORROW_AFTER_RETURN(capsys):
    manager = LibraryManager()
    manager.add_book("Python 101", "Guido", "12345")
    manager.borrow_book("12345")
    manager.return_book("12345")
    manager.borrow_book("12345")
    captured = capsys.readouterr()
    assert "Success: You have borrowed 'Python 101'." in captured.out

def test_T_DOUBLE_RETURN(capsys):
    manager = LibraryManager()
    manager.add_book("Python 101", "Guido", "12345")
    manager.return_book("12345")
    manager.return_book("12345")
    captured = capsys.readouterr()
    assert "[!] Strange: You are trying to return 'Python 101', but it was already here." in captured.out