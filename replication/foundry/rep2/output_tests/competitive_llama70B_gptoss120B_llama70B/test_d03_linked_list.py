import pytest
from data.input_code.d03_linked_list import *

@pytest.fixture
def empty_list():
    return LinkedList()

@pytest.fixture
def populated_list():
    """Creates list with elements [-1, 0, 1, 2] in that order."""
    ll = LinkedList()
    ll.append(1)
    ll.append(2)
    ll.prepend(0)
    ll.prepend(-1)
    return ll

def test_init(empty_list):
    assert empty_list.head is None
    assert len(empty_list) == 0

def test_append():
    ll = LinkedList()
    ll.append(1)
    assert ll.to_list() == [1]
    assert len(ll) == 1
    ll.append(2)
    assert ll.to_list() == [1, 2]
    assert len(ll) == 2

def test_prepend():
    ll = LinkedList()
    ll.prepend(0)
    assert ll.to_list() == [0]
    assert len(ll) == 1
    ll.prepend(-1)
    assert ll.to_list() == [-1, 0]
    assert len(ll) == 2

@pytest.mark.parametrize(
    "data, expected, post_list",
    [
        (1, True, [-1, 0, 2]),   # delete existing
        (3, False, [-1, 0, 1, 2])  # delete non‑existing
    ]
)
def test_delete(populated_list, data, expected, post_list):
    result = populated_list.delete(data)
    assert result is expected
    assert populated_list.to_list() == post_list

@pytest.mark.parametrize(
    "data, expected",
    [
        (1, 2),   # find existing
        (3, -1)   # find non‑existing
    ]
)
def test_find(populated_list, data, expected):
    assert populated_list.find(data) == expected

def test_get_valid_index(populated_list):
    # index 0 should return the first element (-1)
    assert populated_list.get(0) == -1

@pytest.mark.parametrize(
    "index, exc",
    [
        (-1, IndexError),   # negative index
        (3, IndexError)     # out‑of‑range after deletion of one element
    ]
)
def test_get_errors(populated_list, index, exc):
    # Adjust list for the out‑of‑range case
    if index == 3:
        populated_list.delete(1)  # list becomes [-1, 0, 2] (size 3)
    with pytest.raises(exc):
        populated_list.get(index)

def test_to_list(populated_list):
    assert populated_list.to_list() == [-1, 0, 1, 2]

def test_len(populated_list):
    assert len(populated_list) == 4

import pytest

def test_prepend_empty(empty_list):
    empty_list.prepend(1)
    assert empty_list.to_list() == [1]
    assert len(empty_list) == 1

@pytest.mark.parametrize(
    "data, expected, post_list",
    [
        (-1, True, [0, 1, 2]),   # delete head
        (2, True, [-1, 0, 1]),   # delete tail
    ]
)
def test_delete_head_and_tail(populated_list, data, expected, post_list):
    result = populated_list.delete(data)
    assert result is expected
    assert populated_list.to_list() == post_list

def test_get_last_index(populated_list):
    # index 3 corresponds to the last element (value 2) in the initial list
    assert populated_list.get(3) == 2

@pytest.mark.parametrize(
    "data, expected",
    [
        (-1, 0),  # find at head
        (2, 3),   # find at tail
    ]
)
def test_find_head_and_tail(populated_list, data, expected):
    assert populated_list.find(data) == expected

import pytest

def test_get_middle_index(populated_list):
    # Index 1 corresponds to the second element (0) in the initial list [-1, 0, 1, 2]
    assert populated_list.get(1) == 0

@pytest.mark.parametrize(
    "data, expected, post_list",
    [
        (5, False, [-1, 0, 1, 2]),   # delete non‑existing element
        (1, True, [-1, 0, 2]),       # delete middle element
    ]
)
def test_delete_additional_cases(populated_list, data, expected, post_list):
    result = populated_list.delete(data)
    assert result is expected
    assert populated_list.to_list() == post_list

def test_find_middle(populated_list):
    # Element 1 is at index 2 in the initial list [-1, 0, 1, 2]
    assert populated_list.find(1) == 2

def test_append_multiple_elements():
    ll = LinkedList()
    ll.append(1)
    ll.append(2)
    for val in [3, 4, 5]:
        ll.append(val)
    assert ll.to_list() == [1, 2, 3, 4, 5]
    assert len(ll) == 5

def test_prepend_multiple_elements():
    ll = LinkedList()
    ll.append(1)
    ll.append(2)
    for val in [6, 7, 8]:
        ll.prepend(val)
    assert ll.to_list() == [8, 7, 6, 1, 2]
    assert len(ll) == 5

def test_get_from_empty_raises(empty_list):
    with pytest.raises(IndexError):
        empty_list.get(0)


@pytest.mark.parametrize("index", [100])
def test_get_large_index_raises(empty_list, index):
    with pytest.raises(IndexError):
        empty_list.get(index)


def test_delete_from_empty_returns_false(empty_list):
    result = empty_list.delete(1)
    assert result is False


def test_find_in_empty_returns_minus_one(empty_list):
    assert empty_list.find(1) == -1


def test_delete_after_prepend():
    ll = LinkedList()
    ll.prepend(1)
    ll.append(2)
    result = ll.delete(1)
    assert result is True
    assert ll.to_list() == [2]


def test_find_after_append():
    ll = LinkedList()
    ll.append(1)
    assert ll.find(1) == 0


def test_get_after_deleting_only_element_raises():
    ll = LinkedList()
    ll.append(1)
    ll.delete(1)
    with pytest.raises(IndexError):
        ll.get(0)