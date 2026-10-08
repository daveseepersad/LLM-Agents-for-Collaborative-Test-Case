import pytest
from data.input_code.d04_library import LibraryManager

def test_add_book_success_and_state(capsys):
    lm = LibraryManager()
    lm.add_book("1984", "George Orwell", "123")
    captured = capsys.readouterr()
    assert "Success: Added '1984' to the library." in captured.out
    assert "123" in lm.inventory
    book = lm.inventory["123"]
    assert book.title == "1984"
    assert book.author == "George Orwell"
    assert book.isbn == "123"
    assert book.is_available is True

def test_add_book_short_isbn(capsys):
    lm = LibraryManager()
    lm.add_book("Some Book", "Some Author", "12")
    captured = capsys.readouterr()
    assert "[!] Error: ISBN '12' is too short." in captured.out
    assert "12" not in lm.inventory

def test_add_book_duplicate(capsys):
    lm = LibraryManager()
    lm.add_book("BookA", "AuthorA", "555")
    capsys.readouterr()
    lm.add_book("BookB", "AuthorB", "555")
    captured = capsys.readouterr()
    assert "[!] Error: A book with ISBN 555 already exists." in captured.out
    assert lm.inventory["555"].title == "BookA"

def test_borrow_book_not_exist(capsys):
    lm = LibraryManager()
    lm.borrow_book("000")
    captured = capsys.readouterr()
    assert "[!] Error: Book with ISBN 000 not found." in captured.out

def test_borrow_book_success(capsys):
    lm = LibraryManager()
    lm.add_book("Dune", "Frank Herbert", "321")
    cap = capsys.readouterr()
    lm.borrow_book("321")
    captured = capsys.readouterr()
    assert "Success: You have borrowed 'Dune'." in captured.out
    assert lm.inventory["321"].is_available is False


def test_return_book_not_exist(capsys):
    lm = LibraryManager()
    lm.return_book("999")
    captured = capsys.readouterr()
    assert "[!] Error: We do not own a book with ISBN 999." in captured.out

def test_return_book_strange_when_already_available(capsys):
    lm = LibraryManager()
    lm.add_book("Foundation", "Isaac Asimov", "111")
    cap = capsys.readouterr()
    lm.return_book("111")
    captured = capsys.readouterr()
    assert "[!] Strange: You are trying to return 'Foundation', but it was already here." in captured.out


def test_show_inventory_empty(capsys):
    lm = LibraryManager()
    lm.show_inventory()
    captured = capsys.readouterr()
    assert "The library is empty." in captured.out

def test_show_inventory_non_empty(capsys):
    lm = LibraryManager()
    lm.add_book("Dune", "Frank Herbert", "999")
    cap = capsys.readouterr()
    lm.show_inventory()
    captured = capsys.readouterr()
    assert "[Available] Dune by Frank Herbert (ISBN: 999)" in captured.out

def test_add_book_none_isbn_raises_typeerror():
    lm = LibraryManager()
    with pytest.raises(TypeError):
        lm.add_book("X", "Y", None)