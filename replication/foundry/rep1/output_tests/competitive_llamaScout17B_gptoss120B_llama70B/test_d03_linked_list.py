import pytest
from data.input_code.d03_linked_list import *

def build_linked_list(values):
    """Utility to create a LinkedList from a Python list."""
    ll = LinkedList()
    for v in values:
        ll.append(v)
    return ll

@pytest.mark.parametrize(
    "initial, data, expected_list, expected_size",
    [
        ([], 5, [5], 1),                     # append to empty
        ([1], 2, [1, 2], 2),                 # append to non‑empty
    ],
)
def test_append(initial, data, expected_list, expected_size):
    ll = build_linked_list(initial)
    ll.append(data)
    assert ll.to_list() == expected_list
    assert len(ll) == expected_size

@pytest.mark.parametrize(
    "initial, data, expected_list, expected_size",
    [
        ([], 5, [5], 1),                     # prepend to empty
        ([1], 2, [2, 1], 2),                 # prepend to non‑empty
    ],
)
def test_prepend(initial, data, expected_list, expected_size):
    ll = build_linked_list(initial)
    ll.prepend(data)
    assert ll.to_list() == expected_list
    assert len(ll) == expected_size

@pytest.mark.parametrize(
    "initial, delete_val, expected_result, expected_list, expected_size",
    [
        ([], 5, False, [], 0),                               # delete from empty
        ([1], 1, True, [], 0),                               # delete head (single element)
        ([1, 2], 1, True, [2], 1),                           # delete head (multiple)
        ([1, 2], 2, True, [1], 1),                           # delete non‑head
        ([1], 2, False, [1], 1),                             # delete missing
    ],
)
def test_delete(initial, delete_val, expected_result, expected_list, expected_size):
    ll = build_linked_list(initial)
    result = ll.delete(delete_val)
    assert result is expected_result
    assert ll.to_list() == expected_list
    assert len(ll) == expected_size

@pytest.mark.parametrize(
    "initial, find_val, expected_index",
    [
        ([1, 2, 3], 2, 1),          # existing value
        ([1, 2, 3], 4, -1),         # non‑existent value
        ([], 1, -1),                # empty list
    ],
)
def test_find(initial, find_val, expected_index):
    ll = build_linked_list(initial)
    assert ll.find(find_val) == expected_index

@pytest.mark.parametrize(
    "initial, index, expected",
    [
        ([1, 2, 3], 0, 1),          # first element
        ([1, 2, 3], 2, 3),          # last element
    ],
)
def test_get_valid(initial, index, expected):
    ll = build_linked_list(initial)
    assert ll.get(index) == expected

@pytest.mark.parametrize(
    "initial, index, exc",
    [
        ([], 0, IndexError),               # empty list, any index invalid
        ([1], -1, IndexError),             # negative index
        ([1], 1, IndexError),              # index equal to size
    ],
)
def test_get_invalid(initial, index, exc):
    ll = build_linked_list(initial)
    with pytest.raises(exc):
        ll.get(index)

@pytest.mark.parametrize(
    "initial, expected",
    [
        ([], []),                           # empty list conversion
        ([1, 2, 3], [1, 2, 3]),             # non‑empty list conversion
    ],
)
def test_to_list(initial, expected):
    ll = build_linked_list(initial)
    assert ll.to_list() == expected

@pytest.mark.parametrize(
    "initial, expected_len",
    [
        ([], 0),                            # empty list length
        ([1, 2, 3], 3),                     # non‑empty list length
    ],
)
def test_len(initial, expected_len):
    ll = build_linked_list(initial)
    assert len(ll) == expected_len

def test_init():
    ll = LinkedList()
    assert ll.head is None
    assert len(ll) == 0

import pytest

@pytest.mark.parametrize(
    "initial, index, expected",
    [
        ([1, 2, 3], 1, 2),  # middle element
    ],
)
def test_get_middle(initial, index, expected):
    ll = build_linked_list(initial)
    assert ll.get(index) == expected


@pytest.mark.parametrize(
    "initial, delete_val, expected_result, expected_list, expected_size",
    [
        ([1, 2, 3, 2, 4], 2, True, [1, 3, 2, 4], 4),  # delete first occurrence among duplicates
    ],
)
def test_delete_multiple(initial, delete_val, expected_result, expected_list, expected_size):
    ll = build_linked_list(initial)
    result = ll.delete(delete_val)
    assert result is expected_result
    assert ll.to_list() == expected_list
    assert len(ll) == expected_size


@pytest.mark.parametrize(
    "initial, find_val, expected_index",
    [
        ([1], 1, 0),  # find in single-element list
    ],
)
def test_find_single_element(initial, find_val, expected_index):
    ll = build_linked_list(initial)
    assert ll.find(find_val) == expected_index

import pytest

@pytest.mark.parametrize(
    "initial, index, expected",
    [
        ([1], 0, 1),  # single-element list, get index 0
    ],
)
def test_get_boundary(initial, index, expected):
    ll = build_linked_list(initial)
    assert ll.get(index) == expected


@pytest.mark.parametrize(
    "initial, delete_val, expected_result",
    [
        ([1, 2, 3], 1, True),  # delete head when multiple elements exist
    ],
)
def test_delete_head_multiple(initial, delete_val, expected_result):
    ll = build_linked_list(initial)
    result = ll.delete(delete_val)
    assert result is expected_result
    # optional sanity check: ensure the new head is the former second element
    assert ll.head.data == 2


@pytest.mark.parametrize(
    "initial, data, expected_list, expected_size",
    [
        ([1, 2], 3, [3, 1, 2], 3),  # prepend to a list with existing elements
    ],
)
def test_prepend_multiple(initial, data, expected_list, expected_size):
    ll = build_linked_list(initial)
    ll.prepend(data)
    assert ll.to_list() == expected_list
    assert len(ll) == expected_size


@pytest.mark.parametrize(
    "initial, data, expected_list, expected_size",
    [
        ([1, 2], 3, [1, 2, 3], 3),  # append to a list with existing elements
    ],
)
def test_append_multiple(initial, data, expected_list, expected_size):
    ll = build_linked_list(initial)
    ll.append(data)
    assert ll.to_list() == expected_list
    assert len(ll) == expected_size


def test_len_after_multiple_ops():
    ll = build_linked_list([1, 2, 3])
    # perform additional operations to simulate "multiple ops"
    ll.append(4)
    ll.delete(2)
    ll.prepend(0)
    # final expected length: original 3 + 1 append - 1 delete + 1 prepend = 4
    assert len(ll) == 4

import pytest

@pytest.mark.parametrize(
    "initial, index, expected",
    [
        ([1, 2, 3], 2, 3),  # edge index (size - 1)
    ],
)
def test_get_edge(initial, index, expected):
    ll = build_linked_list(initial)
    assert ll.get(index) == expected


@pytest.mark.parametrize(
    "initial, delete_val, expected_result, expected_list, expected_size",
    [
        ([1, 2, 3], 3, True, [1, 2], 2),  # delete tail element
    ],
)
def test_delete_tail(initial, delete_val, expected_result, expected_list, expected_size):
    ll = build_linked_list(initial)
    result = ll.delete(delete_val)
    assert result is expected_result
    assert ll.to_list() == expected_list
    assert len(ll) == expected_size


def test_prepend_empty():
    ll = LinkedList()
    ll.prepend(1)
    assert ll.to_list() == [1]
    assert len(ll) == 1


def test_append_empty():
    ll = LinkedList()
    ll.append(1)
    assert ll.to_list() == [1]
    assert len(ll) == 1


def test_find_missing_in_empty():
    ll = LinkedList()
    result = ll.find(1)
    assert result == -1


def test_len_after_clear():
    ll = build_linked_list([1, 2, 3])
    # delete all elements one by one
    assert ll.delete(1) is True
    assert ll.delete(2) is True
    assert ll.delete(3) is True
    assert len(ll) == 0