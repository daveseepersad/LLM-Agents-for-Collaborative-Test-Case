import pytest
from data.input_code.d02_stack import Stack, Queue

@pytest.mark.parametrize('pre_items, expected', [
    ([1, 2], 2)
])
def test_Stack_pop(pre_items, expected):
    stack = Stack()
    for item in pre_items:
        stack.push(item)
    assert stack.pop() == expected

def test_Stack_pop_empty():
    stack = Stack()
    with pytest.raises(IndexError):
        stack.pop()

@pytest.mark.parametrize('pre_items, expected', [
    (["a"], "a")
])
def test_Stack_peek(pre_items, expected):
    stack = Stack()
    for item in pre_items:
        stack.push(item)
    assert stack.peek() == expected

def test_Stack_peek_empty():
    stack = Stack()
    with pytest.raises(IndexError):
        stack.peek()

@pytest.mark.parametrize('pre_items, expected', [
    ([1, 2, 3], 3)
])
def test_Stack_len(pre_items, expected):
    stack = Stack()
    for item in pre_items:
        stack.push(item)
    assert len(stack) == expected

@pytest.mark.parametrize('pre_items, item, expected', [
    ([1, 2, 3], 2, True),
    ([1, 2, 3], 4, False)
])
def test_Stack_contains(pre_items, item, expected):
    stack = Stack()
    for i in pre_items:
        stack.push(i)
    assert (item in stack) == expected

def test_Stack_clear():
    stack = Stack()
    stack.push(1)
    stack.push(2)
    stack.clear()
    assert len(stack) == 0

@pytest.mark.parametrize('pre_items, expected', [
    ([1, 2], 1)
])
def test_Queue_dequeue(pre_items, expected):
    queue = Queue()
    for item in pre_items:
        queue.enqueue(item)
    assert queue.dequeue() == expected

def test_Queue_dequeue_empty():
    queue = Queue()
    with pytest.raises(IndexError):
        queue.dequeue()

@pytest.mark.parametrize('pre_items, expected', [
    (["x"], "x")
])
def test_Queue_front(pre_items, expected):
    queue = Queue()
    for item in pre_items:
        queue.enqueue(item)
    assert queue.front() == expected

def test_Queue_front_empty():
    queue = Queue()
    with pytest.raises(IndexError):
        queue.front()

@pytest.mark.parametrize('pre_items, expected', [
    ([5, 6], 2)
])
def test_Queue_len(pre_items, expected):
    queue = Queue()
    for item in pre_items:
        queue.enqueue(item)
    assert len(queue) == expected

@pytest.mark.parametrize('pre_items, item, expected', [
    ([5, 6], 6, True),
    ([5, 6], 7, False)
])
def test_Queue_contains(pre_items, item, expected):
    queue = Queue()
    for i in pre_items:
        queue.enqueue(i)
    assert (item in queue) == expected

def test_Queue_clear():
    queue = Queue()
    queue.enqueue(5)
    queue.enqueue(6)
    queue.clear()
    assert len(queue) == 0

@pytest.mark.parametrize('pre_items, expected', [
    ([], True)
])
def test_Stack_is_empty(pre_items, expected):
    stack = Stack()
    for item in pre_items:
        stack.push(item)
    assert stack.is_empty() == expected

@pytest.mark.parametrize('pre_items, expected', [
    ([1], False)
])
def test_Stack_is_not_empty(pre_items, expected):
    stack = Stack()
    for item in pre_items:
        stack.push(item)
    assert stack.is_empty() == expected

@pytest.mark.parametrize('pre_items, expected', [
    ([1, 2, 3], 3)
])
def test_Stack_size(pre_items, expected):
    stack = Stack()
    for item in pre_items:
        stack.push(item)
    assert stack.size() == expected

@pytest.mark.parametrize('pre_items, expected', [
    ([], 0)
])
def test_Stack_len_empty(pre_items, expected):
    stack = Stack()
    for item in pre_items:
        stack.push(item)
    assert len(stack) == expected

@pytest.mark.parametrize('pre_items, expected', [
    ([], True)
])
def test_Queue_is_empty(pre_items, expected):
    queue = Queue()
    for item in pre_items:
        queue.enqueue(item)
    assert queue.is_empty() == expected

@pytest.mark.parametrize('pre_items, expected', [
    ([5], False)
])
def test_Queue_is_not_empty(pre_items, expected):
    queue = Queue()
    for item in pre_items:
        queue.enqueue(item)
    assert queue.is_empty() == expected

@pytest.mark.parametrize('pre_items, expected', [
    ([5, 6, 7], 3)
])
def test_Queue_size(pre_items, expected):
    queue = Queue()
    for item in pre_items:
        queue.enqueue(item)
    assert queue.size() == expected

@pytest.mark.parametrize('pre_items, expected', [
    ([], 0)
])
def test_Queue_len_empty(pre_items, expected):
    queue = Queue()
    for item in pre_items:
        queue.enqueue(item)
    assert len(queue) == expected