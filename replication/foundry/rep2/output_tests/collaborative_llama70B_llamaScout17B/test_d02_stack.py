import pytest
from data.input_code.d02_stack import *

@pytest.mark.parametrize('target, input_args, expected', [
    ('Stack.__init__', [], None),
    ('Queue.__init__', [], None),
])
def test_init(target, input_args, expected):
    if target == 'Stack.__init__':
        instance = Stack(*input_args)
    elif target == 'Queue.__init__':
        instance = Queue(*input_args)
    if expected is None:
        assert instance is not None
    else:
        assert instance == expected

@pytest.mark.parametrize('input_args, expected', [
    ([1], None),
])
def test_stack_push(input_args, expected):
    stack = Stack()
    stack.push(*input_args)
    assert stack.size() == 1

def test_stack_pop_empty():
    stack = Stack()
    with pytest.raises(IndexError):
        stack.pop()

def test_stack_pop():
    stack = Stack()
    stack.push(1)
    assert stack.pop() == 1

def test_stack_peek_empty():
    stack = Stack()
    with pytest.raises(IndexError):
        stack.peek()

def test_stack_peek():
    stack = Stack()
    stack.push(1)
    assert stack.peek() == 1

@pytest.mark.parametrize('input_args, expected', [
    ([], True),
    ([1], False),
])
def test_stack_is_empty(input_args, expected):
    stack = Stack()
    if input_args:
        stack.push(input_args[0])
    assert stack.is_empty() == expected

@pytest.mark.parametrize('input_args, expected', [
    ([], 0),
    ([1], 1),
])
def test_stack_size(input_args, expected):
    stack = Stack()
    if input_args:
        stack.push(input_args[0])
    assert stack.size() == expected

def test_stack_clear():
    stack = Stack()
    stack.push(1)
    stack.clear()
    assert stack.is_empty()

@pytest.mark.parametrize('item, expected', [
    (1, False),
    (1, True),
])
def test_stack_contains(item, expected):
    stack = Stack()
    if expected:
        stack.push(item)
    assert (item in stack) == expected

@pytest.mark.parametrize('input_args, expected', [
    ([1], None),
])
def test_queue_enqueue(input_args, expected):
    queue = Queue()
    queue.enqueue(*input_args)
    assert queue.size() == 1

def test_queue_dequeue_empty():
    queue = Queue()
    with pytest.raises(IndexError):
        queue.dequeue()

def test_queue_dequeue():
    queue = Queue()
    queue.enqueue(1)
    assert queue.dequeue() == 1

def test_queue_front_empty():
    queue = Queue()
    with pytest.raises(IndexError):
        queue.front()

def test_queue_front():
    queue = Queue()
    queue.enqueue(1)
    assert queue.front() == 1

@pytest.mark.parametrize('input_args, expected', [
    ([], True),
    ([1], False),
])
def test_queue_is_empty(input_args, expected):
    queue = Queue()
    if input_args:
        queue.enqueue(input_args[0])
    assert queue.is_empty() == expected

@pytest.mark.parametrize('input_args, expected', [
    ([], 0),
    ([1], 1),
])
def test_queue_size(input_args, expected):
    queue = Queue()
    if input_args:
        queue.enqueue(input_args[0])
    assert queue.size() == expected

def test_queue_clear():
    queue = Queue()
    queue.enqueue(1)
    queue.clear()
    assert queue.is_empty()

@pytest.mark.parametrize('item, expected', [
    (1, False),
    (1, True),
])
def test_queue_contains(item, expected):
    queue = Queue()
    if expected:
        queue.enqueue(item)
    assert (item in queue) == expected

import pytest
from data.input_code.d02_stack import *

def test_stack_len():
    stack = Stack()
    assert len(stack) == 0

def test_queue_len():
    queue = Queue()
    assert len(queue) == 0

def test_stack_multiple_push():
    stack = Stack()
    stack.push(1)
    stack.push(2)
    stack.push(3)
    assert stack.size() == 3

def test_queue_multiple_enqueue():
    queue = Queue()
    queue.enqueue(1)
    queue.enqueue(2)
    queue.enqueue(3)
    assert queue.size() == 3

def test_stack_multiple_pop():
    stack = Stack()
    stack.push(1)
    stack.push(2)
    stack.push(3)
    assert [stack.pop() for _ in range(3)] == [3, 2, 1]

def test_queue_multiple_dequeue():
    queue = Queue()
    queue.enqueue(1)
    queue.enqueue(2)
    queue.enqueue(3)
    assert [queue.dequeue() for _ in range(3)] == [1, 2, 3]