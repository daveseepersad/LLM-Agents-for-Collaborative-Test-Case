import pytest
from data.input_code.d02_stack import *

@pytest.mark.parametrize('target, input_args, expected, precondition', [
    ('Stack.__init__', [], {'size': 0, '_items': []}, None),
    ('Stack.push', [5], None, None),
    ('Stack.pop', [], 5, 'push(5)'),
    ('Stack.peek', [], 5, 'push(5)'),
    ('Stack.is_empty', [], True, None),
    ('Stack.is_empty', [], False, 'push(5)'),
    ('Stack.size', [], 1, 'push(5)'),
    ('Stack.clear', [], None, None),
    ('Stack.__len__', [], 1, 'push(5)'),
    ('Stack.__contains__', [5], True, 'push(5)'),
    ('Stack.__contains__', [10], False, 'push(5)'),
    ('Queue.__init__', [], {'size': 0, '_items': []}, None),
    ('Queue.enqueue', [5], None, None),
    ('Queue.dequeue', [], 5, 'enqueue(5)'),
    ('Queue.front', [], 5, 'enqueue(5)'),
    ('Queue.is_empty', [], True, None),
    ('Queue.is_empty', [], False, 'enqueue(5)'),
    ('Queue.size', [], 1, 'enqueue(5)'),
    ('Queue.clear', [], None, None),
    ('Queue.__len__', [], 1, 'enqueue(5)'),
    ('Queue.__contains__', [5], True, 'enqueue(5)'),
    ('Queue.__contains__', [10], False, 'enqueue(5)'),
])
def test_data_structures(target, input_args, expected, precondition):
    if target.startswith('Stack'):
        obj = Stack()
    else:
        obj = Queue()

    if precondition:
        for action in precondition.split(';'):
            precondition_method, *precondition_args = action.split('(')
            precondition_args = precondition_args[0].strip(')').split(', ')
            precondition_args = [int(arg) if arg.isdigit() else arg for arg in precondition_args]
            getattr(obj, precondition_method)(*precondition_args)

    method_name = target.split('.')[-1]
    if method_name == '__init__':
        if isinstance(expected, dict):
            assert obj.size() == expected['size']
            assert obj._items == expected['_items']
        else:
            assert obj == expected
    else:
        method = getattr(obj, method_name)
        if isinstance(expected, str) and expected.endswith('Error'):
            with pytest.raises(eval(expected)):
                method(*input_args)
        else:
            result = method(*input_args)
            if isinstance(expected, dict):
                assert {'size': obj.size(), '_items': obj._items} == expected
            else:
                assert result == expected

import pytest
from data.input_code.d02_stack import *

@pytest.mark.parametrize('target, input_args, expected, precondition', [
    ('Stack.pop', [], 'IndexError', None),
    ('Stack.peek', [], 'IndexError', None),
    ('Queue.dequeue', [], 'IndexError', None),
    ('Queue.front', [], 'IndexError', None),
])
def test_new_data_structures(target, input_args, expected, precondition):
    if target.startswith('Stack'):
        obj = Stack()
    else:
        obj = Queue()

    if precondition:
        for action in precondition.split(';'):
            precondition_method, *precondition_args = action.split('(')
            precondition_args = precondition_args[0].strip(')').split(', ')
            precondition_args = [int(arg) if arg.isdigit() else arg for arg in precondition_args]
            getattr(obj, precondition_method)(*precondition_args)

    method_name = target.split('.')[-1]
    method = getattr(obj, method_name)
    with pytest.raises(eval(expected)):
        method(*input_args)