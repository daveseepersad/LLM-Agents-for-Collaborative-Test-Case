import pytest
from data.input_code.d04_library import Book, LibraryManager

class TestLibraryManager:
    def test_add_book_success_and_duplicate_and_short_isbn(self, capsys):
        lib = LibraryManager()
        # Success add
        lib.add_book("Title1", "Author1", "123")
        captured = capsys.readouterr()
        assert "Success" in captured.out
        assert "123" in lib.inventory
        # Duplicate add
        lib.add_book("Title2", "Author2", "123")
        captured = capsys.readouterr()
        assert "already exists" in captured.out
        # Short ISBN
        lib.add_book("Title3", "Author3", "12")
        captured = capsys.readouterr()
        assert "too short" in captured.out

    def test_borrow_book_success_and_not_found_and_unavailable(self, capsys):
        lib = LibraryManager()
        lib.add_book("Title1", "Author1", "123")
        capsys.readouterr()
        # Borrow success
        lib.borrow_book("123")
        captured = capsys.readouterr()
        assert "Success" in captured.out
        assert lib.inventory["123"].is_available is False
        # Borrow unavailable
        lib.borrow_book("123")
        captured = capsys.readouterr()
        assert "Unavailable" in captured.out
        # Borrow not found
        lib.borrow_book("999")
        captured = capsys.readouterr()
        assert "not found" in captured.out

    def test_return_book_success_and_not_found_and_already_available(self, capsys):
        lib = LibraryManager()
        lib.add_book("Title1", "Author1", "123")
        capsys.readouterr()
        # Return not found
        lib.return_book("999")
        captured = capsys.readouterr()
        assert "do not own" in captured.out
        # Return when already available
        lib.return_book("123")
        captured = capsys.readouterr()
        assert "Strange" in captured.out
        # Borrow then return success
        lib.borrow_book("123")
        capsys.readouterr()
        lib.return_book("123")
        captured = capsys.readouterr()
        assert "Success" in captured.out
        assert lib.inventory["123"].is_available is True

    def test_show_inventory_empty_and_nonempty(self, capsys):
        lib = LibraryManager()
        lib.show_inventory()
        captured = capsys.readouterr()
        assert "empty" in captured.out
        lib.add_book("Title1", "Author1", "123")
        capsys.readouterr()
        lib.show_inventory()
        captured = capsys.readouterr()
        assert "Title1" in captured.out
        assert "Available" in captured.out

class TestBook:
    def test_book_str_available_and_borrowed(self):
        book = Book("Title", "Author", "123")
        s = str(book)
        assert "Available" in s
        book.is_available = False
        s = str(book)
        assert "Borrowed" in s