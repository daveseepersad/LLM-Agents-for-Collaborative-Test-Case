import pytest
from data.input_code.d03_linked_list import *

def test_T1_APPEND_EMPTY():
    ll = LinkedList()
    ll.append(10)

def test_T2_APPEND_NONEMPTY():
    ll = LinkedList()
    ll.append(1)
    ll.append(2)

def test_T3_PREPEND():
    ll = LinkedList()
    ll.append(5)
    ll.prepend(3)

def test_T4_DELETE_EMPTY():
    ll = LinkedList()
    assert ll.delete(1) is False

def test_T5_DELETE_HEAD():
    ll = LinkedList()
    ll.append(1)
    ll.append(2)
    assert ll.delete(1) is True

def test_T6_DELETE_MIDDLE():
    ll = LinkedList()
    ll.append(1)
    ll.append(2)
    ll.append(3)
    assert ll.delete(2) is True

def test_T7_DELETE_TAIL():
    ll = LinkedList()
    ll.append(1)
    ll.append(2)
    assert ll.delete(2) is True

def test_T8_DELETE_NOTFOUND():
    ll = LinkedList()
    ll.append(1)
    assert ll.delete(99) is False

def test_T9_FIND_EXISTING():
    ll = LinkedList()
    ll.append("a")
    ll.append("b")
    ll.append("c")
    assert ll.find("b") == 1

def test_T10_FIND_NOTFOUND():
    ll = LinkedList()
    ll.append("a")
    assert ll.find("z") == -1

def test_T11_GET_VALID():
    ll = LinkedList()
    ll.append(10)
    ll.append(20)
    ll.append(30)
    assert ll.get(2) == 30

def test_T12_GET_NEGATIVE_INDEX():
    ll = LinkedList()
    ll.append(1)
    with pytest.raises(IndexError):
        ll.get(-1)

def test_T13_GET_OUT_OF_RANGE():
    ll = LinkedList()
    ll.append(1)
    with pytest.raises(IndexError):
        ll.get(1)

def test_T14_TO_LIST():
    ll = LinkedList()
    ll.append(5)
    ll.prepend(3)
    ll.append(7)
    assert ll.to_list() == [3, 5, 7]

def test_T15_LEN():
    ll = LinkedList()
    ll.append(1)
    ll.append(2)
    ll.prepend(0)
    assert len(ll) == 3

def test_T16_DELETE_SINGLE_ELEMENT():
    ll = LinkedList()
    ll.append(42)
    result = ll.delete(42)
    assert result is True
    assert len(ll) == 0
    assert ll.head is None

def test_T17_DELETE_NOTFOUND_MULTIPLE():
    ll = LinkedList()
    ll.append(1)
    ll.append(2)
    ll.append(3)
    result = ll.delete(99)
    assert result is False
    assert len(ll) == 3
    assert ll.to_list() == [1, 2, 3]

def test_T18_DELETE_TAIL_LONGER():
    ll = LinkedList()
    ll.append(1)
    ll.append(2)
    ll.append(3)
    result = ll.delete(3)
    assert result is True
    assert len(ll) == 2
    assert ll.to_list() == [1, 2]

def test_T19_FIND_HEAD():
    ll = LinkedList()
    ll.append("first")
    ll.append("second")
    ll.append("third")
    assert ll.find("first") == 0

def test_T20_FIND_TAIL():
    ll = LinkedList()
    ll.append("first")
    ll.append("middle")
    ll.append("last")
    assert ll.find("last") == 2

def test_T21_TO_LIST_EMPTY():
    ll = LinkedList()
    assert ll.to_list() == []