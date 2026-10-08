import pytest
from data.input_code.d03_linked_list import Node, LinkedList

def test_append():
    ll = LinkedList()
    ll.append(1)
    assert ll.to_list() == [1]
    ll.append(2)
    assert ll.to_list() == [1, 2]
    assert len(ll) == 2

def test_prepend():
    ll = LinkedList()
    ll.prepend(1)
    assert ll.to_list() == [1]
    ll.prepend(0)
    assert ll.to_list() == [0, 1]
    assert len(ll) == 2

def test_delete():
    ll = LinkedList()
    ll.append(1)
    ll.append(2)
    assert ll.delete(1)
    assert ll.to_list() == [2]
    assert not ll.delete(3)
    assert ll.to_list() == [2]
    assert ll.delete(2)
    assert ll.to_list() == []
    assert len(ll) == 0

def test_find():
    ll = LinkedList()
    ll.append(1)
    ll.append(2)
    assert ll.find(1) == 0
    assert ll.find(2) == 1
    assert ll.find(3) == -1

def test_get():
    ll = LinkedList()
    ll.append(1)
    ll.append(2)
    assert ll.get(0) == 1
    assert ll.get(1) == 2
    with pytest.raises(IndexError):
        ll.get(2)
    with pytest.raises(IndexError):
        ll.get(-1)

def test_to_list():
    ll = LinkedList()
    ll.append(1)
    ll.append(2)
    assert ll.to_list() == [1, 2]
    ll.prepend(0)
    assert ll.to_list() == [0, 1, 2]

def test_len():
    ll = LinkedList()
    assert len(ll) == 0
    ll.append(1)
    assert len(ll) == 1
    ll.append(2)
    assert len(ll) == 2
    ll.delete(1)
    assert len(ll) == 1