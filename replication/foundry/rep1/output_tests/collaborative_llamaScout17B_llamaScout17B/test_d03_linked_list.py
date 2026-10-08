import pytest
from data.input_code.d03_linked_list import *

def test_init():
    linked_list = LinkedList()
    assert linked_list.head is None
    assert linked_list._size == 0

@pytest.mark.parametrize('data, expected_head, expected_size', [
    (5, {'data': 5, 'next': None}, 1)
])
def test_append_empty(data, expected_head, expected_size):
    linked_list = LinkedList()
    linked_list.append(data)
    assert linked_list.head.data == expected_head['data']
    assert linked_list.head.next == expected_head['next']
    assert linked_list._size == expected_size

def test_append_nonempty():
    linked_list = LinkedList()
    linked_list.head = Node(1)
    linked_list._size = 1
    linked_list.append(2)
    assert linked_list.head.data == 1
    assert linked_list.head.next.data == 2
    assert linked_list.head.next.next is None
    assert linked_list._size == 2

@pytest.mark.parametrize('data, expected_head, expected_size', [
    (5, {'data': 5, 'next': None}, 1)
])
def test_prepend_empty(data, expected_head, expected_size):
    linked_list = LinkedList()
    linked_list.prepend(data)
    assert linked_list.head.data == expected_head['data']
    assert linked_list.head.next == expected_head['next']
    assert linked_list._size == expected_size

def test_prepend_nonempty():
    linked_list = LinkedList()
    linked_list.head = Node(1)
    linked_list._size = 1
    linked_list.prepend(2)
    assert linked_list.head.data == 2
    assert linked_list.head.next.data == 1
    assert linked_list.head.next.next is None
    assert linked_list._size == 2

def test_delete_empty():
    linked_list = LinkedList()
    assert not linked_list.delete(5)

def test_delete_head():
    linked_list = LinkedList()
    linked_list.head = Node(1)
    linked_list._size = 1
    assert linked_list.delete(1)
    assert linked_list.head is None
    assert linked_list._size == 0

def test_delete_nonhead():
    linked_list = LinkedList()
    linked_list.head = Node(1)
    linked_list.head.next = Node(2)
    linked_list._size = 2
    assert linked_list.delete(2)
    assert linked_list.head.data == 1
    assert linked_list.head.next is None
    assert linked_list._size == 1

def test_delete_missing():
    linked_list = LinkedList()
    linked_list.head = Node(1)
    linked_list._size = 1
    assert not linked_list.delete(2)

def test_find_present():
    linked_list = LinkedList()
    linked_list.head = Node(1)
    linked_list.head.next = Node(2)
    linked_list._size = 2
    assert linked_list.find(2) == 1

def test_find_missing():
    linked_list = LinkedList()
    linked_list.head = Node(1)
    linked_list._size = 1
    assert linked_list.find(2) == -1

def test_get_valid():
    linked_list = LinkedList()
    linked_list.head = Node(1)
    linked_list.head.next = Node(2)
    linked_list._size = 2
    assert linked_list.get(1) == 2

def test_get_invalid_low():
    linked_list = LinkedList()
    linked_list.head = Node(1)
    linked_list._size = 1
    with pytest.raises(IndexError):
        linked_list.get(-1)

def test_get_invalid_high():
    linked_list = LinkedList()
    linked_list.head = Node(1)
    linked_list._size = 1
    with pytest.raises(IndexError):
        linked_list.get(1)

def test_to_list():
    linked_list = LinkedList()
    linked_list.head = Node(1)
    linked_list.head.next = Node(2)
    linked_list._size = 2
    assert linked_list.to_list() == [1, 2]

def test_len():
    linked_list = LinkedList()
    linked_list.head = Node(1)
    linked_list.head.next = Node(2)
    linked_list._size = 2
    assert len(linked_list) == 2

import pytest
from data.input_code.d03_linked_list import *

def test_append_multiple():
    linked_list = LinkedList()
    linked_list.head = Node(1)
    linked_list.head.next = Node(2)
    linked_list._size = 2
    linked_list.append(3)
    assert linked_list.head.data == 1
    assert linked_list.head.next.data == 2
    assert linked_list.head.next.next.data == 3
    assert linked_list.head.next.next.next is None
    assert linked_list._size == 3

def test_prepend_multiple():
    linked_list = LinkedList()
    linked_list.head = Node(1)
    linked_list.head.next = Node(2)
    linked_list._size = 2
    linked_list.prepend(3)
    assert linked_list.head.data == 3
    assert linked_list.head.next.data == 1
    assert linked_list.head.next.next.data == 2
    assert linked_list.head.next.next.next is None
    assert linked_list._size == 3

def test_delete_multiple():
    linked_list = LinkedList()
    linked_list.head = Node(1)
    linked_list.head.next = Node(2)
    linked_list.head.next.next = Node(3)
    linked_list._size = 3
    assert linked_list.delete(2)
    assert linked_list.head.data == 1
    assert linked_list.head.next.data == 3
    assert linked_list.head.next.next is None
    assert linked_list._size == 2

def test_find_head():
    linked_list = LinkedList()
    linked_list.head = Node(1)
    linked_list.head.next = Node(2)
    linked_list._size = 2
    assert linked_list.find(1) == 0

@pytest.mark.parametrize('index, expected', [
    (0, 1),
    (2, 3)
])
def test_get_edge(index, expected):
    linked_list = LinkedList()
    linked_list.head = Node(1)
    linked_list.head.next = Node(2)
    linked_list.head.next.next = Node(3)
    linked_list._size = 3
    assert linked_list.get(index) == expected

import pytest
from data.input_code.d03_linked_list import *

def test_prepend_empty_size_check():
    linked_list = LinkedList()
    linked_list.prepend(5)
    assert linked_list._size == 1

def test_append_empty_size_check():
    linked_list = LinkedList()
    linked_list.append(5)
    assert linked_list._size == 1

def test_delete_multiple_head():
    linked_list = LinkedList()
    linked_list.head = Node(1)
    linked_list.head.next = Node(2)
    linked_list._size = 2
    assert linked_list.delete(1)
    assert linked_list.head.data == 2
    assert linked_list.head.next is None
    assert linked_list._size == 1

def test_to_list_empty():
    linked_list = LinkedList()
    assert linked_list.to_list() == []

def test_len_empty():
    linked_list = LinkedList()
    assert len(linked_list) == 0

def test_find_empty():
    linked_list = LinkedList()
    assert linked_list.find(5) == -1

def test_get_empty():
    linked_list = LinkedList()
    with pytest.raises(IndexError):
        linked_list.get(0)

import pytest
from data.input_code.d03_linked_list import *

def test_append_empty_size():
    linked_list = LinkedList()
    linked_list.append(5)
    assert linked_list._size == 1

def test_prepend_nonempty_size():
    linked_list = LinkedList()
    linked_list.head = Node(1)
    linked_list._size = 1
    linked_list.prepend(5)
    assert linked_list._size == 2

def test_delete_nonexistent_multiple():
    linked_list = LinkedList()
    linked_list.head = Node(1)
    linked_list.head.next = Node(2)
    linked_list._size = 2
    assert not linked_list.delete(5)

@pytest.mark.parametrize('data, expected', [
    (1, 1)
])
def test_get_boundary(data, expected):
    linked_list = LinkedList()
    linked_list.head = Node(data)
    linked_list._size = 1
    assert linked_list.get(0) == expected