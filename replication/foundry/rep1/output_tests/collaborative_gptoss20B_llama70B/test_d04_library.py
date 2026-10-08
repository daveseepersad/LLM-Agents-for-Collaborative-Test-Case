import pytest
from data.input_code.d04_library import Book, LibraryManager

@pytest.mark.parametrize('title, author, isbn, expected', [
    ("1984", "George Orwell", "12345", "[Available] 1984 by George Orwell (ISBN: 12345)")
])
def test_book_str(title, author, isbn, expected):
    book = Book(title, author, isbn)
    assert str(book) == expected

@pytest.mark.parametrize('title, author, isbn, expected', [
    ("X", "A", [], False),
    ("X", "A", "", False),
    ("X", "A", "ab", False)
])
def test_library_manager_add_book_invalid_isbn(title, author, isbn, expected):
    library = LibraryManager()
    library.add_book(title, author, isbn)
    assert (str(isbn) in library.inventory) == expected

def test_library_manager_add_book_valid_isbn():
    library = LibraryManager()
    library.add_book("The Hobbit", "J.R.R. Tolkien", "123")
    assert "123" in library.inventory


def test_library_manager_add_book_invalid_isbn_type():
    library = LibraryManager()
    with pytest.raises(TypeError):
        library.add_book("X", "A", [1, 2, 3])

def test_library_manager_add_book_empty_isbn():
    library = LibraryManager()
    library.add_book("X", "A", "")
    assert "" not in library.inventory

def test_library_manager_add_book_short_isbn():
    library = LibraryManager()
    library.add_book("X", "A", "ab")
    assert "ab" not in library.inventory

def test_library_manager_borrow_book_not_found():
    library = LibraryManager()
    library.borrow_book("9999")
    # No assertion, just checking that it doesn't throw an error

def test_library_manager_return_book_not_found():
    library = LibraryManager()
    library.return_book("9999")
    # No assertion, just checking that it doesn't throw an error

def test_library_manager_show_inventory_empty():
    library = LibraryManager()
    library.show_inventory()
    # No assertion, just checking that it doesn't throw an error

def test_library_manager_add_book_long_isbn():
    library = LibraryManager()
    library.add_book("Dune", "Frank Herbert", "abcdefgh")
    assert "abcdefgh" in library.inventory