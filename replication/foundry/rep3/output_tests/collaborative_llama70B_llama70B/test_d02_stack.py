import pytest
from data.input_code.d02_stack import Stack, Queue

@pytest.mark.parametrize('expected', [
    (None)
])
def test_Stack_init(expected):
    stack = Stack()
    assert stack._items == []

@pytest.mark.parametrize('item, expected', [
    (1, None)
])
def test_Stack_push(item, expected):
    stack = Stack()
    stack.push(item)
    assert stack._items == [item]

@pytest.mark.parametrize('item, expected', [
    (1, 1)
])
def test_Stack_pop(item, expected):
    stack = Stack()
    stack.push(item)
    assert stack.pop() == expected

def test_Stack_pop_error():
    stack = Stack()
    with pytest.raises(IndexError):
        stack.pop()

@pytest.mark.parametrize('item, expected', [
    (1, 1)
])
def test_Stack_peek(item, expected):
    stack = Stack()
    stack.push(item)
    assert stack.peek() == expected

def test_Stack_peek_error():
    stack = Stack()
    with pytest.raises(IndexError):
        stack.peek()

@pytest.mark.parametrize('item, expected', [
    (1, False)
])
def test_Stack_is_empty(item, expected):
    stack = Stack()
    stack.push(item)
    assert stack.is_empty() == expected

def test_Stack_is_empty_true():
    stack = Stack()
    assert stack.is_empty() == True

@pytest.mark.parametrize('item, expected', [
    (1, 1)
])
def test_Stack_size(item, expected):
    stack = Stack()
    stack.push(item)
    assert stack.size() == expected

def test_Stack_size_empty():
    stack = Stack()
    assert stack.size() == 0

@pytest.mark.parametrize('item, expected', [
    (1, None)
])
def test_Stack_clear(item, expected):
    stack = Stack()
    stack.push(item)
    stack.clear()
    assert stack._items == []

@pytest.mark.parametrize('item, expected', [
    (1, 1)
])
def test_Stack_len(item, expected):
    stack = Stack()
    stack.push(item)
    assert len(stack) == expected

@pytest.mark.parametrize('item, expected', [
    (1, True)
])
def test_Stack_contains(item, expected):
    stack = Stack()
    stack.push(item)
    assert (item in stack) == expected

@pytest.mark.parametrize('item, expected', [
    (2, False)
])
def test_Stack_contains_false(item, expected):
    stack = Stack()
    stack.push(1)
    assert (item in stack) == expected

@pytest.mark.parametrize('expected', [
    (None)
])
def test_Queue_init(expected):
    queue = Queue()
    assert queue._items == []

@pytest.mark.parametrize('item, expected', [
    (1, None)
])
def test_Queue_enqueue(item, expected):
    queue = Queue()
    queue.enqueue(item)
    assert queue._items == [item]

@pytest.mark.parametrize('item, expected', [
    (1, 1)
])
def test_Queue_dequeue(item, expected):
    queue = Queue()
    queue.enqueue(item)
    assert queue.dequeue() == expected

def test_Queue_dequeue_error():
    queue = Queue()
    with pytest.raises(IndexError):
        queue.dequeue()

@pytest.mark.parametrize('item, expected', [
    (1, 1)
])
def test_Queue_front(item, expected):
    queue = Queue()
    queue.enqueue(item)
    assert queue.front() == expected

def test_Queue_front_error():
    queue = Queue()
    with pytest.raises(IndexError):
        queue.front()

@pytest.mark.parametrize('item, expected', [
    (1, False)
])
def test_Queue_is_empty(item, expected):
    queue = Queue()
    queue.enqueue(item)
    assert queue.is_empty() == expected

def test_Queue_is_empty_true():
    queue = Queue()
    assert queue.is_empty() == True

@pytest.mark.parametrize('item, expected', [
    (1, 1)
])
def test_Queue_size(item, expected):
    queue = Queue()
    queue.enqueue(item)
    assert queue.size() == expected

def test_Queue_size_empty():
    queue = Queue()
    assert queue.size() == 0

@pytest.mark.parametrize('item, expected', [
    (1, None)
])
def test_Queue_clear(item, expected):
    queue = Queue()
    queue.enqueue(item)
    queue.clear()
    assert queue._items == []

@pytest.mark.parametrize('item, expected', [
    (1, 1)
])
def test_Queue_len(item, expected):
    queue = Queue()
    queue.enqueue(item)
    assert len(queue) == expected

@pytest.mark.parametrize('item, expected', [
    (1, True)
])
def test_Queue_contains(item, expected):
    queue = Queue()
    queue.enqueue(item)
    assert (item in queue) == expected

@pytest.mark.parametrize('item, expected', [
    (2, False)
])
def test_Queue_contains_false(item, expected):
    queue = Queue()
    queue.enqueue(1)
    assert (item in queue) == expected