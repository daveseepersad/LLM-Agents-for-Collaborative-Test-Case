import pytest
from data.input_code.d03_linked_list import *

def test_linked_list_operations_sequence():
    ll = LinkedList()
    assert len(ll) == 0
    assert ll.to_list() == []

    ll.append(1)
    assert ll.to_list() == [1]

    ll.append(2)
    assert ll.to_list() == [1, 2]

    ll.prepend(0)
    ll.prepend(3)
    assert ll.to_list() == [3, 0, 1, 2]

    assert ll.delete(1) == True
    assert ll.to_list() == [3, 0, 2]

    assert ll.delete(4) == False

    assert ll.find(2) == 2
    assert ll.find(4) == -1

    assert ll.get(0) == 3
    with pytest.raises(IndexError):
        ll.get(-1)
    with pytest.raises(IndexError):
        ll.get(5)

    assert ll.to_list() == [3, 0, 2]
    assert len(ll) == 3

def test_empty_delete_find_get():
    ll = LinkedList()
    # Delete from empty list should return False
    assert ll.delete(1) is False
    # Find in empty list should return -1
    assert ll.find(1) == -1
    # Get from empty list should raise IndexError
    with pytest.raises(IndexError):
        ll.get(0)

def test_prepend_on_empty_returns_none_and_builds_list():
    ll = LinkedList()
    # Prepend should return None and build the list
    assert ll.prepend(1) is None
    assert ll.to_list() == [1]

def test_append_on_empty_returns_none_and_builds_list():
    ll = LinkedList()
    # Append should return None and build the list
    assert ll.append(2) is None
    assert ll.to_list() == [2]

def test_delete_head_and_tail():
    # Delete the head node
    ll = LinkedList()
    ll.append(1)
    ll.append(2)
    assert ll.delete(1) is True
    assert ll.to_list() == [2]

    # Delete the tail node
    ll_tail = LinkedList()
    ll_tail.append(1)
    ll_tail.append(2)
    assert ll_tail.delete(2) is True
    assert ll_tail.to_list() == [1]

def test_find_head_and_tail():
    ll = LinkedList()
    ll.append(1)
    ll.append(2)
    assert ll.find(1) == 0  # head
    assert ll.find(2) == 1  # tail

def test_get_head_and_tail():
    ll = LinkedList()
    ll.append(1)
    ll.append(2)
    assert ll.get(0) == 1  # head
    assert ll.get(1) == 2  # tail

def test_get_on_empty_raises_index_error():
    ll = LinkedList()
    with pytest.raises(IndexError):
        ll.get(0)

def test_length_after_deleting_last_node():
    ll = LinkedList()
    ll.append(1)
    assert len(ll) == 1
    ll.delete(1)
    assert len(ll) == 0

def test_delete_after_prepend():
    ll = LinkedList()
    ll.prepend(1)
    assert ll.delete(1) is True

def test_find_after_delete():
    ll = LinkedList()
    ll.prepend(1)
    ll.delete(1)
    assert ll.find(1) == -1

def test_to_list_after_delete_all_nodes():
    ll = LinkedList()
    ll.append(1)
    ll.delete(1)
    assert ll.to_list() == []

def test_prepend_after_delete_builds_list():
    ll = LinkedList()
    ll.prepend(1)
    ll.delete(1)
    assert ll.prepend(1) is None
    assert ll.to_list() == [1]

def test_append_after_delete_builds_list():
    ll = LinkedList()
    ll.append(1)
    ll.delete(1)
    assert ll.append(1) is None
    assert ll.to_list() == [1]

def test_get_max_index():
    ll = LinkedList()
    ll.prepend(1)
    assert ll.get(0) == 1

def test_delete_after_get():
    ll = LinkedList()
    ll.append(1)
    ll.get(0)
    assert ll.delete(1) is True

@pytest.mark.parametrize("data, expected", [(2, 2), (3, 0)])
def test_find_after_prepend_and_append(data, expected):
    ll = LinkedList()
    ll.prepend(3)
    ll.append(1)
    ll.append(2)
    assert ll.find(data) == expected

def test_length_after_prepend_and_append():
    ll = LinkedList()
    ll.prepend(3)
    ll.append(1)
    ll.append(2)
    assert len(ll) == 3

def test_to_list_after_prepend_and_append():
    ll = LinkedList()
    ll.prepend(3)
    ll.append(1)
    ll.append(2)
    assert ll.to_list() == [3, 1, 2]

def test_delete_all_nodes_after_prepend_and_append():
    ll = LinkedList()
    ll.prepend(3)
    ll.append(1)
    ll.append(2)
    assert ll.delete(1) is True

def test_get_after_delete_all_nodes():
    ll = LinkedList()
    ll.append(1)
    ll.delete(1)
    with pytest.raises(IndexError):
        ll.get(0)

def test_find_after_delete_all_nodes():
    ll = LinkedList()
    ll.append(1)
    ll.delete(1)
    assert ll.find(1) == -1

def test_to_list_after_delete_all_nodes():
    ll = LinkedList()
    ll.append(1)
    ll.delete(1)
    assert ll.to_list() == []

def test_length_after_delete_all_nodes():
    ll = LinkedList()
    ll.append(1)
    ll.delete(1)
    assert len(ll) == 0