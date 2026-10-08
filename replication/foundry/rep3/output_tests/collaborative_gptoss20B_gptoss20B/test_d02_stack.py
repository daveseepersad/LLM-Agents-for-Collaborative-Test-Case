import pytest
from data.input_code.d02_stack import *

# Stack tests
@pytest.mark.parametrize("method, item, expected", [
    ("is_empty", None, True),
    ("__len__", None, 0),
    ("__contains__", 1, False)
])
def test_stack_basic_methods(method, item, expected):
    s = Stack()
    if method == "is_empty":
        assert s.is_empty() == expected
    elif method == "__len__":
        assert len(s) == expected
    elif method == "__contains__":
        assert (item in s) == expected

def test_stack_pop_empty_raises():
    s = Stack()
    with pytest.raises(IndexError):
        s.pop()

def test_stack_peek_empty_raises():
    s = Stack()
    with pytest.raises(IndexError):
        s.peek()

def test_stack_push_returns_none():
    s = Stack()
    result = s.push(99)
    assert result is None

def test_stack_clear_returns_none():
    s = Stack()
    result = s.clear()
    assert result is None

# Queue tests
@pytest.mark.parametrize("method, value, expected", [
    ("is_empty", None, True),
    ("__len__", None, 0),
    ("__contains__", "x", False)
])
def test_queue_basic_methods(method, value, expected):
    q = Queue()
    if method == "is_empty":
        assert q.is_empty() == expected
    elif method == "__len__":
        assert len(q) == expected
    elif method == "__contains__":
        assert (value in q) == expected

def test_queue_dequeue_empty_raises():
    q = Queue()
    with pytest.raises(IndexError):
        q.dequeue()

def test_queue_front_empty_raises():
    q = Queue()
    with pytest.raises(IndexError):
        q.front()

def test_queue_enqueue_returns_none():
    q = Queue()
    result = q.enqueue("a")
    assert result is None

def test_queue_clear_returns_none():
    q = Queue()
    result = q.clear()
    assert result is None

import pytest
from data.input_code.d02_stack import *

def test_stack_pop_after_push():
    s = Stack()
    s.push(1)
    s.push(2)
    assert s.pop() == 2

def test_stack_peek_after_push():
    s = Stack()
    s.push(1)
    s.push(2)
    assert s.peek() == 2

def test_stack_size_after_sequence():
    s = Stack()
    s.push(1)
    s.push(2)
    s.push(3)
    assert s.size() == 3

def test_stack_contains_after_push():
    s = Stack()
    s.push(1)
    s.push(2)
    s.push(3)
    assert (2 in s) is True

def test_queue_dequeue_after_enqueue():
    q = Queue()
    q.enqueue(5)
    q.enqueue(7)
    assert q.dequeue() == 5

def test_queue_front_after_enqueue():
    q = Queue()
    q.enqueue(5)
    q.enqueue(7)
    assert q.front() == 5

def test_queue_size_after_enqueue():
    q = Queue()
    q.enqueue(5)
    q.enqueue(7)
    q.enqueue(9)
    assert q.size() == 3