import pytest
from data.input_code.d02_stack import Stack, Queue

@pytest.mark.parametrize('initial, expected', [
    ([], True)
])
def test_Stack_is_empty(initial, expected):
    stack = Stack()
    stack._items = initial
    assert stack.is_empty() == expected

@pytest.mark.parametrize('initial, expected', [
    ([], 0)
])
def test_Stack_size(initial, expected):
    stack = Stack()
    stack._items = initial
    assert stack.size() == expected

@pytest.mark.parametrize('initial, item', [
    ([], 5)
])
def test_Stack_push(initial, item):
    stack = Stack()
    stack._items = initial
    stack.push(item)
    assert stack._items == [item]

@pytest.mark.parametrize('initial, expected', [
    ([1, 2], 2)
])
def test_Stack_peek_nonempty(initial, expected):
    stack = Stack()
    stack._items = initial
    assert stack.peek() == expected

@pytest.mark.parametrize('initial, expected', [
    ([1, 2], 2)
])
def test_Stack_pop_nonempty(initial, expected):
    stack = Stack()
    stack._items = initial
    assert stack.pop() == expected

def test_Stack_pop_empty():
    stack = Stack()
    with pytest.raises(IndexError):
        stack.pop()

@pytest.mark.parametrize('initial, item, expected', [
    ([1, 2], 1, True),
    ([1, 2], 2, True),
    ([1, 2], 3, False)
])
def test_Stack_contains(initial, item, expected):
    stack = Stack()
    stack._items = initial
    assert (item in stack) == expected

@pytest.mark.parametrize('initial, expected', [
    ([1, 2], 2)
])
def test_Stack_len(initial, expected):
    stack = Stack()
    stack._items = initial
    assert len(stack) == expected

@pytest.mark.parametrize('initial', [
    ([1, 2])
])
def test_Stack_clear(initial):
    stack = Stack()
    stack._items = initial
    stack.clear()
    assert stack._items == []

@pytest.mark.parametrize('initial, expected', [
    ([], True)
])
def test_Queue_is_empty(initial, expected):
    queue = Queue()
    queue._items = initial
    assert queue.is_empty() == expected

@pytest.mark.parametrize('initial, item', [
    ([], 7)
])
def test_Queue_enqueue(initial, item):
    queue = Queue()
    queue._items = initial
    queue.enqueue(item)
    assert queue._items == [item]

@pytest.mark.parametrize('initial, expected', [
    ([1, 2], 1)
])
def test_Queue_front_nonempty(initial, expected):
    queue = Queue()
    queue._items = initial
    assert queue.front() == expected

@pytest.mark.parametrize('initial, expected', [
    ([1, 2], 1)
])
def test_Queue_dequeue_nonempty(initial, expected):
    queue = Queue()
    queue._items = initial
    assert queue.dequeue() == expected

def test_Queue_dequeue_empty():
    queue = Queue()
    with pytest.raises(IndexError):
        queue.dequeue()

@pytest.mark.parametrize('initial, expected', [
    ([1, 2], 2)
])
def test_Queue_size(initial, expected):
    queue = Queue()
    queue._items = initial
    assert queue.size() == expected

@pytest.mark.parametrize('initial', [
    ([1, 2])
])
def test_Queue_clear(initial):
    queue = Queue()
    queue._items = initial
    queue.clear()
    assert queue._items == []

@pytest.mark.parametrize('initial, item, expected', [
    ([1, 2], 1, True),
    ([1, 2], 2, True),
    ([1, 2], 3, False)
])
def test_Queue_contains(initial, item, expected):
    queue = Queue()
    queue._items = initial
    assert (item in queue) == expected

@pytest.mark.parametrize('initial, expected', [
    ([1, 2], 2)
])
def test_Queue_len(initial, expected):
    queue = Queue()
    queue._items = initial
    assert len(queue) == expected

def test_Queue_front_empty():
    queue = Queue()
    with pytest.raises(IndexError):
        queue.front()