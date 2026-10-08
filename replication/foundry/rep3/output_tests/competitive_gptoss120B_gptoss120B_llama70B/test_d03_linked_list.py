import pytest
from data.input_code.d03_linked_list import *

def _apply_setup(ll, steps):
    """Utility to run a sequence of method calls on a LinkedList."""
    for step in steps:
        getattr(ll, step["method"])(**step["args"])

# ---------- append ----------
@pytest.mark.parametrize(
    "setup,input_data,expected_list,expected_len",
    [
        ([], 1, [1], 1),                                   # T1_APPEND_EMPTY
        ([{"method": "append", "args": {"data": 1}}], 2, [1, 2], 2),  # T2_APPEND_NONEMPTY
    ],
)
def test_append(setup, input_data, expected_list, expected_len):
    ll = LinkedList()
    _apply_setup(ll, setup)
    ll.append(input_data)
    assert ll.to_list() == expected_list
    assert len(ll) == expected_len

# ---------- prepend ----------
@pytest.mark.parametrize(
    "setup,input_data,expected_list,expected_len",
    [
        ([], 5, [5], 1),                                   # T3_PREPEND_EMPTY
        ([{"method": "append", "args": {"data": 10}}], 5, [5, 10], 2),  # T4_PREPEND_NONEMPTY
    ],
)
def test_prepend(setup, input_data, expected_list, expected_len):
    ll = LinkedList()
    _apply_setup(ll, setup)
    ll.prepend(input_data)
    assert ll.to_list() == expected_list
    assert len(ll) == expected_len

# ---------- delete ----------
@pytest.mark.parametrize(
    "setup,del_data,expected_result,expected_list,expected_len",
    [
        ([], 99, False, [], 0),                            # T5_DELETE_EMPTY
        (
            [
                {"method": "append", "args": {"data": 1}},
                {"method": "append", "args": {"data": 2}},
            ],
            1,
            True,
            [2],
            1,
        ),                                                 # T6_DELETE_HEAD
        (
            [
                {"method": "append", "args": {"data": 1}},
                {"method": "append", "args": {"data": 2}},
                {"method": "append", "args": {"data": 3}},
            ],
            2,
            True,
            [1, 3],
            2,
        ),                                                 # T7_DELETE_MIDDLE
        (
            [
                {"method": "append", "args": {"data": 1}},
                {"method": "append", "args": {"data": 2}},
            ],
            2,
            True,
            [1],
            1,
        ),                                                 # T8_DELETE_TAIL
        (
            [{"method": "append", "args": {"data": 1}}],
            99,
            False,
            [1],
            1,
        ),                                                 # T9_DELETE_NOT_FOUND
    ],
)
def test_delete(setup, del_data, expected_result, expected_list, expected_len):
    ll = LinkedList()
    _apply_setup(ll, setup)
    result = ll.delete(del_data)
    assert result is expected_result
    assert ll.to_list() == expected_list
    assert len(ll) == expected_len

# ---------- find ----------
@pytest.mark.parametrize(
    "setup,find_data,expected_index",
    [
        ([], 1, -1),                                      # T10_FIND_EMPTY
        ([{"method": "append", "args": {"data": 7}}], 7, 0),  # T11_FIND_HEAD
        (
            [
                {"method": "append", "args": {"data": 1}},
                {"method": "append", "args": {"data": 2}},
                {"method": "append", "args": {"data": 3}},
            ],
            2,
            1,
        ),                                                # T12_FIND_MIDDLE
        ([{"method": "append", "args": {"data": 1}}], 99, -1),  # T13_FIND_NOT_FOUND
    ],
)
def test_find(setup, find_data, expected_index):
    ll = LinkedList()
    _apply_setup(ll, setup)
    assert ll.find(find_data) == expected_index

# ---------- get ----------
@pytest.mark.parametrize(
    "setup,index,expected",
    [
        (
            [{"method": "append", "args": {"data": 42}}],
            0,
            42,
        ),                                                # T14_GET_VALID_ZERO
        (
            [
                {"method": "append", "args": {"data": 1}},
                {"method": "append", "args": {"data": 2}},
            ],
            1,
            2,
        ),                                                # T15_GET_VALID_LAST
    ],
)
def test_get_success(setup, index, expected):
    ll = LinkedList()
    _apply_setup(ll, setup)
    assert ll.get(index) == expected

@pytest.mark.parametrize(
    "setup,index,exc",
    [
        (
            [{"method": "append", "args": {"data": 1}}],
            -1,
            IndexError,
        ),                                                # T16_GET_NEGATIVE
        (
            [{"method": "append", "args": {"data": 1}}],
            1,
            IndexError,
        ),                                                # T17_GET_OUT_OF_RANGE
    ],
)
def test_get_errors(setup, index, exc):
    ll = LinkedList()
    _apply_setup(ll, setup)
    with pytest.raises(exc):
        ll.get(index)

# ---------- to_list ----------
@pytest.mark.parametrize(
    "setup,expected",
    [
        ([], []),                                          # T18_TOLIST_EMPTY
        (
            [
                {"method": "append", "args": {"data": 1}},
                {"method": "prepend", "args": {"data": 0}},
                {"method": "append", "args": {"data": 2}},
            ],
            [0, 1, 2],
        ),                                                # T19_TOLIST_ORDER
    ],
)
def test_to_list(setup, expected):
    ll = LinkedList()
    _apply_setup(ll, setup)
    assert ll.to_list() == expected

# ---------- __len__ ----------
def test_len_after_ops():
    ll = LinkedList()
    _apply_setup(
        ll,
        [
            {"method": "append", "args": {"data": 1}},
            {"method": "append", "args": {"data": 2}},
        ],
    )
    assert len(ll) == 2

import pytest

# ---------- append (multiple) ----------
@pytest.mark.parametrize(
    "initial,data,expected_list,expected_len",
    [
        ([1, 2], 3, [1, 2, 3], 3),  # T20_APPEND_MULTIPLE
    ],
)
def test_append_multiple(initial, data, expected_list, expected_len):
    ll = LinkedList()
    # set up initial list via append
    for val in initial:
        ll.append(val)
    ll.append(data)
    assert ll.to_list() == expected_list
    assert len(ll) == expected_len


# ---------- find (tail) ----------
@pytest.mark.parametrize(
    "initial,find_data,expected_index",
    [
        ([1, 2, 3], 3, 2),  # T21_FIND_TAIL
    ],
)
def test_find_tail(initial, find_data, expected_index):
    ll = LinkedList()
    for val in initial:
        ll.append(val)
    assert ll.find(find_data) == expected_index


# ---------- get (middle) ----------
@pytest.mark.parametrize(
    "initial,index,expected",
    [
        ([1, 2, 3], 1, 2),  # T22_GET_MIDDLE
    ],
)
def test_get_middle(initial, index, expected):
    ll = LinkedList()
    for val in initial:
        ll.append(val)
    assert ll.get(index) == expected


# ---------- __len__ after prepend and delete ----------
@pytest.mark.parametrize(
    "prepend_vals,append_vals,delete_val,expected_len",
    [
        ([5], [1, 2], 5, 2),  # T23_LEN_AFTER_PREPEND_DELETE
    ],
)
def test_len_after_prepend_delete(prepend_vals, append_vals, delete_val, expected_len):
    ll = LinkedList()
    for val in prepend_vals:
        ll.prepend(val)
    for val in append_vals:
        ll.append(val)
    ll.delete(delete_val)
    assert len(ll) == expected_len

# ---------- delete (single element) ----------
@pytest.mark.parametrize(
    "setup,del_data,expected_result,expected_list,expected_len",
    [
        (
            [{"method": "append", "args": {"data": 42}}],
            42,
            True,
            [],
            0,
        ),  # T24_DELETE_SINGLE
    ],
)
def test_delete_single(setup, del_data, expected_result, expected_list, expected_len):
    ll = LinkedList()
    _apply_setup(ll, setup)
    result = ll.delete(del_data)
    assert result is expected_result
    assert ll.to_list() == expected_list
    assert len(ll) == expected_len


# ---------- get (empty list) ----------
@pytest.mark.parametrize(
    "setup,index,exc",
    [
        ([], 0, IndexError),  # T25_GET_EMPTY
    ],
)
def test_get_empty(setup, index, exc):
    ll = LinkedList()
    _apply_setup(ll, setup)
    with pytest.raises(exc):
        ll.get(index)

import pytest

# ---------- delete (tail in longer list & duplicate first) ----------
@pytest.mark.parametrize(
    "setup,del_data,expected_result,expected_list,expected_len",
    [
        (
            [
                {"method": "append", "args": {"data": 1}},
                {"method": "append", "args": {"data": 2}},
                {"method": "append", "args": {"data": 3}},
            ],
            3,
            True,
            [1, 2],
            2,
        ),  # T26_DELETE_TAIL_LONG
        (
            [
                {"method": "append", "args": {"data": 1}},
                {"method": "append", "args": {"data": 2}},
                {"method": "append", "args": {"data": 2}},
                {"method": "append", "args": {"data": 3}},
            ],
            2,
            True,
            [1, 2, 3],
            3,
        ),  # T27_DELETE_DUP_FIRST
    ],
)
def test_delete_additional(setup, del_data, expected_result, expected_list, expected_len):
    ll = LinkedList()
    _apply_setup(ll, setup)
    result = ll.delete(del_data)
    assert result is expected_result
    assert ll.to_list() == expected_list
    assert len(ll) == expected_len


# ---------- prepend (multiple) ----------
@pytest.mark.parametrize(
    "setup,input_data,expected_list,expected_len",
    [
        (
            [{"method": "prepend", "args": {"data": 1}}],
            2,
            [2, 1],
            2,
        ),  # T28_PREPEND_MULTIPLE
    ],
)
def test_prepend_multiple(setup, input_data, expected_list, expected_len):
    ll = LinkedList()
    _apply_setup(ll, setup)
    ll.prepend(input_data)
    assert ll.to_list() == expected_list
    assert len(ll) == expected_len