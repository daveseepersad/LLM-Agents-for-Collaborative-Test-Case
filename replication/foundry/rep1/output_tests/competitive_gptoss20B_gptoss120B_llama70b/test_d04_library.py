import pytest
from data.input_code.d04_library import *

@pytest.fixture
def manager():
    return LibraryManager()

def test_T1_AddBook_ShortISBN(manager, capsys):
    manager.add_book(title="The Tiny Book", author="A. Author", isbn="12")
    captured = capsys.readouterr().out.strip()
    assert captured == "[!] Error: ISBN '12' is too short."

def test_T2_AddBook_New(manager, capsys):
    manager.add_book(title="Dune", author="Frank Herbert", isbn="9780441172719")
    captured = capsys.readouterr().out.strip()
    assert captured == "Success: Added 'Dune' to the library."
    assert "9780441172719" in manager.inventory
    assert isinstance(manager.inventory["9780441172719"], Book)

def test_T3_AddBook_Duplicate(manager, capsys):
    # First add the book
    manager.add_book(title="Dune", author="Frank Herbert", isbn="9780441172719")
    capsys.readouterr()  # clear previous output
    # Attempt duplicate
    manager.add_book(title="Dune - Duplicate", author="F. Herbert", isbn="9780441172719")
    captured = capsys.readouterr().out.strip()
    assert captured == "[!] Error: A book with ISBN 9780441172719 already exists."

def test_T4_BorrowBook_NotFound(manager, capsys):
    manager.borrow_book(isbn="0000")
    captured = capsys.readouterr().out.strip()
    assert captured == "[!] Error: Book with ISBN 0000 not found."

def test_T5_BorrowBook_Available(manager, capsys):
    manager.add_book(title="Dune", author="Frank Herbert", isbn="9780441172719")
    capsys.readouterr()  # clear add_book output
    manager.borrow_book(isbn="9780441172719")
    captured = capsys.readouterr().out.strip()
    assert captured == "Success: You have borrowed 'Dune'."
    assert not manager.inventory["9780441172719"].is_available

def test_T6_BorrowBook_Unavailable(manager, capsys):
    manager.add_book(title="Dune", author="Frank Herbert", isbn="9780441172719")
    capsys.readouterr()
    # First borrow to make it unavailable
    manager.borrow_book(isbn="9780441172719")
    capsys.readouterr()
    # Second borrow attempt
    manager.borrow_book(isbn="9780441172719")
    captured = capsys.readouterr().out.strip()
    assert captured == "[!] Unavailable: 'Dune' is currently borrowed by someone else."

def test_T7_ReturnBook_NotFound(manager, capsys):
    manager.return_book(isbn="1111")
    captured = capsys.readouterr().out.strip()
    assert captured == "[!] Error: We do not own a book with ISBN 1111."

def test_T8_ReturnBook_Success(manager, capsys):
    manager.add_book(title="Dune", author="Frank Herbert", isbn="9780441172719")
    capsys.readouterr()
    manager.borrow_book(isbn="9780441172719")
    capsys.readouterr()
    manager.return_book(isbn="9780441172719")
    captured = capsys.readouterr().out.strip()
    assert captured == "Success: 'Dune' has been returned."
    assert manager.inventory["9780441172719"].is_available

def test_T9_ReturnBook_Strange(manager, capsys):
    manager.add_book(title="Dune", author="Frank Herbert", isbn="9780441172719")
    capsys.readouterr()
    # Return without borrowing first
    manager.return_book(isbn="9780441172719")
    captured = capsys.readouterr().out.strip()
    assert captured == "[!] Strange: You are trying to return 'Dune', but it was already here."

def test_T10_ShowInventory_Empty(manager, capsys):
    manager.show_inventory()
    captured = capsys.readouterr().out
    assert "The library is empty." in captured

def test_T11_ShowInventory_NonEmpty(manager, capsys):
    manager.add_book(title="Dune", author="Frank Herbert", isbn="9780441172719")
    manager.add_book(title="1984", author="George Orwell", isbn="9780451524935")
    capsys.readouterr()  # clear add_book outputs
    manager.show_inventory()
    captured = capsys.readouterr().out
    # Verify that each book's __str__ appears in the output
    assert "[Available] Dune by Frank Herbert (ISBN: 9780441172719)" in captured
    assert "[Available] 1984 by George Orwell (ISBN: 9780451524935)" in captured