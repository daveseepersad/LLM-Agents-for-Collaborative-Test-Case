import pytest
from data.input_code.d03_linked_list import *

@pytest.fixture
def empty_ll():
    """Provide a fresh empty LinkedList for each test."""
    return LinkedList()

@pytest.mark.parametrize(
    "method, args, expected_head, expected_size",
    [
        ("append", (1,), 1, 1),   # T1_LL_append_empty
        ("prepend", (1,), 1, 1),  # T2_LL_prepend_empty
    ],
)
def test_append_prepend_on_empty(empty_ll, method, args, expected_head, expected_size):
    """Append or prepend on an empty list should initialize head and size correctly."""
    # invoke the method dynamically
    getattr(empty_ll, method)(*args)

    # head should contain the inserted data
    assert empty_ll.head is not None
    assert empty_ll.head.data == expected_head

    # size should be updated
    assert len(empty_ll) == expected_size


def test_delete_on_empty_returns_false(empty_ll):
    """Deleting from an empty list should return False."""
    result = empty_ll.delete(1)  # T3_LL_delete_empty
    assert result is False


def test_find_on_empty_returns_minus_one(empty_ll):
    """Finding any element in an empty list should return -1."""
    result = empty_ll.find(1)  # T4_LL_find_empty
    assert result == -1


@pytest.mark.parametrize(
    "index, exc",
    [
        (0, IndexError),   # T5_LL_get_empty_0
        (-1, IndexError),  # T6_LL_get_empty_negative
    ],
)
def test_get_on_empty_raises_index_error(empty_ll, index, exc):
    """Getting any index from an empty list should raise IndexError."""
    with pytest.raises(exc):
        empty_ll.get(index)


def test_to_list_on_empty_returns_empty_list(empty_ll):
    """to_list on an empty list should return an empty Python list."""
    result = empty_ll.to_list()  # T7_LL_to_list_empty
    assert result == []


def test_len_on_empty_returns_zero(empty_ll):
    """len() on an empty list should be 0."""
    assert len(empty_ll) == 0  # T8_LL_len_empty

import pytest
from data.input_code.d03_linked_list import *

@pytest.fixture
def ll_1_2_3():
    """LinkedList containing [1, 2, 3]."""
    ll = LinkedList()
    ll.append(1)
    ll.append(2)
    ll.append(3)
    return ll

@pytest.fixture
def ll_10_20_30():
    """LinkedList containing [10, 20, 30]."""
    ll = LinkedList()
    ll.append(10)
    ll.append(20)
    ll.append(30)
    return ll

@pytest.mark.parametrize(
    "data, expected",
    [
        (1, True),   # delete head
        (2, True),   # delete middle
        (99, False), # not found
    ],
)
def test_delete_various(ll_1_2_3, data, expected):
    """Deleting elements from a non‑empty list should return the correct boolean."""
    result = ll_1_2_3.delete(data)
    assert result is expected

def test_find_non_empty(ll_10_20_30):
    """Finding an existing element should return its index."""
    result = ll_10_20_30.find(20)  # T_MISSING_FIND_NON_EMPTY
    assert result == 1

def test_get_valid_index(ll_1_2_3):
    """Getting a valid index should return the correct data."""
    result = ll_1_2_3.get(2)  # T_MISSING_GET_VALID_INDEX
    assert result == 3

def test_get_out_of_range_raises(ll_1_2_3):
    """Getting an index outside the bounds should raise IndexError."""
    with pytest.raises(IndexError):
        ll_1_2_3.get(3)  # T_MISSING_GET_OUT_OF_RANGE

import pytest
from data.input_code.d03_linked_list import *

def test_to_list_on_non_empty(ll_1_2_3):
    result = ll_1_2_3.to_list()
    assert result == [1, 2, 3]

def test_len_on_non_empty(ll_1_2_3):
    assert len(ll_1_2_3) == 3

def test_find_non_existent_on_non_empty(ll_1_2_3):
    result = ll_1_2_3.find(99)
    assert result == -1

def test_delete_tail_on_non_empty(ll_1_2_3):
    result = ll_1_2_3.delete(3)
    assert result is True