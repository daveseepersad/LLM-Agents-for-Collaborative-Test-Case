import pytest
from data.input_code.d02_stack import *

def test_stack_init():
    s = Stack()
    assert isinstance(s, Stack)
    assert s.is_empty() is True
    assert len(s) == 0

def test_stack_push():
    s = Stack()
    s.push(5)
    assert s.size() == 1
    assert len(s) == 1
    assert 5 in s
    assert s.is_empty() is False

def test_stack_pop():
    s = Stack()
    s.push(5)
    assert s.pop() == 5
    assert s.is_empty() is True
    assert len(s) == 0

def test_stack_pop_empty_raises():
    s = Stack()
    with pytest.raises(IndexError):
        s.pop()

def test_stack_peek():
    s = Stack()
    s.push(5)
    assert s.peek() == 5
    # ensure stack remains unchanged
    assert len(s) == 1
    assert not s.is_empty()

def test_stack_peek_empty_raises():
    s = Stack()
    with pytest.raises(IndexError):
        s.peek()

def test_stack_is_empty_false_true():
    s_not_empty = Stack()
    s_not_empty.push(5)
    assert s_not_empty.is_empty() is False

    s_empty = Stack()
    assert s_empty.is_empty() is True

def test_stack_size_len_contains():
    s = Stack()
    s.push(5)
    assert s.size() == 1
    assert len(s) == 1
    assert 5 in s
    assert 10 not in s

def test_queue_init():
    q = Queue()
    assert q.is_empty() is True
    assert len(q) == 0

def test_queue_enqueue():
    q = Queue()
    q.enqueue(5)
    assert q.is_empty() is False
    assert q.size() == 1
    assert 5 in q
    assert len(q) == 1

def test_queue_dequeue():
    q = Queue()
    q.enqueue(5)
    assert q.dequeue() == 5
    assert q.is_empty() is True
    assert len(q) == 0

def test_queue_dequeue_empty_raises():
    q = Queue()
    with pytest.raises(IndexError):
        q.dequeue()

def test_queue_front():
    q = Queue()
    q.enqueue(5)
    assert q.front() == 5
    # ensure front does not remove the item
    assert len(q) == 1

def test_queue_front_empty_raises():
    q = Queue()
    with pytest.raises(IndexError):
        q.front()

def test_queue_is_empty_false_true():
    q_not_empty = Queue()
    q_not_empty.enqueue(5)
    assert q_not_empty.is_empty() is False

    q_empty = Queue()
    assert q_empty.is_empty() is True

def test_queue_size_len():
    q = Queue()
    q.enqueue(5)
    assert q.size() == 1
    assert len(q) == 1

def test_queue_clear_len_zero():
    q = Queue()
    q.enqueue(5)
    q.clear()
    assert len(q) == 0
    assert q.is_empty() is True

def test_queue_contains_true_false():
    q = Queue()
    q.enqueue(5)
    assert 5 in q
    assert 10 not in q