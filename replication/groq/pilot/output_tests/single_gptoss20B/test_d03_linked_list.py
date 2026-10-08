import pytest
from data.input_code.d03_linked_list import Node, LinkedList


def test_append_prepend_and_len_and_to_list():
    ll = LinkedList()
    # Append 1, 2, 3
    ll.append(1)
    ll.append(2)
    ll.append(3)
    assert len(ll) == 3
    assert ll.to_list() == [1, 2, 3]
    # Prepend 0
    ll.prepend(0)
    assert len(ll) == 4
    assert ll.to_list() == [0, 1, 2, 3]
    # Prepend -1
    ll.prepend(-1)
    assert len(ll) == 5
    assert ll.to_list() == [-1, 0, 1, 2, 3]
    # Append 4
    ll.append(4)
    assert len(ll) == 6
    assert ll.to_list() == [-1, 0, 1, 2, 3, 4]


def test_delete_operations_and_len():
    # Delete on empty list
    empty_ll = LinkedList()
    assert empty_ll.delete(1) is False
    # Setup list with 1-5
    ll = LinkedList()
    for i in range(1, 6):
        ll.append(i)
    # Delete head
    assert ll.delete(1) is True
    assert len(ll) == 4
    assert ll.to_list() == [2, 3, 4, 5]
    # Delete middle (4)
    assert ll.delete(4) is True
    assert len(ll) == 3
    assert ll.to_list() == [2, 3, 5]
    # Delete last (5)
    assert ll.delete(5) is True
    assert len(ll) == 2
    assert ll.to_list() == [2, 3]
    # Delete non-existent
    assert ll.delete(10) is False
    assert len(ll) == 2
    assert ll.to_list() == [2, 3]


def test_find_and_get_and_exceptions():
    # Empty list find and get
    empty_ll = LinkedList()
    assert empty_ll.find(1) == -1
    assert len(empty_ll) == 0
    assert empty_ll.to_list() == []
    with pytest.raises(IndexError):
        empty_ll.get(0)
    # Setup list
    ll = LinkedList()
    ll.append(10)
    ll.append(20)
    ll.append(30)
    # Find existing
    assert ll.find(20) == 1
    # Find non-existing
    assert ll.find(40) == -1
    # Get valid indices
    assert ll.get(0) == 10
    assert ll.get(1) == 20
    assert ll.get(2) == 30
    # Get negative index
    with pytest.raises(IndexError):
        ll.get(-1)
    # Get out-of-range
    with pytest.raises(IndexError):
        ll.get(3)


def test_node_data_types_and_get():
    ll = LinkedList()
    ll.append(None)
    ll.append("")
    ll.append(0)
    assert ll.to_list() == [None, "", 0]
    assert ll.get(0) is None
    assert ll.get(1) == ""
    assert ll.get(2) == 0


def test_delete_single_element_and_get_exception():
    ll = LinkedList()
    ll.append(42)
    assert ll.delete(42) is True
    assert len(ll) == 0
    assert ll.to_list() == []
    with pytest.raises(IndexError):
        ll.get(0)


def test_find_duplicates_and_delete_all():
    ll = LinkedList()
    ll.append(5)
    ll.append(5)
    ll.append(5)
    # Find first
    assert ll.find(5) == 0
    # Delete first
    assert ll.delete(5) is True
    assert ll.find(5) == 0
    # Delete second
    assert ll.delete(5) is True
    assert ll.find(5) == 0
    # Delete third
    assert ll.delete(5) is True
    assert ll.find(5) == -1


def test_prepend_and_append_combination():
    ll = LinkedList()
    ll.append(3)
    ll.prepend(2)
    ll.prepend(1)
    ll.append(4)
    assert ll.to_list() == [1, 2, 3, 4]
    assert len(ll) == 4