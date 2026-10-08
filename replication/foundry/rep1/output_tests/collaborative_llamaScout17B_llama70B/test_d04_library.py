import pytest
from data.input_code.d04_library import *

@pytest.mark.parametrize('title, author, isbn, expected', [
    ('Test Book', 'Test Author', '123', None),
    ('Test Book', 'Test Author', '12', None),
    ('Test Book', 'Test Author', '123', None),
])
def test_add_book(title, author, isbn, expected, capsys):
    library = LibraryManager()
    library.add_book(title, author, isbn)
    captured = capsys.readouterr()
    if isbn == '12':
        assert '[!] Error: ISBN \'12\' is too short.' in captured.out
    elif isbn == '123' and title == 'Test Book' and author == 'Test Author':
        if expected is None:
            library.add_book(title, author, isbn)
            captured = capsys.readouterr()
            assert '[!] Error: A book with ISBN 123 already exists.' in captured.out

@pytest.mark.parametrize('isbn, expected', [
    ('123', None),
    ('1234', None),
    ('123', None),
])
def test_borrow_book(isbn, expected, capsys):
    library = LibraryManager()
    library.add_book('Test Book', 'Test Author', '123')
    library.borrow_book(isbn)
    captured = capsys.readouterr()
    if isbn == '1234':
        assert '[!] Error: Book with ISBN 1234 not found.' in captured.out
    elif isbn == '123' and expected is None:
        library.borrow_book(isbn)
        captured = capsys.readouterr()
        assert '[!] Unavailable: \'Test Book\' is currently borrowed by someone else.' in captured.out

@pytest.mark.parametrize('isbn, expected', [
    ('1234', None),
    ('123', None),
    ('123', None),
])
def test_return_book(isbn, expected, capsys):
    library = LibraryManager()
    library.add_book('Test Book', 'Test Author', '123')
    library.borrow_book('123')
    library.return_book(isbn)
    captured = capsys.readouterr()
    if isbn == '1234':
        assert '[!] Error: We do not own a book with ISBN 1234.' in captured.out
    elif isbn == '123' and expected is None:
        library.return_book(isbn)
        captured = capsys.readouterr()
        assert '[!] Strange: You are trying to return \'Test Book\', but it was already here.' in captured.out

def test_show_inventory(capsys):
    library = LibraryManager()
    library.show_inventory()
    captured = capsys.readouterr()
    assert 'The library is empty.' in captured.out
    library.add_book('Test Book', 'Test Author', '123')
    library.show_inventory()
    captured = capsys.readouterr()
    assert '[Available] Test Book by Test Author (ISBN: 123)' in captured.out

@pytest.mark.parametrize('title, author, isbn, expected', [
    ('Test', 'Author', '123', {'title': 'Test', 'author': 'Author', 'isbn': '123', 'is_available': True}),
])
def test_book_init(title, author, isbn, expected):
    book = Book(title, author, isbn)
    assert book.title == expected['title']
    assert book.author == expected['author']
    assert book.isbn == expected['isbn']
    assert book.is_available == expected['is_available']

@pytest.mark.parametrize('title, author, isbn, is_available, expected', [
    ('Test', 'Author', '123', True, '[Available] Test by Author (ISBN: 123)'),
    ('Test', 'Author', '123', False, '[Borrowed] Test by Author (ISBN: 123)'),
])
def test_book_str(title, author, isbn, is_available, expected):
    book = Book(title, author, isbn)
    book.is_available = is_available
    assert str(book) == expected