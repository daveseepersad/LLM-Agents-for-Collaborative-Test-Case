import pytest
from data.input_code.d03_linked_list import LinkedList, Node

def test_init():
    linked_list = LinkedList()
    assert linked_list.head is None
    assert linked_list._size == 0

@pytest.mark.parametrize('data, expected', [
    (5, {'head': {'data': 5, 'next': None}, '_size': 1}),
    (10, {'head': {'data': 10, 'next': None}, '_size': 1})
])
def test_append_empty(data, expected):
    linked_list = LinkedList()
    linked_list.append(data)
    assert linked_list.head.data == expected['head']['data']
    assert linked_list.head.next == expected['head']['next']
    assert linked_list._size == expected['_size']

@pytest.mark.parametrize('data, expected', [
    (10, {'head': {'data': 5, 'next': {'data': 10, 'next': None}}, '_size': 2})
])
def test_append_nonempty(data, expected):
    linked_list = LinkedList()
    linked_list.append(5)
    linked_list.append(data)
    assert linked_list.head.data == expected['head']['data']
    assert linked_list.head.next.data == expected['head']['next']['data']
    assert linked_list.head.next.next == expected['head']['next']['next']
    assert linked_list._size == expected['_size']

@pytest.mark.parametrize('data, expected', [
    (3, {'head': {'data': 3, 'next': None}, '_size': 1})
])
def test_prepend_empty(data, expected):
    linked_list = LinkedList()
    linked_list.prepend(data)
    assert linked_list.head.data == expected['head']['data']
    assert linked_list.head.next == expected['head']['next']
    assert linked_list._size == expected['_size']

@pytest.mark.parametrize('data, expected', [
    (2, {'head': {'data': 2, 'next': {'data': 3, 'next': None}}, '_size': 2})
])
def test_prepend_nonempty(data, expected):
    linked_list = LinkedList()
    linked_list.append(3)
    linked_list.prepend(data)
    assert linked_list.head.data == expected['head']['data']
    assert linked_list.head.next.data == expected['head']['next']['data']
    assert linked_list.head.next.next == expected['head']['next']['next']
    assert linked_list._size == expected['_size']

def test_delete_empty():
    linked_list = LinkedList()
    assert linked_list.delete(5) is False

def test_delete_head():
    linked_list = LinkedList()
    linked_list.append(2)
    linked_list.append(3)
    assert linked_list.delete(2) is True
    assert linked_list.head.data == 3
    assert linked_list._size == 1

def test_delete_middle():
    linked_list = LinkedList()
    linked_list.append(2)
    linked_list.append(3)
    linked_list.append(4)
    assert linked_list.delete(3) is True
    assert linked_list.head.data == 2
    assert linked_list.head.next.data == 4
    assert linked_list._size == 2

def test_delete_notfound():
    linked_list = LinkedList()
    linked_list.append(2)
    linked_list.append(3)
    assert linked_list.delete(10) is False
    assert linked_list.head.data == 2
    assert linked_list.head.next.data == 3
    assert linked_list._size == 2

@pytest.mark.parametrize('data, expected', [
    (3, 1)
])
def test_find_found(data, expected):
    linked_list = LinkedList()
    linked_list.append(2)
    linked_list.append(3)
    assert linked_list.find(data) == expected

def test_find_notfound():
    linked_list = LinkedList()
    linked_list.append(2)
    linked_list.append(3)
    assert linked_list.find(10) == -1

@pytest.mark.parametrize('index, expected', [
    (1, 3)
])
def test_get_valid(index, expected):
    linked_list = LinkedList()
    linked_list.append(2)
    linked_list.append(3)
    assert linked_list.get(index) == expected

def test_get_invalid():
    linked_list = LinkedList()
    linked_list.append(2)
    linked_list.append(3)
    with pytest.raises(IndexError):
        linked_list.get(5)

def test_to_list_empty():
    linked_list = LinkedList()
    assert linked_list.to_list() == []

def test_to_list_nonempty():
    linked_list = LinkedList()
    linked_list.append(2)
    linked_list.append(3)
    assert linked_list.to_list() == [2, 3]

def test_len_empty():
    linked_list = LinkedList()
    assert len(linked_list) == 0

def test_len_nonempty():
    linked_list = LinkedList()
    linked_list.append(2)
    linked_list.append(3)
    assert len(linked_list) == 2