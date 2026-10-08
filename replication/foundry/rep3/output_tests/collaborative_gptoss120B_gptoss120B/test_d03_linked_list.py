import pytest
from data.input_code.d03_linked_list import *

def build_linked_list(values):
    ll = LinkedList()
    for v in values:
        ll.append(v)
    return ll

def apply_operations(ll, ops):
    for op in ops:
        name, arg = op
        if name == "append":
            ll.append(arg)
        elif name == "prepend":
            ll.prepend(arg)
        elif name == "delete":
            ll.delete(arg)
        else:
            raise ValueError(f"Unsupported operation {name}")

@pytest.mark.parametrize(
    "initial, data, expected_list, expected_len",
    [
        ([], 1, [1], 1),                 # T1_APPEND_EMPTY
        ([1], 2, [1, 2], 2),             # T2_APPEND_NONEMPTY
    ],
)
def test_append(initial, data, expected_list, expected_len):
    ll = build_linked_list(initial)
    ll.append(data)
    assert ll.to_list() == expected_list
    assert len(ll) == expected_len

@pytest.mark.parametrize(
    "initial, data, expected_list, expected_len",
    [
        ([], 5, [5], 1),                 # T3_PREPEND_EMPTY
        ([2, 3], 1, [1, 2, 3], 3),       # T4_PREPEND_NONEMPTY
    ],
)
def test_prepend(initial, data, expected_list, expected_len):
    ll = build_linked_list(initial)
    ll.prepend(data)
    assert ll.to_list() == expected_list
    assert len(ll) == expected_len

@pytest.mark.parametrize(
    "initial, data, expected_result, expected_list, expected_len",
    [
        ([], 10, False, [], 0),                     # T5_DELETE_EMPTY
        ([1, 2, 3], 1, True, [2, 3], 2),            # T6_DELETE_HEAD
        ([1, 2, 3], 2, True, [1, 3], 2),            # T7_DELETE_MIDDLE
        ([1, 2, 3], 3, True, [1, 2], 2),            # T8_DELETE_TAIL
        ([1, 2], 5, False, [1, 2], 2),              # T9_DELETE_NOT_FOUND
    ],
)
def test_delete(initial, data, expected_result, expected_list, expected_len):
    ll = build_linked_list(initial)
    result = ll.delete(data)
    assert result is expected_result
    assert ll.to_list() == expected_list
    assert len(ll) == expected_len

@pytest.mark.parametrize(
    "initial, data, expected_index",
    [
        ([], 7, -1),                                 # T10_FIND_EMPTY
        ([10, 20, 30], 10, 0),                       # T11_FIND_HEAD
        ([10, 20, 30], 20, 1),                       # T12_FIND_MIDDLE
        ([10, 20, 30], 30, 2),                       # T13_FIND_TAIL
        ([1, 2, 3], 99, -1),                         # T14_FIND_NOT_FOUND
    ],
)
def test_find(initial, data, expected_index):
    ll = build_linked_list(initial)
    assert ll.find(data) == expected_index

@pytest.mark.parametrize(
    "initial, index, expected",
    [
        ([5, 6, 7], 0, 5),                           # T15_GET_VALID_FIRST
        ([5, 6, 7], 2, 7),                           # T16_GET_VALID_LAST
    ],
)
def test_get_valid(initial, index, expected):
    ll = build_linked_list(initial)
    assert ll.get(index) == expected

@pytest.mark.parametrize(
    "initial, index, exc",
    [
        ([1, 2], -1, IndexError),                   # T17_GET_NEGATIVE_INDEX
        ([1, 2], 2, IndexError),                    # T18_GET_OUT_OF_RANGE
    ],
)
def test_get_exceptions(initial, index, exc):
    ll = build_linked_list(initial)
    with pytest.raises(exc):
        ll.get(index)

def test_to_list_empty():
    ll = LinkedList()
    assert ll.to_list() == []                         # T19_TOLIST_EMPTY

def test_to_list_after_operations():
    ll = LinkedList()
    ops = [["append", 1], ["prepend", 0], ["append", 2]]
    apply_operations(ll, ops)
    assert ll.to_list() == [0, 1, 2]                  # T20_TOLIST_AFTER_OPERATIONS

def test_len_after_modifications():
    ll = LinkedList()
    ops = [["append", 10], ["append", 20], ["delete", 10]]
    apply_operations(ll, ops)
    assert len(ll) == 1                               # T21_LEN_AFTER_MODIFICATIONS