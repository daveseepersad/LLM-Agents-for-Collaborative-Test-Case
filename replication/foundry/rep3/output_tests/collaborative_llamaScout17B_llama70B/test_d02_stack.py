import pytest
from data.input_code.d02_stack import Stack, Queue

@pytest.mark.parametrize('expected', [
    ({"size": 0, "_items": []})
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
    result = stack.push(item)
    assert result == expected

@pytest.mark.parametrize('item, expected', [
    (5, 5)
])
def test_stack_pop(item, expected):
    stack = Stack()
    stack.push(item)
    result = stack.pop()
    assert result == expected

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
    result = stack.peek()
    assert result == expected

def test_stack_peek_error():
    stack = Stack()
    with pytest.raises(IndexError):
        stack.peek()

@pytest.mark.parametrize('expected', [
    (True)
])
def test_stack_is_empty_true(expected):
    stack = Stack()
    result = stack.is_empty()
    assert result == expected

@pytest.mark.parametrize('item, expected', [
    (5, False)
])
def test_stack_is_empty_false(item, expected):
    stack = Stack()
    stack.push(item)
    result = stack.is_empty()
    assert result == expected

@pytest.mark.parametrize('item, expected', [
    (5, 1)
])
def test_stack_size(item, expected):
    stack = Stack()
    stack.push(item)
    result = stack.size()
    assert result == expected

@pytest.mark.parametrize('item, expected', [
    (5, None)
])
def test_stack_clear(item, expected):
    stack = Stack()
    stack.push(item)
    result = stack.clear()
    assert result == expected

@pytest.mark.parametrize('item, expected', [
    (5, 1)
])
def test_stack_len(item, expected):
    stack = Stack()
    stack.push(item)
    result = len(stack)
    assert result == expected

@pytest.mark.parametrize('item, expected', [
    (5, True)
])
def test_stack_contains_true(item, expected):
    stack = Stack()
    stack.push(item)
    result = item in stack
    assert result == expected

@pytest.mark.parametrize('item, expected', [
    (10, False)
])
def test_stack_contains_false(item, expected):
    stack = Stack()
    stack.push(5)
    result = item in stack
    assert result == expected

@pytest.mark.parametrize('expected', [
    ({"size": 0, "_items": []})
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
    result = queue.enqueue(item)
    assert result == expected

@pytest.mark.parametrize('item, expected', [
    (5, 5)
])
def test_queue_dequeue(item, expected):
    queue = Queue()
    queue.enqueue(item)
    result = queue.dequeue()
    assert result == expected

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
    result = queue.front()
    assert result == expected

def test_queue_front_error():
    queue = Queue()
    with pytest.raises(IndexError):
        queue.front()

@pytest.mark.parametrize('expected', [
    (True)
])
def test_queue_is_empty_true(expected):
    queue = Queue()
    result = queue.is_empty()
    assert result == expected

@pytest.mark.parametrize('item, expected', [
    (5, False)
])
def test_queue_is_empty_false(item, expected):
    queue = Queue()
    queue.enqueue(item)
    result = queue.is_empty()
    assert result == expected

@pytest.mark.parametrize('item, expected', [
    (5, 1)
])
def test_queue_size(item, expected):
    queue = Queue()
    queue.enqueue(item)
    result = queue.size()
    assert result == expected

@pytest.mark.parametrize('item, expected', [
    (5, None)
])
def test_queue_clear(item, expected):
    queue = Queue()
    queue.enqueue(item)
    result = queue.clear()
    assert result == expected

@pytest.mark.parametrize('item, expected', [
    (5, 1)
])
def test_queue_len(item, expected):
    queue = Queue()
    queue.enqueue(item)
    result = len(queue)
    assert result == expected

@pytest.mark.parametrize('item, expected', [
    (5, True)
])
def test_queue_contains_true(item, expected):
    queue = Queue()
    queue.enqueue(item)
    result = item in queue
    assert result == expected

@pytest.mark.parametrize('item, expected', [
    (10, False)
])
def test_queue_contains_false(item, expected):
    queue = Queue()
    queue.enqueue(5)
    result = item in queue
    assert result == expected