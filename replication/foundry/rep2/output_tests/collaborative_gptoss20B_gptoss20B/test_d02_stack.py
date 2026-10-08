import pytest
from data.input_code.d02_stack import *

def test_T1_Stack_push_basic():
    s = Stack()
    s.push(5)
    assert len(s) == 1
    assert 5 in s

def test_T2_Stack_pop_nonempty():
    s = Stack()
    s.push(1)
    s.push(2)
    assert s.pop() == 2
    assert len(s) == 1
    assert 1 in s

def test_T3_Stack_pop_empty():
    s = Stack()
    with pytest.raises(IndexError):
        s.pop()

def test_T4_Stack_peek_nonempty():
    s = Stack()
    s.push(3)
    s.push(4)
    assert s.peek() == 4

def test_T5_Stack_peek_empty():
    s = Stack()
    with pytest.raises(IndexError):
        s.peek()

def test_T6_Stack_is_empty_true():
    s = Stack()
    assert s.is_empty() is True

def test_T7_Stack_is_empty_false():
    s = Stack()
    s.push(1)
    assert s.is_empty() is False

def test_T8_Stack_size_nonempty():
    s = Stack()
    s.push(1)
    s.push(2)
    s.push(3)
    assert s.size() == 3

def test_T9_Stack_clear():
    s = Stack()
    s.push(1)
    s.push(2)
    s.clear()
    assert len(s) == 0
    assert (1 in s) is False

def test_T10_Stack_len():
    s = Stack()
    s.push(1)
    s.push(2)
    s.push(3)
    assert len(s) == 3

def test_T11_Stack_contains_present():
    s = Stack()
    s.push(1)
    s.push(2)
    s.push(3)
    assert (2 in s) is True

def test_T12_Stack_contains_missing():
    s = Stack()
    s.push(1)
    s.push(2)
    s.push(3)
    assert (4 in s) is False

def test_T13_Queue_enqueue():
    q = Queue()
    q.enqueue(9)
    assert len(q) == 1
    assert 9 in q

def test_T14_Queue_dequeue_nonempty():
    q = Queue()
    for v in [1, 2, 3]:
        q.enqueue(v)
    assert q.dequeue() == 1
    assert len(q) == 2

def test_T15_Queue_dequeue_empty():
    q = Queue()
    with pytest.raises(IndexError):
        q.dequeue()

def test_T16_Queue_front_nonempty():
    q = Queue()
    q.enqueue(7)
    q.enqueue(8)
    assert q.front() == 7

def test_T17_Queue_front_empty():
    q = Queue()
    with pytest.raises(IndexError):
        q.front()

def test_T18_Queue_is_empty_true():
    q = Queue()
    assert q.is_empty() is True

def test_T19_Queue_is_empty_false():
    q = Queue()
    q.enqueue(1)
    assert q.is_empty() is False

def test_T20_Queue_size():
    q = Queue()
    for v in [1, 2, 3]:
        q.enqueue(v)
    assert q.size() == 3

def test_T21_Queue_clear():
    q = Queue()
    q.enqueue(1)
    q.enqueue(2)
    q.clear()
    assert len(q) == 0

def test_T22_Queue_len():
    q = Queue()
    for v in [1, 2, 3]:
        q.enqueue(v)
    assert len(q) == 3

def test_T23_Queue_contains_present():
    q = Queue()
    for v in [1, 2, 3]:
        q.enqueue(v)
    assert (2 in q) is True

def test_T24_Queue_contains_missing():
    q = Queue()
    for v in [1, 2, 3]:
        q.enqueue(v)
    assert (4 in q) is False