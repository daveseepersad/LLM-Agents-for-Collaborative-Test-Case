import pytest
from data.input_code.d04_library import LibraryManager, Book


def test_add_book_success(capsys):
    library = LibraryManager()
    library.add_book("Effective Python", "Brett Slatkin", "12345")
    captured = capsys.readouterr()
    assert captured.out.strip().split('\n') == ["Success: Added 'Effective Python' to the library."]

@pytest.mark.parametrize('isbn, expected', [
    ("99999", ["[!] Error: Book with ISBN 99999 not found."]),
    ("12345", ["[!] Unavailable: 'Effective Python' is currently borrowed by someone else."]),
])
def test_borrow_book_error(capsys, isbn, expected):
    library = LibraryManager()
    library.add_book("Effective Python", "Brett Slatkin", "12345")
    library.borrow_book("12345")
    library.borrow_book(isbn)
    captured = capsys.readouterr()
    assert captured.out.strip().split('\n')[-1] == expected[0]

def test_borrow_book_success(capsys):
    library = LibraryManager()
    library.add_book("Effective Python", "Brett Slatkin", "12345")
    library.borrow_book("12345")
    captured = capsys.readouterr()
    assert captured.out.strip().split('\n')[-1] == "Success: You have borrowed 'Effective Python'."

@pytest.mark.parametrize('isbn, expected', [
    ("88888", ["[!] Error: We do not own a book with ISBN 88888."]),
    ("12345", ["[!] Strange: You are trying to return 'Effective Python', but it was already here."]),
])
def test_return_book_error(capsys, isbn, expected):
    library = LibraryManager()
    library.add_book("Effective Python", "Brett Slatkin", "12345")
    library.return_book(isbn)
    captured = capsys.readouterr()
    assert captured.out.strip().split('\n')[-1] == expected[0]

def test_return_book_success(capsys):
    library = LibraryManager()
    library.add_book("Effective Python", "Brett Slatkin", "12345")
    library.borrow_book("12345")
    library.return_book("12345")
    captured = capsys.readouterr()
    assert captured.out.strip().split('\n')[-1] == "Success: 'Effective Python' has been returned."

def test_show_inventory_empty(capsys):
    library = LibraryManager()
    library.show_inventory()
    captured = capsys.readouterr()
    expected = [
        "\n--- Current Library Inventory ---",
        "The library is empty.",
        "---------------------------------\n"
    ]
    assert captured.out.strip().split('\n') == [line.strip() for line in expected]

def test_show_inventory_non_empty(capsys):
    library = LibraryManager()
    library.add_book("Effective Python", "Brett Slatkin", "12345")
    captured = capsys.readouterr() # Clear the output buffer
    library.show_inventory()
    captured = capsys.readouterr()
    expected = [
        "\n--- Current Library Inventory ---",
        "[Available] Effective Python by Brett Slatkin (ISBN: 12345)",
        "---------------------------------\n"
    ]
    assert captured.out.strip().split('\n') == [line.strip() for line in expected]

def test_add_book_error_duplicate(capsys):
    library = LibraryManager()
    library.add_book("Effective Python", "Brett Slatkin", "12345")
    captured = capsys.readouterr() # Clear the output buffer
    library.add_book("Duplicate Book", "Author B", "12345")
    captured = capsys.readouterr()
    expected = [
        "[!] Error: A book with ISBN 12345 already exists."
    ]
    assert captured.out.strip().split('\n') == expected

def test_show_inventory_non_empty_with_add_message(capsys):
    library = LibraryManager()
    library.add_book("Effective Python", "Brett Slatkin", "12345")
    captured = capsys.readouterr() # Clear the output buffer
    library.show_inventory()
    captured = capsys.readouterr()
    expected = [
        "\n--- Current Library Inventory ---",
        "[Available] Effective Python by Brett Slatkin (ISBN: 12345)",
        "---------------------------------\n"
    ]
    assert captured.out.strip().split('\n') == [line.strip() for line in expected]