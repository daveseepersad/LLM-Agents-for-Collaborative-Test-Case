import pytest
from data.input_code.d03_linked_list import *

@pytest.fixture
def linked_list():
    return LinkedList()

def test_linked_list_init():
    linked_list = LinkedList()
    assert linked_list.head is None
    assert linked_list._size == 0

def test_linked_list_append_empty():
    linked_list = LinkedList()
    linked_list.append(1)
    assert linked_list.head.data == 1
    assert linked_list._size == 1

def test_linked_list_append_non_empty():
    linked_list = LinkedList()
    linked_list.append(1)
    linked_list.append(2)
    assert linked_list.head.data == 1
    assert linked_list.head.next.data == 2
    assert linked_list._size == 2

def test_linked_list_prepend_empty():
    linked_list = LinkedList()
    linked_list.prepend(0)
    assert linked_list.head.data == 0
    assert linked_list._size == 1

def test_linked_list_prepend_non_empty():
    linked_list = LinkedList()
    linked_list.append(1)
    linked_list.prepend(-1)
    assert linked_list.head.data == -1
    assert linked_list.head.next.data == 1
    assert linked_list._size == 2

def test_linked_list_delete_existing():
    linked_list = LinkedList()
    linked_list.append(1)
    assert linked_list.delete(1) is True
    assert linked_list.head is None
    assert linked_list._size == 0

def test_linked_list_delete_non_existing():
    linked_list = LinkedList()
    linked_list.append(1)
    assert linked_list.delete(3) is False
    assert linked_list.head.data == 1
    assert linked_list._size == 1

def test_linked_list_find_existing():
    linked_list = LinkedList()
    linked_list.append(1)
    assert linked_list.find(1) == 0

def test_linked_list_find_non_existing():
    linked_list = LinkedList()
    linked_list.append(1)
    assert linked_list.find(3) == -1

def test_linked_list_get_valid_index():
    linked_list = LinkedList()
    linked_list.append(-1)
    linked_list.append(0)
    linked_list.append(1)
    linked_list.append(2)
    assert linked_list.get(0) == -1

def test_linked_list_get_negative_index():
    linked_list = LinkedList()
    linked_list.append(-1)
    linked_list.append(0)
    linked_list.append(1)
    linked_list.append(2)
    with pytest.raises(IndexError):
        linked_list.get(-1)

def test_linked_list_get_index_out_of_range():
    linked_list = LinkedList()
    linked_list.append(-1)
    linked_list.append(0)
    linked_list.append(1)
    linked_list.append(2)
    with pytest.raises(IndexError):
        linked_list.get(4)

def test_linked_list_to_list():
    linked_list = LinkedList()
    linked_list.append(-1)
    linked_list.append(0)
    linked_list.append(1)
    linked_list.append(2)
    assert linked_list.to_list() == [-1, 0, 1, 2]

def test_linked_list_len():
    linked_list = LinkedList()
    linked_list.append(-1)
    linked_list.append(0)
    linked_list.append(1)
    linked_list.append(2)
    assert len(linked_list) == 4

def test_linked_list_prepend_delete():
    linked_list = LinkedList()
    linked_list.prepend(0)
    assert linked_list.delete(0) is True
    assert linked_list.head is None
    assert linked_list._size == 0

def test_linked_list_delete_head():
    linked_list = LinkedList()
    linked_list.append(0)
    linked_list.append(1)
    linked_list.append(2)
    linked_list.prepend(-1)
    assert linked_list.delete(-1) is True
    assert linked_list.head.data == 0
    assert linked_list._size == 3

def test_linked_list_find_at_end():
    linked_list = LinkedList()
    linked_list.append(-1)
    linked_list.append(0)
    linked_list.append(1)
    linked_list.append(2)
    assert linked_list.find(2) == 3

def test_linked_list_get_last_index():
    linked_list = LinkedList()
    linked_list.append(-1)
    linked_list.append(0)
    linked_list.append(1)
    linked_list.append(2)
    assert linked_list.get(3) == 2

def test_linked_list_to_list_empty():
    linked_list = LinkedList()
    assert linked_list.to_list() == []

def test_linked_list_len_empty():
    linked_list = LinkedList()
    assert len(linked_list) == 0

def test_linked_list_delete_all_nodes():
    linked_list = LinkedList()
    linked_list.append(0)
    linked_list.append(0)
    linked_list.append(0)
    assert linked_list.delete(0) is True
    assert linked_list.delete(0) is True
    assert linked_list.delete(0) is True
    assert linked_list.head is None
    assert linked_list._size == 0

def test_linked_list_delete_middle_after_prepend():
    linked_list = LinkedList()
    linked_list.append(0)
    linked_list.append(1)
    linked_list.append(2)
    linked_list.prepend(-1)
    assert linked_list.delete(1) is True
    assert linked_list.head.data == -1
    assert linked_list.head.next.data == 0
    assert linked_list.head.next.next.data == 2
    assert linked_list._size == 3

def test_linked_list_find_after_delete():
    linked_list = LinkedList()
    linked_list.append(0)
    linked_list.append(1)
    linked_list.append(2)
    linked_list.delete(0)
    assert linked_list.find(1) == 0

def test_linked_list_get_after_delete():
    linked_list = LinkedList()
    linked_list.append(0)
    linked_list.append(1)
    linked_list.append(2)
    linked_list.delete(0)
    assert linked_list.get(0) == 1

def test_linked_list_to_list_after_delete():
    linked_list = LinkedList()
    linked_list.append(0)
    linked_list.append(1)
    linked_list.append(2)
    linked_list.delete(0)
    assert linked_list.to_list() == [1, 2]

def test_linked_list_len_after_delete():
    linked_list = LinkedList()
    linked_list.append(0)
    linked_list.append(1)
    linked_list.append(2)
    linked_list.delete(0)
    assert len(linked_list) == 2

def test_linked_list_delete_prepend():
    linked_list = LinkedList()
    linked_list.append(0)
    linked_list.append(1)
    linked_list.append(2)
    linked_list.prepend(-1)
    assert linked_list.delete(-1) is True
    assert linked_list.head.data == 0
    assert linked_list._size == 3

def test_linked_list_delete_all_nodes_twice():
    linked_list = LinkedList()
    linked_list.append(0)
    linked_list.append(0)
    linked_list.append(0)
    linked_list.delete(0)
    linked_list.delete(0)
    linked_list.delete(0)
    assert linked_list.delete(0) is False
    assert linked_list.head is None
    assert linked_list._size == 0