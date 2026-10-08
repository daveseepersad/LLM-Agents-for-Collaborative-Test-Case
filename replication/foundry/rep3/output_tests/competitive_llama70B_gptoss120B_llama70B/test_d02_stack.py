import pytest
from data.input_code.d02_stack import Stack, Queue

@pytest.mark.parametrize('expected', [
    (None)
])
def test_stack_init(expected):
    stack = Stack()
    assert stack._items == []

@pytest.mark.parametrize('item, expected', [
    (5, None)
])
def test_stack_push(item, expected):
    stack = Stack()
    stack.push(item)
    assert stack._items == [item]

@pytest.mark.parametrize('expected', [
    (5)
])
def test_stack_pop(expected):
    stack = Stack()
    stack.push(5)
    assert stack.pop() == expected

def test_stack_pop_error():
    stack = Stack()
    with pytest.raises(IndexError):
        stack.pop()

@pytest.mark.parametrize('expected', [
    (5)
])
def test_stack_peek(expected):
    stack = Stack()
    stack.push(5)
    assert stack.peek() == expected

def test_stack_peek_error():
    stack = Stack()
    with pytest.raises(IndexError):
        stack.peek()

@pytest.mark.parametrize('expected', [
    (True)
])
def test_stack_is_empty(expected):
    stack = Stack()
    assert stack.is_empty() == expected

@pytest.mark.parametrize('expected', [
    (False)
])
def test_stack_is_empty_false(expected):
    stack = Stack()
    stack.push(5)
    assert stack.is_empty() == expected

@pytest.mark.parametrize('expected', [
    (1)
])
def test_stack_size(expected):
    stack = Stack()
    stack.push(5)
    assert stack.size() == expected

@pytest.mark.parametrize('expected', [
    (0)
])
def test_stack_size_zero(expected):
    stack = Stack()
    assert stack.size() == expected

@pytest.mark.parametrize('expected', [
    (None)
])
def test_stack_clear(expected):
    stack = Stack()
    stack.push(5)
    stack.clear()
    assert stack._items == []

@pytest.mark.parametrize('expected', [
    (1)
])
def test_stack_len(expected):
    stack = Stack()
    stack.push(5)
    assert len(stack) == expected

@pytest.mark.parametrize('expected', [
    (0)
])
def test_stack_len_zero(expected):
    stack = Stack()
    assert len(stack) == expected

@pytest.mark.parametrize('item, expected', [
    (5, True)
])
def test_stack_contains(item, expected):
    stack = Stack()
    stack.push(5)
    assert (item in stack) == expected

@pytest.mark.parametrize('item, expected', [
    (5, False)
])
def test_stack_contains_false(item, expected):
    stack = Stack()
    assert (item in stack) == expected

@pytest.mark.parametrize('expected', [
    (None)
])
def test_queue_init(expected):
    queue = Queue()
    assert queue._items == []

@pytest.mark.parametrize('item, expected', [
    (5, None)
])
def test_queue_enqueue(item, expected):
    queue = Queue()
    queue.enqueue(item)
    assert queue._items == [item]

@pytest.mark.parametrize('expected', [
    (5)
])
def test_queue_dequeue(expected):
    queue = Queue()
    queue.enqueue(5)
    assert queue.dequeue() == expected

def test_queue_dequeue_error():
    queue = Queue()
    with pytest.raises(IndexError):
        queue.dequeue()

@pytest.mark.parametrize('expected', [
    (5)
])
def test_queue_front(expected):
    queue = Queue()
    queue.enqueue(5)
    assert queue.front() == expected

def test_queue_front_error():
    queue = Queue()
    with pytest.raises(IndexError):
        queue.front()

@pytest.mark.parametrize('expected', [
    (True)
])
def test_queue_is_empty(expected):
    queue = Queue()
    assert queue.is_empty() == expected

@pytest.mark.parametrize('expected', [
    (False)
])
def test_queue_is_empty_false(expected):
    queue = Queue()
    queue.enqueue(5)
    assert queue.is_empty() == expected

@pytest.mark.parametrize('expected', [
    (1)
])
def test_queue_size(expected):
    queue = Queue()
    queue.enqueue(5)
    assert queue.size() == expected

@pytest.mark.parametrize('expected', [
    (0)
])
def test_queue_size_zero(expected):
    queue = Queue()
    assert queue.size() == expected

@pytest.mark.parametrize('expected', [
    (None)
])
def test_queue_clear(expected):
    queue = Queue()
    queue.enqueue(5)
    queue.clear()
    assert queue._items == []

@pytest.mark.parametrize('expected', [
    (1)
])
def test_queue_len(expected):
    queue = Queue()
    queue.enqueue(5)
    assert len(queue) == expected

@pytest.mark.parametrize('expected', [
    (0)
])
def test_queue_len_zero(expected):
    queue = Queue()
    assert len(queue) == expected

@pytest.mark.parametrize('item, expected', [
    (5, True)
])
def test_queue_contains(item, expected):
    queue = Queue()
    queue.enqueue(5)
    assert (item in queue) == expected

@pytest.mark.parametrize('item, expected', [
    (5, False)
])
def test_queue_contains_false(item, expected):
    queue = Queue()
    assert (item in queue) == expected