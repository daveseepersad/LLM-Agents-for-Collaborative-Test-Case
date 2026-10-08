import pytest
from data.input_code.d02_stack import *

@pytest.mark.parametrize('items, expected', [
    ([], True),
])
def test_stack_is_empty(items, expected):
    stack = Stack()
    stack._items = items
    assert stack.is_empty() == expected

def test_stack_push():
    stack = Stack()
    stack._items = []
    stack.push('A')
    assert stack._items == ['A']

@pytest.mark.parametrize('items, item, expected', [
    ([1, 2, 3], 2, True),
    ([1, 2, 3], 4, False),
])
def test_stack_contains(items, item, expected):
    stack = Stack()
    stack._items = items
    assert (item in stack) == expected

def test_stack_peek_empty():
    stack = Stack()
    stack._items = []
    with pytest.raises(IndexError):
        stack.peek()

def test_stack_pop_empty():
    stack = Stack()
    stack._items = []
    with pytest.raises(IndexError):
        stack.pop()

def test_stack_pop_nonempty():
    stack = Stack()
    stack._items = [1, 2, 3]
    assert stack.pop() == 3

def test_stack_peek_nonempty():
    stack = Stack()
    stack._items = [1, 2, 3]
    assert stack.peek() == 3

def test_stack_clear():
    stack = Stack()
    stack._items = [1, 2, 3]
    stack.clear()
    assert stack._items == []

def test_stack_len():
    stack = Stack()
    stack._items = [1, 2, 3]
    assert len(stack) == 3

@pytest.mark.parametrize('items, expected', [
    ([], True),
])
def test_queue_is_empty(items, expected):
    queue = Queue()
    queue._items = items
    assert queue.is_empty() == expected

def test_queue_enqueue():
    queue = Queue()
    queue._items = []
    queue.enqueue('X')
    assert queue._items == ['X']

def test_queue_front_nonempty():
    queue = Queue()
    queue._items = [1, 2, 3]
    assert queue.front() == 1

def test_queue_dequeue_nonempty():
    queue = Queue()
    queue._items = [1, 2, 3]
    assert queue.dequeue() == 1

def test_queue_dequeue_empty():
    queue = Queue()
    queue._items = []
    with pytest.raises(IndexError):
        queue.dequeue()

def test_queue_clear():
    queue = Queue()
    queue._items = [1, 2, 3]
    queue.clear()
    assert queue._items == []

def test_queue_len():
    queue = Queue()
    queue._items = [1, 2, 3]
    assert len(queue) == 3

@pytest.mark.parametrize('items, item, expected', [
    ([1, 2, 3], 2, True),
    ([1, 2, 3], 5, False),
])
def test_queue_contains(items, item, expected):
    queue = Queue()
    queue._items = items
    assert (item in queue) == expected

import pytest
from data.input_code.d02_stack import *

def test_stack_size():
    stack = Stack()
    stack._items = [1, 2, 3]
    assert stack.size() == 3

def test_queue_size():
    queue = Queue()
    queue._items = [1, 2, 3, 4]
    assert queue.size() == 4

def test_queue_front_empty():
    queue = Queue()
    queue._items = []
    with pytest.raises(IndexError):
        queue.front()