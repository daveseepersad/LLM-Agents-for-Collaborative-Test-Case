import pytest
from data.input_code.d03_linked_list import Node, LinkedList

def test_append_and_len_and_to_list():
    ll = LinkedList()
    assert len(ll) == 0
    assert ll.to_list() == []
    ll.append(1)  # head was None branch
    ll.append(2)  # traverses while loop
    assert ll.to_list() == [1, 2]
    assert len(ll) == 2

def test_prepend_and_order():
    ll = LinkedList()
    ll.prepend('a')
    ll.prepend('b')
    # prepend adds to front each time
    assert ll.to_list() == ['b', 'a']
    assert len(ll) == 2

def test_delete_head_and_empty():
    ll = LinkedList()
    ll.append(1)
    ll.append(2)
    ll.append(3)
    # delete head
    result = ll.delete(1)
    assert result is True
    assert ll.to_list() == [2, 3]
    assert len(ll) == 2
    # delete from empty list returns False
    empty = LinkedList()
    assert empty.delete(99) is False

def test_delete_middle_and_not_found():
    ll = LinkedList()
    for i in [1, 2, 3]:
        ll.append(i)
    # delete middle element
    assert ll.delete(2) is True
    assert ll.to_list() == [1, 3]
    assert len(ll) == 2
    # attempt to delete non‑existent element
    assert ll.delete(4) is False
    # list unchanged
    assert ll.to_list() == [1, 3]

def test_find_various_positions():
    ll = LinkedList()
    for val in [10, 20, 30]:
        ll.append(val)
    assert ll.find(10) == 0   # first
    assert ll.find(20) == 1   # middle
    assert ll.find(30) == 2   # last
    assert ll.find(40) == -1  # not present

def test_get_valid_and_invalid_indices():
    ll = LinkedList()
    for val in [5, 6, 7]:
        ll.append(val)
    assert ll.get(0) == 5
    assert ll.get(2) == 7
    with pytest.raises(IndexError):
        ll.get(-1)
    with pytest.raises(IndexError):
        ll.get(3)

def test_to_list_and_len_on_empty():
    ll = LinkedList()
    assert ll.to_list() == []
    assert len(ll) == 0

def test_handling_of_various_data_types():
    ll = LinkedList()
    # use None, empty string, zero
    ll.append(None)
    ll.append("")
    ll.append(0)
    assert ll.to_list() == [None, "", 0]
    assert ll.find(None) == 0
    assert ll.find("") == 1
    assert ll.find(0) == 2
    assert ll.get(0) is None
    assert ll.get(1) == ""
    assert ll.get(2) == 0
    # delete each type
    assert ll.delete("") is True
    assert ll.to_list() == [None, 0]
    assert ll.delete(None) is True
    assert ll.to_list() == [0]
    assert ll.delete(0) is True
    assert ll.to_list() == []
    assert len(ll) == 0