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

def test_prepend():
    linked_list = LinkedList()
    linked_list.append(1)
    linked_list.append(2)
    linked_list.prepend(0)
    assert linked_list.to_list() == [0, 1, 2]
    assert len(linked_list) == 3

@pytest.mark.parametrize('initial, data, expected_result, expected_list, expected_size', [
    ([], 10, False, [], 0),
    ([5, 6], 5, True, [6], 1),
    ([1, 2, 3], 2, True, [1, 3], 2),
    ([1, 3], 4, False, [1, 3], 2)
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
    ([1, 3], 3, 1),
    ([1, 3], 5, -1)
])
def test_find(initial, data, expected):
    linked_list = LinkedList()
    for item in initial:
        linked_list.append(item)
    assert linked_list.find(data) == expected

@pytest.mark.parametrize('initial, index, expected', [
    ([10, 20], 0, 10),
    ([10, 20], 1, 20)
])
def test_get_success(initial, index, expected):
    linked_list = LinkedList()
    for item in initial:
        linked_list.append(item)
    assert linked_list.get(index) == expected

@pytest.mark.parametrize('initial, index', [
    ([1], -1),
    ([1], 1)
])
def test_get_error(initial, index):
    linked_list = LinkedList()
    for item in initial:
        linked_list.append(item)
    with pytest.raises(IndexError):
        linked_list.get(index)

@pytest.mark.parametrize('initial, expected', [
    ([], []),
    ([7, 8, 9], [7, 8, 9])
])
def test_to_list(initial, expected):
    linked_list = LinkedList()
    for item in initial:
        linked_list.append(item)
    assert linked_list.to_list() == expected

def test_len():
    linked_list = LinkedList()
    operations = ["append", "append", "prepend", "delete"]
    values = [1, 2, 0, 1]
    for op, val in zip(operations, values):
        if op == "append":
            linked_list.append(val)
        elif op == "prepend":
            linked_list.prepend(val)
        elif op == "delete":
            linked_list.delete(val)
    assert len(linked_list) == 2