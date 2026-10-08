import pytest
from data.input_code.d02_stack import Stack, Queue

@pytest.mark.parametrize('expected', [
    {"size": 0, "_items": []}
])
def test_stack_init(expected):
    stack = Stack()
    assert stack.size() == expected["size"]
    assert stack._items == expected["_items"]

@pytest.mark.parametrize('item, expected', [
    (5, None)
])
def test_stack_push(item, expected):
    stack = Stack()
    assert stack.push(item) == expected

@pytest.mark.parametrize('item, expected', [
    (5, 5)
])
def test_stack_pop(item, expected):
    stack = Stack()
    stack.push(item)
    assert stack.pop() == expected

def test_stack_pop_error():
    stack = Stack()
    with pytest.raises(IndexError):
        stack.pop()

@pytest.mark.parametrize('item, expected', [
    (5, 5)
])
def test_stack_peek(item, expected):
    stack = Stack()
    stack.push(item)
    assert stack.peek() == expected

def test_stack_peek_error():
    stack = Stack()
    with pytest.raises(IndexError):
        stack.peek()

@pytest.mark.parametrize('expected', [
    True
])
def test_stack_is_empty_true(expected):
    stack = Stack()
    assert stack.is_empty() == expected

@pytest.mark.parametrize('item, expected', [
    (5, False)
])
def test_stack_is_empty_false(item, expected):
    stack = Stack()
    stack.push(item)
    assert stack.is_empty() == expected

@pytest.mark.parametrize('item, expected', [
    (5, 1)
])
def test_stack_size(item, expected):
    stack = Stack()
    stack.push(item)
    assert stack.size() == expected

@pytest.mark.parametrize('item, expected', [
    (5, None)
])
def test_stack_clear(item, expected):
    stack = Stack()
    stack.push(item)
    assert stack.clear() == expected

@pytest.mark.parametrize('item, expected', [
    (5, 1)
])
def test_stack_len(item, expected):
    stack = Stack()
    stack.push(item)
    assert len(stack) == expected

@pytest.mark.parametrize('item, expected', [
    (5, True)
])
def test_stack_contains_true(item, expected):
    stack = Stack()
    stack.push(item)
    assert (item in stack) == expected

@pytest.mark.parametrize('item, expected', [
    (5, False)
])
def test_stack_contains_false(item, expected):
    stack = Stack()
    assert (item in stack) == expected

@pytest.mark.parametrize('expected', [
    {"size": 0, "_items": []}
])
def test_queue_init(expected):
    queue = Queue()
    assert queue.size() == expected["size"]
    assert queue._items == expected["_items"]

@pytest.mark.parametrize('item, expected', [
    (5, None)
])
def test_queue_enqueue(item, expected):
    queue = Queue()
    assert queue.enqueue(item) == expected

@pytest.mark.parametrize('item, expected', [
    (5, 5)
])
def test_queue_dequeue(item, expected):
    queue = Queue()
    queue.enqueue(item)
    assert queue.dequeue() == expected

def test_queue_dequeue_error():
    queue = Queue()
    with pytest.raises(IndexError):
        queue.dequeue()

@pytest.mark.parametrize('item, expected', [
    (5, 5)
])
def test_queue_front(item, expected):
    queue = Queue()
    queue.enqueue(item)
    assert queue.front() == expected

def test_queue_front_error():
    queue = Queue()
    with pytest.raises(IndexError):
        queue.front()

@pytest.mark.parametrize('expected', [
    True
])
def test_queue_is_empty_true(expected):
    queue = Queue()
    assert queue.is_empty() == expected

@pytest.mark.parametrize('item, expected', [
    (5, False)
])
def test_queue_is_empty_false(item, expected):
    queue = Queue()
    queue.enqueue(item)
    assert queue.is_empty() == expected

@pytest.mark.parametrize('item, expected', [
    (5, 1)
])
def test_queue_size(item, expected):
    queue = Queue()
    queue.enqueue(item)
    assert queue.size() == expected

@pytest.mark.parametrize('item, expected', [
    (5, None)
])
def test_queue_clear(item, expected):
    queue = Queue()
    queue.enqueue(item)
    assert queue.clear() == expected

@pytest.mark.parametrize('item, expected', [
    (5, 1)
])
def test_queue_len(item, expected):
    queue = Queue()
    queue.enqueue(item)
    assert len(queue) == expected

@pytest.mark.parametrize('item, expected', [
    (5, True)
])
def test_queue_contains_true(item, expected):
    queue = Queue()
    queue.enqueue(item)
    assert (item in queue) == expected

@pytest.mark.parametrize('item, expected', [
    (5, False)
])
def test_queue_contains_false(item, expected):
    queue = Queue()
    assert (item in queue) == expected