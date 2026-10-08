import pytest
from data.input_code.d04_library import *

def test_T_sequence_operations():
    lm = LibraryManager()

    # T1: Add valid book
    assert lm.add_book("Book1", "Author1", "123") is None

    # T2: ISBN too short
    assert lm.add_book("Book2", "Author2", "12") is None

    # T3: Duplicate ISBN
    assert lm.add_book("Book3", "Author3", "123") is None

    # T4: Borrow non-existent book
    assert lm.borrow_book("1234") is None

    # T5: Borrow available book
    assert lm.borrow_book("123") is None

    # T6: Borrow already borrowed
    assert lm.borrow_book("123") is None

    # T7: Return non-existent book
    assert lm.return_book("1234") is None

    # T8: Return available (or borrowed) book
    assert lm.return_book("123") is None

    # T9: Return again (now should be already available)
    assert lm.return_book("123") is None

def test_show_inventory_behaviors(capsys):
    lm = LibraryManager()

    # T10: Show inventory when empty
    lm.show_inventory()
    out = capsys.readouterr().out
    assert "The library is empty." in out

    # T11: Show inventory when non-empty
    lm.add_book("BookA", "AuthorA", "999")
    lm.show_inventory()
    out = capsys.readouterr().out
    assert "[Available] BookA by AuthorA (ISBN: 999)" in out

def test_book_init_and_str():
    # T12: Initialize book
    b = Book("Test", "Test", "123")
    assert b.title == "Test"
    assert b.author == "Test"
    assert b.isbn == "123"
    assert b.is_available is True

    # T13: String representation of available book
    assert str(b) == "[Available] Test by Test (ISBN: 123)"

    # T14: String representation of borrowed book
    b.is_available = False
    assert str(b) == "[Borrowed] Test by Test (ISBN: 123)"