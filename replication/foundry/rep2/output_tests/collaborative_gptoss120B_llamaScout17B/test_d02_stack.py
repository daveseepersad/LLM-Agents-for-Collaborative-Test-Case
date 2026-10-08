import pytest
from data.input_code.d02_stack import *

@pytest.mark.parametrize('item', [1])
def test_stack_push(item):
    stack = Stack()
    stack.push(item)
    assert stack.size() == 1

def test_stack_pop_ok():
    stack = Stack()
    stack.push(1)
    assert stack.pop() == 1

def test_stack_pop_err():
    stack = Stack()
    with pytest.raises(IndexError):
        stack.pop()

def test_stack_peek_ok():
    stack = Stack()
    stack.push(2)
    assert stack.peek() == 2

def test_stack_peek_err():
    stack = Stack()
    with pytest.raises(IndexError):
        stack.peek()

def test_stack_is_empty_true():
    stack = Stack()
    assert stack.is_empty() == True

def test_stack_is_empty_false():
    stack = Stack()
    stack.push(1)
    assert stack.is_empty() == False

def test_stack_size():
    stack = Stack()
    stack.push(1)
    stack.push(2)
    assert stack.size() == 2

def test_stack_clear():
    stack = Stack()
    stack.push(1)
    stack.clear()
    assert stack.is_empty()

def test_stack_len():
    stack = Stack()
    stack.push(1)
    stack.clear()
    assert len(stack) == 0

def test_stack_contains_true():
    stack = Stack()
    stack.push('x')
    assert 'x' in stack

def test_stack_contains_false():
    stack = Stack()
    assert 'y' not in stack

@pytest.mark.parametrize('item', [1])
def test_queue_enqueue(item):
    queue = Queue()
    queue.enqueue(item)
    assert queue.size() == 1

def test_queue_dequeue_ok():
    queue = Queue()
    queue.enqueue(1)
    assert queue.dequeue() == 1

def test_queue_dequeue_err():
    queue = Queue()
    with pytest.raises(IndexError):
        queue.dequeue()

def test_queue_front_ok():
    queue = Queue()
    queue.enqueue(2)
    assert queue.front() == 2

def test_queue_front_err():
    queue = Queue()
    with pytest.raises(IndexError):
        queue.front()

def test_queue_is_empty_true():
    queue = Queue()
    assert queue.is_empty() == True

def test_queue_is_empty_false():
    queue = Queue()
    queue.enqueue(1)
    assert queue.is_empty() == False

def test_queue_size():
    queue = Queue()
    queue.enqueue(1)
    queue.enqueue(2)
    assert queue.size() == 2

def test_queue_clear():
    queue = Queue()
    queue.enqueue(1)
    queue.clear()
    assert queue.is_empty()

def test_queue_len():
    queue = Queue()
    queue.enqueue(1)
    queue.clear()
    assert len(queue) == 0

def test_queue_contains_true():
    queue = Queue()
    queue.enqueue('a')
    assert 'a' in queue

def test_queue_contains_false():
    queue = Queue()
    assert 'b' not in queue