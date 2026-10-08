import pytest
from data.input_code.d02_stack import *

@pytest.mark.parametrize('method_name, expected', [
    ('is_empty', True),
    ('__len__', 0),
    ('size', 0)
])
def test_stack_initial_state(method_name, expected):
    stack = Stack()
    result = getattr(stack, method_name)()
    if isinstance(expected, bool):
        assert result == expected
    else:
        assert result == expected

def test_stack_peek_on_empty():
    stack = Stack()
    with pytest.raises(IndexError):
        stack.peek()

def test_stack_pop_on_empty():
    stack = Stack()
    with pytest.raises(IndexError):
        stack.pop()

def test_stack_contains_on_empty():
    stack = Stack()
    assert 1 not in stack

def test_stack_clear():
    stack = Stack()
    stack.clear()
    assert stack.is_empty()

@pytest.mark.parametrize('method_name, expected', [
    ('is_empty', True),
    ('__len__', 0),
    ('size', 0)
])
def test_queue_initial_state(method_name, expected):
    queue = Queue()
    result = getattr(queue, method_name)()
    if isinstance(expected, bool):
        assert result == expected
    else:
        assert result == expected

def test_queue_dequeue_on_empty():
    queue = Queue()
    with pytest.raises(IndexError):
        queue.dequeue()

def test_queue_front_on_empty():
    queue = Queue()
    with pytest.raises(IndexError):
        queue.front()

def test_queue_contains_on_empty():
    queue = Queue()
    assert 5 not in queue

def test_queue_clear():
    queue = Queue()
    queue.clear()
    assert queue.is_empty()

def test_stack_non_empty_sequence():
    stack = Stack()
    stack.push(1)
    stack.push(2)
    assert stack.peek() == 2
    assert stack.pop() == 2
    assert stack.peek() == 1
    assert (1 in stack) is True
    assert (3 in stack) is False

def test_queue_fifo_sequence():
    queue = Queue()
    queue.enqueue("a")
    queue.enqueue("b")
    assert queue.front() == "a"
    assert queue.dequeue() == "a"
    assert queue.dequeue() == "b"
    assert queue.is_empty() is True