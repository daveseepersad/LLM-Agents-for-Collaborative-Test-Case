import pytest
from data.input_code.d03_linked_list import *

@pytest.mark.parametrize('data', [
    (5),
    (None),
    (0)
])
def test_append(data):
    linked_list = LinkedList()
    linked_list.append(data)
    assert linked_list.to_list() == [data]

@pytest.mark.parametrize('data', [
    (3)
])
def test_prepend(data):
    linked_list = LinkedList()
    linked_list.prepend(data)
    assert linked_list.to_list() == [data]

def test_get_empty_index0():
    linked_list = LinkedList()
    with pytest.raises(IndexError):
        linked_list.get(0)

def test_get_negative():
    linked_list = LinkedList()
    linked_list.append(5)
    with pytest.raises(IndexError):
        linked_list.get(-1)

def test_find_empty():
    linked_list = LinkedList()
    assert linked_list.find(5) == -1

def test_to_list_empty():
    linked_list = LinkedList()
    assert linked_list.to_list() == []

def test_len_empty():
    linked_list = LinkedList()
    assert len(linked_list) == 0

def test_delete_empty():
    linked_list = LinkedList()
    assert linked_list.delete(42) == False

def test_delete():
    linked_list = LinkedList()
    linked_list.append(5)
    assert linked_list.delete(5) == True
    assert linked_list.to_list() == []

def test_find():
    linked_list = LinkedList()
    linked_list.append(5)
    assert linked_list.find(5) == 0
    assert linked_list.find(3) == -1

@pytest.mark.parametrize('sequence, index, expected', [
    ([["append", 1]], 1, 'IndexError')
])
def test_get_out_of_bounds(sequence, index, expected):
    linked_list = LinkedList()
    for method, data in sequence:
        if method == "append":
            linked_list.append(data)
    if expected == 'IndexError':
        with pytest.raises(IndexError):
            linked_list.get(index)
    else:
        assert linked_list.get(index) == expected

@pytest.mark.parametrize('sequence, index, expected', [
    ([["append", 10], ["append", 20], ["append", 30]], 2, 30)
])
def test_get_last_valid(sequence, index, expected):
    linked_list = LinkedList()
    for method, data in sequence:
        if method == "append":
            linked_list.append(data)
    assert linked_list.get(index) == expected

@pytest.mark.parametrize('sequence, data, expected', [
    ([["append", 1], ["append", 2], ["append", 3]], 2, True)
])
def test_delete_non_head(sequence, data, expected):
    linked_list = LinkedList()
    for method, value in sequence:
        if method == "append":
            linked_list.append(value)
    assert linked_list.delete(data) == expected

@pytest.mark.parametrize('sequence, data, expected', [
    ([["append", 1], ["append", 2]], 3, False)
])
def test_delete_not_found(sequence, data, expected):
    linked_list = LinkedList()
    for method, value in sequence:
        if method == "append":
            linked_list.append(value)
    assert linked_list.delete(data) == expected

@pytest.mark.parametrize('sequence, data, expected', [
    ([["append", 5], ["append", 10], ["append", 15]], 10, 1)
])
def test_find_middle(sequence, data, expected):
    linked_list = LinkedList()
    for method, value in sequence:
        if method == "append":
            linked_list.append(value)
    assert linked_list.find(data) == expected