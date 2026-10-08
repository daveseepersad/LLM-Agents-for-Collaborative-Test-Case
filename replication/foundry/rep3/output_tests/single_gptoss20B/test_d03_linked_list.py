import pytest
from data.input_code.d03_linked_list import LinkedList

def test_empty_list_behaviors():
    ll = LinkedList()
    assert len(ll) == 0
    assert ll.to_list() == []
    assert ll.delete(1) is False
    assert ll.find(1) == -1
    with pytest.raises(IndexError):
        ll.get(0)
    with pytest.raises(IndexError):
        ll.get(-1)

def test_append_and_get_to_list_and_bounds():
    ll = LinkedList()
    ll.append('a')
    ll.append('b')
    ll.append('c')
    assert ll.to_list() == ['a', 'b', 'c']
    assert len(ll) == 3
    assert ll.get(0) == 'a'
    assert ll.get(1) == 'b'
    assert ll.get(2) == 'c'
    with pytest.raises(IndexError):
        ll.get(3)
    with pytest.raises(IndexError):
        ll.get(-1)

def test_delete_middle_path_and_rest():
    ll = LinkedList()
    ll.append(1)
    ll.append(2)
    ll.append(3)
    # delete middle element 2 (not head)
    assert ll.delete(2) is True
    assert ll.to_list() == [1, 3]
    assert len(ll) == 2
    # delete head
    assert ll.delete(1) is True
    assert ll.to_list() == [3]
    assert len(ll) == 1
    # delete tail
    assert ll.delete(3) is True
    assert ll.to_list() == []
    assert len(ll) == 0
    # deleting non-existing on empty
    assert ll.delete(99) is False

def test_find_present_and_absent():
    ll = LinkedList()
    ll.append(9)
    ll.append(8)
    ll.append(7)
    assert ll.find(8) == 1
    assert ll.find(5) == -1

def test_get_boundaries():
    ll = LinkedList()
    ll.append(100)
    assert ll.get(0) == 100
    with pytest.raises(IndexError):
        ll.get(1)
    with pytest.raises(IndexError):
        ll.get(-1)