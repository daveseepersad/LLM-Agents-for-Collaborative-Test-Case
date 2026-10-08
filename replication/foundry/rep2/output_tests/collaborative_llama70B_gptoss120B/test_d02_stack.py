import pytest
from data.input_code.d02_stack import *

# Helper factories
def make_stack(items=None):
    s = Stack()
    if items:
        for it in items:
            s.push(it)
    return s

def make_queue(items=None):
    q = Queue()
    if items:
        for it in items:
            q.enqueue(it)
    return q

# ---------- Stack Tests ----------
def test_stack_initialization():
    s = Stack()
    assert isinstance(s, Stack)
    assert s.is_empty()
    assert s.size() == 0
    assert len(s) == 0

@pytest.mark.parametrize("items", [
    ([5]),
    ([])
])
def test_stack_is_empty_and_size(items):
    s = make_stack(items)
    expected_empty = len(items) == 0
    assert s.is_empty() is expected_empty
    assert s.size() == len(items)
    assert len(s) == len(items)

def test_stack_push_and_contains():
    s = Stack()
    s.push(5)
    assert 5 in s
    assert s.is_empty() is False
    assert s.size() == 1
    assert len(s) == 1

def test_stack_pop_success():
    s = make_stack([5])
    popped = s.pop()
    assert popped == 5
    assert s.is_empty()
    assert s.size() == 0

def test_stack_pop_error():
    s = Stack()
    with pytest.raises(IndexError):
        s.pop()

def test_stack_peek_success():
    s = make_stack([5, 10])
    top = s.peek()
    assert top == 10
    # Ensure peek does not remove the item
    assert s.size() == 2
    assert len(s) == 2

def test_stack_peek_error():
    s = Stack()
    with pytest.raises(IndexError):
        s.peek()

def test_stack_clear():
    s = make_stack([1, 2, 3])
    s.clear()
    assert s.is_empty()
    assert s.size() == 0
    assert len(s) == 0

# ---------- Queue Tests ----------
def test_queue_initialization():
    q = Queue()
    assert isinstance(q, Queue)
    assert q.is_empty()
    assert q.size() == 0
    assert len(q) == 0

@pytest.mark.parametrize("items", [
    ([5]),
    ([])
])
def test_queue_is_empty_and_size(items):
    q = make_queue(items)
    expected_empty = len(items) == 0
    assert q.is_empty() is expected_empty
    assert q.size() == len(items)
    assert len(q) == len(items)

def test_queue_enqueue_and_contains():
    q = Queue()
    q.enqueue(5)
    assert 5 in q
    assert q.is_empty() is False
    assert q.size() == 1
    assert len(q) == 1

def test_queue_dequeue_success():
    q = make_queue([5, 10])
    front = q.dequeue()
    assert front == 5
    # Ensure remaining items shift correctly
    assert q.size() == 1
    assert len(q) == 1
    assert q.front() == 10

def test_queue_dequeue_error():
    q = Queue()
    with pytest.raises(IndexError):
        q.dequeue()

def test_queue_front_success():
    q = make_queue([7])
    assert q.front() == 7
    # front should not remove the item
    assert q.size() == 1
    assert len(q) == 1

def test_queue_front_error():
    q = Queue()
    with pytest.raises(IndexError):
        q.front()

def test_queue_clear():
    q = make_queue([1, 2, 3])
    q.clear()
    assert q.is_empty()
    assert q.size() == 0
    assert len(q) == 0