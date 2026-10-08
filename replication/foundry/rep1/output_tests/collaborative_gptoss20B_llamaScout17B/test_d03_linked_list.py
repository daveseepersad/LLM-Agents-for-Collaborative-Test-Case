import pytest
from data.input_code.d03_linked_list import *

@pytest.mark.parametrize('input_data, expected', [
    ({}, 0)
])
def test_linked_list_len(input_data, expected):
    linked_list = LinkedList()
    assert len(linked_list) == expected

@pytest.mark.parametrize('data', [
    10, None
])
def test_linked_list_append(data):
    linked_list = LinkedList()
    linked_list.append(data)
    assert linked_list.to_list() == [data]

@pytest.mark.parametrize('data', [
    7, None
])
def test_linked_list_prepend(data):
    linked_list = LinkedList()
    linked_list.prepend(data)
    assert linked_list.to_list() == [data]

def test_linked_list_to_list_empty():
    linked_list = LinkedList()
    assert linked_list.to_list() == []

def test_linked_list_delete_empty():
    linked_list = LinkedList()
    assert not linked_list.delete(99)

def test_linked_list_find_empty():
    linked_list = LinkedList()
    assert linked_list.find(123) == -1

@pytest.mark.parametrize('index, expected', [
    (-1, 'IndexError'),
    (1, 'IndexError')
])
def test_linked_list_get_error(index, expected):
    linked_list = LinkedList()
    with pytest.raises(IndexError):
        linked_list.get(index)

import pytest
from data.input_code.d03_linked_list import *

def test_linked_list_get_zero_on_empty():
    linked_list = LinkedList()
    with pytest.raises(IndexError):
        linked_list.get(0)

import pytest
from data.input_code.d03_linked_list import *

@pytest.mark.parametrize('data, expected', [
    (2, [1, 2])
])
def test_linked_list_append_else(data, expected):
    linked_list = LinkedList()
    linked_list.append(1)
    linked_list.append(data)
    assert linked_list.to_list() == expected

@pytest.mark.parametrize('data, expected', [
    (1, True)
])
def test_linked_list_delete_head(data, expected):
    linked_list = LinkedList()
    linked_list.append(1)
    linked_list.append(2)
    result = linked_list.delete(data)
    assert result == expected
    assert linked_list.to_list() == [2]

@pytest.mark.parametrize('data, expected', [
    (2, True)
])
def test_linked_list_delete_middle(data, expected):
    linked_list = LinkedList()
    linked_list.append(1)
    linked_list.append(2)
    linked_list.append(3)
    result = linked_list.delete(data)
    assert result == expected
    assert linked_list.to_list() == [1, 3]

@pytest.mark.parametrize('data, expected', [
    (3, 2)
])
def test_linked_list_find_non_empty(data, expected):
    linked_list = LinkedList()
    linked_list.append(1)
    linked_list.append(2)
    linked_list.append(3)
    result = linked_list.find(data)
    assert result == expected

@pytest.mark.parametrize('index, expected', [
    (1, 2)
])
def test_linked_list_get_valid(index, expected):
    linked_list = LinkedList()
    linked_list.append(1)
    linked_list.append(2)
    linked_list.append(3)
    result = linked_list.get(index)
    assert result == expected

@pytest.mark.parametrize('data, seed, expected', [
    (1, [2], [1, 2])
])
def test_linked_list_prepend_non_empty(data, seed, expected):
    linked_list = LinkedList()
    for s in seed:
        linked_list.append(s)
    linked_list.prepend(data)
    assert linked_list.to_list() == expected

@pytest.mark.parametrize('data, seed, expected', [
    (3, [1, 2, 3], True)
])
def test_linked_list_delete_tail(data, seed, expected):
    linked_list = LinkedList()
    for s in seed:
        linked_list.append(s)
    result = linked_list.delete(data)
    assert result == expected
    assert linked_list.to_list() == seed[:-1]

@pytest.mark.parametrize('data, seed, expected', [
    (4, [1, 2], False)
])
def test_linked_list_delete_not_found_non_empty(data, seed, expected):
    linked_list = LinkedList()
    for s in seed:
        linked_list.append(s)
    result = linked_list.delete(data)
    assert result == expected
    assert linked_list.to_list() == seed

@pytest.mark.parametrize('index, seed, expected', [
    (2, [10, 20, 30], 30)
])
def test_linked_list_get_last_elem(index, seed, expected):
    linked_list = LinkedList()
    for s in seed:
        linked_list.append(s)
    result = linked_list.get(index)
    assert result == expected

@pytest.mark.parametrize('data, seed, expected', [
    (5, [5, 6, 7], 0)
])
def test_linked_list_find_first_elem(data, seed, expected):
    linked_list = LinkedList()
    for s in seed:
        linked_list.append(s)
    result = linked_list.find(data)
    assert result == expected

@pytest.mark.parametrize('index, seed, expected', [
    (0, [10, 20, 30], 10)
])
def test_linked_list_get_first_elem(index, seed, expected):
    linked_list = LinkedList()
    for s in seed:
        linked_list.append(s)
    result = linked_list.get(index)
    assert result == expected