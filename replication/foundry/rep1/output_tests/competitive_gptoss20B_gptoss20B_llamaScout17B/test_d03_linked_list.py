import pytest
from data.input_code.d03_linked_list import *

@pytest.mark.parametrize('input_data, expected', [
    ({}, 0)
])
def test_linked_list_len(input_data, expected):
    linked_list = LinkedList()
    assert len(linked_list) == expected

@pytest.mark.parametrize('input_data, expected', [
    ({}, []),
    ({'data': 9}, [9])  # Test to_list after prepend
])
def test_linked_list_to_list(input_data, expected):
    linked_list = LinkedList()
    if 'data' in input_data:
        linked_list.prepend(input_data['data'])
    assert linked_list.to_list() == expected

@pytest.mark.parametrize('data, expected', [
    (5, None)
])
def test_linked_list_append(data, expected):
    linked_list = LinkedList()
    assert linked_list.append(data) == expected

@pytest.mark.parametrize('data, expected', [
    (5, False)
])
def test_linked_list_delete_empty(data, expected):
    linked_list = LinkedList()
    assert linked_list.delete(data) == expected

@pytest.mark.parametrize('index, expected', [
    (-1, 'IndexError'),
    (1, 'IndexError')
])
def test_linked_list_get_error(index, expected):
    linked_list = LinkedList()
    with pytest.raises(IndexError):
        linked_list.get(index)

@pytest.mark.parametrize('data, expected', [
    (7, -1)
])
def test_linked_list_find_not_found(data, expected):
    linked_list = LinkedList()
    assert linked_list.find(data) == expected

@pytest.mark.parametrize('data, expected', [
    (9, None)
])
def test_linked_list_prepend(data, expected):
    linked_list = LinkedList()
    assert linked_list.prepend(data) == expected

def test_linked_list_delete_head():
    linked_list = LinkedList()
    linked_list.append(1)
    linked_list.append(2)
    assert linked_list.delete(1) is True

def test_linked_list_delete_middle():
    linked_list = LinkedList()
    linked_list.append(1)
    linked_list.append(2)
    linked_list.append(3)
    assert linked_list.delete(2) is True

def test_linked_list_delete_tail():
    linked_list = LinkedList()
    linked_list.append(1)
    linked_list.append(2)
    assert linked_list.delete(2) is True

def test_linked_list_find_found():
    linked_list = LinkedList()
    linked_list.append(10)
    linked_list.append(20)
    linked_list.append(30)
    assert linked_list.find(20) == 1

def test_linked_list_get_valid():
    linked_list = LinkedList()
    linked_list.append(11)
    linked_list.append(22)
    linked_list.append(33)
    assert linked_list.get(2) == 33

def test_linked_list_get_zero_one():
    linked_list = LinkedList()
    linked_list.append(7)
    assert linked_list.get(0) == 7

def test_linked_list_find_head():
    linked_list = LinkedList()
    linked_list.prepend(5)
    assert linked_list.find(5) == 0

def test_linked_list_delete_not_found_non_empty():
    linked_list = LinkedList()
    linked_list.append(1)
    linked_list.append(2)
    assert linked_list.delete(3) is False

def test_linked_list_get_out_of_range_non_empty():
    linked_list = LinkedList()
    linked_list.append(1)
    with pytest.raises(IndexError):
        linked_list.get(5)

def test_linked_list_len_after_single_append():
    linked_list = LinkedList()
    linked_list.append(1)
    assert len(linked_list) == 1