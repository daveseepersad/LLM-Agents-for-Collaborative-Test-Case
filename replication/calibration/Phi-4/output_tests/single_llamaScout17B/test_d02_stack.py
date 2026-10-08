import pytest
from data.input_code.d02_stack import Stack, Queue

# Stack Tests

def test_stack_initialization():
    stack = Stack()
    assert stack.is_empty() is True
    assert stack.size() == 0

def test_stack_push():
    stack = Stack()
    stack.push(1)
    assert stack.size() == 1
    assert 1 in stack

def test_stack_pop():
    stack = Stack()
    stack.push(1)
    stack.push(2)
    assert stack.pop() == 2
    assert stack.size() == 1

def test_stack_pop_empty():
    stack = Stack()
    with pytest.raises(IndexError, match="Pop from empty stack"):
        stack.pop()

def test_stack_peek():
    stack = Stack()
    stack.push(1)
    assert stack.peek() == 1

def test_stack_peek_empty():
    stack = Stack()
    with pytest.raises(IndexError, match="Peek from empty stack"):
        stack.peek()

def test_stack_is_empty():
    stack = Stack()
    assert stack.is_empty() is True
    stack.push(1)
    assert stack.is_empty() is False

def test_stack_size():
    stack = Stack()
    assert stack.size() == 0
    stack.push(1)
    stack.push(2)
    assert stack.size() == 2

def test_stack_clear():
    stack = Stack()
    stack.push(1)
    stack.push(2)
    stack.clear()
    assert stack.is_empty() is True
    assert stack.size() == 0

def test_stack_len():
    stack = Stack()
    assert len(stack) == 0
    stack.push(1)
    assert len(stack) == 1

def test_stack_contains():
    stack = Stack()
    stack.push(1)
    assert 1 in stack
    assert 2 not in stack

# Queue Tests

def test_queue_initialization():
    queue = Queue()
    assert queue.is_empty() is True
    assert queue.size() == 0

def test_queue_enqueue():
    queue = Queue()
    queue.enqueue(1)
    assert queue.size() == 1
    assert 1 in queue

def test_queue_dequeue():
    queue = Queue()
    queue.enqueue(1)
    queue.enqueue(2)
    assert queue.dequeue() == 1
    assert queue.size() == 1

def test_queue_dequeue_empty():
    queue = Queue()
    with pytest.raises(IndexError, match="Dequeue from empty queue"):
        queue.dequeue()

def test_queue_front():
    queue = Queue()
    queue.enqueue(1)
    assert queue.front() == 1

def test_queue_front_empty():
    queue = Queue()
    with pytest.raises(IndexError, match="Front from empty queue"):
        queue.front()

def test_queue_is_empty():
    queue = Queue()
    assert queue.is_empty() is True
    queue.enqueue(1)
    assert queue.is_empty() is False

def test_queue_size():
    queue = Queue()
    assert queue.size() == 0
    queue.enqueue(1)
    queue.enqueue(2)
    assert queue.size() == 2

def test_queue_clear():
    queue = Queue()
    queue.enqueue(1)
    queue.enqueue(2)
    queue.clear()
    assert queue.is_empty() is True
    assert queue.size() == 0

def test_queue_len():
    queue = Queue()
    assert len(queue) == 0
    queue.enqueue(1)
    assert len(queue) == 1

def test_queue_contains():
    queue = Queue()
    queue.enqueue(1)
    assert 1 in queue
    assert 2 not in queue