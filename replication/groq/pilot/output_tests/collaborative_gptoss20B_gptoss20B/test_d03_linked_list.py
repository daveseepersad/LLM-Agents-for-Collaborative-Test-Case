import pytest
from data.input_code.d03_linked_list import *

def test_append_empty():
    ll = LinkedList()
    ll.append(10)
    assert ll.head.data == 10
    assert len(ll) == 1
    assert ll.to_list() == [10]

def test_append_nonempty():
    ll = LinkedList()
    ll.append(10)
    ll.append(20)
    assert ll.head.data == 10
    assert len(ll) == 2
    assert ll.to_list() == [10, 20]

def test_prepend_empty():
    ll = LinkedList()
    ll.prepend(None)
    assert ll.head.data is None
    assert len(ll) == 1
    assert ll.to_list() == [None]

def test_prepend_nonempty():
    ll = LinkedList()
    ll.prepend(None)
    ll.prepend("a")
    assert ll.head.data == "a"
    assert len(ll) == 2
    assert ll.to_list() == ["a", None]

def test_delete_empty():
    ll = LinkedList()
    assert ll.delete(5) is False

def test_delete_head():
    ll = LinkedList()
    ll.append(10)
    assert ll.delete(10) is True
    assert len(ll) == 0
    assert ll.to_list() == []

def test_delete_middle():
    ll = LinkedList()
    ll.append(10)
    ll.append(20)
    ll.append(30)
    assert ll.delete(20) is True
    assert len(ll) == 2
    assert ll.to_list() == [10, 30]

def test_delete_notfound():
    ll = LinkedList()
    ll.append(10)
    ll.append(20)
    assert ll.delete(99) is False

def test_find_found():
    ll = LinkedList()
    ll.append(10)
    ll.append(20)
    ll.append(30)
    assert ll.find(20) == 1

def test_find_notfound():
    ll = LinkedList()
    ll.append(10)
    ll.append(20)
    assert ll.find(99) == -1

def test_get_valid():
    ll = LinkedList()
    ll.append(10)
    ll.append(20)
    assert ll.get(1) == 20

def test_get_negative():
    ll = LinkedList()
    ll.append(10)
    with pytest.raises(IndexError):
        ll.get(-1)

def test_get_outofrange():
    ll = LinkedList()
    ll.append(10)
    with pytest.raises(IndexError):
        ll.get(1)

def test_to_list_empty():
    ll = LinkedList()
    assert ll.to_list() == []

def test_to_list_nonempty():
    ll = LinkedList()
    ll.append(10)
    assert ll.to_list() == [10]

def test_len():
    ll = LinkedList()
    ll.append(10)
    ll.append(20)
    assert len(ll) == 2