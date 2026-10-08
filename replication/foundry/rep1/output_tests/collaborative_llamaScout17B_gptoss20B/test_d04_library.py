import pytest
from data.input_code.d04_library import *

def test_library_manager_plan(capsys):
    # T1_INIT
    lm1 = LibraryManager()
    assert lm1.inventory == {}

    # T2_ADD_VALID
    lm1.add_book(title="Book1", author="Author1", isbn="1234567890")
    out = capsys.readouterr().out
    assert "Success: Added 'Book1' to the library." in out
    assert "1234567890" in lm1.inventory
    assert lm1.inventory["1234567890"].title == "Book1"

    # T3_ADD_DUPLICATE
    lm1.add_book(title="Book1", author="Author1", isbn="1234567890")
    out = capsys.readouterr().out
    assert "[!] Error: A book with ISBN 1234567890 already exists." in out
    assert len(lm1.inventory) == 1

    # T4_ADD_INVALID_ISBN
    lm1.add_book(title="Book2", author="Author2", isbn="12")
    out = capsys.readouterr().out
    assert "[!] Error: ISBN '12' is too short." in out
    assert len(lm1.inventory) == 1

    # T5_BORROW_EXISTING_AVAILABLE
    lm1.borrow_book(isbn="1234567890")
    out = capsys.readouterr().out
    assert "Success: You have borrowed 'Book1'." in out
    assert not lm1.inventory["1234567890"].is_available

    # T6_BORROW_EXISTING_UNAVAILABLE
    lm1.borrow_book(isbn="1234567890")
    out = capsys.readouterr().out
    assert "[!] Unavailable: 'Book1' is currently borrowed by someone else." in out
    assert not lm1.inventory["1234567890"].is_available

    # T7_BORROW_NON_EXISTENT
    lm1.borrow_book(isbn="9999999999")
    out = capsys.readouterr().out
    assert "[!] Error: Book with ISBN 9999999999 not found." in out

    # T8_RETURN_EXISTING_BORROWED
    lm1.return_book(isbn="1234567890")
    out = capsys.readouterr().out
    assert "Success: 'Book1' has been returned." in out
    assert lm1.inventory["1234567890"].is_available

    # T9_RETURN_EXISTING_AVAILABLE
    lm1.return_book(isbn="1234567890")
    out = capsys.readouterr().out
    assert "[!] Strange: You are trying to return 'Book1', but it was already here." in out
    assert lm1.inventory["1234567890"].is_available

    # T10_RETURN_NON_EXISTENT
    lm1.return_book(isbn="9999999999")
    out = capsys.readouterr().out
    assert "[!] Error: We do not own a book with ISBN 9999999999." in out

    # T11_SHOW_EMPTY_INVENTORY
    lm2 = LibraryManager()
    lm2.show_inventory()
    out = capsys.readouterr().out
    assert "The library is empty." in out

    # T12_SHOW_POPULATED_INVENTORY
    lm3 = LibraryManager()
    lm3.add_book(title="Book1", author="Author1", isbn="1234567890")
    lm3.show_inventory()
    out = capsys.readouterr().out
    assert "[Available] Book1 by Author1 (ISBN: 1234567890)" in out