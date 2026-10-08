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
    "pre_vals, append_val, expected_list, expected_size",
    [
        ([], 5, [5], 1),                 # T2_APPEND_EMPTY
        ([5], 10, [5, 10], 2),           # T3_APPEND_NONEMPTY
    ],
)
def test_append(pre_vals, append_val, expected_list, expected_size):
    ll = _build_linked_list(pre_vals)
    ll.append(append_val)
    assert ll.to_list() == expected_list
    assert len(ll) == expected_size

@pytest.mark.parametrize(
    "pre_vals, prepend_val, expected_list, expected_size",
    [
        ([], 3, [3], 1),                 # T4_PREPEND_EMPTY
        ([3], 2, [2, 3], 2),             # T5_PREPEND_NONEMPTY
    ],
)
def test_prepend(pre_vals, prepend_val, expected_list, expected_size):
    ll = _build_linked_list(pre_vals)
    ll.prepend(prepend_val)
    assert ll.to_list() == expected_list
    assert len(ll) == expected_size

@pytest.mark.parametrize(
    "pre_vals, del_val, expected_result, expected_list, expected_size",
    [
        ([], 5, False, [], 0),                           # T6_DELETE_EMPTY
        ([2, 3], 2, True, [3], 1),                       # T7_DELETE_HEAD
        ([2, 3, 4], 3, True, [2, 4], 2),                 # T8_DELETE_MIDDLE
        ([2, 3], 10, False, [2, 3], 2),                  # T9_DELETE_NOTFOUND
    ],
)
def test_delete(pre_vals, del_val, expected_result, expected_list, expected_size):
    ll = _build_linked_list(pre_vals)
    result = ll.delete(del_val)
    assert result is expected_result
    assert ll.to_list() == expected_list
    assert len(ll) == expected_size

@pytest.mark.parametrize(
    "pre_vals, find_val, expected_index",
    [
        ([2, 3], 3, 1),          # T10_FIND_FOUND
        ([2, 3], 10, -1),        # T11_FIND_NOTFOUND
    ],
)
def test_find(pre_vals, find_val, expected_index):
    ll = _build_linked_list(pre_vals)
    assert ll.find(find_val) == expected_index

@pytest.mark.parametrize(
    "pre_vals, get_index, expected_result",
    [
        ([2, 3], 1, 3),          # T12_GET_VALID
    ],
)
def test_get_valid(pre_vals, get_index, expected_result):
    ll = _build_linked_list(pre_vals)
    assert ll.get(get_index) == expected_result

def test_get_invalid():
    ll = _build_linked_list([2, 3])
    with pytest.raises(IndexError):
        ll.get(5)               # T13_GET_INVALID

@pytest.mark.parametrize(
    "pre_vals, expected_list",
    [
        ([], []),                # T14_TOLIST_EMPTY
        ([2, 3], [2, 3]),        # T15_TOLIST_NONEMPTY
    ],
)
def test_to_list(pre_vals, expected_list):
    ll = _build_linked_list(pre_vals)
    assert ll.to_list() == expected_list

@pytest.mark.parametrize(
    "pre_vals, expected_len",
    [
        ([], 0),                 # T16_LEN_EMPTY
        ([2, 3], 2),             # T17_LEN_NONEMPTY
    ],
)
def test_len(pre_vals, expected_len):
    ll = _build_linked_list(pre_vals)
    assert len(ll) == expected_len