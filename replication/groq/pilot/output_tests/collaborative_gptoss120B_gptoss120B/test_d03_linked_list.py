import pytest
from data.input_code.d03_linked_list import *

def build_linked_list(values):
    """Utility to create a LinkedList with the given iterable of values."""
    ll = LinkedList()
    for v in values:
        ll.append(v)
    return ll

@pytest.mark.parametrize(
    "initial, new_data, expected",
    [
        ([], 5, [5]),                     # T1_APPEND_EMPTY
        ([1], 2, [1, 2]),                 # T2_APPEND_NONEMPTY
    ],
)
def test_append(initial, new_data, expected):
    ll = build_linked_list(initial)
    ll.append(new_data)
    assert ll.to_list() == expected
    # size should match length of list
    assert len(ll) == len(expected)

@pytest.mark.parametrize(
    "initial, new_data, expected",
    [
        ([], 3, [3]),                     # T3_PREPEND_EMPTY
        ([1, 2], 0, [0, 1, 2]),           # prepend onto non‑empty list
    ],
)
def test_prepend(initial, new_data, expected):
    ll = build_linked_list(initial)
    ll.prepend(new_data)
    assert ll.to_list() == expected
    assert len(ll) == len(expected)

@pytest.mark.parametrize(
    "initial, del_data, expected_ret, expected_list",
    [
        ([], 1, False, []),                               # T4_DELETE_EMPTY
        ([1, 2], 1, True, [2]),                           # T5_DELETE_HEAD
        ([1, 2, 3], 3, True, [1, 2]),                     # T6_DELETE_TAIL
        ([1, 2], 5, False, [1, 2]),                       # T7_DELETE_NOT_FOUND
    ],
)
def test_delete(initial, del_data, expected_ret, expected_list):
    ll = build_linked_list(initial)
    ret = ll.delete(del_data)
    assert ret is expected_ret
    assert ll.to_list() == expected_list
    assert len(ll) == len(expected_list)

@pytest.mark.parametrize(
    "initial, find_data, expected_index",
    [
        ([7, 8], 7, 0),          # T8_FIND_HEAD
        ([7, 8], 8, 1),          # T9_FIND_TAIL
        ([1], 9, -1),            # T10_FIND_NOT_FOUND
    ],
)
def test_find(initial, find_data, expected_index):
    ll = build_linked_list(initial)
    assert ll.find(find_data) == expected_index

@pytest.mark.parametrize(
    "initial, index, expected_value",
    [
        ([42], 0, 42),                     # T11_GET_VALID_ZERO
        ([1, 2, 3], 2, 3),                 # T12_GET_VALID_LAST
    ],
)
def test_get_success(initial, index, expected_value):
    ll = build_linked_list(initial)
    assert ll.get(index) == expected_value

@pytest.mark.parametrize(
    "initial, index, exc",
    [
        ([], -1, IndexError),             # T13_GET_NEGATIVE_INDEX
        ([1], 1, IndexError),             # T14_GET_OUT_OF_RANGE
    ],
)
def test_get_errors(initial, index, exc):
    ll = build_linked_list(initial)
    with pytest.raises(exc):
        ll.get(index)

@pytest.mark.parametrize(
    "initial, expected",
    [
        ([], []),                          # T15_TOLIST_EMPTY
        ([5, 6], [5, 6]),                  # T16_TOLIST_NONEMPTY
    ],
)
def test_to_list(initial, expected):
    ll = build_linked_list(initial)
    assert ll.to_list() == expected

def test_len_after_operations():
    ll = LinkedList()
    ll.append(1)
    ll.append(2)
    assert len(ll) == 2                     # T17_LEN_AFTER_OPERATIONS