import pytest
from data.input_code.d03_linked_list import *

def make_linked_list(values):
    """Utility to create a LinkedList populated with the given iterable of values."""
    ll = LinkedList()
    for v in values:
        ll.append(v)
    return ll

def list_structure(ll):
    """Return a tuple (head_data, next_head_data, ...) for easy comparison."""
    result = []
    current = ll.head
    while current:
        result.append(current.data)
        current = current.next
    return result

def test_init():
    ll = LinkedList()
    assert ll.head is None
    assert len(ll) == 0

@pytest.mark.parametrize(
    "initial, append_val, expected_list, expected_size",
    [
        ([], 5, [5], 1),                     # T2_APPEND_EMPTY
        ([5], 10, [5, 10], 2),               # T3_APPEND_NONEMPTY
    ],
)
def test_append(initial, append_val, expected_list, expected_size):
    ll = make_linked_list(initial)
    ll.append(append_val)
    assert list_structure(ll) == expected_list
    assert len(ll) == expected_size

@pytest.mark.parametrize(
    "initial, prepend_val, expected_list, expected_size",
    [
        ([], 3, [3], 1),                     # T4_PREPEND_EMPTY
        ([3], 2, [2, 3], 2),                 # T5_PREPEND_NONEMPTY
    ],
)
def test_prepend(initial, prepend_val, expected_list, expected_size):
    ll = make_linked_list(initial)
    ll.prepend(prepend_val)
    assert list_structure(ll) == expected_list
    assert len(ll) == expected_size

@pytest.mark.parametrize(
    "initial, delete_val, expected_result, expected_list, expected_size",
    [
        ([], 5, False, [], 0),                               # T6_DELETE_EMPTY
        ([2, 3], 2, True, [3], 1),                           # T7_DELETE_HEAD
        ([2, 3, 4], 3, True, [2, 4], 2),                     # T8_DELETE_MIDDLE
        ([2, 3, 4], 4, True, [2, 3], 2),                     # T9_DELETE_TAIL
        ([2, 3], 10, False, [2, 3], 2),                      # T10_DELETE_MISS
    ],
)
def test_delete(initial, delete_val, expected_result, expected_list, expected_size):
    ll = make_linked_list(initial)
    result = ll.delete(delete_val)
    assert result is expected_result
    assert list_structure(ll) == expected_list
    assert len(ll) == expected_size

@pytest.mark.parametrize(
    "initial, find_val, expected_index",
    [
        ([2, 3], 10, -1),   # T11_FIND_MISS
        ([2, 3], 2, 0),    # T12_FIND_HIT
    ],
)
def test_find(initial, find_val, expected_index):
    ll = make_linked_list(initial)
    assert ll.find(find_val) == expected_index

def test_get_out_of_bounds():
    ll = make_linked_list([2, 3])
    with pytest.raises(IndexError):
        ll.get(5)   # T13_GET_OOB

@pytest.mark.parametrize(
    "initial, index, expected_value",
    [
        ([2, 3], 1, 3),   # T14_GET_VALID
    ],
)
def test_get_valid(initial, index, expected_value):
    ll = make_linked_list(initial)
    assert ll.get(index) == expected_value

@pytest.mark.parametrize(
    "initial, expected_list",
    [
        ([], []),                     # T15_TO_LIST_EMPTY
        ([2, 3], [2, 3]),             # T16_TO_LIST_NONEMPTY
    ],
)
def test_to_list(initial, expected_list):
    ll = make_linked_list(initial)
    assert ll.to_list() == expected_list

@pytest.mark.parametrize(
    "initial, expected_len",
    [
        ([], 0),          # T17_LEN_EMPTY
        ([2, 3], 2),      # T18_LEN_NONEMPTY
    ],
)
def test_len(initial, expected_len):
    ll = make_linked_list(initial)
    assert len(ll) == expected_len