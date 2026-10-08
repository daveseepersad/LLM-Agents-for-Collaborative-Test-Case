import pytest
from data.input_code.d04_library import *

def test_T1_add_book_valid():
    lm = LibraryManager()
    lm.add_book("Book1", "Author1", "123")
    assert "123" in lm.inventory
    assert lm.inventory["123"].title == "Book1"
    assert lm.inventory["123"].author == "Author1"
    assert lm.inventory["123"].is_available is True

def test_T2_add_book_short_isbn():
    lm = LibraryManager()
    lm.add_book("Book2", "Author2", "12")
    assert "12" not in lm.inventory

def test_T3_add_book_duplicate_isbn():
    lm = LibraryManager()
    lm.add_book("Book1", "Author1", "123")
    lm.add_book("Book3", "Author3", "123")
    assert len(lm.inventory) == 1
    assert "123" in lm.inventory
    assert lm.inventory["123"].title == "Book1"

def test_T4_borrow_non_existent():
    lm = LibraryManager()
    lm.borrow_book("1234")
    assert "1234" not in lm.inventory

def test_T5_borrow_available_book():
    lm = LibraryManager()
    lm.add_book("Book", "Author", "123")
    lm.borrow_book("123")
    assert not lm.inventory["123"].is_available

def test_T6_borrow_already_borrowed():
    lm = LibraryManager()
    lm.add_book("Book", "Author", "123")
    lm.borrow_book("123")
    lm.borrow_book("123")
    assert not lm.inventory["123"].is_available

def test_T7_return_non_existent():
    lm = LibraryManager()
    lm.return_book("1234")

def test_T8_return_available_book():
    lm = LibraryManager()
    lm.add_book("Book", "Author", "123")
    lm.return_book("123")
    assert lm.inventory["123"].is_available

def test_T9_return_borrowed_book():
    lm = LibraryManager()
    lm.add_book("Book", "Author", "123")
    lm.borrow_book("123")
    lm.return_book("123")
    assert lm.inventory["123"].is_available

def test_T10_show_inventory_empty(capfd):
    lm = LibraryManager()
    lm.show_inventory()
    captured = capfd.readouterr()
    assert "The library is empty." in captured.out

def test_T11_show_inventory_non_empty(capfd):
    lm = LibraryManager()
    lm.add_book("Book", "Author", "123")
    lm.show_inventory()
    captured = capfd.readouterr()
    assert "[Available] Book by Author (ISBN: 123)" in captured.out

def test_T12_book_init():
    b = Book("Test", "Test", "12345")
    assert b.title == "Test"
    assert b.author == "Test"
    assert b.isbn == "12345"
    assert b.is_available is True

def test_T13_book_str_available():
    b = Book("Test", "Test", "12345")
    assert str(b) == "[Available] Test by Test (ISBN: 12345)"

def test_T14_book_str_borrowed():
    b = Book("Test", "Test", "12345")
    b.is_available = False
    assert str(b) == "[Borrowed] Test by Test (ISBN: 12345)"