import pytest
from data.input_code.d02_stack import *

# Stack tests
def test_stack_is_empty_on_new():
    s = Stack()
    assert s.is_empty() is True

def test_stack_size_after_push():
    s = Stack()
    s.push(42)
    assert s.size() == 1

def test_stack_contains_none_after_push_none():
    s = Stack()
    s.push(None)
    assert (None in s) is True

def test_stack_peek_after_push_empty_string():
    s = Stack()
    s.push("")
    assert s.peek() == ""

def test_stack_pop_normal():
    s = Stack()
    s.push(99)
    assert s.pop() == 99

def test_stack_pop_empty_raises():
    s = Stack()
    with pytest.raises(IndexError):
        s.pop()

def test_stack_peek_empty_raises():
    s = Stack()
    with pytest.raises(IndexError):
        s.peek()

def test_stack_clear_results_none_and_len_zero():
    s = Stack()
    s.push(1)
    s.push(2)
    s.push(3)
    result = s.clear()
    assert result is None
    assert len(s) == 0

def test_stack_len_after_pushes():
    s = Stack()
    s.push(10)
    s.push(20)
    assert len(s) == 2

# Queue tests
def test_queue_is_empty_new():
    q = Queue()
    assert q.is_empty() is True

def test_queue_size_after_enqueue():
    q = Queue()
    q.enqueue(7)
    assert q.size() == 1

def test_queue_contains_none_after_enqueue_none():
    q = Queue()
    q.enqueue(None)
    assert (None in q) is True

def test_queue_front_after_enqueue_emptystring():
    q = Queue()
    q.enqueue("")
    assert q.front() == ""

def test_queue_dequeue_normal():
    q = Queue()
    q.enqueue(55)
    assert q.dequeue() == 55

def test_queue_dequeue_empty_raises():
    q = Queue()
    with pytest.raises(IndexError):
        q.dequeue()

def test_queue_front_empty_raises():
    q = Queue()
    with pytest.raises(IndexError):
        q.front()

def test_queue_clear_results_none_and_len_zero():
    q = Queue()
    q.enqueue(4)
    q.enqueue(5)
    q.enqueue(6)
    result = q.clear()
    assert result is None
    assert len(q) == 0

def test_queue_len_after_enqueues():
    q = Queue()
    q.enqueue(1)
    q.enqueue(2)
    q.enqueue(3)
    assert len(q) == 3