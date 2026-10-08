import pytest
from data.input_code.d02_stack import *

# ---------- Stack Tests ----------

def test_stack_init():
    s = Stack()
    assert s.is_empty()
    assert len(s) == 0

def test_stack_push_and_state():
    s = Stack()
    s.push(5)
    assert not s.is_empty()
    assert s.peek() == 5
    assert s.size() == 1
    assert len(s) == 1
    assert (5 in s) is True
    assert (10 in s) is False

def test_stack_pop():
    s = Stack()
    s.push(5)
    assert s.pop() == 5
    assert s.is_empty()

def test_stack_pop_error():
    s = Stack()
    with pytest.raises(IndexError):
        s.pop()

def test_stack_peek():
    s = Stack()
    s.push(5)
    assert s.peek() == 5

def test_stack_peek_error():
    s = Stack()
    with pytest.raises(IndexError):
        s.peek()

def test_stack_is_empty_true():
    s = Stack()
    assert s.is_empty() is True

def test_stack_is_empty_false():
    s = Stack()
    s.push(5)
    assert s.is_empty() is False

def test_stack_clear():
    s = Stack()
    s.push(5)
    s.clear()
    assert s.is_empty()
    assert len(s) == 0

# ---------- Queue Tests ----------

def test_queue_init():
    q = Queue()
    assert q.is_empty()
    assert len(q) == 0

def test_queue_enqueue_and_state():
    q = Queue()
    q.enqueue(5)
    assert not q.is_empty()
    assert q.front() == 5
    assert q.size() == 1
    assert len(q) == 1
    assert (5 in q) is True
    assert (10 in q) is False

def test_queue_dequeue():
    q = Queue()
    q.enqueue(5)
    assert q.dequeue() == 5
    assert q.is_empty()

def test_queue_dequeue_error():
    q = Queue()
    with pytest.raises(IndexError):
        q.dequeue()

def test_queue_front():
    q = Queue()
    q.enqueue(5)
    assert q.front() == 5

def test_queue_front_error():
    q = Queue()
    with pytest.raises(IndexError):
        q.front()

def test_queue_is_empty_true():
    q = Queue()
    assert q.is_empty() is True

def test_queue_is_empty_false():
    q = Queue()
    q.enqueue(5)
    assert q.is_empty() is False

def test_queue_clear():
    q = Queue()
    q.enqueue(5)
    q.clear()
    assert q.is_empty()
    assert len(q) == 0