import pytest
from data.input_code.d02_stack import Stack, Queue

def test_stack_init():
    stack = Stack()
    assert stack.is_empty()
    assert len(stack) == 0

def test_stack_push():
    stack = Stack()
    stack.push(1)
    assert not stack.is_empty()
    assert len(stack) == 1
    assert stack.peek() == 1

def test_stack_pop():
    stack = Stack()
    stack.push(1)
    assert stack.pop() == 1
    assert stack.is_empty()

def test_stack_pop_empty():
    stack = Stack()
    with pytest.raises(IndexError):
        stack.pop()

def test_stack_peek():
    stack = Stack()
    stack.push(1)
    assert stack.peek() == 1

def test_stack_peek_empty():
    stack = Stack()
    with pytest.raises(IndexError):
        stack.peek()

def test_stack_clear():
    stack = Stack()
    stack.push(1)
    stack.clear()
    assert stack.is_empty()

def test_stack_contains():
    stack = Stack()
    stack.push(1)
    assert 1 in stack
    assert 2 not in stack

def test_queue_init():
    queue = Queue()
    assert queue.is_empty()
    assert len(queue) == 0

def test_queue_enqueue():
    queue = Queue()
    queue.enqueue(1)
    assert not queue.is_empty()
    assert len(queue) == 1
    assert queue.front() == 1

def test_queue_dequeue():
    queue = Queue()
    queue.enqueue(1)
    assert queue.dequeue() == 1
    assert queue.is_empty()

def test_queue_dequeue_empty():
    queue = Queue()
    with pytest.raises(IndexError):
        queue.dequeue()

def test_queue_front():
    queue = Queue()
    queue.enqueue(1)
    assert queue.front() == 1

def test_queue_front_empty():
    queue = Queue()
    with pytest.raises(IndexError):
        queue.front()

def test_queue_clear():
    queue = Queue()
    queue.enqueue(1)
    queue.clear()
    assert queue.is_empty()

def test_queue_contains():
    queue = Queue()
    queue.enqueue(1)
    assert 1 in queue
    assert 2 not in queue

def test_stack_size():
    stack = Stack()
    assert stack.size() == 0
    stack.push(1)
    assert stack.size() == 1
    stack.push(2)
    assert stack.size() == 2

def test_queue_size():
    queue = Queue()
    assert queue.size() == 0
    queue.enqueue(1)
    assert queue.size() == 1
    queue.enqueue(2)
    assert queue.size() == 2