import pytest
from data.input_code.d02_stack import Stack, Queue

@pytest.mark.parametrize('expected', [
    (None)
])
def test_stack_init(expected):
    stack = Stack()
    assert stack._items == []

@pytest.mark.parametrize('expected', [
    (True)
])
def test_stack_is_empty_true(expected):
    stack = Stack()
    assert stack.is_empty() == expected

@pytest.mark.parametrize('item, expected', [
    (42, None)
])
def test_stack_push(item, expected):
    stack = Stack()
    stack.push(item)
    assert stack._items[-1] == item

@pytest.mark.parametrize('expected', [
    (1)
])
def test_stack_size_after_push(expected):
    stack = Stack()
    stack.push(42)
    assert stack.size() == expected

@pytest.mark.parametrize('expected', [
    (1)
])
def test_stack_len_after_push(expected):
    stack = Stack()
    stack.push(42)
    assert len(stack) == expected

@pytest.mark.parametrize('item, expected', [
    (42, True)
])
def test_stack_contains_item(item, expected):
    stack = Stack()
    stack.push(item)
    assert item in stack

@pytest.mark.parametrize('expected', [
    (False)
])
def test_stack_is_empty_false(expected):
    stack = Stack()
    stack.push(42)
    assert stack.is_empty() == expected

@pytest.mark.parametrize('expected', [
    (42)
])
def test_stack_peek(expected):
    stack = Stack()
    stack.push(expected)
    assert stack.peek() == expected

@pytest.mark.parametrize('expected', [
    (42)
])
def test_stack_pop(expected):
    stack = Stack()
    stack.push(expected)
    assert stack.pop() == expected

@pytest.mark.parametrize('expected', [
    (True)
])
def test_stack_is_empty_after_pop(expected):
    stack = Stack()
    stack.push(42)
    stack.pop()
    assert stack.is_empty() == expected

def test_stack_pop_empty():
    stack = Stack()
    with pytest.raises(IndexError):
        stack.pop()

def test_stack_peek_empty():
    stack = Stack()
    with pytest.raises(IndexError):
        stack.peek()

@pytest.mark.parametrize('item, expected', [
    (None, None)
])
def test_stack_push_none(item, expected):
    stack = Stack()
    stack.push(item)
    assert stack._items[-1] == item

@pytest.mark.parametrize('item, expected', [
    (None, True)
])
def test_stack_contains_none(item, expected):
    stack = Stack()
    stack.push(item)
    assert item in stack

@pytest.mark.parametrize('expected', [
    (None)
])
def test_stack_clear(expected):
    stack = Stack()
    stack.push(42)
    stack.clear()
    assert stack._items == []

@pytest.mark.parametrize('expected', [
    (True)
])
def test_stack_is_empty_after_clear(expected):
    stack = Stack()
    stack.push(42)
    stack.clear()
    assert stack.is_empty() == expected

@pytest.mark.parametrize('expected', [
    (None)
])
def test_queue_init(expected):
    queue = Queue()
    assert queue._items == []

@pytest.mark.parametrize('expected', [
    (True)
])
def test_queue_is_empty_true(expected):
    queue = Queue()
    assert queue.is_empty() == expected

@pytest.mark.parametrize('item, expected', [
    ("a", None)
])
def test_queue_enqueue(item, expected):
    queue = Queue()
    queue.enqueue(item)
    assert queue._items[-1] == item

@pytest.mark.parametrize('expected', [
    (1)
])
def test_queue_size_after_enqueue(expected):
    queue = Queue()
    queue.enqueue("a")
    assert queue.size() == expected

@pytest.mark.parametrize('expected', [
    (1)
])
def test_queue_len_after_enqueue(expected):
    queue = Queue()
    queue.enqueue("a")
    assert len(queue) == expected

@pytest.mark.parametrize('item, expected', [
    ("a", True)
])
def test_queue_contains_item(item, expected):
    queue = Queue()
    queue.enqueue(item)
    assert item in queue

@pytest.mark.parametrize('expected', [
    (False)
])
def test_queue_is_empty_false(expected):
    queue = Queue()
    queue.enqueue("a")
    assert queue.is_empty() == expected

@pytest.mark.parametrize('expected', [
    ("a")
])
def test_queue_front(expected):
    queue = Queue()
    queue.enqueue(expected)
    assert queue.front() == expected

@pytest.mark.parametrize('expected', [
    ("a")
])
def test_queue_dequeue(expected):
    queue = Queue()
    queue.enqueue(expected)
    assert queue.dequeue() == expected

@pytest.mark.parametrize('expected', [
    (True)
])
def test_queue_is_empty_after_dequeue(expected):
    queue = Queue()
    queue.enqueue("a")
    queue.dequeue()
    assert queue.is_empty() == expected

def test_queue_dequeue_empty():
    queue = Queue()
    with pytest.raises(IndexError):
        queue.dequeue()

def test_queue_front_empty():
    queue = Queue()
    with pytest.raises(IndexError):
        queue.front()

@pytest.mark.parametrize('item, expected', [
    (None, None)
])
def test_queue_enqueue_none(item, expected):
    queue = Queue()
    queue.enqueue(item)
    assert queue._items[-1] == item

@pytest.mark.parametrize('item, expected', [
    (None, True)
])
def test_queue_contains_none(item, expected):
    queue = Queue()
    queue.enqueue(item)
    assert item in queue

@pytest.mark.parametrize('expected', [
    (None)
])
def test_queue_clear(expected):
    queue = Queue()
    queue.enqueue("a")
    queue.clear()
    assert queue._items == []

@pytest.mark.parametrize('expected', [
    (True)
])
def test_queue_is_empty_after_clear(expected):
    queue = Queue()
    queue.enqueue("a")
    queue.clear()
    assert queue.is_empty() == expected