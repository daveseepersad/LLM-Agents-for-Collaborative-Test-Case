import pytest
from data.input_code.d02_stack import *

def test_stack_init():
    # Stack initialization should not raise
    s = Stack()

def test_stack_push_and_pop():
    s = Stack()
    s.push(5)
    assert s.pop() == 5
    assert s.is_empty() is True

def test_stack_pop_from_empty_raises():
    s = Stack()
    with pytest.raises(IndexError):
        s.pop()

def test_stack_peek_and_errors():
    s = Stack()
    with pytest.raises(IndexError):
        s.peek()
    s.push(5)
    assert s.peek() == 5

def test_stack_len_contains_is_empty_and_clear():
    s = Stack()
    assert s.is_empty() is True
    assert len(s) == 0
    assert (5 in s) is False

    s.push(5)
    assert s.is_empty() is False
    assert len(s) == 1
    assert (5 in s) is True

    s.clear()
    assert len(s) == 0
    assert s.is_empty() is True

def test_queue_init():
    # Queue initialization should not raise
    q = Queue()

def test_queue_enqueue_and_front_and_size_and_len_and_contains():
    q = Queue()
    q.enqueue(5)
    assert q.front() == 5
    assert q.size() == 1
    assert len(q) == 1
    assert (5 in q) is True

def test_queue_dequeue_from_empty_raises():
    q = Queue()
    with pytest.raises(IndexError):
        q.dequeue()

def test_queue_dequeue_and_front_after_enqueue():
    q = Queue()
    q.enqueue(5)
    assert q.dequeue() == 5
    assert q.is_empty() is True

def test_queue_front_from_empty_raises():
    q = Queue()
    with pytest.raises(IndexError):
        q.front()

def test_queue_is_empty_and_size_and_len_and_clear():
    q = Queue()
    assert q.is_empty() is True
    assert q.size() == 0
    assert len(q) == 0

    q.enqueue(5)
    assert q.is_empty() is False
    assert q.size() == 1
    assert len(q) == 1

    q.clear()
    assert q.is_empty() is True
    assert len(q) == 0