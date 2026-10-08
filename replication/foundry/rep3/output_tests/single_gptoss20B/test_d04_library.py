import pytest
from data.input_code.d04_library import Book, LibraryManager

def test_book_str_and_status():
    b = Book("The Python Life", "Guido", "123")
    assert "[Available]" in str(b)
    assert "The Python Life" in str(b)
    assert "Guido" in str(b)
    b.is_available = False
    assert "[Borrowed]" in str(b)

def test_add_book_validation_dup_and_none(capsys):
    lm = LibraryManager()
    # ISBN too short
    lm.add_book("Book One", "Author A", "12")
    captured = capsys.readouterr().out
    assert "too short" in captured

    # Valid add
    lm.add_book("Book Two", "Author B", "123")
    captured = capsys.readouterr().out
    assert "Success: Added" in captured
    assert "123" in lm.inventory

    # Duplicate ISBN
    lm.add_book("Another Book", "Author C", "123")
    captured = capsys.readouterr().out
    assert "already exists" in captured

    # None ISBN should raise a TypeError due to len(None)
    with pytest.raises(TypeError):
        lm.add_book("Book None", "Author N", None)

def test_borrow_and_return_flow(capsys):
    lm = LibraryManager()
    lm.add_book("Borrowable", "Author", "999")
    _ = capsys.readouterr().out  # clear any output from add_book

    # Borrow existing book
    lm.borrow_book("999")
    captured = capsys.readouterr().out
    assert "Success: You have borrowed" in captured

    # Borrow again should be unavailable
    lm.borrow_book("999")
    captured = capsys.readouterr().out
    assert "Unavailable" in captured

    # Borrow non-existent
    lm.borrow_book("000")
    captured = capsys.readouterr().out
    assert "not found" in captured

    # Return non-existent
    lm.return_book("000")
    captured = capsys.readouterr().out
    assert "We do not own a book" in captured

    # Return borrowed book
    lm.return_book("999")
    captured = capsys.readouterr().out
    assert "has been returned" in captured

    # Return again when already there
    lm.return_book("999")
    captured = capsys.readouterr().out
    assert "Strange" in captured or "already here" in captured

def test_show_inventory_empty_and_nonempty(capsys):
    lm = LibraryManager()

    # Empty inventory
    lm.show_inventory()
    captured = capsys.readouterr().out
    assert "Current Library Inventory" in captured
    assert "The library is empty." in captured

    # Add a book and show inventory again
    lm.add_book("Inventory Book", "Author", "321")
    _ = capsys.readouterr().out  # clear

    lm.show_inventory()
    captured = capsys.readouterr().out
    assert "Current Library Inventory" in captured
    assert "Inventory Book" in captured
    assert "[Available]" in captured