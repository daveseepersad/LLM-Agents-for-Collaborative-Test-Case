import pytest
from data.input_code.d04_library import Book, LibraryManager

def test_add_book_short_isbn():
    lib = LibraryManager()
    lib.add_book("Short ISBN Book", "Author A", "12")
    assert "12" not in lib.inventory

def test_add_book_duplicate_isbn(capsys):
    lib = LibraryManager()
    lib.add_book("First Book", "Author A", "12345")
    assert "12345" in lib.inventory
    lib.add_book("Duplicate Book", "Author B", "12345")
    captured = capsys.readouterr().out
    assert "[!] Error: A book with ISBN 12345 already exists." in captured
    # Ensure original book unchanged
    assert lib.inventory["12345"].title == "First Book"

def test_successful_add_and_str():
    lib = LibraryManager()
    lib.add_book("The Great Gatsby", "F. Scott Fitzgerald", "978")
    book = lib.inventory["978"]
    assert isinstance(book, Book)
    expected = "[Available] The Great Gatsby by F. Scott Fitzgerald (ISBN: 978)"
    assert str(book) == expected

def test_borrow_book_not_found(capsys):
    lib = LibraryManager()
    lib.borrow_book("999")
    captured = capsys.readouterr().out
    assert "[!] Error: Book with ISBN 999 not found." in captured

def test_borrow_book_already_borrowed(capsys):
    lib = LibraryManager()
    lib.add_book("1984", "George Orwell", "111")
    lib.borrow_book("111")  # first borrow succeeds
    lib.borrow_book("111")  # second attempt should fail
    captured = capsys.readouterr().out
    assert "Success: You have borrowed '1984'." in captured
    assert "[!] Unavailable: '1984' is currently borrowed by someone else." in captured
    # Status should remain False
    assert not lib.inventory["111"].is_available

def test_return_book_not_found(capsys):
    lib = LibraryManager()
    lib.return_book("222")
    captured = capsys.readouterr().out
    assert "[!] Error: We do not own a book with ISBN 222." in captured

def test_return_book_already_available(capsys):
    lib = LibraryManager()
    lib.add_book("Brave New World", "Aldous Huxley", "333")
    lib.return_book("333")
    captured = capsys.readouterr().out
    assert "[!] Strange: You are trying to return 'Brave New World', but it was already here." in captured
    # Book should still be available
    assert lib.inventory["333"].is_available

def test_successful_borrow_and_return(capsys):
    lib = LibraryManager()
    lib.add_book("Dune", "Frank Herbert", "444")
    lib.borrow_book("444")
    lib.return_book("444")
    captured = capsys.readouterr().out
    assert "Success: You have borrowed 'Dune'." in captured
    assert "Success: 'Dune' has been returned." in captured
    assert lib.inventory["444"].is_available

def test_show_inventory_empty_and_filled(capsys):
    lib = LibraryManager()
    lib.show_inventory()
    empty_output = capsys.readouterr().out
    assert "The library is empty." in empty_output

    lib.add_book("Sapiens", "Yuval Noah Harari", "555")
    lib.show_inventory()
    filled_output = capsys.readouterr().out
    assert "[Available] Sapiens by Yuval Noah Harari (ISBN: 555)" in filled_output
    assert "--- Current Library Inventory ---" in filled_output
    assert "---------------------------------" in filled_output