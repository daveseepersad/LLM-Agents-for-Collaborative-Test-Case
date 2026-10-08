import pytest
from data.input_code.d03_linked_list import *

def build_linked_list(values):
    """Utility to create a LinkedList from an iterable of values."""
    ll = LinkedList()
    for v in values:
        ll.append(v)
    return ll

def list_structure(head):
    """Return a list of node data following the linked list starting at head."""
    result = []
    current = head
    while current:
        result.append(current.data)
        current = current.next
    return result

def test_init():
    ll = LinkedList()
    assert ll.head is None
    assert ll._size == 0

@pytest.mark.parametrize(
    "initial, data, expected_vals, expected_size",
    [
        ([], 5, [5], 1),                     # T2_APPEND_EMPTY
        ([1], 2, [1, 2], 2),                 # T3_APPEND_NONEMPTY
    ],
)
def test_append(initial, data, expected_vals, expected_size):
    ll = build_linked_list(initial)
    ll.append(data)
    assert list_structure(ll.head) == expected_vals
    assert ll._size == expected_size

@pytest.mark.parametrize(
    "initial, data, expected_vals, expected_size",
    [
        ([], 5, [5], 1),                     # T4_PREPEND_EMPTY
        ([1], 2, [2, 1], 2),                 # T5_PREPEND_NONEMPTY
    ],
)
def test_prepend(initial, data, expected_vals, expected_size):
    ll = build_linked_list(initial)
    ll.prepend(data)
    assert list_structure(ll.head) == expected_vals
    assert ll._size == expected_size

@pytest.mark.parametrize(
    "initial, data, expected_result, expected_vals, expected_size",
    [
        ([], 5, False, [], 0),               # T6_DELETE_EMPTY
        ([1], 1, True, [], 0),               # T7_DELETE_HEAD
        ([1, 2, 3], 2, True, [1, 3], 2),     # T8_DELETE_MIDDLE
        ([1], 5, False, [1], 1),             # T9_DELETE_NOTFOUND
    ],
)
def test_delete(initial, data, expected_result, expected_vals, expected_size):
    ll = build_linked_list(initial)
    result = ll.delete(data)
    assert result is expected_result
    assert list_structure(ll.head) == expected_vals
    assert ll._size == expected_size

@pytest.mark.parametrize(
    "initial, data, expected_index",
    [
        ([1, 2, 3], 2, 1),   # T10_FIND_FOUND
        ([1], 5, -1),       # T11_FIND_NOTFOUND
    ],
)
def test_find(initial, data, expected_index):
    ll = build_linked_list(initial)
    assert ll.find(data) == expected_index

@pytest.mark.parametrize(
    "initial, index, expected",
    [
        ([1, 2], 1, 2),                     # T12_GET_VALID
    ],
)
def test_get_valid(initial, index, expected):
    ll = build_linked_list(initial)
    assert ll.get(index) == expected

def test_get_invalid_low():
    ll = build_linked_list([1])            # T13_GET_INVALID_LOW
    with pytest.raises(IndexError):
        ll.get(-1)

def test_get_invalid_high():
    ll = build_linked_list([1])            # T14_GET_INVALID_HIGH
    with pytest.raises(IndexError):
        ll.get(1)

@pytest.mark.parametrize(
    "initial, expected_list",
    [
        ([], []),                           # T15_TOLIST_EMPTY
        ([1, 2], [1, 2]),                   # T16_TOLIST_NONEMPTY
    ],
)
def test_to_list(initial, expected_list):
    ll = build_linked_list(initial)
    assert ll.to_list() == expected_list

@pytest.mark.parametrize(
    "initial, expected_len",
    [
        ([], 0),                            # T17_LEN_EMPTY
        ([1], 1),                           # T18_LEN_NONEMPTY
    ],
)
def test_len(initial, expected_len):
    ll = build_linked_list(initial)
    assert len(ll) == expected_len

import pytest

@pytest.mark.parametrize(
    "initial, data, expected_result, expected_vals, expected_size",
    [
        ([1, 2, 3], 3, True, [1, 2], 2),  # T_MISSING_DELETE_LAST
    ],
)
def test_delete_last(initial, data, expected_result, expected_vals, expected_size):
    ll = build_linked_list(initial)
    result = ll.delete(data)
    assert result is expected_result
    assert list_structure(ll.head) == expected_vals
    assert ll._size == expected_size


@pytest.mark.parametrize(
    "initial, index, expected",
    [
        ([1, 2, 3], 0, 1),  # T_MISSING_GET_EDGE
    ],
)
def test_get_edge(initial, index, expected):
    ll = build_linked_list(initial)
    assert ll.get(index) == expected


@pytest.mark.parametrize(
    "initial, data, expected_index",
    [
        ([1, 2, 3], 1, 0),  # T_MISSING_FIND_EDGE
    ],
)
def test_find_edge(initial, data, expected_index):
    ll = build_linked_list(initial)
    assert ll.find(data) == expected_index


@pytest.mark.parametrize(
    "initial, expected_len",
    [
        ([1, 2, 3], 3),  # T_MISSING_LEN_MULTIELEM
    ],
)
def test_len_multi(initial, expected_len):
    ll = build_linked_list(initial)
    assert len(ll) == expected_len