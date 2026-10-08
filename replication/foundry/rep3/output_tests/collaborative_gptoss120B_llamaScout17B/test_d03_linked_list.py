import pytest
from data.input_code.d03_linked_list import *

@pytest.mark.parametrize('initial, data, expected_list, expected_size', [
    ([], 1, [1], 1),
    ([1], 2, [1, 2], 2)
])
def test_append(initial, data, expected_list, expected_size):
    linked_list = LinkedList()
    for item in initial:
        linked_list.append(item)
    linked_list.append(data)
    assert linked_list.to_list() == expected_list
    assert len(linked_list) == expected_size

@pytest.mark.parametrize('initial, data, expected_list, expected_size', [
    ([], 5, [5], 1),
    ([5], 3, [3, 5], 2)
])
def test_prepend(initial, data, expected_list, expected_size):
    linked_list = LinkedList()
    for item in initial:
        linked_list.append(item)
    linked_list.prepend(data)
    assert linked_list.to_list() == expected_list
    assert len(linked_list) == expected_size

@pytest.mark.parametrize('initial, data, expected_result, expected_list, expected_size', [
    ([], 10, False, [], 0),
    ([7, 8, 9], 7, True, [8, 9], 2),
    ([1, 2, 3, 4], 3, True, [1, 2, 4], 3),
    ([10, 20, 30], 30, True, [10, 20], 2),
    ([4, 5, 6], 99, False, [4, 5, 6], 3)
])
def test_delete(initial, data, expected_result, expected_list, expected_size):
    linked_list = LinkedList()
    for item in initial:
        linked_list.append(item)
    result = linked_list.delete(data)
    assert result == expected_result
    assert linked_list.to_list() == expected_list
    assert len(linked_list) == expected_size

@pytest.mark.parametrize('initial, data, expected', [
    ([], 1, -1),
    ([42, 99, 100], 42, 0),
    ([5, 6, 7], 7, 2)
])
def test_find(initial, data, expected):
    linked_list = LinkedList()
    for item in initial:
        linked_list.append(item)
    assert linked_list.find(data) == expected

@pytest.mark.parametrize('initial, index, expected', [
    ([11, 22, 33], 0, 11),
    ([11, 22, 33], 2, 33)
])
def test_get_valid(initial, index, expected):
    linked_list = LinkedList()
    for item in initial:
        linked_list.append(item)
    assert linked_list.get(index) == expected

@pytest.mark.parametrize('initial, index', [
    ([1, 2], -1),
    ([1, 2], 2)
])
def test_get_invalid(initial, index):
    linked_list = LinkedList()
    for item in initial:
        linked_list.append(item)
    with pytest.raises(IndexError):
        linked_list.get(index)

@pytest.mark.parametrize('initial, expected', [
    ([], []),
    ([9, 8, 7], [9, 8, 7])
])
def test_to_list(initial, expected):
    linked_list = LinkedList()
    for item in initial:
        linked_list.append(item)
    assert linked_list.to_list() == expected

def test_len():
    linked_list = LinkedList()
    linked_list.append(1)
    linked_list.append(2)
    linked_list.append(3)
    linked_list.append(4)
    assert len(linked_list) == 4