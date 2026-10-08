import pytest
from data.input_code.d03_linked_list import LinkedList, Node

@pytest.mark.parametrize('initial, data, expected', [
    ([], 10, {'to_list': [10], 'len': 1}),
    ([1], 2, {'to_list': [1, 2], 'len': 2})
])
def test_append(initial, data, expected):
    linked_list = LinkedList()
    for value in initial:
        linked_list.append(value)
    linked_list.append(data)
    assert linked_list.to_list() == expected['to_list']
    assert len(linked_list) == expected['len']

@pytest.mark.parametrize('initial, data, expected', [
    ([], 5, {'to_list': [5], 'len': 1}),
    ([7], 3, {'to_list': [3, 7], 'len': 2})
])
def test_prepend(initial, data, expected):
    linked_list = LinkedList()
    for value in initial:
        linked_list.append(value)
    linked_list.prepend(data)
    assert linked_list.to_list() == expected['to_list']
    assert len(linked_list) == expected['len']

@pytest.mark.parametrize('initial, data, expected', [
    ([], 99, False),
    ([4, 8, 12], 4, {'to_list': [8, 12], 'len': 2, 'return': True}),
    ([1, 2, 3], 3, {'to_list': [1, 2], 'len': 2, 'return': True}),
    ([5, 6, 7], 9, {'to_list': [5, 6, 7], 'len': 3, 'return': False})
])
def test_delete(initial, data, expected):
    linked_list = LinkedList()
    for value in initial:
        linked_list.append(value)
    if isinstance(expected, dict):
        result = linked_list.delete(data)
        assert linked_list.to_list() == expected['to_list']
        assert len(linked_list) == expected['len']
        assert result == expected['return']
    else:
        assert linked_list.delete(data) == expected

@pytest.mark.parametrize('initial, data, expected', [
    ([], 1, -1),
    ([42, 99], 42, 0),
    ([11, 22, 33], 33, 2),
    ([4, 5, 6], 7, -1)
])
def test_find(initial, data, expected):
    linked_list = LinkedList()
    for value in initial:
        linked_list.append(value)
    assert linked_list.find(data) == expected

@pytest.mark.parametrize('initial, index, expected', [
    ([100, 200, 300], 0, 100),
    ([10, 20, 30], 2, 30)
])
def test_get_valid(initial, index, expected):
    linked_list = LinkedList()
    for value in initial:
        linked_list.append(value)
    assert linked_list.get(index) == expected

@pytest.mark.parametrize('initial, index, expected', [
    ([1, 2], -1, 'IndexError'),
    ([1, 2], 2, 'IndexError')
])
def test_get_invalid(initial, index, expected):
    linked_list = LinkedList()
    for value in initial:
        linked_list.append(value)
    with pytest.raises(IndexError):
        linked_list.get(index)

@pytest.mark.parametrize('initial, expected', [
    ([], []),
    ([9, 8, 7], [9, 8, 7])
])
def test_to_list(initial, expected):
    linked_list = LinkedList()
    for value in initial:
        linked_list.append(value)
    assert linked_list.to_list() == expected

def test_len_after_operations():
    linked_list = LinkedList()
    linked_list.append(1)
    linked_list.append(2)
    linked_list.prepend(0)
    linked_list.delete(2)
    assert len(linked_list) == 2