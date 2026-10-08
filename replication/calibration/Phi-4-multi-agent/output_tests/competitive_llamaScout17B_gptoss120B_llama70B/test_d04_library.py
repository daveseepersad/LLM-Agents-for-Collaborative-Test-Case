import pytest
from data.input_code.d04_library import *

# ---------- Fixtures ----------
@pytest.fixture
def empty_manager():
    """Provides a fresh LibraryManager with no books."""
    return LibraryManager()


@pytest.fixture
def manager_with_one_book():
    """Provides a LibraryManager with a single available book (ISBN 12345)."""
    mgr = LibraryManager()
    mgr.add_book("Book One", "Author A", "12345")
    return mgr


@pytest.fixture
def manager_with_borrowed_book():
    """Provides a LibraryManager with a single borrowed book (ISBN 12345)."""
    mgr = LibraryManager()
    mgr.add_book("Book One", "Author A", "12345")
    mgr.borrow_book("12345")
    return mgr


# ---------- Add Book Tests ----------
@pytest.mark.parametrize(
    "title, author, isbn, expected_output, prepopulate",
    [
        # Success case
        ("Book One", "Author A", "12345",
         "Success: Added 'Book One' to the library.\n", False),
        # Short ISBN case
        ("Book Two", "Author B", "12",
         "[!] Error: ISBN '12' is too short.\n", False),
        # Duplicate ISBN case (prepopulate with same ISBN)
        ("Book Three", "Author C", "12345",
         "[!] Error: A book with ISBN 12345 already exists.\n", True),
    ]
)
def test_add_book(title, author, isbn, expected_output, prepopulate, empty_manager, capsys):
    manager = empty_manager
    if prepopulate:
        manager.add_book("Existing", "Someone", isbn)  # add first to cause duplicate
        # discard the output from the pre‑population step
        capsys.readouterr()
    manager.add_book(title, author, isbn)
    captured = capsys.readouterr().out
    assert captured == expected_output


# ---------- Borrow Book Tests ----------
@pytest.mark.parametrize(
    "setup_fixture, isbn, expected_output",
    [
        # Borrow success
        ("manager_with_one_book", "12345",
         "Success: You have borrowed 'Book One'.\n"),
        # Book not found
        ("empty_manager", "67890",
         "[!] Error: Book with ISBN 67890 not found.\n"),
        # Book unavailable (already borrowed)
        ("manager_with_borrowed_book", "12345",
         "[!] Unavailable: 'Book One' is currently borrowed by someone else.\n"),
    ]
)
def test_borrow_book(request, setup_fixture, isbn, expected_output, capsys):
    manager = request.getfixturevalue(setup_fixture)
    # clear any output produced during fixture creation
    capsys.readouterr()
    manager.borrow_book(isbn)
    captured = capsys.readouterr().out
    assert captured == expected_output


# ---------- Return Book Tests ----------
@pytest.mark.parametrize(
    "setup_fixture, isbn, expected_output",
    [
        # Return success (book was borrowed)
        ("manager_with_borrowed_book", "12345",
         "Success: 'Book One' has been returned.\n"),
        # Book not found
        ("empty_manager", "67890",
         "[!] Error: We do not own a book with ISBN 67890.\n"),
        # Return already here (book is available)
        ("manager_with_one_book", "12345",
         "[!] Strange: You are trying to return 'Book One', but it was already here.\n"),
    ]
)
def test_return_book(request, setup_fixture, isbn, expected_output, capsys):
    manager = request.getfixturevalue(setup_fixture)
    # clear any output produced during fixture creation
    capsys.readouterr()
    manager.return_book(isbn)
    captured = capsys.readouterr().out
    assert captured == expected_output


# ---------- Show Inventory Tests ----------
def test_show_inventory_empty(empty_manager, capsys):
    empty_manager.show_inventory()
    captured = capsys.readouterr().out
    expected = (
        "\n--- Current Library Inventory ---\n"
        "The library is empty.\n"
        "---------------------------------\n"
        "\n"
    )
    assert captured == expected


def test_show_inventory_non_empty(manager_with_one_book, capsys):
    manager_with_one_book.show_inventory()
    captured = capsys.readouterr().out
    expected = (
        "\n--- Current Library Inventory ---\n"
        "[Available] Book One by Author A (ISBN: 12345)\n"
        "---------------------------------\n"
        "\n"
    )
    assert captured == expected