import pytest
from data.input_code.d02_stack import *

@pytest.mark.parametrize('expected', [None])
def test_stack_init(expected):
    stack = Stack()
    assert stack.size() == 0

def test_stack_push():
    stack = Stack()
    stack.push(5)
    assert stack.size() == 1

def test_stack_pop_empty():
    stack = Stack()
    with pytest.raises(IndexError):
        stack.pop()

def test_stack_pop_non_empty():
    stack = Stack()
    stack.push(5)
    assert stack.pop() == 5

def test_stack_peek_empty():
    stack = Stack()
    with pytest.raises(IndexError):
        stack.peek()

def test_stack_peek_non_empty():
    stack = Stack()
    stack.push(5)
    assert stack.peek() == 5

@pytest.mark.parametrize('expected', [True, False])
def test_stack_is_empty(expected):
    stack = Stack()
    if not expected:
        stack.push(5)
    assert stack.is_empty() == expected

@pytest.mark.parametrize('expected', [0, 1])
def test_stack_size(expected):
    stack = Stack()
    if expected > 0:
        stack.push(5)
    assert stack.size() == expected

def test_stack_clear():
    stack = Stack()
    stack.push(5)
    stack.clear()
    assert stack.is_empty()

@pytest.mark.parametrize('expected', [0, 1])
def test_stack_len(expected):
    stack = Stack()
    if expected > 0:
        stack.push(5)
    assert len(stack) == expected

@pytest.mark.parametrize('item, expected', [(5, False), (5, True)])
def test_stack_contains(item, expected):
    stack = Stack()
    if expected:
        stack.push(item)
    assert (item in stack) == expected

@pytest.mark.parametrize('expected', [None])
def test_queue_init(expected):
    queue = Queue()
    assert queue.size() == 0

def test_queue_enqueue():
    queue = Queue()
    queue.enqueue(5)
    assert queue.size() == 1

def test_queue_dequeue_empty():
    queue = Queue()
    with pytest.raises(IndexError):
        queue.dequeue()

def test_queue_dequeue_non_empty():
    queue = Queue()
    queue.enqueue(5)
    assert queue.dequeue() == 5

def test_queue_front_empty():
    queue = Queue()
    with pytest.raises(IndexError):
        queue.front()

def test_queue_front_non_empty():
    queue = Queue()
    queue.enqueue(5)
    assert queue.front() == 5

@pytest.mark.parametrize('expected', [True, False])
def test_queue_is_empty(expected):
    queue = Queue()
    if not expected:
        queue.enqueue(5)
    assert queue.is_empty() == expected

@pytest.mark.parametrize('expected', [0, 1])
def test_queue_size(expected):
    queue = Queue()
    if expected > 0:
        queue.enqueue(5)
    assert queue.size() == expected

def test_queue_clear():
    queue = Queue()
    queue.enqueue(5)
    queue.clear()
    assert queue.is_empty()

@pytest.mark.parametrize('expected', [0, 1])
def test_queue_len(expected):
    queue = Queue()
    if expected > 0:
        queue.enqueue(5)
    assert len(queue) == expected

@pytest.mark.parametrize('item, expected', [(5, False), (5, True)])
def test_queue_contains(item, expected):
    queue = Queue()
    if expected:
        queue.enqueue(item)
    assert (item in queue) == expected