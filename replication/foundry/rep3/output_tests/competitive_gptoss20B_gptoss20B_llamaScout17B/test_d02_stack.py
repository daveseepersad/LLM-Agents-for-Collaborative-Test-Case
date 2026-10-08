import pytest
from data.input_code.d02_stack import *

# Stack tests

@pytest.mark.parametrize("initial_items, expected", [
    ([], True),
    ([1], False),
])
def test_stack_is_empty(initial_items, expected):
    s = Stack()
    for item in initial_items:
        s.push(item)
    assert s.is_empty() is expected

def test_stack_pop_non_empty():
    s = Stack()
    for item in [1, 2, 3]:
        s.push(item)
    assert s.pop() == 3

def test_stack_peek_non_empty():
    s = Stack()
    for item in [5, 6]:
        s.push(item)
    assert s.peek() == 6

def test_stack_size():
    s = Stack()
    for item in [1, 2, 3, 4]:
        s.push(item)
    assert s.size() == 4

def test_stack_len_matches_size():
    s = Stack()
    for item in [9, 8]:
        s.push(item)
    assert len(s) == 2

@pytest.mark.parametrize("initial_items, item, expected", [
    ([1, 2, 3], 2, True),
    ([1, 2, 3], 5, False),
])
def test_stack_contains(initial_items, item, expected):
    s = Stack()
    for it in initial_items:
        s.push(it)
    assert (item in s) == expected

# Queue tests

@pytest.mark.parametrize("initial_items, expected", [
    ([], True),
    ([1], False),
])
def test_queue_is_empty(initial_items, expected):
    q = Queue()
    for item in initial_items:
        q.enqueue(item)
    assert q.is_empty() is expected

def test_queue_dequeue_non_empty():
    q = Queue()
    for item in [1, 2, 3]:
        q.enqueue(item)
    assert q.dequeue() == 1

def test_queue_dequeue_empty_raises():
    q = Queue()
    with pytest.raises(IndexError):
        q.dequeue()

def test_queue_front_non_empty():
    q = Queue()
    for item in [9, 8]:
        q.enqueue(item)
    assert q.front() == 9

def test_queue_front_empty_raises():
    q = Queue()
    with pytest.raises(IndexError):
        q.front()

def test_queue_size():
    q = Queue()
    for item in [1, 2, 3]:
        q.enqueue(item)
    assert q.size() == 3

@pytest.mark.parametrize("initial_items, item, expected", [
    ([1, 2, 3], 2, True),
    ([1, 2, 3], 5, False),
])
def test_queue_contains(initial_items, item, expected):
    q = Queue()
    for it in initial_items:
        q.enqueue(it)
    assert (item in q) == expected

def test_stack_pop_empty_raises():
    s = Stack()
    with pytest.raises(IndexError):
        s.pop()

def test_stack_peek_empty_raises():
    s = Stack()
    with pytest.raises(IndexError):
        s.peek()

def test_stack_clear_executes_without_error():
    s = Stack()
    for item in [1, 2, 3]:
        s.push(item)
    s.clear()
    assert len(s) == 0

def test_queue_clear_executes_without_error():
    q = Queue()
    for item in [1, 2]:
        q.enqueue(item)
    q.clear()
    assert q.is_empty() is True
    assert len(q) == 0