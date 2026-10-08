import pytest
from data.input_code.d02_stack import *

@pytest.mark.parametrize('target, input, expected', [
    ('Stack.push', {'item': 5}, None),
    ('Queue.enqueue', {'item': 'a'}, None),
    ('Queue.clear', {}, None),
])
def test_methods_do_not_raise(target, input, expected):
    if target.startswith('Stack'):
        obj = Stack()
    else:
        obj = Queue()
    method = getattr(obj, target.split('.')[1])
    method(**input)

@pytest.mark.parametrize('target, input, expected_exception', [
    ('Stack.pop', {}, IndexError),
    ('Stack.peek', {}, IndexError),
    ('Queue.dequeue', {}, IndexError),
    ('Queue.front', {}, IndexError),
])
def test_methods_raise_exception(target, input, expected_exception):
    if target.startswith('Stack'):
        obj = Stack()
    else:
        obj = Queue()
    method = getattr(obj, target.split('.')[1])
    with pytest.raises(expected_exception):
        method(**input)

@pytest.mark.parametrize('target, input, expected', [
    ('Stack.is_empty', {}, True),
    ('Stack.size', {}, 0),
    ('Stack.__len__', {}, 0),
    ('Stack.__contains__', {'item': 0}, False),
    ('Queue.is_empty', {}, True),
    ('Queue.size', {}, 0),
    ('Queue.__len__', {}, 0),
    ('Queue.__contains__', {'item': 'x'}, False),
])
def test_methods_return_expected(target, input, expected):
    if target.startswith('Stack'):
        obj = Stack()
    else:
        obj = Queue()
    method = getattr(obj, target.split('.')[1])
    result = method(**input)
    assert result == expected

@pytest.mark.parametrize('target, input, expected', [
    ('Stack.peek', {}, 5),
    ('Stack.pop', {}, 5),
    ('Stack.__contains__', {'item': 5}, True),
    ('Stack.clear', {}, None),
    ('Queue.__contains__', {'item': 1}, True),
    ('Queue.front', {}, 1),
    ('Queue.dequeue', {}, 1),
])
def test_new_methods_return_expected(target, input, expected):
    if target.startswith('Stack'):
        obj = Stack()
        obj.push(5)
    else:
        obj = Queue()
        obj.enqueue(1)
    method = getattr(obj, target.split('.')[1])
    result = method(**input)
    if isinstance(expected, bool):
        assert result == expected
    elif expected is None:
        assert result is expected
    else:
        assert result == expected

@pytest.mark.parametrize('target, input', [
    ('Stack.clear', {}),
])
def test_new_methods_do_not_raise(target, input):
    obj = Stack()
    obj.push(5)
    method = getattr(obj, target.split('.')[1])
    method(**input)