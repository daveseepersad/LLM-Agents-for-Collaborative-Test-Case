import pytest
from data.input_code.d02_stack import *

def test_stack_behavior():
    # Initialization
    stack = Stack()
    assert stack.is_empty() is True
    assert stack.size() == 0
    assert len(stack) == 0
    assert stack._items == []

    # Errors on empty stack
    with pytest.raises(IndexError):
        stack.pop()
    with pytest.raises(IndexError):
        stack.peek()

    # Push and state checks
    stack.push(5)
    assert stack.is_empty() is False
    assert stack.size() == 1
    assert len(stack) == 1
    assert stack.peek() == 5
    assert 5 in stack
    assert 10 not in stack

    # Pop and post‑pop state
    assert stack.pop() == 5
    assert stack.is_empty() is True
    assert stack.size() == 0
    assert len(stack) == 0

    # Clear after push
    stack.push(5)
    stack.clear()
    assert stack.is_empty() is True
    assert stack.size() == 0
    assert len(stack) == 0
    assert stack._items == []


def test_queue_behavior():
    # Initialization
    queue = Queue()
    assert queue.is_empty() is True
    assert queue.size() == 0
    assert len(queue) == 0
    assert queue._items == []

    # Errors on empty queue
    with pytest.raises(IndexError):
        queue.dequeue()
    with pytest.raises(IndexError):
        queue.front()

    # Enqueue and state checks
    queue.enqueue(5)
    assert queue.is_empty() is False
    assert queue.size() == 1
    assert len(queue) == 1
    assert queue.front() == 5
    assert 5 in queue
    assert 10 not in queue

    # Dequeue and post‑dequeue state
    assert queue.dequeue() == 5
    assert queue.is_empty() is True
    assert queue.size() == 0
    assert len(queue) == 0

    # Clear after enqueue
    queue.enqueue(5)
    queue.clear()
    assert queue.is_empty() is True
    assert queue.size() == 0
    assert len(queue) == 0
    assert queue._items == []