import pytest
from data.input_code.d04_library import *

def test_library_plan_sequence(capfd):
    # T1_BOOK_INIT
    book = Book("Test Book", "Test Author", "1234567890")
    assert isinstance(book, Book)

    # T2_BOOK_STR
    assert str(book) == "[Available] Test Book by Test Author (ISBN: 1234567890)"

    # T3_LIB_INIT
    lib = LibraryManager()
    assert isinstance(lib, LibraryManager)

    # T4_ADD_BOOK_OK
    lib.add_book("Test Book", "Test Author", "1234567890")
    out = capfd.readouterr().out
    assert "Success: Added 'Test Book' to the library." in out

    # T5_ADD_BOOK_SHORT_ISBN
    lib.add_book("Test Book", "Test Author", "12")
    out = capfd.readouterr().out
    assert "[!] Error: ISBN '12' is too short." in out

    # T6_ADD_BOOK_DUPLICATE_ISBN
    lib.add_book("Test Book 2", "Test Author 2", "1234567890")
    out = capfd.readouterr().out
    assert "[!] Error: A book with ISBN 1234567890 already exists." in out

    # T7_BORROW_BOOK_OK
    lib.borrow_book("1234567890")
    out = capfd.readouterr().out
    assert "Success: You have borrowed 'Test Book'." in out
    assert lib.inventory["1234567890"].is_available is False

    # T8_BORROW_BOOK_NOT_FOUND
    lib.borrow_book("9876543210")
    out = capfd.readouterr().out
    assert "[!] Error: Book with ISBN 9876543210 not found." in out

    # T9_BORROW_BOOK_ALREADY_BORROWED
    lib.borrow_book("1234567890")
    out = capfd.readouterr().out
    assert "[!] Unavailable: 'Test Book' is currently borrowed by someone else." in out

    # T10_RETURN_BOOK_OK
    lib.return_book("1234567890")
    out = capfd.readouterr().out
    assert "Success: 'Test Book' has been returned." in out
    assert lib.inventory["1234567890"].is_available is True

    # T11_RETURN_BOOK_NOT_FOUND
    lib.return_book("9876543210")
    out = capfd.readouterr().out
    assert "[!] Error: We do not own a book with ISBN 9876543210." in out

    # T12_RETURN_BOOK_ALREADY_RETURNED
    lib.return_book("1234567890")
    out = capfd.readouterr().out
    assert "[!] Strange: You are trying to return 'Test Book', but it was already here." in out

    # T13_SHOW_INVENTORY_EMPTY
    lib.inventory.clear()
    lib.show_inventory()
    out = capfd.readouterr().out
    assert "The library is empty." in out

    # T14_SHOW_INVENTORY_NOT_EMPTY
    lib.add_book("Test Book", "Test Author", "1234567890")
    out = capfd.readouterr().out
    assert "Success: Added 'Test Book' to the library." in out
    lib.show_inventory()
    out = capfd.readouterr().out
    assert "[Available] Test Book by Test Author (ISBN: 1234567890)" in out