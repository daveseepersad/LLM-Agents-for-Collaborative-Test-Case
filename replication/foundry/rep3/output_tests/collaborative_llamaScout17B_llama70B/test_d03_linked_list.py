import pytest
from data.input_code.d03_linked_list import LinkedList, Node

def test_init():
    linked_list = LinkedList()
    assert linked_list.head is None
    assert linked_list._size == 0

@pytest.mark.parametrize('data', [5, 10, 15])
def test_append_empty(data):
    linked_list = LinkedList()
    linked_list.append(data)
    assert linked_list.head.data == data
    assert linked_list._size == 1

@pytest.mark.parametrize('data', [10, 20, 30])
def test_append_nonempty(data):
    linked_list = LinkedList()
    linked_list.append(5)
    linked_list.append(data)
    assert linked_list.head.data == 5
    assert linked_list.head.next.data == data
    assert linked_list._size == 2

@pytest.mark.parametrize('data', [5, 10, 15])
def test_prepend_empty(data):
    linked_list = LinkedList()
    linked_list.prepend(data)
    assert linked_list.head.data == data
    assert linked_list._size == 1

@pytest.mark.parametrize('data', [10, 20, 30])
def test_prepend_nonempty(data):
    linked_list = LinkedList()
    linked_list.append(5)
    linked_list.prepend(data)
    assert linked_list.head.data == data
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

def test_delete_middle():
    linked_list = LinkedList()
    linked_list.append(5)
    linked_list.append(10)
    linked_list.append(15)
    assert linked_list.delete(10) is True
    assert linked_list.head.data == 5
    assert linked_list.head.next.data == 15
    assert linked_list._size == 2

def test_delete_tail():
    linked_list = LinkedList()
    linked_list.append(5)
    linked_list.append(10)
    linked_list.append(15)
    assert linked_list.delete(15) is True
    assert linked_list.head.data == 5
    assert linked_list.head.next.data == 10
    assert linked_list.head.next.next is None
    assert linked_list._size == 2

def test_delete_nonexistent():
    linked_list = LinkedList()
    linked_list.append(5)
    linked_list.append(10)
    linked_list.append(15)
    assert linked_list.delete(20) is False
    assert linked_list.head.data == 5
    assert linked_list.head.next.data == 10
    assert linked_list.head.next.next.data == 15
    assert linked_list._size == 3

def test_find_empty():
    linked_list = LinkedList()
    assert linked_list.find(5) == -1

def test_find_existent():
    linked_list = LinkedList()
    linked_list.append(5)
    linked_list.append(10)
    linked_list.append(15)
    assert linked_list.find(10) == 1

def test_find_nonexistent():
    linked_list = LinkedList()
    linked_list.append(5)
    linked_list.append(10)
    linked_list.append(15)
    assert linked_list.find(20) == -1

def test_get_valid():
    linked_list = LinkedList()
    linked_list.append(5)
    linked_list.append(10)
    linked_list.append(15)
    assert linked_list.get(1) == 10

def test_get_invalid_low():
    linked_list = LinkedList()
    linked_list.append(5)
    linked_list.append(10)
    linked_list.append(15)
    with pytest.raises(IndexError):
        linked_list.get(-1)

def test_get_invalid_high():
    linked_list = LinkedList()
    linked_list.append(5)
    linked_list.append(10)
    linked_list.append(15)
    with pytest.raises(IndexError):
        linked_list.get(3)

def test_to_list_empty():
    linked_list = LinkedList()
    assert linked_list.to_list() == []

def test_to_list_nonempty():
    linked_list = LinkedList()
    linked_list.append(5)
    linked_list.append(10)
    linked_list.append(15)
    assert linked_list.to_list() == [5, 10, 15]

def test_len_empty():
    linked_list = LinkedList()
    assert len(linked_list) == 0

def test_len_nonempty():
    linked_list = LinkedList()
    linked_list.append(5)
    linked_list.append(10)
    linked_list.append(15)
    assert len(linked_list) == 3