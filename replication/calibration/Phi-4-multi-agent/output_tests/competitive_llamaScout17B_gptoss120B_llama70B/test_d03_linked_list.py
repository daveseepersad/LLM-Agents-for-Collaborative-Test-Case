import pytest
from data.input_code.d03_linked_list import *

@pytest.fixture
def empty_list():
    return LinkedList()

@pytest.fixture
def populated_list():
    """Creates a list with elements [15, 5, 20] in that order."""
    ll = LinkedList()
    ll.append(20)   # list: [20]
    ll.prepend(5)   # list: [5, 20]
    ll.prepend(15)  # list: [15, 5, 20]
    return ll

def test_append_to_empty(empty_list):
    empty_list.append(10)
    assert empty_list.to_list() == [10]
    assert len(empty_list) == 1

def test_append_to_nonempty(populated_list):
    populated_list.append(30)
    assert populated_list.to_list() == [15, 5, 20, 30]
    assert len(populated_list) == 4

def test_prepend_to_empty(empty_list):
    empty_list.prepend(5)
    assert empty_list.to_list() == [5]
    assert len(empty_list) == 1

def test_prepend_to_nonempty(populated_list):
    populated_list.prepend(99)
    assert populated_list.to_list() == [99, 15, 5, 20]
    assert len(populated_list) == 4

def test_delete_from_empty(empty_list):
    assert empty_list.delete(10) is False
    assert len(empty_list) == 0

@pytest.mark.parametrize(
    "value,expected_list,expected_len",
    [
        (15, [5, 20], 2),   # delete head
        (5,  [15, 20], 2),  # delete middle
        (20, [15, 5], 2),   # delete tail
    ],
)
def test_delete_existing(value, expected_list, expected_len, populated_list):
    result = populated_list.delete(value)
    assert result is True
    assert populated_list.to_list() == expected_list
    assert len(populated_list) == expected_len

def test_delete_nonexistent(populated_list):
    assert populated_list.delete(99) is False
    # list should remain unchanged
    assert populated_list.to_list() == [15, 5, 20]
    assert len(populated_list) == 3

@pytest.mark.parametrize(
    "value,expected_index",
    [
        (15, 0),
        (5, 1),
        (20, 2),
    ],
)
def test_find_existing(value, expected_index, populated_list):
    assert populated_list.find(value) == expected_index

def test_find_nonexistent(populated_list):
    assert populated_list.find(99) == -1

@pytest.mark.parametrize(
    "index,expected",
    [
        (0, 15),   # head
        (2, 20),   # tail
    ],
)
def test_get_valid(index, expected, populated_list):
    assert populated_list.get(index) == expected

@pytest.mark.parametrize(
    "index",
    [3, -1],
)
def test_get_out_of_range(index, populated_list):
    with pytest.raises(IndexError):
        populated_list.get(index)

def test_to_list(populated_list):
    assert populated_list.to_list() == [15, 5, 20]

def test_len_empty(empty_list):
    assert len(empty_list) == 0

def test_len_nonempty(populated_list):
    assert len(populated_list) == 3