import pytest
from data.input_code.d02_stack import *

@pytest.mark.parametrize('target, method, expected', [
    ('Stack', 'is_empty', True),
    ('Stack', '__len__', 0),
    ('Stack', 'size', 0),
    ('Queue', 'is_empty', True),
    ('Queue', '__len__', 0),
    ('Queue', 'size', 0),
])
def test_init(target, method, expected):
    if target == 'Stack':
        obj = Stack()
    else:
        obj = Queue()
    assert getattr(obj, method)() == expected

@pytest.mark.parametrize('target, method, item, expected', [
    ('Stack', '__contains__', 1, False),
    ('Queue', '__contains__', 'x', False),
])
def test_contains_init(target, method, item, expected):
    if target == 'Stack':
        obj = Stack()
    else:
        obj = Queue()
    assert getattr(obj, method)(item) == expected

@pytest.mark.parametrize('target, method, expected_exception', [
    ('Stack', 'pop', IndexError),
    ('Stack', 'peek', IndexError),
    ('Queue', 'dequeue', IndexError),
    ('Queue', 'front', IndexError),
])
def test_empty_operations(target, method, expected_exception):
    if target == 'Stack':
        obj = Stack()
    else:
        obj = Queue()
    with pytest.raises(expected_exception):
        getattr(obj, method)()

@pytest.mark.parametrize('target, method', [
    ('Stack', 'clear'),
    ('Queue', 'clear'),
])
def test_clear(target, method):
    if target == 'Stack':
        obj = Stack()
    else:
        obj = Queue()
    getattr(obj, method)()
    assert getattr(obj, 'is_empty')() == True

import pytest
from data.input_code.d02_stack import *

@pytest.mark.parametrize('target, item, expected', [
    ('Stack', 42, None),
    ('Queue', 'task', None),
])
def test_new_operations(target, item, expected):
    if target == 'Stack':
        obj = Stack()
    else:
        obj = Queue()
    assert getattr(obj, 'push' if target == 'Stack' else 'enqueue')(item) == expected

import pytest
from data.input_code.d02_stack import *

@pytest.mark.parametrize('target, items, expected', [
    ('Stack', [1, 2, 3], [1, 2, 3]),
    ('Queue', ['a', 'b', 'c'], ['a', 'b', 'c']),
])
def test_multiple_operations(target, items, expected):
    if target == 'Stack':
        obj = Stack()
        for item in items:
            obj.push(item)
        assert obj._items == expected
    else:
        obj = Queue()
        for item in items:
            obj.enqueue(item)
        assert obj._items == expected

@pytest.mark.parametrize('target, item, expected_len', [
    ('Stack', 'x', 1),
    ('Queue', 42, 1),
])
def test_len_after_add(target, item, expected_len):
    if target == 'Stack':
        obj = Stack()
        obj.push(item)
    else:
        obj = Queue()
        obj.enqueue(item)
    assert len(obj) == expected_len

@pytest.mark.parametrize('target, item, expected_contains', [
    ('Stack', 10, True),
    ('Queue', 'test', True),
])
def test_contains_after_add(target, item, expected_contains):
    if target == 'Stack':
        obj = Stack()
        obj.push(item)
    else:
        obj = Queue()
        obj.enqueue(item)
    assert (item in obj) == expected_contains

@pytest.mark.parametrize('target, initial_items, expected', [
    ('Stack', [1, 2, 3], 3),
    ('Queue', ['a', 'b', 'c'], 'a'),
])
def test_pop_dequeue(target, initial_items, expected):
    if target == 'Stack':
        obj = Stack()
        for item in initial_items:
            obj.push(item)
        assert obj.pop() == expected
    else:
        obj = Queue()
        for item in initial_items:
            obj.enqueue(item)
        assert obj.dequeue() == expected

@pytest.mark.parametrize('target, initial_items, expected', [
    ('Stack', [1, 2, 3], 3),
    ('Queue', ['a', 'b', 'c'], 'a'),
])
def test_peek_front(target, initial_items, expected):
    if target == 'Stack':
        obj = Stack()
        for item in initial_items:
            obj.push(item)
        assert obj.peek() == expected
    else:
        obj = Queue()
        for item in initial_items:
            obj.enqueue(item)
        assert obj.front() == expected