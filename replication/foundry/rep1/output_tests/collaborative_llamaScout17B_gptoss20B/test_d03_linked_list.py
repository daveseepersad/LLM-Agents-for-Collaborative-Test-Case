import pytest
from data.input_code.d03_linked_list import *

def dict_from_node(n):
    if n is None:
        return None
    return {'data': n.data, 'next': dict_from_node(n.next)}

def test_T1_INIT():
    ll = LinkedList()
    assert ll.head is None
    assert ll._size == 0

def test_T2_APPEND_EMPTY():
    ll = LinkedList()
    ll.append(5)
    assert ll._size == 1
    assert ll.head is not None
    assert ll.head.data == 5
    assert ll.head.next is None
    assert dict_from_node(ll.head) == {'data': 5, 'next': None}

def test_T3_APPEND_NONEMPTY():
    ll = LinkedList()
    ll.head = Node(1)
    ll._size = 1
    ll.append(2)
    assert ll._size == 2
    assert ll.head.data == 1
    assert ll.head.next is not None
    assert ll.head.next.data == 2
    assert ll.head.next.next is None
    assert dict_from_node(ll.head) == {'data': 1, 'next': {'data': 2, 'next': None}}

def test_T4_PREPEND_EMPTY():
    ll = LinkedList()
    ll.prepend(5)
    assert ll._size == 1
    assert ll.head is not None
    assert ll.head.data == 5
    assert ll.head.next is None
    assert dict_from_node(ll.head) == {'data': 5, 'next': None}

def test_T5_PREPEND_NONEMPTY():
    ll = LinkedList()
    ll.head = Node(1)
    ll._size = 1
    ll.prepend(2)
    assert ll._size == 2
    assert ll.head.data == 2
    assert ll.head.next is not None
    assert ll.head.next.data == 1
    assert ll.head.next.next is None
    assert dict_from_node(ll.head) == {'data': 2, 'next': {'data': 1, 'next': None}}

def test_T6_DELETE_EMPTY():
    ll = LinkedList()
    assert ll.delete(5) is False

def test_T7_DELETE_HEAD():
    ll = LinkedList()
    ll.head = Node(1)
    ll._size = 1
    assert ll.delete(1) is True
    assert ll.head is None
    assert ll._size == 0

def test_T8_DELETE_NONHEAD():
    ll = LinkedList()
    ll.head = Node(1)
    ll.head.next = Node(2)
    ll._size = 2
    assert ll.delete(2) is True
    assert ll.head.data == 1
    assert ll.head.next is None
    assert ll._size == 1

def test_T9_DELETE_MISSING():
    ll = LinkedList()
    ll.head = Node(1)
    ll._size = 1
    assert ll.delete(2) is False
    assert ll.head.data == 1
    assert ll.head.next is None
    assert ll._size == 1

def test_T10_FIND_PRESENT():
    ll = LinkedList()
    ll.head = Node(1)
    ll.head.next = Node(2)
    ll._size = 2
    assert ll.find(2) == 1

def test_T11_FIND_MISSING():
    ll = LinkedList()
    ll.head = Node(1)
    ll._size = 1
    assert ll.find(2) == -1

def test_T12_GET_VALID():
    ll = LinkedList()
    ll.head = Node(1)
    ll.head.next = Node(2)
    ll._size = 2
    assert ll.get(1) == 2

@pytest.mark.parametrize("idx", [-1, 1])
def test_T13_T14_GET_INVALID(idx):
    ll = LinkedList()
    ll.head = Node(1)
    ll._size = 1
    with pytest.raises(IndexError):
        ll.get(idx)

def test_T15_TOLIST_EMPTY():
    ll = LinkedList()
    assert ll.to_list() == []

def test_T16_TOLIST_NONEMPTY():
    ll = LinkedList()
    ll.head = Node(1)
    ll.head.next = Node(2)
    ll._size = 2
    assert ll.to_list() == [1, 2]

def test_T17_LEN_EMPTY():
    ll = LinkedList()
    assert len(ll) == 0

def test_T18_LEN_NONEMPTY():
    ll = LinkedList()
    ll.head = Node(1)
    ll._size = 1
    assert len(ll) == 1

import pytest
from data.input_code.d03_linked_list import *

def test_T_MISSING_DELETE_MULTIPLE():
    ll = LinkedList()
    ll.head = Node(1)
    ll.head.next = Node(2)
    ll.head.next.next = Node(2)
    ll.head.next.next.next = Node(3)
    ll._size = 4
    res = ll.delete(2)
    assert res is True
    assert ll._size == 3
    assert ll.find(2) == 1
    assert ll.to_list() == [1, 2, 3]

def test_T_MISSING_GET_EDGE():
    ll = LinkedList()
    ll.head = Node(1)
    ll._size = 1
    assert ll.get(0) == 1

def test_T_MISSING_APPEND_MULTIPLE():
    ll = LinkedList()
    ll.head = Node(1)
    ll.head.next = Node(2)
    ll._size = 2
    ll.append(3)
    assert ll.to_list() == [1, 2, 3]
    assert ll._size == 3

def test_T_MISSING_PREPEND_MULTIPLE():
    ll = LinkedList()
    ll.head = Node(1)
    ll.head.next = Node(2)
    ll._size = 2
    ll.prepend(3)
    assert ll.to_list() == [3, 1, 2]
    assert ll._size == 3

def test_T_MISSING_FIND_HEAD():
    ll = LinkedList()
    ll.head = Node(1)
    ll.head.next = Node(2)
    ll.head.next.next = Node(3)
    ll._size = 3
    assert ll.find(1) == 0

def test_T_MISSING_TOLIST_MULTIPLE():
    ll = LinkedList()
    ll.head = Node(1)
    ll.head.next = Node(2)
    ll.head.next.next = Node(3)
    ll._size = 3
    assert ll.to_list() == [1, 2, 3]

def test_T_MISSING_LEN_MULTIPLE():
    ll = LinkedList()
    ll.head = Node(1)
    ll.head.next = Node(2)
    ll.head.next.next = Node(3)
    ll._size = 3
    assert len(ll) == 3

import pytest
from data.input_code.d03_linked_list import *

def test_T_MISSING_1_DELETE_MULTIPLE_OCCURRENCES():
    ll = LinkedList()
    ll.head = Node(1)
    ll.head.next = Node(2)
    ll.head.next.next = Node(2)
    ll.head.next.next.next = Node(3)
    ll._size = 4
    res = ll.delete(2)
    assert res is True
    assert ll._size == 3
    assert ll.find(2) == 1
    assert ll.to_list() == [1, 2, 3]

def test_T_MISSING_2_FIND_ON_EMPTY():
    ll = LinkedList()
    assert ll.find(1) == -1

def test_T_MISSING_3_GET_AT_ZERO():
    ll = LinkedList()
    ll.head = Node(1)
    ll.head.next = Node(2)
    ll._size = 2
    assert ll.get(0) == 1

def test_T_MISSING_4_PREPEND_MULTIPLE():
    ll = LinkedList()
    ll.head = Node(1)
    ll.head.next = Node(2)
    ll._size = 2
    res = ll.prepend(0)
    assert res is None
    assert ll.to_list() == [0, 1, 2]
    assert ll._size == 3

def test_T_MISSING_5_APPEND_ON_EMPTY():
    ll = LinkedList()
    res = ll.append(5)
    assert res is None
    assert ll._size == 1
    assert ll.head is not None
    assert ll.head.data == 5
    assert ll.head.next is None
    assert ll.to_list() == [5]

def test_T_MISSING_6_LEN_AFTER_OPERATIONS():
    ll = LinkedList()
    ll.append(1)
    ll.append(2)
    ll.delete(1)
    ll.delete(2)
    assert len(ll) == 0

import pytest
from data.input_code.d03_linked_list import *

def test_T_MISSING_7_DELETE_NOT_PRESENT():
    ll = LinkedList()
    ll.head = Node(1)
    ll.head.next = Node(2)
    ll.head.next.next = Node(3)
    ll._size = 3
    res = ll.delete(4)
    assert res is False
    assert ll.to_list() == [1, 2, 3]
    assert ll._size == 3

def test_T_MISSING_8_FIND_LAST():
    ll = LinkedList()
    ll.head = Node(1)
    ll.head.next = Node(2)
    ll.head.next.next = Node(3)
    ll._size = 3
    assert ll.find(3) == 2

def test_T_MISSING_9_GET_LAST():
    ll = LinkedList()
    ll.head = Node(1)
    ll.head.next = Node(2)
    ll.head.next.next = Node(3)
    ll._size = 3
    assert ll.get(2) == 3

def test_T_MISSING_10_TOLIST_SINGLE():
    ll = LinkedList()
    ll.head = Node(1)
    ll._size = 1
    assert ll.to_list() == [1]

def test_T_MISSING_11_LEN_AFTER_APPEND_THREE():
    ll = LinkedList()
    ll.append(1)
    ll.append(2)
    ll.append(3)
    assert len(ll) == 3