import pytest
from data.input_code.d03_linked_list import *

def _build_linked_list(values):
    """Utility to create a LinkedList with the given iterable of values."""
    ll = LinkedList()
    for v in values:
        ll.append(v)
    return ll

def test_init():
    ll = LinkedList()
    assert ll.head is None
    assert ll._size == 0

@pytest.mark.parametrize(
    "initial,append_val,expected_list,expected_size",
    [
        ([], 5, [5], 1),                     # append to empty list
        ([1], 2, [1, 2], 2),                 # append to non‑empty list
    ],
)
def test_append(initial, append_val, expected_list, expected_size):
    ll = _build_linked_list(initial)
    ll.append(append_val)
    assert ll.to_list() == expected_list
    assert ll._size == expected_size

@pytest.mark.parametrize(
    "initial,prepend_val,expected_list,expected_size",
    [
        ([], 5, [5], 1),                     # prepend to empty list
        ([1], 2, [2, 1], 2),                 # prepend to non‑empty list
    ],
)
def test_prepend(initial, prepend_val, expected_list, expected_size):
    ll = _build_linked_list(initial)
    ll.prepend(prepend_val)
    assert ll.to_list() == expected_list
    assert ll._size == expected_size

@pytest.mark.parametrize(
    "initial,delete_val,expected_result,expected_list,expected_size",
    [
        ([], 5, False, [], 0),                               # delete from empty list
        ([1], 1, True, [], 0),                               # delete head node
        ([1, 2], 2, True, [1], 1),                           # delete non‑head node
        ([1], 2, False, [1], 1),                             # delete missing node
    ],
)
def test_delete(initial, delete_val, expected_result, expected_list, expected_size):
    ll = _build_linked_list(initial)
    result = ll.delete(delete_val)
    assert result is expected_result
    assert ll.to_list() == expected_list
    assert ll._size == expected_size

@pytest.mark.parametrize(
    "initial,find_val,expected_index",
    [
        ([1, 2], 2, 1),          # find present node
        ([1], 2, -1),            # find missing node
    ],
)
def test_find(initial, find_val, expected_index):
    ll = _build_linked_list(initial)
    assert ll.find(find_val) == expected_index

@pytest.mark.parametrize(
    "initial,index,expected",
    [
        ([1, 2], 1, 2),          # get valid index
    ],
)
def test_get_valid(initial, index, expected):
    ll = _build_linked_list(initial)
    assert ll.get(index) == expected

@pytest.mark.parametrize(
    "initial,index",
    [
        ([1], -1),               # invalid low index
        ([1], 1),                # invalid high index (out of range)
    ],
)
def test_get_invalid(initial, index):
    ll = _build_linked_list(initial)
    with pytest.raises(IndexError):
        ll.get(index)

@pytest.mark.parametrize(
    "initial,expected",
    [
        ([], []),                # convert empty list
        ([1, 2], [1, 2]),        # convert non‑empty list
    ],
)
def test_to_list(initial, expected):
    ll = _build_linked_list(initial)
    assert ll.to_list() == expected

@pytest.mark.parametrize(
    "initial,expected_len",
    [
        ([], 0),                 # length of empty list
        ([1], 1),                # length of non‑empty list
    ],
)
def test_len(initial, expected_len):
    ll = _build_linked_list(initial)
    assert len(ll) == expected_len