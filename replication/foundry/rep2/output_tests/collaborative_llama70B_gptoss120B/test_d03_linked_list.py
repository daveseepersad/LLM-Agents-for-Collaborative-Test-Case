import pytest
from data.input_code.d03_linked_list import *

@pytest.fixture
def empty_list():
    """Return a freshly initialized empty LinkedList."""
    return LinkedList()

@pytest.fixture
def populated_list():
    """Return a LinkedList populated with [0, 1, 2, 3] using append."""
    ll = LinkedList()
    for i in range(4):
        ll.append(i)
    return ll

def test_init(empty_list):
    assert empty_list.head is None
    assert len(empty_list) == 0

def test_append_and_len(populated_list):
    assert len(populated_list) == 4
    assert populated_list.to_list() == [0, 1, 2, 3]

def test_prepend():
    ll = LinkedList()
    ll.prepend(5)          # list: [5]
    ll.prepend(6)          # list: [6, 5]
    assert ll.to_list() == [6, 5]
    assert len(ll) == 2

@pytest.mark.parametrize(
    "data, expected, final_len",
    [
        (2, True, 3),   # delete existing element
        (99, False, 4), # delete non‑existing element
    ],
)
def test_delete(populated_list, data, expected, final_len):
    result = populated_list.delete(data)
    assert result is expected
    assert len(populated_list) == final_len

@pytest.mark.parametrize(
    "data, expected_index",
    [
        (2, 2),   # existing element
        (99, -1), # non‑existing element
    ],
)
def test_find(populated_list, data, expected_index):
    assert populated_list.find(data) == expected_index

def test_get_success(populated_list):
    assert populated_list.get(1) == 1

@pytest.mark.parametrize(
    "index, exc",
    [
        (-1, IndexError),
        (10, IndexError),
    ],
)
def test_get_errors(populated_list, index, exc):
    with pytest.raises(exc):
        populated_list.get(index)

def test_to_list(populated_list):
    assert populated_list.to_list() == [0, 1, 2, 3]

def test_len(populated_list):
    assert len(populated_list) == 4

import pytest
from data.input_code.d03_linked_list import *

def test_prepend_empty(empty_list):
    empty_list.prepend(5)
    assert empty_list.to_list() == [5]
    assert len(empty_list) == 1

@pytest.mark.parametrize(
    "data, expected, final_len, final_list",
    [
        (0, True, 3, [1, 2, 3]),  # delete head
        (3, True, 3, [0, 1, 2]),  # delete tail
    ],
)
def test_delete_head_and_tail(populated_list, data, expected, final_len, final_list):
    result = populated_list.delete(data)
    assert result is expected
    assert len(populated_list) == final_len
    assert populated_list.to_list() == final_list

@pytest.mark.parametrize(
    "data, expected_index",
    [
        (0, 0),  # find head
        (3, 3),  # find tail
    ],
)
def test_find_head_and_tail(populated_list, data, expected_index):
    assert populated_list.find(data) == expected_index

@pytest.mark.parametrize(
    "index, expected",
    [
        (0, 0),  # get head
        (3, 3),  # get tail
    ],
)
def test_get_head_and_tail(populated_list, index, expected):
    assert populated_list.get(index) == expected

import pytest
from data.input_code.d03_linked_list import *

def test_delete_empty(empty_list):
    result = empty_list.delete(5)
    assert result is False
    assert len(empty_list) == 0

def test_prepend_multiple(empty_list):
    for value in [1, 2, 3]:
        empty_list.prepend(value)
    assert empty_list.to_list() == [3, 2, 1]
    assert len(empty_list) == 3

def test_get_middle(populated_list):
    assert populated_list.get(1) == 1

def test_find_after_delete(populated_list):
    # delete element 2
    deleted = populated_list.delete(2)
    assert deleted is True
    # now find 2 should return -1
    assert populated_list.find(2) == -1

def test_to_list_after_delete(populated_list):
    # delete element 1
    deleted = populated_list.delete(1)
    assert deleted is True
    assert populated_list.to_list() == [0, 2, 3]

def test_len_after_prepend(populated_list):
    populated_list.prepend(99)
    assert len(populated_list) == 5