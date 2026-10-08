import pytest
from data.input_code.d04_library import Book, LibraryManager

def test_book_str_representation():
    book = Book(title="1984", author="George Orwell", isbn="12345")
    # Initially available
    assert str(book) == "[Available] 1984 by George Orwell (ISBN: 12345)"
    # Change status
    book.is_available = False
    assert str(book) == "[Borrowed] 1984 by George Orwell (ISBN: 12345)"

def test_add_book_validations(capsys):
    manager = LibraryManager()
    # ISBN too short
    manager.add_book("Short ISBN", "Author", "12")
    captured = capsys.readouterr()
    assert "[!] Error: ISBN '12' is too short." in captured.out
    assert manager.inventory == {}

    # Valid addition
    manager.add_book("Valid Book", "Author", "ABC")
    captured = capsys.readouterr()
    assert "Success: Added 'Valid Book' to the library." in captured.out
    assert "ABC" in manager.inventory
    assert isinstance(manager.inventory["ABC"], Book)

    # Duplicate ISBN
    manager.add_book("Another Book", "Author", "ABC")
    captured = capsys.readouterr()
    assert "[!] Error: A book with ISBN ABC already exists." in captured.out
    # Inventory unchanged
    assert len(manager.inventory) == 1
    assert manager.inventory["ABC"].title == "Valid Book"

def test_borrow_book_logic(capsys):
    manager = LibraryManager()
    manager.add_book("Borrowable", "Author", "XYZ")
    capsys.readouterr()  # clear

    # Non‑existent ISBN
    manager.borrow_book("NOPE")
    out = capsys.readouterr().out
    assert "[!] Error: Book with ISBN NOPE not found." in out

    # Successful borrow
    manager.borrow_book("XYZ")
    out = capsys.readouterr().out
    assert "Success: You have borrowed 'Borrowable'." in out
    assert not manager.inventory["XYZ"].is_available

    # Borrow again -> unavailable
    manager.borrow_book("XYZ")
    out = capsys.readouterr().out
    assert "[!] Unavailable: 'Borrowable' is currently borrowed by someone else." in out
    assert not manager.inventory["XYZ"].is_available

def test_return_book_logic(capsys):
    manager = LibraryManager()
    manager.add_book("Returnable", "Author", "RET")
    capsys.readouterr()  # clear

    # Non‑existent ISBN
    manager.return_book("NONE")
    out = capsys.readouterr().out
    assert "[!] Error: We do not own a book with ISBN NONE." in out

    # Return when already available -> strange
    manager.return_book("RET")
    out = capsys.readouterr().out
    assert "[!] Strange: You are trying to return 'Returnable', but it was already here." in out
    assert manager.inventory["RET"].is_available

    # Borrow then return successfully
    manager.borrow_book("RET")
    capsys.readouterr()
    manager.return_book("RET")
    out = capsys.readouterr().out
    assert "Success: 'Returnable' has been returned." in out
    assert manager.inventory["RET"].is_available

def test_show_inventory_output(capsys):
    manager = LibraryManager()
    # Empty inventory
    manager.show_inventory()
    out = capsys.readouterr().out
    assert "--- Current Library Inventory ---" in out
    assert "The library is empty." in out
    assert "---------------------------------" in out

    # Add a book and show again
    manager.add_book("Visible", "Author", "VIS")
    capsys.readouterr()
    manager.show_inventory()
    out = capsys.readouterr().out
    assert "[Available] Visible by Author (ISBN: VIS)" in out
    # Ensure header/footer still present
    assert "--- Current Library Inventory ---" in out
    assert "---------------------------------" in out