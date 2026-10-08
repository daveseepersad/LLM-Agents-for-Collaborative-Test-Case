import pytest
from data.input_code.d04_library import *

@pytest.mark.parametrize('title, author, isbn, should_exist, expected_title, expected_author', [
    ('Sample', 'Author', '12', False, None, None),
    ('Brave New World', 'Aldous Huxley', '12345', True, 'Brave New World', 'Aldous Huxley')
])
def test_add_book(title, author, isbn, should_exist, expected_title, expected_author):
    lm = LibraryManager()
    lm.add_book(title, author, isbn)
    if should_exist:
        assert isbn in lm.inventory
        book = lm.inventory[isbn]
        assert book.title == expected_title
        assert book.author == expected_author
    else:
        assert isbn not in lm.inventory

def test_borrow_nonexistent_book():
    lm = LibraryManager()
    lm.borrow_book("9999")
    assert "9999" not in lm.inventory

def test_return_nonexistent_book():
    lm = LibraryManager()
    lm.return_book("9999")
    assert "9999" not in lm.inventory

def test_show_inventory_empty(capsys):
    lm = LibraryManager()
    lm.show_inventory()
    captured = capsys.readouterr().out
    assert "The library is empty." in captured

import pytest
from data.input_code.d04_library import *

def test_T_MISSING_BORROW_SUCCESS(capsys):
    lm = LibraryManager()
    # Pre-seed inventory with the required book
    lm.inventory["111"] = Book("Dune", "Frank Herbert", "111")
    lm.borrow_book("111")
    captured = capsys.readouterr().out
    assert "Success: You have borrowed 'Dune'." in captured
    assert lm.inventory["111"].is_available is False

def test_T_MISSING_BORROW_UNAVAILABLE(capsys):
    lm = LibraryManager()
    # Pre-seed inventory with the required book and set it as already borrowed
    lm.inventory["111"] = Book("Dune", "Frank Herbert", "111")
    lm.inventory["111"].is_available = False
    lm.borrow_book("111")
    captured = capsys.readouterr().out
    assert "Unavailable: 'Dune' is currently borrowed by someone else." in captured
    assert lm.inventory["111"].is_available is False

def test_T_MISSING_RETURN_AFTER_BORROW(capsys):
    lm = LibraryManager()
    # Pre-seed inventory with the required book and mark it as borrowed
    b = Book("Dune", "Frank Herbert", "111")
    b.is_available = False
    lm.inventory["111"] = b
    lm.return_book("111")
    captured = capsys.readouterr().out
    assert "Success: 'Dune' has been returned." in captured
    assert lm.inventory["111"].is_available is True

def test_T_MISSING_RETURN_NOT_BORROWED(capsys):
    lm = LibraryManager()
    # Pre-seed inventory with the required book and ensure it's not borrowed
    b = Book("Dune", "Frank Herbert", "111")
    b.is_available = True
    lm.inventory["111"] = b
    lm.return_book("111")
    captured = capsys.readouterr().out
    assert "Strange: You are trying to return 'Dune', but it was already here." in captured
    assert lm.inventory["111"].is_available is True

def test_T_MISSING_ADD_ISBN3(capsys):
    lm = LibraryManager()
    lm.add_book("BoundaryBook", "AuthorX", "123")
    captured = capsys.readouterr().out
    assert "Success: Added 'BoundaryBook' to the library." in captured
    assert "123" in lm.inventory
    book = lm.inventory["123"]
    assert book.title == "BoundaryBook"
    assert book.author == "AuthorX"

def test_T_MISSING_SHOW_INVENTORY_NON_EMPTY(capsys):
    lm = LibraryManager()
    lm.inventory["456"] = Book("SampleBook", "AuthorA", "456")
    lm.show_inventory()
    captured = capsys.readouterr().out
    assert "--- Current Library Inventory ---" in captured
    assert "[Available] SampleBook by AuthorA (ISBN: 456)" in captured

import pytest
from data.input_code.d04_library import *

def test_T_MISSING_DUPLICATE_ADD(capsys):
    lm = LibraryManager()
    lm.inventory['12345'] = Book('Existing', 'Author', '12345')
    lm.add_book('Duplicate', 'Author2', '12345')
    captured = capsys.readouterr().out
    assert "A book with ISBN 12345 already exists." in captured
    # Ensure inventory was not modified
    assert '12345' in lm.inventory
    book = lm.inventory['12345']
    assert book.title == 'Existing'
    assert book.author == 'Author'
    assert book.isbn == '12345'

def test_T_MISSING_ADD_ISBN_TOO_SHORT(capsys):
    lm = LibraryManager()
    lm.add_book('Short', 'Author', '12')
    captured = capsys.readouterr().out
    assert "ISBN '12' is too short." in captured
    assert "12" not in lm.inventory

def test_T_MISSING_SHOW_INVENTORY_BORROWED_DISPLAY(capsys):
    lm = LibraryManager()
    lm.inventory['001'] = Book('Available', 'AuthorA', '001')
    lm.inventory['001'].is_available = True
    b = Book('Borrowed', 'AuthorB', '002')
    b.is_available = False
    lm.inventory['002'] = b
    lm.show_inventory()
    captured = capsys.readouterr().out
    assert "[Borrowed] Borrowed by AuthorB (ISBN: 002)" in captured