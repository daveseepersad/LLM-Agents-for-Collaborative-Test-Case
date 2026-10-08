import pytest
from data.input_code.d03_linked_list import LinkedList, Node

def test_node_init():
    node = Node(5)
    assert node.data == 5
    assert node.next is None

def test_linked_list_init():
    linked_list = LinkedList()
    assert linked_list.head is None
    assert len(linked_list) == 0

def test_append():
    linked_list = LinkedList()
    linked_list.append(1)
    linked_list.append(2)
    assert linked_list.to_list() == [1, 2]
    assert len(linked_list) == 2

def test_prepend():
    linked_list = LinkedList()
    linked_list.prepend(1)
    linked_list.prepend(2)
    assert linked_list.to_list() == [2, 1]
    assert len(linked_list) == 2

def test_delete_head():
    linked_list = LinkedList()
    linked_list.append(1)
    linked_list.append(2)
    assert linked_list.delete(1) is True
    assert linked_list.to_list() == [2]
    assert len(linked_list) == 1

def test_delete_middle():
    linked_list = LinkedList()
    linked_list.append(1)
    linked_list.append(2)
    linked_list.append(3)
    assert linked_list.delete(2) is True
    assert linked_list.to_list() == [1, 3]
    assert len(linked_list) == 2

def test_delete_tail():
    linked_list = LinkedList()
    linked_list.append(1)
    linked_list.append(2)
    assert linked_list.delete(2) is True
    assert linked_list.to_list() == [1]
    assert len(linked_list) == 1

def test_delete_not_found():
    linked_list = LinkedList()
    linked_list.append(1)
    linked_list.append(2)
    assert linked_list.delete(3) is False
    assert linked_list.to_list() == [1, 2]
    assert len(linked_list) == 2

def test_delete_empty_list():
    linked_list = LinkedList()
    assert linked_list.delete(1) is False
    assert linked_list.to_list() == []
    assert len(linked_list) == 0

def test_find():
    linked_list = LinkedList()
    linked_list.append(1)
    linked_list.append(2)
    linked_list.append(3)
    assert linked_list.find(2) == 1
    assert linked_list.find(4) == -1

def test_get_valid_index():
    linked_list = LinkedList()
    linked_list.append(1)
    linked_list.append(2)
    assert linked_list.get(0) == 1
    assert linked_list.get(1) == 2

def test_get_invalid_index():
    linked_list = LinkedList()
    linked_list.append(1)
    with pytest.raises(IndexError):
        linked_list.get(-1)
    with pytest.raises(IndexError):
        linked_list.get(1)
    with pytest.raises(IndexError):
        linked_list.get(2)

def test_to_list():
    linked_list = LinkedList()
    linked_list.append(1)
    linked_list.append(2)
    assert linked_list.to_list() == [1, 2]

def test_len():
    linked_list = LinkedList()
    assert len(linked_list) == 0
    linked_list.append(1)
    assert len(linked_list) == 1
    linked_list.append(2)
    assert len(linked_list) == 2