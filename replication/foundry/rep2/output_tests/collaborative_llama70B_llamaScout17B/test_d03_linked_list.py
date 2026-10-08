import pytest
from data.input_code.d03_linked_list import *

def node_to_dict(node):
    if node is None:
        return None
    return {"data": node.data, "next": node_to_dict(node.next)}

def test_linked_list_init():
    linked_list = LinkedList()
    assert node_to_dict(linked_list.head) == None
    assert linked_list._size == 0

@pytest.fixture
def linked_list():
    linked_list = LinkedList()
    linked_list.append(1)
    linked_list.append(2)
    return linked_list

def test_append(linked_list):
    linked_list.append(3)
    assert node_to_dict(linked_list.head) == {"data": 1, "next": {"data": 2, "next": {"data": 3, "next": None}}}
    assert linked_list._size == 3

def test_prepend(linked_list):
    linked_list.prepend(0)
    assert node_to_dict(linked_list.head) == {"data": 0, "next": {"data": 1, "next": {"data": 2, "next": None}}}
    assert linked_list._size == 3

@pytest.mark.parametrize('data, expected', [
    (1, True),
    (2, True),
    (3, False)
])
def test_delete(linked_list, data, expected):
    assert linked_list.delete(data) == expected

@pytest.mark.parametrize('data, expected', [
    (1, 0),
    (2, 1),
    (3, -1)
])
def test_find(linked_list, data, expected):
    assert linked_list.find(data) == expected

@pytest.mark.parametrize('index, expected', [
    (0, 1),
    (1, 2)
])
def test_get(linked_list, index, expected):
    assert linked_list.get(index) == expected

def test_get_out_of_range(linked_list):
    with pytest.raises(IndexError):
        linked_list.get(2)

def test_to_list(linked_list):
    assert linked_list.to_list() == [1, 2]

def test_len(linked_list):
    assert len(linked_list) == 2

import pytest
from data.input_code.d03_linked_list import *

def node_to_dict(node):
    if node is None:
        return None
    return {"data": node.data, "next": node_to_dict(node.next)}

def test_prepend_empty():
    linked_list = LinkedList()
    linked_list.prepend(1)
    assert node_to_dict(linked_list.head) == {"data": 1, "next": None}

def test_delete_head():
    linked_list = LinkedList()
    linked_list.append(1)
    linked_list.append(2)
    assert linked_list.delete(1) == True
    assert node_to_dict(linked_list.head) == {"data": 2, "next": None}

def test_delete_tail():
    linked_list = LinkedList()
    linked_list.append(1)
    linked_list.append(2)
    assert linked_list.delete(2) == True
    assert node_to_dict(linked_list.head) == {"data": 1, "next": None}

def test_find_empty():
    linked_list = LinkedList()
    assert linked_list.find(1) == -1

def test_get_negative_index():
    linked_list = LinkedList()
    linked_list.append(1)
    with pytest.raises(IndexError):
        linked_list.get(-1)

def test_to_list_empty():
    linked_list = LinkedList()
    assert linked_list.to_list() == []

def test_len_empty():
    linked_list = LinkedList()
    assert len(linked_list) == 0

import pytest
from data.input_code.d03_linked_list import *

def test_delete_not_found(linked_list):
    assert linked_list.delete(3) == False

def test_get_at_end(linked_list):
    assert linked_list.get(1) == 2

def test_prepend_multiple():
    linked_list = LinkedList()
    linked_list.append(1)
    linked_list.append(2)
    linked_list.prepend(0)
    assert node_to_dict(linked_list.head) == {"data": 0, "next": {"data": 1, "next": {"data": 2, "next": None}}}

def test_find_at_end(linked_list):
    assert linked_list.find(2) == 1

def test_to_list_single_element():
    linked_list = LinkedList()
    linked_list.append(1)
    assert linked_list.to_list() == [1]

def test_len_single_element():
    linked_list = LinkedList()
    linked_list.append(1)
    assert len(linked_list) == 1

import pytest
from data.input_code.d03_linked_list import *

def test_get_at_beginning_empty():
    linked_list = LinkedList()
    with pytest.raises(IndexError):
        linked_list.get(0)

def test_delete_empty():
    linked_list = LinkedList()
    assert linked_list.delete(1) == False

@pytest.mark.parametrize('data', [1, 2, 3])
def test_prepend_multiple_empty(data):
    linked_list = LinkedList()
    linked_list.prepend(data)
    assert node_to_dict(linked_list.head) == {"data": data, "next": None}

def test_find_at_beginning_single_element():
    linked_list = LinkedList()
    linked_list.append(1)
    assert linked_list.find(1) == 0

def test_to_list_single_element_after_delete():
    linked_list = LinkedList()
    linked_list.append(1)
    linked_list.delete(1)
    assert linked_list.to_list() == []

def test_len_after_delete_all():
    linked_list = LinkedList()
    linked_list.append(1)
    linked_list.append(2)
    linked_list.delete(1)
    linked_list.delete(2)
    assert len(linked_list) == 0