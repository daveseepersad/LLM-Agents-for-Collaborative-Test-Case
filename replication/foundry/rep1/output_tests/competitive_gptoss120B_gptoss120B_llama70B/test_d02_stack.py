import pytest
from data.input_code.d02_stack import *

# ---------- Stack Tests ----------

def test_stack_push_returns_none():
    s = Stack()
    result = s.push(1)
    assert result is None

def test_stack_basic_operations():
    s = Stack()
    s.push(1)
    assert s.size() == 1
    assert s.peek() == 1
    assert s.pop() == 1
    assert s.is_empty()

def test_stack_pop_empty_raises():
    s = Stack()
    with pytest.raises(IndexError):
        s.pop()

def test_stack_peek_empty_raises():
    s = Stack()
    with pytest.raises(IndexError):
        s.peek()

def test_stack_is_empty_after_clear():
    s = Stack()
    s.push('x')
    s.clear()
    assert s.is_empty()

@pytest.mark.parametrize(
    "item,expected",
    [
        (None, True),          # after pushing None
        ("missing", False),   # not present
    ],
)
def test_stack_contains(item, expected):
    s = Stack()
    if expected:
        s.push(None)  # only push None when we expect it to be contained
    assert (item in s) is expected

def test_stack_len_after_clear():
    s = Stack()
    s.clear()
    assert len(s) == 0

# ---------- Queue Tests ----------

def test_queue_enqueue_returns_none():
    q = Queue()
    result = q.enqueue('a')
    assert result is None

def test_queue_basic_operations():
    q = Queue()
    q.enqueue('a')
    assert q.size() == 1
    assert q.front() == 'a'
    assert q.dequeue() == 'a'
    assert q.is_empty()

def test_queue_dequeue_empty_raises():
    q = Queue()
    with pytest.raises(IndexError):
        q.dequeue()

def test_queue_front_empty_raises():
    q = Queue()
    with pytest.raises(IndexError):
        q.front()

def test_queue_is_empty_after_clear():
    q = Queue()
    q.enqueue('x')
    q.clear()
    assert q.is_empty()

@pytest.mark.parametrize(
    "item,expected",
    [
        (5, True),   # after enqueuing 5
        (9, False),  # not present
    ],
)
def test_queue_contains(item, expected):
    q = Queue()
    if expected:
        q.enqueue(item)
    assert (item in q) is expected

def test_queue_len_after_clear():
    q = Queue()
    q.clear()
    assert len(q) == 0