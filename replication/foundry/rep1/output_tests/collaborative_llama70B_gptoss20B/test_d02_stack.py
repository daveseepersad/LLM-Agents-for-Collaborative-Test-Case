import pytest
from data.input_code.d02_stack import *

def test_T1_stack_init():
    s = Stack()
    assert isinstance(s, Stack)

def test_T2_stack_push():
    s = Stack()
    s.push(1)
    assert s.size() == 1

def test_T3_stack_pop_empty():
    s = Stack()
    with pytest.raises(IndexError):
        s.pop()

def test_T4_stack_pop_with_setup():
    s = Stack()
    s.push(1)
    assert s.pop() == 1

def test_T5_stack_peek_empty():
    s = Stack()
    with pytest.raises(IndexError):
        s.peek()

def test_T6_stack_peek_with_setup():
    s = Stack()
    s.push(1)
    assert s.peek() == 1

def test_T7_stack_is_empty_empty():
    s = Stack()
    assert s.is_empty() is True

def test_T8_stack_is_empty_with_setup():
    s = Stack()
    s.push(1)
    assert s.is_empty() is False

def test_T9_stack_size_empty():
    s = Stack()
    assert s.size() == 0

def test_T10_stack_size_with_setup():
    s = Stack()
    s.push(1)
    assert s.size() == 1

def test_T11_stack_clear():
    s = Stack()
    s.clear()
    assert s.is_empty() is True

def test_T12_stack_len_empty():
    s = Stack()
    assert len(s) == 0

def test_T13_stack_len_with_setup():
    s = Stack()
    s.push(1)
    assert len(s) == 1

def test_T14_stack_contains_empty():
    s = Stack()
    assert (1 in s) is False

def test_T15_stack_contains_with_setup():
    s = Stack()
    s.push(1)
    assert (1 in s) is True

def test_T16_queue_init():
    q = Queue()
    assert isinstance(q, Queue)

def test_T17_queue_enqueue():
    q = Queue()
    q.enqueue(1)
    assert q.size() == 1

def test_T18_queue_dequeue_empty():
    q = Queue()
    with pytest.raises(IndexError):
        q.dequeue()

def test_T19_queue_dequeue_with_setup():
    q = Queue()
    q.enqueue(1)
    assert q.dequeue() == 1

def test_T20_queue_front_empty():
    q = Queue()
    with pytest.raises(IndexError):
        q.front()

def test_T21_queue_front_with_setup():
    q = Queue()
    q.enqueue(1)
    assert q.front() == 1

def test_T22_queue_is_empty_empty():
    q = Queue()
    assert q.is_empty() is True

def test_T23_queue_is_empty_with_setup():
    q = Queue()
    q.enqueue(1)
    assert q.is_empty() is False

def test_T24_queue_size_empty():
    q = Queue()
    assert q.size() == 0

def test_T25_queue_size_with_setup():
    q = Queue()
    q.enqueue(1)
    assert q.size() == 1

def test_T26_queue_clear():
    q = Queue()
    q.clear()
    assert len(q) == 0

def test_T27_queue_len_empty():
    q = Queue()
    assert len(q) == 0

def test_T28_queue_len_with_setup():
    q = Queue()
    q.enqueue(1)
    assert len(q) == 1

def test_T29_queue_contains_empty():
    q = Queue()
    assert (1 in q) is False

def test_T30_queue_contains_with_setup():
    q = Queue()
    q.enqueue(1)
    assert (1 in q) is True