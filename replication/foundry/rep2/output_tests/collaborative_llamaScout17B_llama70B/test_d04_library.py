import pytest
from data.input_code.d04_library import *




def test_show_inventory(capsys):
    library = LibraryManager()
    library.show_inventory()
    captured = capsys.readouterr()
    assert "The library is empty." in captured.out

def test_show_inventory_non_empty(capsys):
    library = LibraryManager()
    library.add_book("Book1", "Author1", "123")
    library.show_inventory()
    captured = capsys.readouterr()
    assert "[Available] Book1 by Author1 (ISBN: 123)" in captured.out

def test_book_init():
    book = Book("Test", "Test", "123")
    assert book.title == "Test"
    assert book.author == "Test"
    assert book.isbn == "123"
    assert book.is_available == True

def test_book_str():
    book = Book("Test", "Test", "123")
    assert str(book) == "[Available] Test by Test (ISBN: 123)"

def test_book_str_borrowed():
    book = Book("Test", "Test", "123")
    book.is_available = False
    assert str(book) == "[Borrowed] Test by Test (ISBN: 123)"