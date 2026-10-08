import pytest
from data.input_code.d02_stack import *

# ---------- Stack Tests ----------

def test_stack_initial_state():
    s = Stack()
    assert s.is_empty() is True
    assert s.size() == 0
    assert len(s) == 0
    assert (1 in s) is False

def test_stack_push_peek_pop_cycle():
    s = Stack()
    s.push(1)
    assert s.is_empty() is False
    assert s.size() == 1
    assert len(s) == 1
    assert s.peek() == 1
    assert s.pop() == 1
    # after pop, stack should be empty again
    assert s.is_empty() is True
    assert s.size() == 0
    assert len(s) == 0

@pytest.mark.parametrize("method,exc", [
    ("pop", IndexError),
    ("peek", IndexError),
])
def test_stack_error_on_empty(method, exc):
    s = Stack()
    with pytest.raises(exc):
        getattr(s, method)()

def test_stack_contains_and_clear():
    s = Stack()
    s.push(2)
    s.push(3)
    assert (2 in s) is True
    assert (1 in s) is False
    s.clear()
    assert s.is_empty() is True
    assert s.size() == 0
    assert len(s) == 0
    assert (2 in s) is False

# ---------- Queue Tests ----------

def test_queue_initial_state():
    q = Queue()
    assert q.is_empty() is True
    assert q.size() == 0
    assert len(q) == 0
    assert (1 in q) is False

def test_queue_enqueue_front_dequeue_cycle():
    q = Queue()
    q.enqueue(1)
    assert q.is_empty() is False
    assert q.size() == 1
    assert len(q) == 1
    assert q.front() == 1
    assert q.dequeue() == 1
    # after dequeue, queue should be empty again
    assert q.is_empty() is True
    assert q.size() == 0
    assert len(q) == 0

@pytest.mark.parametrize("method,exc", [
    ("dequeue", IndexError),
    ("front", IndexError),
])
def test_queue_error_on_empty(method, exc):
    q = Queue()
    with pytest.raises(exc):
        getattr(q, method)()

def test_queue_contains_and_clear():
    q = Queue()
    q.enqueue(2)
    q.enqueue(3)
    assert (2 in q) is True
    assert (1 in q) is False
    q.clear()
    assert q.is_empty() is True
    assert q.size() == 0
    assert len(q) == 0
    assert (2 in q) is False