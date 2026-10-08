import pytest
from data.input_code.d04_library import *

@pytest.mark.parametrize('title, author, isbn, expect_in_inventory', [
    ("Dune", "Frank Herbert", "1234", True),
    ("Dune", "Frank Herbert", "12", False),
])
def test_library_manager_add_book(title, author, isbn, expect_in_inventory):
    lm = LibraryManager()
    lm.add_book(title, author, isbn)
    if expect_in_inventory:
        assert isbn in lm.inventory
        b = lm.inventory[isbn]
        assert b.title == title
        assert b.author == author
        assert b.isbn == isbn
        assert b.is_available is True
    else:
        assert isbn not in lm.inventory

def test_library_manager_add_book_none_isbn_raises():
    lm = LibraryManager()
    with pytest.raises(TypeError):
        lm.add_book("Dune", "Frank Herbert", None)

def test_library_manager_borrow_book_not_found():
    lm = LibraryManager()
    lm.borrow_book("0000")
    assert lm.inventory == {}

def test_library_manager_return_book_not_found():
    lm = LibraryManager()
    lm.return_book("0000")
    assert lm.inventory == {}

def test_library_manager_show_inventory_empty(capsys):
    lm = LibraryManager()
    lm.show_inventory()
    captured = capsys.readouterr()
    assert "The library is empty." in captured.out

import pytest
from data.input_code.d04_library import *

def test_T_MISSING_BORROW_SUCCESS():
    lm = LibraryManager()
    lm.add_book("The Great Gatsby", "F. Scott Fitzgerald", "1111")
    lm.borrow_book("1111")
    assert lm.inventory["1111"].is_available is False

def test_T_MISSING_BORROW_ALREADY_BORROWED():
    lm = LibraryManager()
    lm.add_book("Borrowed Title", "Author X", "2222")
    lm.borrow_book("2222")
    lm.borrow_book("2222")
    assert lm.inventory["2222"].is_available is False

def test_T_MISSING_RETURN_SUCCESS():
    lm = LibraryManager()
    lm.add_book("Returnable Book", "Author Y", "3333")
    lm.borrow_book("3333")
    lm.return_book("3333")
    assert lm.inventory["3333"].is_available is True

def test_T_MISSING_RETURN_ALREADY_AVAILABLE():
    lm = LibraryManager()
    lm.add_book("Fresh Book", "Author Z", "4444")
    lm.return_book("4444")
    assert lm.inventory["4444"].is_available is True

def test_T_MISSING_SHOW_INVENTORY_NON_EMPTY(capsys):
    lm = LibraryManager()
    lm.add_book("Alpha", "Author A", "1112")
    lm.add_book("Beta", "Author B", "1113")
    lm.borrow_book("1112")
    lm.show_inventory()
    captured = capsys.readouterr()
    assert "[Borrowed] Alpha by Author A (ISBN: 1112)" in captured.out
    assert "[Available] Beta by Author B (ISBN: 1113)" in captured.out

def test_T_MISSING_ADD_BOOK_THREE_CHAR_ISBN():
    lm = LibraryManager()
    lm.add_book("Three Character ISBN", "Author C", "123")
    assert "123" in lm.inventory
    b = lm.inventory["123"]
    assert b.title == "Three Character ISBN"
    assert b.author == "Author C"
    assert b.isbn == "123"
    assert b.is_available is True

def test_T_MISSING_BORROW_NOT_FOUND_PRINTS():
    lm = LibraryManager()
    lm.borrow_book("0000")
    assert lm.inventory == {}

def test_T_MISSING_RETURN_NOT_FOUND_PRINTS():
    lm = LibraryManager()
    lm.return_book("0000")
    assert lm.inventory == {}

def test_T_MISSING_ADD_BOOK_INVALID_ISBN_PRINTS():
    lm = LibraryManager()
    lm.add_book("Sample", "Author", "12")
    assert "12" not in lm.inventory

def test_T_MISSING_DUPLICATE_ISBN_PRINTS(capsys):
    lm = LibraryManager()
    lm.add_book("Original Title", "Original Author", "1111")
    lm.add_book("Duplicate Title", "Author", "1111")
    captured = capsys.readouterr()
    assert "[!] Error: A book with ISBN 1111 already exists." in captured.out

def test_T_MISSING_BOOK_STR_CONSISTENCY():
    b = Book("StrTest", "Auth", "2222")
    assert str(b) == "[Available] StrTest by Auth (ISBN: 2222)"