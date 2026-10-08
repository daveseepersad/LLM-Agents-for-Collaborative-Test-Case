import pytest
from data.input_code.d03_linked_list import *

@pytest.mark.parametrize('data, expected', [
    (None, None),
    ("", None)
])
def test_linked_list_append_prepend(data, expected):
    linked_list = LinkedList()
    if data is None:
        linked_list.append(data)
    else:
        linked_list.prepend(data)
    assert linked_list.to_list() == [data]

def test_linked_list_delete_empty():
    linked_list = LinkedList()
    assert linked_list.delete(1) is False

def test_linked_list_find_empty():
    linked_list = LinkedList()
    assert linked_list.find("x") == -1

@pytest.mark.parametrize('index, expected', [
    (-1, "IndexError"),
    (0, "IndexError")
])
def test_linked_list_get(index, expected):
    linked_list = LinkedList()
    if expected == "IndexError":
        with pytest.raises(IndexError):
            linked_list.get(index)

def test_linked_list_to_list_empty():
    linked_list = LinkedList()
    assert linked_list.to_list() == []

def test_linked_list_len_empty():
    linked_list = LinkedList()
    assert len(linked_list) == 0

import pytest
from data.input_code.d03_linked_list import *

def test_linked_list_prepend_nonempty():
    linked_list = LinkedList()
    linked_list.append(1)
    linked_list.append(2)
    linked_list.prepend(0)
    assert linked_list.to_list() == [0, 1, 2]

def test_linked_list_append_nonempty():
    linked_list = LinkedList()
    linked_list.append(1)
    linked_list.append(2)
    linked_list.append(3)
    assert linked_list.to_list() == [1, 2, 3]

def test_linked_list_delete_head():
    linked_list = LinkedList()
    linked_list.append(1)
    linked_list.append(2)
    assert linked_list.delete(1) is True
    assert linked_list.to_list() == [2]

def test_linked_list_delete_middle():
    linked_list = LinkedList()
    linked_list.append(1)
    linked_list.append(2)
    linked_list.append(3)
    assert linked_list.delete(2) is True
    assert linked_list.to_list() == [1, 3]

def test_linked_list_delete_not_found():
    linked_list = LinkedList()
    linked_list.append(1)
    linked_list.append(2)
    assert linked_list.delete(99) is False

def test_linked_list_find_exist():
    linked_list = LinkedList()
    linked_list.append(1)
    linked_list.append(2)
    linked_list.append(3)
    assert linked_list.find(3) == 2

def test_linked_list_find_not_found():
    linked_list = LinkedList()
    linked_list.append(1)
    linked_list.append(2)
    assert linked_list.find(99) == -1

def test_linked_list_get_valid():
    linked_list = LinkedList()
    linked_list.append(10)
    linked_list.append(20)
    linked_list.append(30)
    assert linked_list.get(1) == 20

@pytest.mark.parametrize('index, expected', [
    (3, "IndexError")
])
def test_linked_list_get_out_of_range(index, expected):
    linked_list = LinkedList()
    linked_list.append(10)
    linked_list.append(20)
    linked_list.append(30)
    if expected == "IndexError":
        with pytest.raises(IndexError):
            linked_list.get(index)