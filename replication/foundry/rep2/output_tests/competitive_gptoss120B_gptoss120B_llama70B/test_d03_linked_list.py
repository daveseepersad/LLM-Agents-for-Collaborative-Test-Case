import pytest
from data.input_code.d03_linked_list import *

@pytest.fixture
def empty_list():
    return LinkedList()

@pytest.fixture
def single_item_list():
    lst = LinkedList()
    lst.append(1)
    return lst

@pytest.fixture
def populated_list():
    lst = LinkedList()
    lst.append(10)
    lst.append(20)
    lst.append(30)
    return lst

def test_append_empty(empty_list):
    empty_list.append(1)
    assert empty_list.head is not None
    assert empty_list.head.data == 1
    assert len(empty_list) == 1

def test_append_nonempty(single_item_list):
    single_item_list.append(2)
    # traverse to tail
    current = single_item_list.head
    while current.next:
        current = current.next
    assert current.data == 2
    assert len(single_item_list) == 2

def test_prepend(empty_list):
    empty_list.prepend(0)
    assert empty_list.head is not None
    assert empty_list.head.data == 0
    assert len(empty_list) == 1

@pytest.mark.parametrize(
    "initial, data, expected, new_head, new_size",
    [
        (LinkedList(), 99, False, None, 0),                     # delete from empty
        (LinkedList(), 1, True, None, 0),                       # placeholder, will be overridden in test
    ],
)
def test_delete_edge_cases(initial, data, expected, new_head, new_size):
    # This param set is only for the empty case; the non‑empty case is handled separately
    if expected is False and len(initial) == 0:
        assert initial.delete(data) is False
        assert len(initial) == 0
    else:
        # placeholder, not used
        pass

def test_delete_head(populated_list):
    result = populated_list.delete(10)
    assert result is True
    assert populated_list.head.data == 20
    assert len(populated_list) == 2

def test_delete_middle(populated_list):
    result = populated_list.delete(20)
    assert result is True
    # after deletion, list should be 10 -> 30
    assert populated_list.head.data == 10
    assert populated_list.head.next.data == 30
    assert len(populated_list) == 2

def test_delete_not_found(populated_list):
    result = populated_list.delete(42)
    assert result is False
    assert len(populated_list) == 3

@pytest.mark.parametrize(
    "setup, data, expected_index",
    [
        (LinkedList(), 5, -1),                     # empty list
        (LinkedList(), 10, 0),                     # head
        (LinkedList(), 30, 2),                     # tail
    ],
)
def test_find(setup, data, expected_index):
    # Build list for head/tail cases
    if expected_index != -1:
        setup.append(10)
        setup.append(20)
        setup.append(30)
    assert setup.find(data) == expected_index

@pytest.mark.parametrize(
    "lst, index, expected",
    [
        (LinkedList(), 0, None),   # will be set up inside test
        (LinkedList(), 2, None),
    ],
)
def test_get_valid(lst, index, expected):
    lst.append(10)
    lst.append(20)
    lst.append(30)
    assert lst.get(index) == (10 if index == 0 else 30)

@pytest.mark.parametrize(
    "lst, index, exc",
    [
        (LinkedList(), -1, IndexError),
        (LinkedList(), 3, IndexError),
    ],
)
def test_get_errors(lst, index, exc):
    lst.append(10)
    lst.append(20)
    lst.append(30)
    with pytest.raises(exc):
        lst.get(index)

def test_to_list_empty(empty_list):
    assert empty_list.to_list() == []

def test_to_list_nonempty(populated_list):
    assert populated_list.to_list() == [10, 20, 30]

def test_len(populated_list):
    assert len(populated_list) == 3