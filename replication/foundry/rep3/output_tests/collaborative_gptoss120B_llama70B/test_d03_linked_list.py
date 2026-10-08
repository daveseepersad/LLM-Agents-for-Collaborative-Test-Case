import pytest
from data.input_code.d03_linked_list import LinkedList, Node

@pytest.mark.parametrize('list_state, data', [
    ([], 1),
    ([1], 2)
])
def test_append(list_state, data):
    linked_list = LinkedList()
    for item in list_state:
        linked_list.append(item)
    linked_list.append(data)
    assert linked_list.to_list() == list_state + [data]

@pytest.mark.parametrize('list_state, data', [
    ([], 5),
    ([1], 0)
])
def test_prepend(list_state, data):
    linked_list = LinkedList()
    for item in list_state:
        linked_list.append(item)
    linked_list.prepend(data)
    assert linked_list.to_list() == [data] + list_state

@pytest.mark.parametrize('list_state, data, expected', [
    ([], 1, False),
    ([1, 2, 3], 1, True),
    ([1, 2, 3], 2, True),
    ([1, 2, 3], 3, True),
    ([1, 2, 3], 4, False)
])
def test_delete(list_state, data, expected):
    linked_list = LinkedList()
    for item in list_state:
        linked_list.append(item)
    assert linked_list.delete(data) == expected

@pytest.mark.parametrize('list_state, data, expected', [
    ([7, 8, 9], 7, 0),
    ([7, 8, 9], 9, 2),
    ([7, 8, 9], 5, -1)
])
def test_find(list_state, data, expected):
    linked_list = LinkedList()
    for item in list_state:
        linked_list.append(item)
    assert linked_list.find(data) == expected

@pytest.mark.parametrize('list_state, index, expected', [
    ([10, 20, 30], 0, 10),
    ([10, 20, 30], 2, 30)
])
def test_get(list_state, index, expected):
    linked_list = LinkedList()
    for item in list_state:
        linked_list.append(item)
    assert linked_list.get(index) == expected

@pytest.mark.parametrize('list_state, index', [
    ([10, 20], -1),
    ([10, 20], 2)
])
def test_get_error(list_state, index):
    linked_list = LinkedList()
    for item in list_state:
        linked_list.append(item)
    with pytest.raises(IndexError):
        linked_list.get(index)

@pytest.mark.parametrize('list_state, expected', [
    ([], []),
    ([1, 2, 3], [1, 2, 3])
])
def test_to_list(list_state, expected):
    linked_list = LinkedList()
    for item in list_state:
        linked_list.append(item)
    assert linked_list.to_list() == expected

@pytest.mark.parametrize('list_state, expected', [
    ([], 0),
    ([1, 2, 3, 4], 4)
])
def test_len(list_state, expected):
    linked_list = LinkedList()
    for item in list_state:
        linked_list.append(item)
    assert len(linked_list) == expected

def test_find_none():
    linked_list = LinkedList()
    linked_list.append(None)
    linked_list.append(1)
    assert linked_list.find(None) == 0