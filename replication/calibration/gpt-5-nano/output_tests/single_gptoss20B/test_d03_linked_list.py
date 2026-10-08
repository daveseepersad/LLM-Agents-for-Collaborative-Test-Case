import pytest
from data.input_code.d03_linked_list import LinkedList

def test_append_prepend_to_list_len():
    ll = LinkedList()
    ll.append(1)
    ll.append(2)
    ll.append(3)
    assert ll.to_list() == [1, 2, 3]
    assert len(ll) == 3
    ll.prepend(0)
    assert ll.to_list() == [0, 1, 2, 3]
    assert len(ll) == 4

def test_delete_head_middle_tail_and_empty():
    ll = LinkedList()
    assert ll.delete(5) is False  # delete on empty list
    ll.append('a')
    ll.append('b')
    ll.append('c')
    assert ll.delete('a') is True  # delete head
    assert ll.to_list() == ['b', 'c']
    assert len(ll) == 2
    assert ll.delete('c') is True  # delete tail
    assert ll.to_list() == ['b']
    assert len(ll) == 1
    assert ll.delete('x') is False  # non-existent

def test_find_get_and_exceptions():
    ll = LinkedList()
    ll.append(5)
    ll.append(10)
    ll.append(15)
    assert ll.find(10) == 1
    assert ll.find(20) == -1
    assert ll.get(0) == 5
    assert ll.get(2) == 15
    with pytest.raises(IndexError):
        ll.get(-1)
    with pytest.raises(IndexError):
        ll.get(3)