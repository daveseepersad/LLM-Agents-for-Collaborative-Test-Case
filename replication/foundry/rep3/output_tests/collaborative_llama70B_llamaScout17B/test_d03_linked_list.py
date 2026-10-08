import pytest
from data.input_code.d03_linked_list import *

def test_linked_list_init():
    linked_list = LinkedList()
    assert linked_list.head is None
    assert len(linked_list) == 0

@pytest.mark.parametrize('data', [1, 2])
def test_linked_list_append(data):
    linked_list = LinkedList()
    linked_list.append(data)
    assert linked_list.to_list() == [data]

@pytest.mark.parametrize('data', [0, -1])
def test_linked_list_prepend(data):
    linked_list = LinkedList()
    linked_list.append(1)
    linked_list.prepend(data)
    assert linked_list.to_list() == [data, 1]

@pytest.mark.parametrize('data, expected', [(1, True), (10, False)])
def test_linked_list_delete(data, expected):
    linked_list = LinkedList()
    linked_list.append(-1)
    linked_list.append(0)
    linked_list.append(1)
    linked_list.append(2)
    assert linked_list.delete(data) == expected

@pytest.mark.parametrize('data, expected', [(1, 2), (10, -1)])
def test_linked_list_find(data, expected):
    linked_list = LinkedList()
    linked_list.append(-1)
    linked_list.append(0)
    linked_list.append(1)
    linked_list.append(2)
    assert linked_list.find(data) == expected

@pytest.mark.parametrize('index, expected', [(0, -1), (3, 2)])
def test_linked_list_get_success(index, expected):
    linked_list = LinkedList()
    linked_list.append(-1)
    linked_list.append(0)
    linked_list.append(1)
    linked_list.append(2)
    assert linked_list.get(index) == expected

def test_linked_list_get_error():
    linked_list = LinkedList()
    linked_list.append(-1)
    linked_list.append(0)
    linked_list.append(1)
    linked_list.append(2)
    with pytest.raises(IndexError):
        linked_list.get(10)

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

import pytest
from data.input_code.d03_linked_list import *

def test_linked_list_delete_empty():
    linked_list = LinkedList()
    assert linked_list.delete(1) == False

def test_linked_list_find_empty():
    linked_list = LinkedList()
    assert linked_list.find(1) == -1

def test_linked_list_get_empty():
    linked_list = LinkedList()
    with pytest.raises(IndexError):
        linked_list.get(0)

def test_linked_list_get_negative_index():
    linked_list = LinkedList()
    linked_list.append(1)
    linked_list.append(2)
    with pytest.raises(IndexError):
        linked_list.get(-1)

def test_linked_list_prepend_empty():
    linked_list = LinkedList()
    linked_list.prepend(1)
    assert linked_list.to_list() == [1]

def test_linked_list_delete_head():
    linked_list = LinkedList()
    linked_list.append(1)
    linked_list.append(2)
    assert linked_list.delete(1) == True
    assert linked_list.to_list() == [2]

def test_linked_list_find_head():
    linked_list = LinkedList()
    linked_list.append(1)
    linked_list.append(2)
    assert linked_list.find(1) == 0