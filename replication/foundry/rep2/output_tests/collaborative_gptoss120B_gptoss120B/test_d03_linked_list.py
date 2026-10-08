import pytest
from data.input_code.d03_linked_list import *

@pytest.fixture
def empty_list():
    return LinkedList()

@pytest.fixture
def three_elem_list():
    lst = LinkedList()
    lst.append(1)
    lst.append(2)
    lst.append(3)
    return lst

def test_append_empty(empty_list):
    empty_list.append(1)
    assert empty_list.head is not None
    assert empty_list.head.data == 1
    assert len(empty_list) == 1

def test_append_nonempty(three_elem_list):
    three_elem_list.append(4)
    # traverse to tail
    current = three_elem_list.head
    while current.next:
        current = current.next
    assert current.data == 4
    assert len(three_elem_list) == 4

def test_prepend(three_elem_list):
    three_elem_list.prepend(0)
    assert three_elem_list.head.data == 0
    assert len(three_elem_list) == 4
    # ensure order is preserved after prepend
    assert three_elem_list.to_list() == [0, 1, 2, 3]

def test_delete_empty(empty_list):
    assert empty_list.delete(10) is False
    assert len(empty_list) == 0

@pytest.mark.parametrize(
    "initial, target, expected_head, expected_len, expected_list",
    [
        ([1, 2, 3], 1, 2, 2, [2, 3]),  # delete head
        ([1, 2, 3], 2, 1, 2, [1, 3]),  # delete middle
    ],
)
def test_delete_success(initial, target, expected_head, expected_len, expected_list):
    lst = LinkedList()
    for val in initial:
        lst.append(val)
    assert lst.delete(target) is True
    assert lst.head.data == expected_head
    assert len(lst) == expected_len
    assert lst.to_list() == expected_list

def test_delete_notfound(three_elem_list):
    original = three_elem_list.to_list()
    assert three_elem_list.delete(99) is False
    assert len(three_elem_list) == 3
    assert three_elem_list.to_list() == original

@pytest.mark.parametrize(
    "initial, target, expected",
    [
        ([], 5, -1),                # empty list
        ([1, 2, 3], 2, 1),          # found in middle
        ([1, 2, 3], 99, -1),        # not found
    ],
)
def test_find(initial, target, expected):
    lst = LinkedList()
    for val in initial:
        lst.append(val)
    assert lst.find(target) == expected

@pytest.mark.parametrize(
    "initial, index, expected",
    [
        ([1, 2, 3], 0, 1),
        ([1, 2, 3], 2, 3),
    ],
)
def test_get_success(initial, index, expected):
    lst = LinkedList()
    for val in initial:
        lst.append(val)
    assert lst.get(index) == expected

@pytest.mark.parametrize(
    "initial, index, exc",
    [
        ([], -1, IndexError),
        ([1, 2, 3], -1, IndexError),
        ([1, 2, 3], 3, IndexError),
    ],
)
def test_get_errors(initial, index, exc):
    lst = LinkedList()
    for val in initial:
        lst.append(val)
    with pytest.raises(exc):
        lst.get(index)

def test_to_list_empty(empty_list):
    assert empty_list.to_list() == []

def test_to_list_nonempty(three_elem_list):
    assert three_elem_list.to_list() == [1, 2, 3]

def test_len(three_elem_list):
    assert len(three_elem_list) == 3