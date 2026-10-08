import pytest
from data.input_code.d02_stack import *

@pytest.mark.parametrize('expected_size, expected_is_empty', [
    (0, True)
])
def test_stack_init(expected_size, expected_is_empty):
    stack = Stack()
    assert stack.size() == expected_size
    assert stack.is_empty() == expected_is_empty

def test_stack_push():
    stack = Stack()
    stack.push(5)
    assert stack.size() == 1

@pytest.mark.parametrize('expected', [
    5
])
def test_stack_pop_ok(expected):
    stack = Stack()
    stack.push(5)
    assert stack.pop() == expected

def test_stack_pop_err():
    stack = Stack()
    with pytest.raises(IndexError):
        stack.pop()

@pytest.mark.parametrize('expected', [
    5
])
def test_stack_peek_ok(expected):
    stack = Stack()
    stack.push(5)
    assert stack.peek() == expected

def test_stack_peek_err():
    stack = Stack()
    with pytest.raises(IndexError):
        stack.peek()

def test_stack_is_empty():
    stack = Stack()
    assert stack.is_empty()

@pytest.mark.parametrize('expected', [
    2
])
def test_stack_size(expected):
    stack = Stack()
    stack.push(1)
    stack.push(2)
    assert stack.size() == expected

def test_stack_clear():
    stack = Stack()
    stack.push(1)
    stack.push(2)
    stack.clear()
    assert stack.size() == 0
    assert stack.is_empty()

@pytest.mark.parametrize('expected', [
    2
])
def test_stack_len(expected):
    stack = Stack()
    stack.push(1)
    stack.push(2)
    assert len(stack) == expected

@pytest.mark.parametrize('item, expected', [
    (1, True)
])
def test_stack_contains(item, expected):
    stack = Stack()
    stack.push(item)
    assert (item in stack) == expected

@pytest.mark.parametrize('expected_size, expected_is_empty', [
    (0, True)
])
def test_queue_init(expected_size, expected_is_empty):
    queue = Queue()
    assert queue.size() == expected_size
    assert queue.is_empty() == expected_is_empty

def test_queue_enqueue():
    queue = Queue()
    queue.enqueue(5)
    assert queue.size() == 1

@pytest.mark.parametrize('expected', [
    5
])
def test_queue_dequeue_ok(expected):
    queue = Queue()
    queue.enqueue(5)
    assert queue.dequeue() == expected

def test_queue_dequeue_err():
    queue = Queue()
    with pytest.raises(IndexError):
        queue.dequeue()

@pytest.mark.parametrize('expected', [
    5
])
def test_queue_front_ok(expected):
    queue = Queue()
    queue.enqueue(5)
    assert queue.front() == expected

def test_queue_front_err():
    queue = Queue()
    with pytest.raises(IndexError):
        queue.front()

def test_queue_is_empty():
    queue = Queue()
    assert queue.is_empty()

@pytest.mark.parametrize('expected', [
    2
])
def test_queue_size(expected):
    queue = Queue()
    queue.enqueue(1)
    queue.enqueue(2)
    assert queue.size() == expected

def test_queue_clear():
    queue = Queue()
    queue.enqueue(1)
    queue.enqueue(2)
    queue.clear()
    assert queue.size() == 0
    assert queue.is_empty()

@pytest.mark.parametrize('expected', [
    2
])
def test_queue_len(expected):
    queue = Queue()
    queue.enqueue(1)
    queue.enqueue(2)
    assert len(queue) == expected

@pytest.mark.parametrize('item, expected', [
    (1, True)
])
def test_queue_contains(item, expected):
    queue = Queue()
    queue.enqueue(item)
    assert (item in queue) == expected