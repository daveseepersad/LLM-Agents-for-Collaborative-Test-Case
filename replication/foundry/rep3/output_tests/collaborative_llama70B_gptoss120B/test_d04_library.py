import pytest
from data.input_code.d04_library import *

# ---------- Book tests ----------
def test_book_init():
    b = Book(title="Test Book", author="Test Author", isbn="1234567890")
    assert b.title == "Test Book"
    assert b.author == "Test Author"
    assert b.isbn == "1234567890"
    assert b.is_available is True

def test_book_str():
    b = Book(title="Test Book", author="Test Author", isbn="1234567890")
    assert str(b) == "[Available] Test Book by Test Author (ISBN: 1234567890)"
    b.is_available = False
    assert str(b) == "[Borrowed] Test Book by Test Author (ISBN: 1234567890)"


# ---------- LibraryManager tests ----------
def test_library_manager_init():
    lm = LibraryManager()
    assert isinstance(lm.inventory, dict)
    assert not lm.inventory  # should be empty


@pytest.mark.parametrize(
    "title, author, isbn, expected_output, prepopulate",
    [
        # successful addition
        ("Test Book", "Test Author", "1234567890",
         "Success: Added 'Test Book' to the library.", False),
        # short ISBN
        ("Test Book", "Test Author", "12",
         "[!] Error: ISBN '12' is too short.", False),
        # duplicate ISBN (prepopulate with same ISBN first)
        ("Test Book 2", "Test Author 2", "1234567890",
         "[!] Error: A book with ISBN 1234567890 already exists.", True),
    ]
)
def test_add_book(title, author, isbn, expected_output, prepopulate, capsys):
    lm = LibraryManager()
    if prepopulate:
        lm.add_book("Test Book", "Test Author", "1234567890")
        capsys.readouterr()  # clear previous output
    lm.add_book(title, author, isbn)
    out = capsys.readouterr().out.strip().splitlines()[-1]
    assert out == expected_output


@pytest.mark.parametrize(
    "setup_actions, isbn, expected_output",
    [
        # borrow available book
        (["add"], "1234567890",
         "Success: You have borrowed 'Test Book'."),
        # borrow unavailable book (already borrowed)
        (["add", "borrow"], "1234567890",
         "[!] Unavailable: 'Test Book' is currently borrowed by someone else."),
        # borrow non‑existent book
        ([], "9876543210",
         "[!] Error: Book with ISBN 9876543210 not found."),
    ]
)
def test_borrow_book(setup_actions, isbn, expected_output, capsys):
    lm = LibraryManager()
    if "add" in setup_actions:
        lm.add_book("Test Book", "Test Author", "1234567890")
        capsys.readouterr()
    if "borrow" in setup_actions:
        lm.borrow_book("1234567890")
        capsys.readouterr()
    lm.borrow_book(isbn)
    out = capsys.readouterr().out.strip().splitlines()[-1]
    assert out == expected_output


@pytest.mark.parametrize(
    "setup_actions, isbn, expected_output",
    [
        # return borrowed book
        (["add", "borrow"], "1234567890",
         "Success: 'Test Book' has been returned."),
        # return already returned book
        (["add"], "1234567890",
         "[!] Strange: You are trying to return 'Test Book', but it was already here."),
        # return non‑existent book
        ([], "9876543210",
         "[!] Error: We do not own a book with ISBN 9876543210."),
    ]
)
def test_return_book(setup_actions, isbn, expected_output, capsys):
    lm = LibraryManager()
    if "add" in setup_actions:
        lm.add_book("Test Book", "Test Author", "1234567890")
        capsys.readouterr()
    if "borrow" in setup_actions:
        lm.borrow_book("1234567890")
        capsys.readouterr()
    lm.return_book(isbn)
    out = capsys.readouterr().out.strip().splitlines()[-1]
    assert out == expected_output


@pytest.mark.parametrize(
    "prepopulate, expected_line",
    [
        (False, "The library is empty."),
        (True, "[Available] Test Book by Test Author (ISBN: 1234567890)"),
    ]
)
def test_show_inventory(prepopulate, expected_line, capsys):
    lm = LibraryManager()
    if prepopulate:
        lm.add_book("Test Book", "Test Author", "1234567890")
        capsys.readouterr()
    lm.show_inventory()
    out = capsys.readouterr().out
    # The expected line should appear somewhere in the printed block
    assert expected_line in out