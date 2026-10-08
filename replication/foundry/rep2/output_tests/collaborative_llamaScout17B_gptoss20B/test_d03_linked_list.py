import pytest
from data.input_code.d03_linked_list import *

def test_T1_INIT():
    ll = LinkedList()
    assert ll.head is None
    assert ll._size == 0

def test_T2_APPEND_EMPTY():
    ll = LinkedList()
    ll.append(5)
    assert ll.head is not None and ll.head.data == 5
    assert ll._size == 1

def test_T3_APPEND_NONEMPTY():
    ll = LinkedList()
    ll.append(5)
    ll.append(10)
    assert ll._size == 2
    assert ll.to_list() == [5, 10]

def test_T4_PREPEND_EMPTY():
    ll = LinkedList()
    ll.prepend(5)
    assert ll.head is not None and ll.head.data == 5
    assert ll._size == 1

def test_T5_PREPEND_NONEMPTY():
    ll = LinkedList()
    ll.append(5)
    ll.prepend(10)
    assert ll.to_list() == [10, 5]
    assert ll._size == 2

def test_T6_DELETE_EMPTY():
    ll = LinkedList()
    assert ll.delete(5) is False
    assert ll._size == 0
    assert ll.to_list() == []

def test_T7_DELETE_HEAD():
    ll = LinkedList()
    ll.prepend(5)
    assert ll.delete(5) is True
    assert ll.head is None
    assert ll._size == 0

def test_T8_DELETE_MIDDLE():
    ll = LinkedList()
    ll.append(5)
    ll.append(10)
    ll.append(15)
    assert ll.delete(10) is True
    assert ll.to_list() == [5, 15]
    assert ll._size == 2

def test_T9_DELETE_TAIL():
    ll = LinkedList()
    ll.append(5)
    ll.append(10)
    ll.append(15)
    assert ll.delete(15) is True
    assert ll.to_list() == [5, 10]
    assert ll._size == 2

def test_T10_DELETE_NOTFOUND():
    ll = LinkedList()
    ll.append(5)
    ll.append(10)
    ll.append(15)
    assert ll.delete(20) is False
    assert ll.to_list() == [5, 10, 15]
    assert ll._size == 3

def test_T11_FIND_EMPTY():
    ll = LinkedList()
    assert ll.find(5) == -1

def test_T12_FIND_HEAD():
    ll = LinkedList()
    ll.append(5)
    assert ll.find(5) == 0

def test_T13_FIND_MIDDLE():
    ll = LinkedList()
    ll.append(5)
    ll.append(10)
    ll.append(15)
    assert ll.find(10) == 1

def test_T14_FIND_TAIL():
    ll = LinkedList()
    ll.append(5)
    ll.append(10)
    ll.append(15)
    assert ll.find(15) == 2

def test_T15_FIND_NOTFOUND():
    ll = LinkedList()
    ll.append(5)
    ll.append(10)
    ll.append(15)
    assert ll.find(20) == -1

def test_T16_GET_VALID():
    ll = LinkedList()
    ll.append(5)
    ll.append(10)
    ll.append(15)
    assert ll.get(1) == 10

def test_T17_GET_OUTOFRANGE_LOW():
    ll = LinkedList()
    ll.append(5)
    ll.append(10)
    ll.append(15)
    with pytest.raises(IndexError):
        ll.get(-1)

def test_T18_GET_OUTOFRANGE_HIGH():
    ll = LinkedList()
    ll.append(5)
    ll.append(10)
    ll.append(15)
    with pytest.raises(IndexError):
        ll.get(3)

def test_T19_TO_LIST_EMPTY():
    ll = LinkedList()
    assert ll.to_list() == []

def test_T20_TO_LIST_NONEMPTY():
    ll = LinkedList()
    ll.append(5)
    ll.append(10)
    ll.append(15)
    assert ll.to_list() == [5, 10, 15]

def test_T21_LEN_EMPTY():
    ll = LinkedList()
    assert len(ll) == 0

def test_T22_LEN_NONEMPTY():
    ll = LinkedList()
    ll.append(5)
    ll.append(10)
    ll.append(15)
    assert len(ll) == 3