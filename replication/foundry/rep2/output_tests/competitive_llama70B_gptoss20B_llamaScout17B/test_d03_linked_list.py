import pytest
from data.input_code.d03_linked_list import *

@pytest.mark.parametrize('input, expected', [
    ({}, None)
])
def test_LinkedList_init(input, expected):
    linked_list = LinkedList()
    assert linked_list.head is None
    assert linked_list._size == 0

def test_LinkedList_append():
    linked_list = LinkedList()
    linked_list.append(1)
    assert linked_list.head.data == 1
    linked_list.append(2)
    assert linked_list.head.next.data == 2

def test_LinkedList_prepend():
    linked_list = LinkedList()
    linked_list.prepend(0)
    assert linked_list.head.data == 0
    linked_list.prepend(-1)
    assert linked_list.head.data == -1

@pytest.mark.parametrize('data, expected', [
    (1, True),
    (10, False)
])
def test_LinkedList_delete(data, expected):
    linked_list = LinkedList()
    linked_list.append(1)
    linked_list.append(2)
    assert linked_list.delete(data) == expected

@pytest.mark.parametrize('data, expected', [
    (-1, 0),
    (1, 2),
    (10, -1)
])
def test_LinkedList_find(data, expected):
    linked_list = LinkedList()
    linked_list.append(-1)
    linked_list.append(0)
    linked_list.append(1)
    linked_list.append(2)
    assert linked_list.find(data) == expected

@pytest.mark.parametrize('index, expected', [
    (0, -1),
    (1, 0),
    (2, 1),
    (3, 2),
    (-1, 'IndexError'),
    (10, 'IndexError')
])
def test_LinkedList_get(index, expected):
    linked_list = LinkedList()
    linked_list.append(-1)
    linked_list.append(0)
    linked_list.append(1)
    linked_list.append(2)
    if isinstance(expected, str) and expected == 'IndexError':
        with pytest.raises(IndexError):
            linked_list.get(index)
    else:
        assert linked_list.get(index) == expected

def test_LinkedList_to_list():
    linked_list = LinkedList()
    linked_list.append(-1)
    linked_list.append(0)
    linked_list.append(1)
    linked_list.append(2)
    assert linked_list.to_list() == [-1, 0, 1, 2]

def test_LinkedList_len():
    linked_list = LinkedList()
    linked_list.append(-1)
    linked_list.append(0)
    linked_list.append(1)
    linked_list.append(2)
    assert len(linked_list) == 4

import pytest
from data.input_code.d03_linked_list import *

def test_T_MISSING_EMPTY_DELETE():
    ll = LinkedList()
    assert ll.delete(1) is False

def test_T_MISSING_EMPTY_FIND():
    ll = LinkedList()
    assert ll.find(1) == -1

def test_T_MISSING_EMPTY_GET():
    ll = LinkedList()
    with pytest.raises(IndexError):
        ll.get(0)

def test_T_MISSING_PREPEND_DELETE():
    ll = LinkedList()
    ll.prepend(-1)
    assert ll.delete(-1) is True

def test_T_MISSING_APPEND_PREPEND_FIND():
    ll = LinkedList()
    ll.append(1)
    ll.append(0)
    assert ll.find(0) == 1

def test_T_MISSING_DELETE_GET():
    ll = LinkedList()
    ll.append(0)
    ll.append(1)
    ll.delete(1)
    assert ll.get(0) == 0

def test_T_MISSING_EDGE_CASE_TO_LIST():
    ll = LinkedList()
    assert ll.to_list() == []

def test_T_MISSING_EDGE_CASE_LEN():
    ll = LinkedList()
    assert len(ll) == 0