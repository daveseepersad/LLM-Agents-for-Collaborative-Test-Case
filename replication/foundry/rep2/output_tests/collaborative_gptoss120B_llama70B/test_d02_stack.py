import pytest
from data.input_code.d02_stack import *

@pytest.fixture
def stack():
    return Stack()

@pytest.fixture
def queue():
    return Queue()

@pytest.mark.parametrize('expected', [
    (True)
])
def test_stack_is_empty(stack, expected):
    assert stack.is_empty() == expected

def test_stack_push(stack):
    stack.push(5)
    assert len(stack) == 1

def test_stack_size(stack):
    stack.push(5)
    assert stack.size() == 1

def test_stack_peek(stack):
    stack.push(5)
    assert stack.peek() == 5

def test_stack_pop(stack):
    stack.push(5)
    assert stack.pop() == 5

def test_stack_pop_error(stack):
    with pytest.raises(IndexError):
        stack.pop()

def test_stack_peek_error(stack):
    with pytest.raises(IndexError):
        stack.peek()

def test_stack_len(stack):
    stack.push(5)
    stack.push(2)
    stack.push(3)
    assert len(stack) == 3

def test_stack_contains(stack):
    stack.push(2)
    assert 2 in stack

def test_stack_not_contains(stack):
    stack.push(2)
    assert 99 not in stack

def test_stack_clear(stack):
    stack.push(5)
    stack.clear()
    assert len(stack) == 0

def test_stack_is_empty_after_clear(stack):
    stack.push(5)
    stack.clear()
    assert stack.is_empty()

@pytest.mark.parametrize('expected', [
    (True)
])
def test_queue_is_empty(queue, expected):
    assert queue.is_empty() == expected

def test_queue_enqueue(queue):
    queue.enqueue('a')
    assert len(queue) == 1

def test_queue_size(queue):
    queue.enqueue('a')
    assert queue.size() == 1

def test_queue_front(queue):
    queue.enqueue('a')
    assert queue.front() == 'a'

def test_queue_dequeue(queue):
    queue.enqueue('a')
    assert queue.dequeue() == 'a'

def test_queue_dequeue_error(queue):
    with pytest.raises(IndexError):
        queue.dequeue()

def test_queue_front_error(queue):
    with pytest.raises(IndexError):
        queue.front()

def test_queue_len(queue):
    queue.enqueue('a')
    queue.enqueue('b')
    assert len(queue) == 2

def test_queue_contains(queue):
    queue.enqueue('y')
    assert 'y' in queue

def test_queue_not_contains(queue):
    queue.enqueue('y')
    assert 'z' not in queue

def test_queue_clear(queue):
    queue.enqueue('a')
    queue.clear()
    assert len(queue) == 0

def test_queue_is_empty_after_clear(queue):
    queue.enqueue('a')
    queue.clear()
    assert queue.is_empty()