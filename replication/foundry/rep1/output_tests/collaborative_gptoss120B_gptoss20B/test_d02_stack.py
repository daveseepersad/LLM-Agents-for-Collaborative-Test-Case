import pytest
from data.input_code.d02_stack import *

@pytest.fixture
def empty_stack():
    return Stack()

@pytest.fixture
def empty_queue():
    return Queue()


def test_stack_pop_empty(empty_stack):
    with pytest.raises(IndexError):
        empty_stack.pop()


def test_stack_peek_empty(empty_stack):
    with pytest.raises(IndexError):
        empty_stack.peek()


def test_queue_dequeue_empty(empty_queue):
    with pytest.raises(IndexError):
        empty_queue.dequeue()


def test_queue_front_empty(empty_queue):
    with pytest.raises(IndexError):
        empty_queue.front()


def test_stack_push_returns_none(empty_stack):
    result = empty_stack.push("A")
    assert result is None
    assert "A" in empty_stack


def test_queue_enqueue_returns_none(empty_queue):
    result = empty_queue.enqueue("A")
    assert result is None
    assert "A" in empty_queue


@pytest.mark.parametrize("stack,expected", [
    (Stack(), True),
])
def test_stack_is_empty_init(stack, expected):
    assert stack.is_empty() == expected


@pytest.mark.parametrize("queue,expected", [
    (Queue(), True),
])
def test_queue_is_empty_init(queue, expected):
    assert queue.is_empty() == expected


@pytest.mark.parametrize("stack,expected", [
    (Stack(), 0),
])
def test_stack_size_init(stack, expected):
    assert stack.size() == expected


@pytest.mark.parametrize("queue,expected", [
    (Queue(), 0),
])
def test_queue_size_init(queue, expected):
    assert queue.size() == expected


@pytest.mark.parametrize("item,expected", [
    (1, False),
])
def test_stack_contains_init(item, expected):
    stack = Stack()
    assert (item in stack) == expected


@pytest.mark.parametrize("item,expected", [
    (1, False),
])
def test_queue_contains_init(item, expected):
    queue = Queue()
    assert (item in queue) == expected

import pytest
from data.input_code.d02_stack import *

@pytest.mark.parametrize("items,expected", [
    ([1, 2, 3], 3),
])
def test_stack_pop_nonempty(items, expected):
    stack = Stack()
    for i in items:
        stack.push(i)
    result = stack.pop()
    assert result == expected
    assert len(stack) == len(items) - 1
    # ensure the popped element is no longer in the stack
    assert expected not in stack

@pytest.mark.parametrize("items,expected", [
    ([1, 2, 3], 3),
])
def test_stack_peek_nonempty(items, expected):
    stack = Stack()
    for i in items:
        stack.push(i)
    result = stack.peek()
    assert result == expected
    # size should remain unchanged
    assert len(stack) == len(items)
    # top element should still be present
    assert expected in stack

@pytest.mark.parametrize("items", [
    ([1, 2, 3]),
])
def test_stack_clear(items):
    stack = Stack()
    for i in items:
        stack.push(i)
    result = stack.clear()
    assert result is None
    assert stack.is_empty()
    assert len(stack) == 0

@pytest.mark.parametrize("items,expected", [
    ([1, 2, 3], 1),
])
def test_queue_dequeue_nonempty(items, expected):
    queue = Queue()
    for i in items:
        queue.enqueue(i)
    result = queue.dequeue()
    assert result == expected
    assert len(queue) == len(items) - 1
    # ensure the dequeued element is no longer in the queue
    assert expected not in queue

@pytest.mark.parametrize("items,expected", [
    ([1, 2, 3], 1),
])
def test_queue_front_nonempty(items, expected):
    queue = Queue()
    for i in items:
        queue.enqueue(i)
    result = queue.front()
    assert result == expected
    # size should remain unchanged
    assert len(queue) == len(items)
    # front element should still be present
    assert expected in queue

@pytest.mark.parametrize("items", [
    ([1, 2, 3]),
])
def test_queue_clear(items):
    queue = Queue()
    for i in items:
        queue.enqueue(i)
    result = queue.clear()
    assert result is None
    assert queue.is_empty()
    assert len(queue) == 0