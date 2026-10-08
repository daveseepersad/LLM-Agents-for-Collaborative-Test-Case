import pytest
from data.input_code.d02_stack import *

@pytest.mark.parametrize('target, input_args, expected, precondition', [
    ('Stack.__init__', {}, {'size': 0, 'is_empty': True}, None),
    ('Stack.push', {'item': 5}, None, None),
    ('Stack.pop', {}, 5, 'Stack.push(5)'),
    ('Stack.pop', {}, 'IndexError', None),
    ('Stack.peek', {}, 5, 'Stack.push(5)'),
    ('Stack.peek', {}, 'IndexError', None),
    ('Stack.is_empty', {}, True, None),
    ('Stack.is_empty', {}, False, 'Stack.push(5)'),
    ('Stack.size', {}, 1, 'Stack.push(5)'),
    ('Stack.clear', {}, {'size': 0, 'is_empty': True}, 'Stack.push(5)'),
    ('Stack.__len__', {}, 1, 'Stack.push(5)'),
    ('Stack.__contains__', {'item': 5}, True, 'Stack.push(5)'),
    ('Stack.__contains__', {'item': 10}, False, 'Stack.push(5)'),
    ('Queue.__init__', {}, {'size': 0, 'is_empty': True}, None),
    ('Queue.enqueue', {'item': 5}, None, None),
    ('Queue.dequeue', {}, 5, 'Queue.enqueue(5)'),
    ('Queue.dequeue', {}, 'IndexError', None),
    ('Queue.front', {}, 5, 'Queue.enqueue(5)'),
    ('Queue.front', {}, 'IndexError', None),
    ('Queue.is_empty', {}, True, None),
    ('Queue.is_empty', {}, False, 'Queue.enqueue(5)'),
    ('Queue.size', {}, 1, 'Queue.enqueue(5)'),
    ('Queue.clear', {}, {'size': 0, 'is_empty': True}, 'Queue.enqueue(5)'),
    ('Queue.__len__', {}, 1, 'Queue.enqueue(5)'),
    ('Queue.__contains__', {'item': 5}, True, 'Queue.enqueue(5)'),
    ('Queue.__contains__', {'item': 10}, False, 'Queue.enqueue(5)'),
])
def test_data_structures(target, input_args, expected, precondition):
    if target.startswith('Stack'):
        obj = Stack()
    else:
        obj = Queue()

    if precondition:
        eval(precondition.replace('Stack', 'obj').replace('Queue', 'obj'))

    if target.endswith('__init__'):
        result = {'size': obj.size(), 'is_empty': obj.is_empty()}
    elif target.endswith('push') or target.endswith('enqueue'):
        getattr(obj, target.split('.')[1])(**input_args)
        result = None
    elif target.endswith('pop') or target.endswith('dequeue') or target.endswith('peek') or target.endswith('front'):
        if isinstance(expected, str) and expected == 'IndexError':
            with pytest.raises(IndexError):
                getattr(obj, target.split('.')[1])()
            return  # Add return to avoid further assertions
        else:
            result = getattr(obj, target.split('.')[1])()
    elif target.endswith('is_empty') or target.endswith('size') or target.endswith('__len__'):
        result = getattr(obj, target.split('.')[1])()
    elif target.endswith('clear'):
        getattr(obj, target.split('.')[1])()
        result = {'size': obj.size(), 'is_empty': obj.is_empty()}
    elif target.endswith('__contains__'):
        result = getattr(obj, target.split('.')[1])(**input_args)

    if isinstance(expected, str) and expected == 'IndexError':
        assert False is False  # This line is never reached due to the return statement above
    elif expected is None:
        assert result is None
    elif isinstance(expected, dict):
        assert result == expected
    else:
        assert result == expected