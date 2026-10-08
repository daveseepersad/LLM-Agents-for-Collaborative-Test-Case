import pytest
from data.input_code.d03_linked_list import *

def _apply_setup(ll, setup):
    """Execute a list of operations on the LinkedList instance."""
    for op in setup:
        if op["op"] == "append":
            ll.append(op["value"])
        elif op["op"] == "prepend":
            ll.prepend(op["value"])
        else:
            raise ValueError(f"Unsupported operation {op['op']}")

# ----------------------------------------------------------------------
# to_list and __len__ on an empty list
# ----------------------------------------------------------------------
def test_ll_init_empty_to_list():
    ll = LinkedList()
    assert ll.to_list() == []

def test_ll_len_empty():
    ll = LinkedList()
    assert len(ll) == 0

# ----------------------------------------------------------------------
# append tests
# ----------------------------------------------------------------------
@pytest.mark.parametrize(
    "setup,data,expected_list",
    [
        ([], 1, [1]),                         # append on empty
        ([{"op": "append", "value": 1}], 2, [1, 2]),  # append to tail
    ],
)
def test_ll_append(setup, data, expected_list):
    ll = LinkedList()
    _apply_setup(ll, setup)
    ll.append(data)
    assert ll.to_list() == expected_list
    # size should match length of list
    assert len(ll) == len(expected_list)

# ----------------------------------------------------------------------
# prepend tests
# ----------------------------------------------------------------------
@pytest.mark.parametrize(
    "setup,data,expected_list",
    [
        ([], 9, [9]),  # prepend on empty
    ],
)
def test_ll_prepend(setup, data, expected_list):
    ll = LinkedList()
    _apply_setup(ll, setup)
    ll.prepend(data)
    assert ll.to_list() == expected_list
    assert len(ll) == len(expected_list)

# ----------------------------------------------------------------------
# find tests
# ----------------------------------------------------------------------
@pytest.mark.parametrize(
    "setup,data,expected_index",
    [
        (
            [{"op": "append", "value": 5}, {"op": "append", "value": 7}],
            7,
            1,
        ),  # found at index 1
        (
            [{"op": "append", "value": 5}, {"op": "append", "value": 7}],
            9,
            -1,
        ),  # not found
    ],
)
def test_ll_find(setup, data, expected_index):
    ll = LinkedList()
    _apply_setup(ll, setup)
    assert ll.find(data) == expected_index

# ----------------------------------------------------------------------
# get tests (including out‑of‑range)
# ----------------------------------------------------------------------
@pytest.mark.parametrize(
    "setup,index,expected",
    [
        (
            [{"op": "append", "value": 5}, {"op": "append", "value": 7}],
            0,
            5,
        ),
        (
            [{"op": "append", "value": 5}, {"op": "append", "value": 7}],
            1,
            7,
        ),
    ],
)
def test_ll_get_valid(setup, index, expected):
    ll = LinkedList()
    _apply_setup(ll, setup)
    assert ll.get(index) == expected

def test_ll_get_out_of_range():
    ll = LinkedList()
    _apply_setup(
        ll,
        [{"op": "append", "value": 5}, {"op": "append", "value": 7}],
    )
    with pytest.raises(IndexError):
        ll.get(2)

# ----------------------------------------------------------------------
# delete tests
# ----------------------------------------------------------------------
@pytest.mark.parametrize(
    "setup,data,expected_success,expected_list",
    [
        (
            [{"op": "append", "value": 5}, {"op": "append", "value": 7}],
            5,
            True,
            [7],
        ),  # delete head
        (
            [{"op": "append", "value": 5}, {"op": "append", "value": 7}, {"op": "append", "value": 9}],
            7,
            True,
            [5, 9],
        ),  # delete middle
        (
            [{"op": "append", "value": 5}, {"op": "append", "value": 7}],
            99,
            False,
            [5, 7],
        ),  # not found
    ],
)
def test_ll_delete(setup, data, expected_success, expected_list):
    ll = LinkedList()
    _apply_setup(ll, setup)
    result = ll.delete(data)
    assert result is expected_success
    assert ll.to_list() == expected_list
    assert len(ll) == len(expected_list)

import pytest

# ----------------------------------------------------------------------
# delete tail cases and empty list
# ----------------------------------------------------------------------
@pytest.mark.parametrize(
    "setup,data,expected_success,expected_list",
    [
        (
            [{"op": "append", "value": 5},
             {"op": "append", "value": 7},
             {"op": "append", "value": 9}],
            9,
            True,
            [5, 7],
        ),  # delete tail in longer list
        (
            [{"op": "append", "value": 5},
             {"op": "append", "value": 7}],
            7,
            True,
            [5],
        ),  # delete tail in 2‑element list
        (
            [],
            1,
            False,
            [],
        ),  # delete from empty list
    ],
)
def test_ll_delete_tail_and_empty(setup, data, expected_success, expected_list):
    ll = LinkedList()
    _apply_setup(ll, setup)
    result = ll.delete(data)
    assert result is expected_success
    assert ll.to_list() == expected_list
    assert len(ll) == len(expected_list)


# ----------------------------------------------------------------------
# find in empty list
# ----------------------------------------------------------------------
def test_ll_find_empty():
    ll = LinkedList()
    _apply_setup(ll, [])
    assert ll.find(10) == -1


# ----------------------------------------------------------------------
# get with negative index should raise IndexError
# ----------------------------------------------------------------------
def test_ll_get_negative_index():
    ll = LinkedList()
    _apply_setup(
        ll,
        [
            {"op": "append", "value": 1},
            {"op": "append", "value": 2},
        ],
    )
    with pytest.raises(IndexError):
        ll.get(-1)


# ----------------------------------------------------------------------
# prepend on non‑empty list and verify to_list order
# ----------------------------------------------------------------------
def test_ll_prepend_to_list_to_list():
    ll = LinkedList()
    _apply_setup(
        ll,
        [
            {"op": "prepend", "value": 1},
            {"op": "append", "value": 2},
        ],
    )
    assert ll.to_list() == [1, 2]
    assert len(ll) == 2