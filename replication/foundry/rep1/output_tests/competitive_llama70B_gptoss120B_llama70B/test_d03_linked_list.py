import pytest
from data.input_code.d03_linked_list import *

@pytest.fixture
def empty_list():
    """Fixture for a newly created empty LinkedList."""
    return LinkedList()

@pytest.fixture
def populated_list():
    """
    Fixture for a LinkedList containing the elements [-1, 0, 1, 2]
    built using the sequence described in the test plan:
    - append 1
    - append 2
    - prepend 0
    - prepend -1
    """
    ll = LinkedList()
    ll.append(1)      # [1]
    ll.append(2)      # [1, 2]
    ll.prepend(0)     # [0, 1, 2]
    ll.prepend(-1)    # [-1, 0, 1, 2]
    return ll

def test_init(empty_list):
    """T1_OK – verify that a new list is empty."""
    assert empty_list.head is None
    assert len(empty_list) == 0

@pytest.mark.parametrize(
    "method, data",
    [
        ("append", 1),
        ("append", 2),
        ("prepend", 0),
        ("prepend", -1),
    ]
)
def test_append_prepend(empty_list, method, data):
    """
    T2_OK, T3_OK, T4_OK, T5_OK – ensure append/prepend execute without error
    and correctly update size and head for a single operation on an empty list.
    """
    # Perform the operation on a fresh empty list
    getattr(empty_list, method)(data)

    # After a single operation the list size should be 1
    assert len(empty_list) == 1

    # The head's data should be the inserted value (both append and prepend
    # on an empty list make the new node the head)
    assert empty_list.head.data == data

@pytest.mark.parametrize(
    "data, expected",
    [
        (1, True),   # T6_OK – delete existing node
        (10, False)  # T7_ERR – attempt to delete non‑existent node
    ]
)
def test_delete(populated_list, data, expected):
    result = populated_list.delete(data)
    assert result is expected
    # Additional sanity checks
    if expected:
        # Deleted element should no longer be found
        assert populated_list.find(data) == -1
    else:
        # List size should remain unchanged for failed deletion
        assert len(populated_list) == 4

@pytest.mark.parametrize(
    "data, expected",
    [
        (1, 2),    # T8_OK – find existing node
        (10, -1)   # T9_ERR – find non‑existent node
    ]
)
def test_find(populated_list, data, expected):
    assert populated_list.find(data) == expected

@pytest.mark.parametrize(
    "index, expected",
    [
        (0, -1),   # T10_OK – get node at valid index
    ]
)
def test_get_success(populated_list, index, expected):
    assert populated_list.get(index) == expected

@pytest.mark.parametrize(
    "index, exc",
    [
        (-1, IndexError),  # T11_ERR – negative index
        (10, IndexError)   # T12_ERR – out‑of‑range index
    ]
)
def test_get_errors(populated_list, index, exc):
    with pytest.raises(exc):
        populated_list.get(index)

def test_to_list(populated_list):
    """T13_OK – convert linked list to Python list."""
    assert populated_list.to_list() == [-1, 0, 1, 2]

def test_len(populated_list):
    """T14_OK – verify __len__ reports correct size."""
    assert len(populated_list) == 4

import pytest

@pytest.mark.parametrize(
    "index, expected",
    [
        (1, 0),   # T_MISSING_GET_MID – get node at middle index
        (3, 2),   # T_MISSING_GET_LAST – get node at last index
    ]
)
def test_get_additional(populated_list, index, expected):
    assert populated_list.get(index) == expected


@pytest.mark.parametrize(
    "data, expected",
    [
        (-1, True),  # T_MISSING_DELETE_HEAD – delete head node
        (2, True),   # T_MISSING_DELETE_TAIL – delete tail node
    ]
)
def test_delete_additional(populated_list, data, expected):
    result = populated_list.delete(data)
    assert result is expected
    # verify the node is really gone
    assert populated_list.find(data) == -1
    # size should have decreased appropriately
    assert len(populated_list) == 3 if expected else len(populated_list) == 4


def test_prepend_empty(empty_list):
    """T_MISSING_PREPEND_EMPTY – prepend to empty list."""
    empty_list.prepend(5)
    assert len(empty_list) == 1
    assert empty_list.head.data == 5
    assert empty_list.to_list() == [5]


def test_append_empty(empty_list):
    """T_MISSING_APPEND_EMPTY – append to empty list."""
    empty_list.append(5)
    assert len(empty_list) == 1
    assert empty_list.head.data == 5
    assert empty_list.to_list() == [5]


@pytest.mark.parametrize(
    "data, expected",
    [
        (-1, 0),  # T_MISSING_FIND_HEAD – find head node
        (2, 3),   # T_MISSING_FIND_TAIL – find tail node
    ]
)
def test_find_additional(populated_list, data, expected):
    assert populated_list.find(data) == expected

import pytest

def test_delete_all_nodes():
    """T_MISSING_EDGE_DELETE_ALL – delete all nodes one by one."""
    ll = LinkedList()
    # create list with multiple distinct nodes
    for val in [1, 2, 3]:
        ll.append(val)
    # delete each node and verify list shrinks
    for i, val in enumerate([1, 2, 3]):
        assert ll.delete(val) is True
        assert ll.find(val) == -1
        assert len(ll) == 2 - i
    # after all deletions the list should be empty
    assert ll.head is None
    assert len(ll) == 0

def test_delete_none_empty(empty_list):
    """T_MISSING_EDGE_DELETE_NONE – delete from empty list returns False."""
    assert empty_list.delete(10) is False
    assert len(empty_list) == 0

def test_find_all(populated_list):
    """T_MISSING_EDGE_FIND_ALL – find existing tail node."""
    assert populated_list.find(2) == 3

def test_get_all(populated_list):
    """T_MISSING_EDGE_GET_ALL – get node at index 2."""
    assert populated_list.get(2) == 1

def test_prepend_many(empty_list):
    """T_MISSING_EDGE_PREPEND_MANY – prepend multiple nodes and verify order."""
    for val in [10, 20, 30]:
        empty_list.prepend(val)
    # after prepending 10,20,30 the list should be [30,20,10]
    assert empty_list.to_list() == [30, 20, 10]
    assert len(empty_list) == 3
    # head should be the last prepended value
    assert empty_list.head.data == 30

def test_append_many(empty_list):
    """T_MISSING_EDGE_APPEND_MANY – append multiple nodes and verify order."""
    for val in [10, 20, 30]:
        empty_list.append(val)
    # after appending 10,20,30 the list should be [10,20,30]
    assert empty_list.to_list() == [10, 20, 30]
    assert len(empty_list) == 3
    # head should be the first appended value
    assert empty_list.head.data == 10

def test_to_list_empty(empty_list):
    """T_MISSING_EDGE_TO_LIST_EMPTY – convert empty list to Python list."""
    assert empty_list.to_list() == []

def test_len_empty(empty_list):
    """T_MISSING_EDGE_LEN_EMPTY – length of empty list is zero."""
    assert len(empty_list) == 0