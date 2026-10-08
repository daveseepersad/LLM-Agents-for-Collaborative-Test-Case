import pytest
from data.input_code.d03_linked_list import *

@pytest.mark.parametrize('data', [
    (42),
    (-1)
])
def test_ll_append_and_prepend(data):
    ll = LinkedList()
    if data == 42:
        ll.append(data)
    else:
        ll.prepend(data)
    assert ll.head is not None

def test_ll_delete_on_empty():
    ll = LinkedList()
    assert ll.delete(7) == False

def test_ll_find_on_empty():
    ll = LinkedList()
    assert ll.find(7) == -1

def test_ll_get_neg_index():
    ll = LinkedList()
    with pytest.raises(IndexError):
        ll.get(-1)

def test_ll_to_list_empty():
    ll = LinkedList()
    assert ll.to_list() == []

def test_ll_len_empty():
    ll = LinkedList()
    assert len(ll) == 0

def test_ll_find_not_found_nonempty():
    ll = LinkedList()
    ll.append(1)
    ll.append(2)
    ll.append(3)
    assert ll.find(999) == -1

import pytest

@pytest.mark.parametrize(
    "delete_data, expected_head, expected_list",
    [
        (1, 2, [2, 3]),   # delete head
        (2, 1, [1, 3]),   # delete middle
        (3, 1, [1, 2]),   # delete tail
    ],
)
def test_ll_delete_various_positions(delete_data, expected_head, expected_list):
    ll = LinkedList()
    for value in [1, 2, 3]:
        ll.append(value)
    result = ll.delete(delete_data)
    assert result is True
    # verify new head (or None if list became empty)
    assert (ll.head.data if ll.head else None) == expected_head
    # verify list contents
    assert ll.to_list() == expected_list


def test_ll_get_out_of_range():
    ll = LinkedList()
    ll.append(10)
    ll.append(20)
    # size is 2, valid indices are 0 and 1; index 2 should raise IndexError
    with pytest.raises(IndexError):
        ll.get(2)


def test_ll_find_present():
    ll = LinkedList()
    ll.append(1)
    ll.append(2)
    ll.append(3)
    assert ll.find(2) == 1

@pytest.mark.parametrize(
    "setup_actions, delete_data, expected_result, expected_list",
    [
        (
            [("append", 1), ("append", 2)],
            3,
            False,
            [1, 2],
        ),
    ],
)
def test_ll_delete_not_found(setup_actions, delete_data, expected_result, expected_list):
    ll = LinkedList()
    for method, value in setup_actions:
        getattr(ll, method)(value)
    result = ll.delete(delete_data)
    assert result is expected_result
    assert ll.to_list() == expected_list


@pytest.mark.parametrize(
    "setup_actions, index, expected",
    [
        (
            [("append", 5), ("append", 10)],
            0,
            5,
        ),
    ],
)
def test_ll_get_valid_index_0(setup_actions, index, expected):
    ll = LinkedList()
    for method, value in setup_actions:
        getattr(ll, method)(value)
    assert ll.get(index) == expected


@pytest.mark.parametrize(
    "setup_actions, expected_len",
    [
        (
            [("append", 100), ("append", 200)],
            2,
        ),
    ],
)
def test_ll_len_non_empty(setup_actions, expected_len):
    ll = LinkedList()
    for method, value in setup_actions:
        getattr(ll, method)(value)
    assert len(ll) == expected_len


@pytest.mark.parametrize(
    "setup_actions, expected",
    [
        (
            [("append", 1), ("append", 2), ("prepend", 0)],
            [0, 1, 2],
        ),
    ],
)
def test_ll_to_list_non_empty(setup_actions, expected):
    ll = LinkedList()
    for method, value in setup_actions:
        getattr(ll, method)(value)
    assert ll.to_list() == expected

import pytest

@pytest.mark.parametrize(
    "setup_actions, data, expected",
    [
        (
            [("append", 5), ("append", 5), ("append", 7)],
            5,
            True,
        ),
    ],
)
def test_ll_delete_duplicate_first_occurrence(setup_actions, data, expected):
    ll = LinkedList()
    for method, value in setup_actions:
        getattr(ll, method)(value)
    result = ll.delete(data)
    assert result is expected
    # only the first occurrence should be removed
    assert ll.to_list() == [5, 7]


@pytest.mark.parametrize(
    "setup_actions, index, expected",
    [
        (
            [("append", 10), ("append", 20), ("append", 30)],
            1,
            20,
        ),
    ],
)
def test_ll_get_middle_value(setup_actions, index, expected):
    ll = LinkedList()
    for method, value in setup_actions:
        getattr(ll, method)(value)
    assert ll.get(index) == expected


@pytest.mark.parametrize(
    "setup_actions, expected",
    [
        (
            [("append", 99)],
            [99],
        ),
    ],
)
def test_ll_to_list_single(setup_actions, expected):
    ll = LinkedList()
    for method, value in setup_actions:
        getattr(ll, method)(value)
    assert ll.to_list() == expected


@pytest.mark.parametrize(
    "setup_actions, expected_len",
    [
        (
            [
                ("append", 1),
                ("prepend", 0),
                ("append", 2),
                ("delete", 0),
                ("delete", 1),
                ("delete", 2),
            ],
            0,
        ),
    ],
)
def test_ll_len_after_operations(setup_actions, expected_len):
    ll = LinkedList()
    for method, value in setup_actions:
        getattr(ll, method)(value)
    assert len(ll) == expected_len