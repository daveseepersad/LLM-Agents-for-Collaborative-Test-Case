import pytest
from data.input_code.d04_library import *

def test_TC1_AddShortISBN(capfd):
    lm = LibraryManager()
    lm.add_book(title="Tiny", author="A", isbn="12")
    out = capfd.readouterr().out
    assert "[!] Error: ISBN '12' is too short." in out
    assert lm.inventory == {}

def test_TC2_AddDuplicateISBN(capfd):
    lm = LibraryManager()
    # First add
    lm.add_book("First", "B", "12345")
    out1 = capfd.readouterr().out
    assert "Success: Added 'First' to the library." in out1

    # Attempt duplicate
    lm.add_book("First", "B", "12345")
    out2 = capfd.readouterr().out
    assert "[!] Error: A book with ISBN 12345 already exists." in out2

    assert "12345" in lm.inventory
    assert len(lm.inventory) == 1
    assert lm.inventory["12345"].is_available is True

def test_TC3_AddSuccess(capfd):
    lm = LibraryManager()
    lm.add_book("Novel", "C", "ABC")
    out = capfd.readouterr().out
    assert "Success: Added 'Novel' to the library." in out
    assert "ABC" in lm.inventory
    assert lm.inventory["ABC"].is_available is True

def test_TC4_BorrowNonexistent(capfd):
    lm = LibraryManager()
    lm.borrow_book("ZZZ")
    out = capfd.readouterr().out
    assert "[!] Error: Book with ISBN ZZZ not found." in out

def test_TC5_BorrowAlreadyBorrowed(capfd):
    lm = LibraryManager()
    lm.add_book("Locked", "X", "BORROW1")
    out1 = capfd.readouterr().out
    assert "Success: Added 'Locked' to the library." in out1

    # First borrow
    lm.borrow_book("BORROW1")
    out2 = capfd.readouterr().out
    assert "Success: You have borrowed 'Locked'." in out2

    # Second borrow should fail due to unavailability
    lm.borrow_book("BORROW1")
    out3 = capfd.readouterr().out
    assert "[!] Unavailable: 'Locked' is currently borrowed by someone else." in out3
    assert lm.inventory["BORROW1"].is_available is False

def test_TC6_BorrowSuccess(capfd):
    lm = LibraryManager()
    lm.add_book("Free", "Y", "BORROW2")
    _ = capfd.readouterr().out  # clear
    lm.borrow_book("BORROW2")
    out = capfd.readouterr().out
    assert "Success: You have borrowed 'Free'." in out
    assert lm.inventory["BORROW2"].is_available is False
    # Also verify the book exists in inventory
    assert "BORROW2" in lm.inventory

def test_TC7_ReturnNonexistent(capfd):
    lm = LibraryManager()
    lm.return_book("NOPE")
    out = capfd.readouterr().out
    assert "[!] Error: We do not own a book with ISBN NOPE." in out

def test_TC8_ReturnAlreadyAvailable(capfd):
    lm = LibraryManager()
    lm.add_book("Idle", "Z", "RET1")
    _ = capfd.readouterr().out  # clear
    # Attempt to return without borrowing
    lm.return_book("RET1")
    out = capfd.readouterr().out
    assert "[!] Strange: You are trying to return 'Idle', but it was already here." in out
    assert lm.inventory["RET1"].is_available is True

def test_TC9_ReturnSuccess(capfd):
    lm = LibraryManager()
    lm.add_book("Travel", "A", "RET2")
    _ = capfd.readouterr().out  # clear
    lm.borrow_book("RET2")
    _ = capfd.readouterr().out  # clear
    lm.return_book("RET2")
    out = capfd.readouterr().out
    assert "Success: Travel" in out or "Success: 'Travel' has been returned." in out
    # Final state should be available
    assert lm.inventory["RET2"].is_available is True

def test_TC10_ShowEmptyInventory(capfd):
    lm = LibraryManager()
    lm.show_inventory()
    out = capfd.readouterr().out
    assert "\n--- Current Library Inventory ---" in out
    assert "The library is empty." in out
    assert "---------------------------------\n" in out or "---------------------------------" in out

def test_TC11_ShowNonEmptyInventory(capfd):
    lm = LibraryManager()
    # Add Alpha
    lm.add_book("Alpha", "AuthorA", "AAA")
    _ = capfd.readouterr().out
    # Add Beta
    lm.add_book("Beta", "AuthorB", "BBB")
    _ = capfd.readouterr().out
    # Borrow Beta to mark as Borrowed
    lm.borrow_book("BBB")
    _ = capfd.readouterr().out

    # Show inventory
    lm.show_inventory()
    out = capfd.readouterr().out
    assert "\n--- Current Library Inventory ---" in out
    assert "[Available] Alpha by AuthorA (ISBN: AAA)" in out
    assert "[Borrowed] Beta by AuthorB (ISBN: BBB)" in out
    assert "---------------------------------\n" in out
    # Inventory keys should reflect both ISBNs
    assert set(lm.inventory.keys()) == {"AAA", "BBB"}

def test_TC12_BookStrRepresentation():
    book = Book("Gamma", "AuthorC", "CCC")
    assert str(book) == "[Available] Gamma by AuthorC (ISBN: CCC)"