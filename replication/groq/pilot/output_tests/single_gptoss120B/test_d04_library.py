import pytest
from data.input_code.d04_library import Book, LibraryManager

def test_add_book_short_isbn(capsys):
    lib = LibraryManager()
    lib.add_book("Short ISBN", "Author A", "12")  # length < 3
    captured = capsys.readouterr()
    assert "[!] Error: ISBN '12' is too short." in captured.out
    assert "12" not in lib.inventory

def test_add_book_duplicate_isbn(capsys):
    lib = LibraryManager()
    lib.add_book("First Book", "Author A", "12345")
    captured1 = capsys.readouterr()
    assert "Success: Added 'First Book' to the library." in captured1.out
    # Attempt duplicate
    lib.add_book("Second Book", "Author B", "12345")
    captured2 = capsys.readouterr()
    assert "[!] Error: A book with ISBN 12345 already exists." in captured2.out
    # Ensure original book unchanged
    assert lib.inventory["12345"].title == "First Book"

def test_add_book_success(capsys):
    lib = LibraryManager()
    lib.add_book("Python 101", "Guido", "ISBN001")
    captured = capsys.readouterr()
    assert "Success: Added 'Python 101' to the library." in captured.out
    book = lib.inventory.get("ISBN001")
    assert isinstance(book, Book)
    assert book.title == "Python 101"
    assert book.author == "Guido"
    assert book.isbn == "ISBN001"
    assert book.is_available is True

def test_borrow_book_nonexistent(capsys):
    lib = LibraryManager()
    lib.borrow_book("NONEXIST")
    captured = capsys.readouterr()
    assert "[!] Error: Book with ISBN NONEXIST not found." in captured.out

def test_borrow_book_already_borrowed(capsys):
    lib = LibraryManager()
    lib.add_book("Borrowed Book", "Author", "ISBNB")
    capsys.readouterr()  # clear
    # Borrow first time
    lib.borrow_book("ISBNB")
    capsys.readouterr()
    # Attempt second borrow
    lib.borrow_book("ISBNB")
    captured = capsys.readouterr()
    assert "[!] Unavailable: 'Borrowed Book' is currently borrowed by someone else." in captured.out
    # Status should remain False
    assert lib.inventory["ISBNB"].is_available is False

def test_borrow_book_success(capsys):
    lib = LibraryManager()
    lib.add_book("Available Book", "Author", "ISBNC")
    capsys.readouterr()
    lib.borrow_book("ISBNC")
    captured = capsys.readouterr()
    assert "Success: You have borrowed 'Available Book'." in captured.out
    assert lib.inventory["ISBNC"].is_available is False

def test_return_book_nonexistent(capsys):
    lib = LibraryManager()
    lib.return_book("NOISBN")
    captured = capsys.readouterr()
    assert "[!] Error: We do not own a book with ISBN NOISBN." in captured.out

def test_return_book_already_available(capsys):
    lib = LibraryManager()
    lib.add_book("Never Borrowed", "Author", "ISBND")
    capsys.readouterr()
    lib.return_book("ISBND")
    captured = capsys.readouterr()
    assert "[!] Strange: You are trying to return 'Never Borrowed', but it was already here." in captured.out
    assert lib.inventory["ISBND"].is_available is True

def test_return_book_success(capsys):
    lib = LibraryManager()
    lib.add_book("To Return", "Author", "ISBNE")
    capsys.readouterr()
    lib.borrow_book("ISBNE")
    capsys.readouterr()
    lib.return_book("ISBNE")
    captured = capsys.readouterr()
    assert "Success: 'To Return' has been returned." in captured.out
    assert lib.inventory["ISBNE"].is_available is True


def test_show_inventory_with_books(capsys):
    lib = LibraryManager()
    lib.add_book("Book One", "Author1", "ISBN1")
    lib.add_book("Book Two", "Author2", "ISBN2")
    capsys.readouterr()
    lib.borrow_book("ISBN2")
    capsys.readouterr()
    lib.show_inventory()
    captured = capsys.readouterr()
    output = captured.out
    # Check both books are listed with correct status
    assert "[Available] Book One by Author1 (ISBN: ISBN1)" in output
    assert "[Borrowed] Book Two by Author2 (ISBN: ISBN2)" in output
    # Header/footer present
    assert "--- Current Library Inventory ---" in output
    assert "---------------------------------" in output