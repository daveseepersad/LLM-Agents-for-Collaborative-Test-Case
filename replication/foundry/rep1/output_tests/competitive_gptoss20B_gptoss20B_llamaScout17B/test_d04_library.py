import pytest
from data.input_code.d04_library import *

def test_library_manager_flow():
    lm = LibraryManager()

    # T1_Add_Valid
    assert lm.add_book("Dune", "Frank Herbert", "111") is None
    assert "111" in lm.inventory

    # T2_Add_Duplicate
    assert lm.add_book("Dune", "Frank Herbert", "111") is None
    assert len(lm.inventory) == 1 and "111" in lm.inventory

    # T3_Borrow_NotFound
    assert lm.borrow_book("222") is None
    assert "111" in lm.inventory and lm.inventory["111"].is_available

    # T4_Borrow_Success
    assert lm.borrow_book("111") is None
    assert not lm.inventory["111"].is_available

    # T5_Borrow_Unavailable
    assert lm.borrow_book("111") is None
    assert not lm.inventory["111"].is_available

    # T6_Return_Success
    assert lm.return_book("111") is None
    assert lm.inventory["111"].is_available

    # T7_Return_AlreadyHere
    assert lm.return_book("111") is None
    assert lm.inventory["111"].is_available

    # T8_ShowInventory_NonEmpty
    assert lm.show_inventory() is None

    # T9_Add_InvalidISBNBoundary
    assert lm.add_book("The", "Anon", "12") is None
    assert "12" not in lm.inventory

import pytest
from data.input_code.d04_library import *

def test_return_not_found():
    lm = LibraryManager()
    result = lm.return_book("999")
    assert result == None
    assert "999" not in lm.inventory

def test_add_empty_isbn():
    lm = LibraryManager()
    result = lm.add_book("Sample", "Anon", "")
    assert result == None
    assert "" not in lm.inventory

def test_book_str_borrowed():
    book = Book("Dune", "Frank Herbert", "111")
    book.is_available = False
    assert str(book) == "[Borrowed] Dune by Frank Herbert (ISBN: 111)"

def test_show_inventory_empty():
    lm = LibraryManager()
    assert lm.show_inventory() is None