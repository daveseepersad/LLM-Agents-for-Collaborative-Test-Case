import pytest
from data.input_code.d03_linked_list import LinkedList

def test_append_and_to_list_and_len():
    ll = LinkedList()
    assert len(ll) == 0
    ll.append(1)
    assert ll.to_list() == [1]
    assert len(ll) == 1
    ll.append(2)
    assert ll.to_list() == [1, 2]
    assert len(ll) == 2

def test_prepend_and_to_list_and_len():
    ll = LinkedList()
    ll.prepend(1)
    assert ll.to_list() == [1]
    assert len(ll) == 1
    ll.prepend(2)
    assert ll.to_list() == [2, 1]
    assert len(ll) == 2

def test_delete_empty_list():
    ll = LinkedList()
    assert ll.delete(1) is False

def test_delete_head():
    ll = LinkedList()
    ll.append(1)
    ll.append(2)
    assert ll.delete(1) is True
    assert ll.to_list() == [2]
    assert len(ll) == 1

def test_delete_middle_and_tail():
    ll = LinkedList()
    ll.append(1)
    ll.append(2)
    ll.append(3)
    assert ll.delete(2) is True
    assert ll.to_list() == [1, 3]
    assert len(ll) == 2
    assert ll.delete(3) is True
    assert ll.to_list() == [1]
    assert len(ll) == 1

def test_delete_nonexistent():
    ll = LinkedList()
    ll.append(1)
    assert ll.delete(99) is False

def test_find_existing_and_nonexisting():
    ll = LinkedList()
    ll.append('a')
    ll.append('b')
    ll.append('c')
    assert ll.find('a') == 0
    assert ll.find('b') == 1
    assert ll.find('c') == 2
    assert ll.find('x') == -1

def test_get_valid_indices():
    ll = LinkedList()
    ll.append(10)
    ll.append(20)
    ll.append(30)
    assert ll.get(0) == 10
    assert ll.get(1) == 20
    assert ll.get(2) == 30

def test_get_invalid_indices():
    ll = LinkedList()
    ll.append(1)
    with pytest.raises(IndexError):
        ll.get(-1)
    with pytest.raises(IndexError):
        ll.get(1)

def test_to_list_empty():
    ll = LinkedList()
    assert ll.to_list() == []

def test_len_empty_and_after_operations():
    ll = LinkedList()
    assert len(ll) == 0
    ll.append(1)
    assert len(ll) == 1
    ll.prepend(2)
    assert len(ll) == 2
    ll.delete(1)
    assert len(ll) == 1
    ll.delete(2)
    assert len(ll) == 0