import pytest
from data.input_code.d03_linked_list import *

def test_T1_INIT():
    ll = LinkedList()
    assert ll.head is None
    assert ll._size == 0

def test_T2_APPEND_EMPTY():
    ll = LinkedList()
    result = ll.append(5)
    assert result is None
    assert ll.head is not None and ll.head.data == 5
    assert ll._size == 1

def test_T3_APPEND_NONEMPTY():
    ll = LinkedList()
    # precondition: LinkedList with head data 5, _size 1
    ll.head = Node(5)
    ll._size = 1
    result = ll.append(10)
    assert result is None
    assert ll.head.data == 5
    assert ll.head.next is not None
    assert ll.head.next.data == 10
    assert ll._size == 2

def test_T4_PREPEND_EMPTY():
    ll = LinkedList()
    result = ll.prepend(5)
    assert result is None
    assert ll.head is not None
    assert ll.head.data == 5
    assert ll.head.next is None
    assert ll._size == 1

def test_T5_PREPEND_NONEMPTY():
    ll = LinkedList()
    # precondition: LinkedList with head data 5, _size 1
    ll.head = Node(5)
    ll._size = 1
    result = ll.prepend(10)
    assert result is None
    assert ll.head.data == 10
    assert ll.head.next is not None
    assert ll.head.next.data == 5
    assert ll._size == 2

def test_T6_DELETE_EMPTY():
    ll = LinkedList()
    result = ll.delete(5)
    assert result is False

def test_T7_DELETE_HEAD():
    ll = LinkedList()
    # precondition: head 5, _size 1
    ll.head = Node(5)
    ll._size = 1
    result = ll.delete(5)
    assert result is True
    assert ll.head is None
    assert ll._size == 0

def test_T8_DELETE_MIDDLE():
    ll = LinkedList()
    # precondition: 5 -> 10 -> 15, _size 3
    n1 = Node(5)
    n2 = Node(10)
    n3 = Node(15)
    n1.next = n2
    n2.next = n3
    ll.head = n1
    ll._size = 3
    result = ll.delete(10)
    assert result is True
    assert ll.head.data == 5
    assert ll.head.next is not None
    assert ll.head.next.data == 15
    assert ll.head.next.next is None
    assert ll._size == 2

def test_T9_DELETE_NOTFOUND():
    ll = LinkedList()
    # precondition: 5 -> None, _size 1
    ll.head = Node(5)
    ll._size = 1
    result = ll.delete(20)
    assert result is False
    assert ll.head is not None
    assert ll.head.data == 5
    assert ll._size == 1

def test_T10_FIND_EMPTY():
    ll = LinkedList()
    assert ll.find(5) == -1

def test_T11_FIND_FOUND():
    ll = LinkedList()
    # precondition: 5 -> 10, _size 2
    ll.head = Node(5)
    ll.head.next = Node(10)
    ll._size = 2
    assert ll.find(10) == 1

def test_T12_FIND_NOTFOUND():
    ll = LinkedList()
    # precondition: 5 -> None, _size 1
    ll.head = Node(5)
    ll._size = 1
    assert ll.find(15) == -1

def test_T13_GET_VALID():
    ll = LinkedList()
    # precondition: 5 -> 10, _size 2
    ll.head = Node(5)
    ll.head.next = Node(10)
    ll._size = 2
    assert ll.get(1) == 10

def test_T14_GET_OOB_LOW():
    ll = LinkedList()
    with pytest.raises(IndexError):
        ll.get(-1)

def test_T15_GET_OOB_HIGH():
    ll = LinkedList()
    # precondition: 5 -> 10, _size 2
    ll.head = Node(5)
    ll.head.next = Node(10)
    ll._size = 2
    with pytest.raises(IndexError):
        ll.get(2)

def test_T16_TOLIST_EMPTY():
    ll = LinkedList()
    assert ll.to_list() == []

def test_T17_TOLIST_NONEMPTY():
    ll = LinkedList()
    # precondition: 5 -> 10, _size 2
    ll.head = Node(5)
    ll.head.next = Node(10)
    ll._size = 2
    assert ll.to_list() == [5, 10]

def test_T18_LEN_EMPTY():
    ll = LinkedList()
    assert len(ll) == 0

def test_T19_LEN_NONEMPTY():
    ll = LinkedList()
    # precondition: 5 -> 10, _size 2
    ll.head = Node(5)
    ll.head.next = Node(10)
    ll._size = 2
    assert len(ll) == 2

def test_T_MISSING_DELETE_LAST():
    ll = LinkedList()
    # precondition: 5 -> 10, _size 2
    ll.head = Node(5)
    ll.head.next = Node(10)
    ll._size = 2
    result = ll.delete(10)
    assert result is True
    assert ll.head.data == 5
    assert ll.head.next is None
    assert ll._size == 1

def test_T_MISSING_GET_EDGE():
    ll = LinkedList()
    # precondition: 5 -> 10, _size 2
    ll.head = Node(5)
    ll.head.next = Node(10)
    ll._size = 2
    assert ll.get(0) == 5

def test_T_MISSING_APPEND_MULTIPLE():
    ll = LinkedList()
    ll.append(5)
    ll.append(10)
    result = ll.append(15)
    assert result is None
    assert ll.to_list() == [5, 10, 15]
    assert len(ll) == 3

def test_T_MISSING_PREPEND_MULTIPLE():
    ll = LinkedList()
    ll.prepend(5)        # list: 5
    ll.prepend(10)       # list: 10 -> 5
    result = ll.prepend(15)  # list: 15 -> 10 -> 5
    assert result is None
    assert ll.to_list() == [15, 10, 5]
    assert len(ll) == 3

def test_T_MISSING_FIND_HEAD():
    ll = LinkedList()
    ll.head = Node(5)
    ll._size = 1
    assert ll.find(5) == 0

def test_T_MISSING_LEN_APPEND():
    ll = LinkedList()
    ll.append(5)
    ll.append(10)
    ll.append(15)
    assert len(ll) == 3

def test_T_MISSING_1_DELETE_SINGLE_ELEMENT():
    ll = LinkedList()
    ll.append(5)
    result = ll.delete(5)
    assert result is True
    assert ll.head is None
    assert ll._size == 0

def test_T_MISSING_2_GET_ON_EMPTY_RAISES():
    ll = LinkedList()
    with pytest.raises(IndexError):
        ll.get(0)

def test_T_MISSING_3_LEN_AFTER_PREPENDS():
    ll = LinkedList()
    ll.prepend(1)
    ll.prepend(2)
    ll.prepend(3)
    assert len(ll) == 3

import pytest
from data.input_code.d03_linked_list import *

def test_T_MISSING_4_DELETE_NOT_FOUND_MULTIPLE():
    ll = LinkedList()
    # precondition: 5 -> 10 -> 15
    n1 = Node(5)
    n2 = Node(10)
    n3 = Node(15)
    n1.next = n2
    n2.next = n3
    ll.head = n1
    ll._size = 3

    result = ll.delete(20)
    assert result is False
    assert ll.to_list() == [5, 10, 15]
    assert len(ll) == 3

def test_T_MISSING_5_FIND_ON_MULTIPLE():
    ll = LinkedList()
    # precondition: 5 -> 10 -> 15
    n1 = Node(5)
    n2 = Node(10)
    n3 = Node(15)
    n1.next = n2
    n2.next = n3
    ll.head = n1
    ll._size = 3

    assert ll.find(15) == 2

def test_T_MISSING_6_TOLIST_ON_MULTIPLE():
    ll = LinkedList()
    # precondition: 5 -> 10 -> 15
    n1 = Node(5)
    n2 = Node(10)
    n3 = Node(15)
    n1.next = n2
    n2.next = n3
    ll.head = n1
    ll._size = 3

    assert ll.to_list() == [5, 10, 15]

def test_T_MISSING_7_LEN_AFTER_APPEND_AND_DELETE():
    ll = LinkedList()
    ll.append(5)
    ll.append(10)
    ll.append(15)
    ll.delete(10)
    assert len(ll) == 2