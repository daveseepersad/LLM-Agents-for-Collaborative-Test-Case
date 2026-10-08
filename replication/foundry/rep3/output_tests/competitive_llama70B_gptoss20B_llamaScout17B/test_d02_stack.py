import pytest
from data.input_code.d02_stack import *

def test_T1_stack_init():
    s = Stack()
    assert isinstance(s, Stack)
    assert len(s) == 0

def test_T2_stack_push():
    s = Stack()
    s.push(1)
    assert len(s) == 1
    assert 1 in s

def test_T3_stack_pop_empty():
    s = Stack()
    with pytest.raises(IndexError):
        s.pop()

def test_T4_stack_pop_ok():
    s = Stack()
    s.push(1)
    assert s.pop() == 1

def test_T5_stack_peek_empty():
    s = Stack()
    with pytest.raises(IndexError):
        s.peek()

def test_T6_stack_peek_ok():
    s = Stack()
    s.push(1)
    assert s.peek() == 1

def test_T7_stack_is_empty():
    s = Stack()
    assert s.is_empty() is True

def test_T8_stack_is_empty_false():
    s = Stack()
    s.push(1)
    assert s.is_empty() is False

def test_T9_stack_size_empty():
    s = Stack()
    assert s.size() == 0

def test_T10_stack_size_ok():
    s = Stack()
    s.push(1)
    assert s.size() == 1

def test_T11_stack_clear():
    s = Stack()
    s.push(1)
    s.clear()
    assert len(s) == 0
    assert s.is_empty() is True

def test_T12_stack_contains_empty():
    s = Stack()
    assert (1 in s) is False

def test_T13_stack_contains_ok():
    s = Stack()
    s.push(1)
    assert (1 in s) is True

def test_T14_queue_init():
    q = Queue()
    assert len(q) == 0
    assert q.is_empty() is True

def test_T15_queue_enqueue():
    q = Queue()
    q.enqueue(1)
    assert len(q) == 1
    assert (1 in q) is True

def test_T16_queue_dequeue_empty():
    q = Queue()
    with pytest.raises(IndexError):
        q.dequeue()

def test_T17_queue_dequeue_ok():
    q = Queue()
    q.enqueue(1)
    assert q.dequeue() == 1

def test_T18_queue_front_empty():
    q = Queue()
    with pytest.raises(IndexError):
        q.front()

def test_T19_queue_front_ok():
    q = Queue()
    q.enqueue(1)
    assert q.front() == 1

def test_T20_queue_is_empty():
    q = Queue()
    assert q.is_empty() is True

def test_T21_queue_is_empty_false():
    q = Queue()
    q.enqueue(1)
    assert q.is_empty() is False

def test_T22_queue_size_empty():
    q = Queue()
    assert q.size() == 0

def test_T23_queue_size_ok():
    q = Queue()
    q.enqueue(1)
    assert q.size() == 1

def test_T24_queue_clear():
    q = Queue()
    q.enqueue(1)
    q.clear()
    assert len(q) == 0

def test_T25_queue_contains_empty():
    q = Queue()
    assert (1 in q) is False

def test_T26_queue_contains_ok():
    q = Queue()
    q.enqueue(1)
    assert (1 in q) is True