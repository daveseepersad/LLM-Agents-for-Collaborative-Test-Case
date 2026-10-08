import pytest
from data.input_code.d03_linked_list import *

@pytest.fixture
def empty_list():
    """Return a freshly initialized empty LinkedList."""
    return LinkedList()

@pytest.fixture
def populated_list():
    """
    Return a LinkedList built with the sequence:
    append 1, append 2, prepend 0, prepend -1
    Final order: [-1, 0, 1, 2]
    """
    ll = LinkedList()
    ll.append(1)
    ll.append(2)
    ll.prepend(0)
    ll.prepend(-1)
    return ll

def test_linkedlist_initial_state(empty_list):
    assert empty_list.head is None
    assert len(empty_list) == 0
    assert empty_list.to_list() == []

def test_append_and_prepend_operations(empty_list):
    # Append operations
    empty_list.append(1)
    assert empty_list.to_list() == [1]
    assert len(empty_list) == 1

    empty_list.append(2)
    assert empty_list.to_list() == [1, 2]
    assert len(empty_list) == 2

    # Prepend operations
    empty_list.prepend(0)
    assert empty_list.to_list() == [0, 1, 2]
    assert len(empty_list) == 3

    empty_list.prepend(-1)
    assert empty_list.to_list() == [-1, 0, 1, 2]
    assert len(empty_list) == 4

@pytest.mark.parametrize(
    "data,expected_index",
    [
        (1, 2),   # existing node
        (10, -1), # non‑existing node
        (-1, 0),  # head node
    ],
)
def test_find(populated_list, data, expected_index):
    assert populated_list.find(data) == expected_index

@pytest.mark.parametrize(
    "data,expected_result,expected_len",
    [
        (1, True, 3),   # delete existing middle node
        (10, False, 4), # attempt to delete non‑existing node
        (-1, True, 3),  # delete head node
    ],
)
def test_delete(populated_list, data, expected_result, expected_len):
    result = populated_list.delete(data)
    assert result is expected_result
    assert len(populated_list) == expected_len

@pytest.mark.parametrize(
    "index,expected",
    [
        (0, -1),  # first element
        (2, 1),   # third element
    ],
)
def test_get_success(populated_list, index, expected):
    assert populated_list.get(index) == expected

def test_get_error(populated_list):
    with pytest.raises(IndexError):
        populated_list.get(10)

def test_to_list_and_len(populated_list):
    assert populated_list.to_list() == [-1, 0, 1, 2]
    assert len(populated_list) == 4

import pytest
from data.input_code.d03_linked_list import *

def test_delete_tail(populated_list):
    result = populated_list.delete(2)  # tail node
    assert result is True
    assert len(populated_list) == 3
    assert populated_list.to_list() == [-1, 0, 1]

def test_get_last_index(populated_list):
    assert populated_list.get(3) == 2

def test_get_negative_index(populated_list):
    with pytest.raises(IndexError):
        populated_list.get(-1)

def test_empty_list_delete(empty_list):
    result = empty_list.delete(1)
    assert result is False
    assert len(empty_list) == 0

def test_empty_list_find(empty_list):
    assert empty_list.find(1) == -1

def test_empty_list_get(empty_list):
    with pytest.raises(IndexError):
        empty_list.get(0)

import pytest
from data.input_code.d03_linked_list import *

def test_delete_head_and_tail(populated_list):
    # Delete a middle node (0) and verify list updates correctly
    result = populated_list.delete(0)
    assert result is True
    assert len(populated_list) == 3
    assert populated_list.to_list() == [-1, 1, 2]

def test_get_after_delete(populated_list):
    # Delete tail (2) then get index 2, which should now be 1
    populated_list.delete(2)
    assert populated_list.get(2) == 1

def test_prepend_after_delete(populated_list):
    # Delete tail (2) then prepend a new value
    populated_list.delete(2)
    populated_list.prepend(10)
    assert populated_list.to_list() == [10, -1, 0, 1]
    assert len(populated_list) == 4

def test_append_after_delete(populated_list):
    # Delete head (-1) then append a new value
    populated_list.delete(-1)
    populated_list.append(10)
    assert populated_list.to_list() == [0, 1, 2, 10]
    assert len(populated_list) == 4

def test_find_after_delete(populated_list):
    # Delete head (-1) then find existing element 1
    populated_list.delete(-1)
    assert populated_list.find(1) == 1

def test_to_list_after_delete(populated_list):
    # Delete tail (2) and verify the list representation
    populated_list.delete(2)
    assert populated_list.to_list() == [-1, 0, 1]

def test_len_after_delete(populated_list):
    # Delete a middle node (0) and verify length
    populated_list.delete(0)
    assert len(populated_list) == 3