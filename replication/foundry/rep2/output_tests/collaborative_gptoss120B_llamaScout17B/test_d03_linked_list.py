import pytest
from data.input_code.d03_linked_list import *

@pytest.mark.parametrize('setup, data, expected', [
    ([], 1, None),
    ([{"method": "append", "args": [1]}], 2, None)
])
def test_append(setup, data, expected):
    linked_list = LinkedList()
    for operation in setup:
        getattr(linked_list, operation['method'])(*operation['args'])
    linked_list.append(data)
    assert linked_list.to_list() == ([1] if not setup else [1, 2])

def test_prepend():
    linked_list = LinkedList()
    linked_list.append(10)
    linked_list.append(20)
    linked_list.prepend(5)
    assert linked_list.to_list() == [5, 10, 20]

@pytest.mark.parametrize('setup, data, expected', [
    ([], 99, False),
    ([{"method": "append", "args": [1]}, {"method": "append", "args": [2]}, {"method": "append", "args": [3]}], 1, True),
    ([{"method": "append", "args": [1]}, {"method": "append", "args": [2]}, {"method": "append", "args": [3]}], 2, True),
    ([{"method": "append", "args": [1]}, {"method": "append", "args": [2]}, {"method": "append", "args": [3]}], 99, False)
])
def test_delete(setup, data, expected):
    linked_list = LinkedList()
    for operation in setup:
        getattr(linked_list, operation['method'])(*operation['args'])
    assert linked_list.delete(data) == expected

@pytest.mark.parametrize('setup, data, expected', [
    ([{"method": "append", "args": ["a"]}, {"method": "append", "args": ["b"]}, {"method": "append", "args": ["c"]}], "b", 1),
    ([{"method": "append", "args": ["x"]}, {"method": "append", "args": ["y"]}, {"method": "append", "args": ["z"]}], "q", -1)
])
def test_find(setup, data, expected):
    linked_list = LinkedList()
    for operation in setup:
        getattr(linked_list, operation['method'])(*operation['args'])
    assert linked_list.find(data) == expected

@pytest.mark.parametrize('setup, index, expected', [
    ([{"method": "append", "args": [10]}, {"method": "append", "args": [20]}, {"method": "append", "args": [30]}], 0, 10),
    ([{"method": "append", "args": [10]}, {"method": "append", "args": [20]}, {"method": "append", "args": [30]}], 2, 30),
    ([{"method": "append", "args": [1]}, {"method": "append", "args": [2]}], -1, 'IndexError'),
    ([{"method": "append", "args": [1]}, {"method": "append", "args": [2]}], 2, 'IndexError')
])
def test_get(setup, index, expected):
    linked_list = LinkedList()
    for operation in setup:
        getattr(linked_list, operation['method'])(*operation['args'])
    if isinstance(expected, str) and expected == 'IndexError':
        with pytest.raises(IndexError):
            linked_list.get(index)
    else:
        assert linked_list.get(index) == expected

@pytest.mark.parametrize('setup, expected', [
    ([{"method": "prepend", "args": [5]}, {"method": "append", "args": [10]}, {"method": "append", "args": [15]}], 3),
    ([{"method": "prepend", "args": [5]}, {"method": "append", "args": [10]}, {"method": "append", "args": [15]}], [5, 10, 15])
])
def test_len_and_to_list(setup, expected):
    linked_list = LinkedList()
    for operation in setup:
        getattr(linked_list, operation['method'])(*operation['args'])
    if isinstance(expected, list):
        assert linked_list.to_list() == expected
    else:
        assert len(linked_list) == expected