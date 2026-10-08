import pytest
from data.input_code.d03_linked_list import LinkedList, Node

def test_init():
    linked_list = LinkedList()
    assert linked_list.head is None
    assert linked_list._size == 0

def test_append_empty():
    linked_list = LinkedList()
    linked_list.append(5)
    assert linked_list.head.data == 5
    assert linked_list._size == 1

def test_append_nonempty():
    linked_list = LinkedList()
    linked_list.append(5)
    linked_list.append(10)
    assert linked_list.head.data == 5
    assert linked_list.head.next.data == 10
    assert linked_list._size == 2

def test_prepend_empty():
    linked_list = LinkedList()
    linked_list.prepend(5)
    assert linked_list.head.data == 5
    assert linked_list._size == 1

def test_prepend_nonempty():
    linked_list = LinkedList()
    linked_list.append(5)
    linked_list.prepend(10)
    assert linked_list.head.data == 10
    assert linked_list.head.next.data == 5
    assert linked_list._size == 2

def test_delete_empty():
    linked_list = LinkedList()
    assert linked_list.delete(5) is False

def test_delete_head():
    linked_list = LinkedList()
    linked_list.append(5)
    assert linked_list.delete(5) is True
    assert linked_list.head is None
    assert linked_list._size == 0

def test_delete_nonhead():
    linked_list = LinkedList()
    linked_list.append(5)
    linked_list.append(10)
    assert linked_list.delete(10) is True
    assert linked_list.head.data == 5
    assert linked_list.head.next is None
    assert linked_list._size == 1

def test_delete_notfound():
    linked_list = LinkedList()
    linked_list.append(5)
    assert linked_list.delete(10) is False
    assert linked_list.head.data == 5
    assert linked_list._size == 1

def test_find_empty():
    linked_list = LinkedList()
    assert linked_list.find(5) == -1

def test_find_found():
    linked_list = LinkedList()
    linked_list.append(5)
    linked_list.append(10)
    assert linked_list.find(10) == 1

def test_find_notfound():
    linked_list = LinkedList()
    linked_list.append(5)
    assert linked_list.find(10) == -1

def test_get_valid():
    linked_list = LinkedList()
    linked_list.append(5)
    linked_list.append(10)
    assert linked_list.get(1) == 10

def test_get_invalid_low():
    linked_list = LinkedList()
    linked_list.append(5)
    with pytest.raises(IndexError):
        linked_list.get(-1)

def test_get_invalid_high():
    linked_list = LinkedList()
    linked_list.append(5)
    with pytest.raises(IndexError):
        linked_list.get(1)

def test_to_list_empty():
    linked_list = LinkedList()
    assert linked_list.to_list() == []

def test_to_list_nonempty():
    linked_list = LinkedList()
    linked_list.append(5)
    linked_list.append(10)
    assert linked_list.to_list() == [5, 10]

def test_len_empty():
    linked_list = LinkedList()
    assert len(linked_list) == 0

def test_len_nonempty():
    linked_list = LinkedList()
    linked_list.append(5)
    linked_list.append(10)
    assert len(linked_list) == 2