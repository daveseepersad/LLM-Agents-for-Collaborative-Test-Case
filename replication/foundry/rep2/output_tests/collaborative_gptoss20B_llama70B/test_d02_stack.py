import pytest
from data.input_code.d02_stack import *

@pytest.mark.parametrize('initial, item, expected', [
    ([], 42, None)
])
def test_stack_push(initial, item, expected):
    stack = Stack()
    stack._items = initial
    result = stack.push(item)
    assert result == expected

@pytest.mark.parametrize('initial, expected', [
    ([1, 2, 3], 3)
])
def test_stack_pop_ok(initial, expected):
    stack = Stack()
    stack._items = initial
    result = stack.pop()
    assert result == expected

def test_stack_pop_empty():
    stack = Stack()
    stack._items = []
    with pytest.raises(IndexError):
        stack.pop()

@pytest.mark.parametrize('initial, expected', [
    ([1, 2, 3], 3)
])
def test_stack_peek_ok(initial, expected):
    stack = Stack()
    stack._items = initial
    result = stack.peek()
    assert result == expected

def test_stack_peek_empty():
    stack = Stack()
    stack._items = []
    with pytest.raises(IndexError):
        stack.peek()

@pytest.mark.parametrize('initial, item, expected', [
    ([], "A", None)
])
def test_queue_enqueue_ok(initial, item, expected):
    queue = Queue()
    queue._items = initial
    result = queue.enqueue(item)
    assert result == expected

@pytest.mark.parametrize('initial, expected', [
    (["x", "y"], "x")
])
def test_queue_dequeue_ok(initial, expected):
    queue = Queue()
    queue._items = initial
    result = queue.dequeue()
    assert result == expected

def test_queue_dequeue_empty():
    queue = Queue()
    queue._items = []
    with pytest.raises(IndexError):
        queue.dequeue()

@pytest.mark.parametrize('initial, expected', [
    ([1, 2, 3], 1)
])
def test_queue_front_ok(initial, expected):
    queue = Queue()
    queue._items = initial
    result = queue.front()
    assert result == expected

def test_queue_front_empty():
    queue = Queue()
    queue._items = []
    with pytest.raises(IndexError):
        queue.front()

@pytest.mark.parametrize('initial, item, expected', [
    ([1, 2, 3], 2, True),
    ([1, 2, 3], 99, False)
])
def test_stack_contains(initial, item, expected):
    stack = Stack()
    stack._items = initial
    result = item in stack
    assert result == expected

@pytest.mark.parametrize('initial, expected', [
    ([1, 2, 3], 3)
])
def test_stack_len(initial, expected):
    stack = Stack()
    stack._items = initial
    result = len(stack)
    assert result == expected

@pytest.mark.parametrize('initial, expected', [
    ([1, 2, 3, 4], 4)
])
def test_queue_len(initial, expected):
    queue = Queue()
    queue._items = initial
    result = len(queue)
    assert result == expected

@pytest.mark.parametrize('initial, expected', [
    ([1, 2, 3], None)
])
def test_stack_clear(initial, expected):
    stack = Stack()
    stack._items = initial
    result = stack.clear()
    assert result == expected

@pytest.mark.parametrize('initial, expected', [
    ([], True),
    ([1], False)
])
def test_stack_is_empty(initial, expected):
    stack = Stack()
    stack._items = initial
    result = stack.is_empty()
    assert result == expected

@pytest.mark.parametrize('initial, expected', [
    ([], True),
    ([1], False)
])
def test_queue_is_empty(initial, expected):
    queue = Queue()
    queue._items = initial
    result = queue.is_empty()
    assert result == expected

@pytest.mark.parametrize('initial, expected', [
    ([1, 2, 3], 3)
])
def test_stack_size(initial, expected):
    stack = Stack()
    stack._items = initial
    result = stack.size()
    assert result == expected

@pytest.mark.parametrize('initial, expected', [
    ([1, 2, 3], 3)
])
def test_queue_size(initial, expected):
    queue = Queue()
    queue._items = initial
    result = queue.size()
    assert result == expected

@pytest.mark.parametrize('initial, item, expected', [
    ([1, 2, 3], 2, True),
    ([1, 2, 3], 99, False)
])
def test_queue_contains(initial, item, expected):
    queue = Queue()
    queue._items = initial
    result = item in queue
    assert result == expected

@pytest.mark.parametrize('initial, expected', [
    ([1, 2, 3], None)
])
def test_queue_clear(initial, expected):
    queue = Queue()
    queue._items = initial
    result = queue.clear()
    assert result == expected