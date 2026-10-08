import pytest
from data.input_code.d02_stack import Stack, Queue

@pytest.mark.parametrize('target, expected', [
    ('Stack.pop', 'IndexError'),
    ('Stack.peek', 'IndexError'),
    ('Queue.dequeue', 'IndexError'),
    ('Queue.front', 'IndexError')
])
def test_empty_operations_raise(target, expected):
    if target == 'Stack.pop':
        stack = Stack()
        with pytest.raises(IndexError):
            stack.pop()
    elif target == 'Stack.peek':
        stack = Stack()
        with pytest.raises(IndexError):
            stack.peek()
    elif target == 'Queue.dequeue':
        queue = Queue()
        with pytest.raises(IndexError):
            queue.dequeue()
    elif target == 'Queue.front':
        queue = Queue()
        with pytest.raises(IndexError):
            queue.front()

@pytest.mark.parametrize('target, expected', [
    ('Stack.is_empty', True),
    ('Queue.is_empty', True)
])
def test_is_empty(target, expected):
    if target == 'Stack.is_empty':
        stack = Stack()
        assert stack.is_empty() == expected
    elif target == 'Queue.is_empty':
        queue = Queue()
        assert queue.is_empty() == expected

@pytest.mark.parametrize('target, expected', [
    ('Stack.size', 0),
    ('Queue.size', 0)
])
def test_size(target, expected):
    if target == 'Stack.size':
        stack = Stack()
        assert stack.size() == expected
    elif target == 'Queue.size':
        queue = Queue()
        assert queue.size() == expected

@pytest.mark.parametrize('target, expected', [
    ('Stack.__len__', 0),
    ('Queue.__len__', 0)
])
def test_len(target, expected):
    if target == 'Stack.__len__':
        stack = Stack()
        assert len(stack) == expected
    elif target == 'Queue.__len__':
        queue = Queue()
        assert len(queue) == expected

def test_clear():
    stack = Stack()
    queue = Queue()
    stack.clear()
    queue.clear()
    assert stack.size() == 0
    assert queue.size() == 0

@pytest.mark.parametrize('target, item, expected', [
    ('Stack.__contains__', None, False),
    ('Queue.__contains__', None, False)
])
def test_contains(target, item, expected):
    if target == 'Stack.__contains__':
        stack = Stack()
        assert (item in stack) == expected
    elif target == 'Queue.__contains__':
        queue = Queue()
        assert (item in queue) == expected

@pytest.mark.parametrize('target, initial, expected', [
    ('Stack.pop', [1, 2, 3], 3),
    ('Stack.peek', [1, 2, 3], 3)
])
def test_stack_operations_with_initial(target, initial, expected):
    if target == 'Stack.pop':
        stack = Stack()
        for item in initial:
            stack.push(item)
        assert stack.pop() == expected
    elif target == 'Stack.peek':
        stack = Stack()
        for item in initial:
            stack.push(item)
        assert stack.peek() == expected

@pytest.mark.parametrize('target, initial, item, expected', [
    ('Stack.__contains__', [4], 4, True),
    ('Queue.__contains__', [10], 10, True)
])
def test_contains_after_init(target, initial, item, expected):
    if target == 'Stack.__contains__':
        stack = Stack()
        for elem in initial:
            stack.push(elem)
        assert (item in stack) == expected
    elif target == 'Queue.__contains__':
        queue = Queue()
        for elem in initial:
            queue.enqueue(elem)
        assert (item in queue) == expected

@pytest.mark.parametrize('target, initial, expected', [
    ('Queue.front', [9, 8], 9),
    ('Queue.dequeue', [4, 5, 6], 4)
])
def test_queue_operations_with_initial(target, initial, expected):
    if target == 'Queue.front':
        queue = Queue()
        for item in initial:
            queue.enqueue(item)
        assert queue.front() == expected
    elif target == 'Queue.dequeue':
        queue = Queue()
        for item in initial:
            queue.enqueue(item)
        assert queue.dequeue() == expected