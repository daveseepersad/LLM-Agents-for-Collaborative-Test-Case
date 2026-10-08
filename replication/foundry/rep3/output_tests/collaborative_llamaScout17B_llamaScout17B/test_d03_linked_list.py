import pytest
from data.input_code.d03_linked_list import *

@pytest.mark.parametrize('expected_head, expected_size', [
    (None, 0)
])
def test_linked_list_init(expected_head, expected_size):
    linked_list = LinkedList()
    assert linked_list.head == expected_head
    assert linked_list._size == expected_size

@pytest.mark.parametrize('data', [
    5
])
def test_linked_list_append_empty(data):
    linked_list = LinkedList()
    linked_list.append(data)
    assert linked_list.head.data == data
    assert linked_list._size == 1

@pytest.mark.parametrize('data, precondition_data', [
    (10, 5)
])
def test_linked_list_append_nonempty(data, precondition_data):
    linked_list = LinkedList()
    linked_list.append(precondition_data)
    linked_list.append(data)
    assert linked_list.to_list() == [precondition_data, data]

@pytest.mark.parametrize('data', [
    5
])
def test_linked_list_prepend_empty(data):
    linked_list = LinkedList()
    linked_list.prepend(data)
    assert linked_list.head.data == data
    assert linked_list._size == 1

@pytest.mark.parametrize('data, precondition_data', [
    (10, 5)
])
def test_linked_list_prepend_nonempty(data, precondition_data):
    linked_list = LinkedList()
    linked_list.append(precondition_data)
    linked_list.prepend(data)
    assert linked_list.to_list() == [data, precondition_data]

@pytest.mark.parametrize('data, expected', [
    (5, False)
])
def test_linked_list_delete_empty(data, expected):
    linked_list = LinkedList()
    assert linked_list.delete(data) == expected

@pytest.mark.parametrize('data, expected, precondition_data', [
    (5, True, 5)
])
def test_linked_list_delete_head(data, expected, precondition_data):
    linked_list = LinkedList()
    linked_list.append(precondition_data)
    assert linked_list.delete(data) == expected
    assert linked_list.to_list() == []

@pytest.mark.parametrize('data, expected, precondition_data_list', [
    (10, True, [5, 10, 15])
])
def test_linked_list_delete_middle(data, expected, precondition_data_list):
    linked_list = LinkedList()
    for precondition_data in precondition_data_list:
        linked_list.append(precondition_data)
    assert linked_list.delete(data) == expected
    assert linked_list.to_list() == [x for x in precondition_data_list if x != data]

@pytest.mark.parametrize('data, expected, precondition_data_list', [
    (15, True, [5, 10, 15])
])
def test_linked_list_delete_tail(data, expected, precondition_data_list):
    linked_list = LinkedList()
    for precondition_data in precondition_data_list:
        linked_list.append(precondition_data)
    assert linked_list.delete(data) == expected
    assert linked_list.to_list() == [x for x in precondition_data_list if x != data]

@pytest.mark.parametrize('data, expected, precondition_data_list', [
    (20, False, [5, 10, 15])
])
def test_linked_list_delete_nonexistent(data, expected, precondition_data_list):
    linked_list = LinkedList()
    for precondition_data in precondition_data_list:
        linked_list.append(precondition_data)
    assert linked_list.delete(data) == expected

@pytest.mark.parametrize('data, expected, precondition_data_list', [
    (10, 1, [5, 10, 15])
])
def test_linked_list_find_existent(data, expected, precondition_data_list):
    linked_list = LinkedList()
    for precondition_data in precondition_data_list:
        linked_list.append(precondition_data)
    assert linked_list.find(data) == expected

@pytest.mark.parametrize('data, expected, precondition_data_list', [
    (20, -1, [5, 10, 15])
])
def test_linked_list_find_nonexistent(data, expected, precondition_data_list):
    linked_list = LinkedList()
    for precondition_data in precondition_data_list:
        linked_list.append(precondition_data)
    assert linked_list.find(data) == expected

@pytest.mark.parametrize('index, expected, precondition_data_list', [
    (1, 10, [5, 10, 15])
])
def test_linked_list_get_valid_index(index, expected, precondition_data_list):
    linked_list = LinkedList()
    for precondition_data in precondition_data_list:
        linked_list.append(precondition_data)
    assert linked_list.get(index) == expected

@pytest.mark.parametrize('index, expected_exception', [
    (-1, IndexError),
    (3, IndexError)
])
def test_linked_list_get_invalid_index(index, expected_exception):
    linked_list = LinkedList()
    if index >= 0:
        linked_list.append(5)
        linked_list.append(10)
        linked_list.append(15)
    with pytest.raises(expected_exception):
        linked_list.get(index)

@pytest.mark.parametrize('expected, precondition_data_list', [
    ([], []),
    ([5, 10, 15], [5, 10, 15])
])
def test_linked_list_to_list(expected, precondition_data_list):
    linked_list = LinkedList()
    for precondition_data in precondition_data_list:
        linked_list.append(precondition_data)
    assert linked_list.to_list() == expected

@pytest.mark.parametrize('expected, precondition_data_list', [
    (0, []),
    (3, [5, 10, 15])
])
def test_linked_list_len(expected, precondition_data_list):
    linked_list = LinkedList()
    for precondition_data in precondition_data_list:
        linked_list.append(precondition_data)
    assert len(linked_list) == expected