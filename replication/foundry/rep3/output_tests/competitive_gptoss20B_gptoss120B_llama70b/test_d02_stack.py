import pytest
from data.input_code.d02_stack import *

# ---------- Stack ----------
@pytest.mark.parametrize("initial_items, expected", [
    ([10], 10),
])
def test_stack_pop_nonempty(initial_items, expected):
    stack = Stack()
    for i in initial_items:
        stack.push(i)
    assert stack.pop() == expected

def test_stack_pop_empty():
    stack = Stack()
    with pytest.raises(IndexError):
        stack.pop()


@pytest.mark.parametrize("initial_items, expected", [
    ([20], 20),
])
def test_stack_peek_nonempty(initial_items, expected):
    stack = Stack()
    for i in initial_items:
        stack.push(i)
    assert stack.peek() == expected

def test_stack_peek_empty():
    stack = Stack()
    with pytest.raises(IndexError):
        stack.peek()


@pytest.mark.parametrize("initial_items, item, expected", [
    ([1, 2, 3], 2, True),
    ([1, 2], 3, False),
])
def test_stack_contains(initial_items, item, expected):
    stack = Stack()
    for i in initial_items:
        stack.push(i)
    assert (item in stack) is expected


@pytest.mark.parametrize("initial_items, expected", [
    ([1, 2, 3], 3),
])
def test_stack_size(initial_items, expected):
    stack = Stack()
    for i in initial_items:
        stack.push(i)
    assert stack.size() == expected


# ---------- Queue ----------
@pytest.mark.parametrize("initial_items, expected", [
    ([7, 8], 7),
])
def test_queue_dequeue_nonempty(initial_items, expected):
    queue = Queue()
    for i in initial_items:
        queue.enqueue(i)
    assert queue.dequeue() == expected

def test_queue_dequeue_empty():
    queue = Queue()
    with pytest.raises(IndexError):
        queue.dequeue()


@pytest.mark.parametrize("initial_items, expected", [
    ([9, 10], 9),
])
def test_queue_front_nonempty(initial_items, expected):
    queue = Queue()
    for i in initial_items:
        queue.enqueue(i)
    assert queue.front() == expected

def test_queue_front_empty():
    queue = Queue()
    with pytest.raises(IndexError):
        queue.front()


@pytest.mark.parametrize("initial_items, item, expected", [
    ([4, 5], 5, True),
    ([4, 5], 6, False),
])
def test_queue_contains(initial_items, item, expected):
    queue = Queue()
    for i in initial_items:
        queue.enqueue(i)
    assert (item in queue) is expected


@pytest.mark.parametrize("initial_items, expected", [
    ([1, 2, 3], 3),
])
def test_queue_size(initial_items, expected):
    queue = Queue()
    for i in initial_items:
        queue.enqueue(i)
    assert queue.size() == expected

@pytest.mark.parametrize("expected", [0])
def test_len_stack_empty(expected):
    stack = Stack()
    assert len(stack) == expected


def test_is_empty_stack_empty():
    stack = Stack()
    assert stack.is_empty() is True


@pytest.mark.parametrize("expected", [0])
def test_len_queue_empty(expected):
    queue = Queue()
    assert len(queue) == expected


def test_is_empty_queue_empty():
    queue = Queue()
    assert queue.is_empty() is True


@pytest.mark.parametrize("item, expected", [
    (1, False),
])
def test_stack_contains_empty(item, expected):
    stack = Stack()
    assert (item in stack) is expected


@pytest.mark.parametrize("item, expected", [
    (1, False),
])
def test_queue_contains_empty(item, expected):
    queue = Queue()
    assert (item in queue) is expected

import pytest

# ---------- Stack ----------
@pytest.mark.parametrize("initial_items, expected", [
    ([1, 2, 3], False),
])
def test_stack_is_empty_nonempty(initial_items, expected):
    stack = Stack()
    for i in initial_items:
        stack.push(i)
    assert stack.is_empty() is expected


@pytest.mark.parametrize("initial_items, expected", [
    ([1, 2, 3], 3),
])
def test_stack_len_nonempty(initial_items, expected):
    stack = Stack()
    for i in initial_items:
        stack.push(i)
    assert len(stack) == expected


def test_stack_clear_returns_none():
    stack = Stack()
    for i in [1, 2, 3]:
        stack.push(i)
    assert stack.clear() is None


# ---------- Queue ----------
@pytest.mark.parametrize("initial_items, expected", [
    ([1, 2, 3], False),
])
def test_queue_is_empty_nonempty(initial_items, expected):
    queue = Queue()
    for i in initial_items:
        queue.enqueue(i)
    assert queue.is_empty() is expected


@pytest.mark.parametrize("initial_items, expected", [
    ([1, 2, 3], 3),
])
def test_queue_len_nonempty(initial_items, expected):
    queue = Queue()
    for i in initial_items:
        queue.enqueue(i)
    assert len(queue) == expected


def test_queue_clear_returns_none():
    queue = Queue()
    for i in [1, 2, 3]:
        queue.enqueue(i)
    assert queue.clear() is None