import pytest
from data.input_code.d02_stack import *

@pytest.mark.parametrize('expected', [None])
def test_stack_init(expected):
    stack = Stack()
    assert stack._items == []

def test_stack_push():
    stack = Stack()
    stack.push(1)
    assert stack._items == [1]

@pytest.mark.parametrize('expected', [IndexError])
def test_stack_pop_empty(expected):
    stack = Stack()
    with pytest.raises(expected):
        stack.pop()

def test_stack_pop():
    stack = Stack()
    stack.push(1)
    assert stack.pop() == 1

@pytest.mark.parametrize('expected', [IndexError])
def test_stack_peek_empty(expected):
    stack = Stack()
    with pytest.raises(expected):
        stack.peek()

def test_stack_peek():
    stack = Stack()
    stack.push(1)
    assert stack.peek() == 1

@pytest.mark.parametrize('expected', [True])
def test_stack_is_empty(expected):
    stack = Stack()
    assert stack.is_empty() == expected

def test_stack_is_not_empty():
    stack = Stack()
    stack.push(1)
    assert not stack.is_empty()

@pytest.mark.parametrize('expected', [0])
def test_stack_size_empty(expected):
    stack = Stack()
    assert stack.size() == expected

def test_stack_size():
    stack = Stack()
    stack.push(1)
    assert stack.size() == 1

def test_stack_clear():
    stack = Stack()
    stack.push(1)
    stack.clear()
    assert stack._items == []

@pytest.mark.parametrize('expected', [0])
def test_stack_len_empty(expected):
    stack = Stack()
    assert len(stack) == expected

def test_stack_len():
    stack = Stack()
    stack.push(1)
    assert len(stack) == 1

def test_stack_contains_false():
    stack = Stack()
    assert 1 not in stack

def test_stack_contains_true():
    stack = Stack()
    stack.push(1)
    assert 1 in stack

@pytest.mark.parametrize('expected', [None])
def test_queue_init(expected):
    queue = Queue()
    assert queue._items == []

def test_queue_enqueue():
    queue = Queue()
    queue.enqueue(1)
    assert queue._items == [1]

@pytest.mark.parametrize('expected', [IndexError])
def test_queue_dequeue_empty(expected):
    queue = Queue()
    with pytest.raises(expected):
        queue.dequeue()

def test_queue_dequeue():
    queue = Queue()
    queue.enqueue(1)
    assert queue.dequeue() == 1

@pytest.mark.parametrize('expected', [IndexError])
def test_queue_front_empty(expected):
    queue = Queue()
    with pytest.raises(expected):
        queue.front()

def test_queue_front():
    queue = Queue()
    queue.enqueue(1)
    assert queue.front() == 1

@pytest.mark.parametrize('expected', [True])
def test_queue_is_empty(expected):
    queue = Queue()
    assert queue.is_empty() == expected

def test_queue_is_not_empty():
    queue = Queue()
    queue.enqueue(1)
    assert not queue.is_empty()

@pytest.mark.parametrize('expected', [0])
def test_queue_size_empty(expected):
    queue = Queue()
    assert queue.size() == expected

def test_queue_size():
    queue = Queue()
    queue.enqueue(1)
    assert queue.size() == 1

def test_queue_clear():
    queue = Queue()
    queue.enqueue(1)
    queue.clear()
    assert queue._items == []

@pytest.mark.parametrize('expected', [0])
def test_queue_len_empty(expected):
    queue = Queue()
    assert len(queue) == expected

def test_queue_len():
    queue = Queue()
    queue.enqueue(1)
    assert len(queue) == 1

def test_queue_contains_false():
    queue = Queue()
    assert 1 not in queue

def test_queue_contains_true():
    queue = Queue()
    queue.enqueue(1)
    assert 1 in queue