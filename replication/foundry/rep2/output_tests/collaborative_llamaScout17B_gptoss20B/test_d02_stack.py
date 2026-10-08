import pytest
from data.input_code.d02_stack import *

def test_S1_init():
    s = Stack()
    assert s.size() == 0
    assert s.is_empty() is True

def test_S2_push():
    s = Stack()
    s.push(5)

def test_S3_pop_ok():
    s = Stack()
    s.push(5)
    assert s.pop() == 5

def test_S4_pop_err():
    with pytest.raises(IndexError):
        Stack().pop()

def test_S5_peek_ok():
    s = Stack()
    s.push(5)
    assert s.peek() == 5

def test_S6_peek_err():
    with pytest.raises(IndexError):
        Stack().peek()

def test_S7_is_empty_true():
    s = Stack()
    assert s.is_empty() is True

def test_S8_is_empty_false():
    s = Stack()
    s.push(5)
    assert s.is_empty() is False

def test_S9_size():
    s = Stack()
    s.push(5)
    assert s.size() == 1

def test_S10_clear():
    s = Stack()
    s.push(5)
    s.clear()
    assert s.size() == 0
    assert s.is_empty() is True

def test_S11_len():
    s = Stack()
    s.push(5)
    assert len(s) == 1

def test_S12_contains_true():
    s = Stack()
    s.push(5)
    assert (5 in s) is True

def test_S13_contains_false():
    s = Stack()
    s.push(5)
    assert (10 in s) is False

def test_Q1_init():
    q = Queue()
    assert q.size() == 0
    assert q.is_empty() is True

def test_Q2_enqueue():
    q = Queue()
    q.enqueue(5)

def test_Q3_dequeue_ok():
    q = Queue()
    q.enqueue(5)
    assert q.dequeue() == 5

def test_Q4_dequeue_err():
    with pytest.raises(IndexError):
        Queue().dequeue()

def test_Q5_front_ok():
    q = Queue()
    q.enqueue(5)
    assert q.front() == 5

def test_Q6_front_err():
    with pytest.raises(IndexError):
        Queue().front()

def test_Q7_is_empty_true():
    q = Queue()
    assert q.is_empty() is True

def test_Q8_is_empty_false():
    q = Queue()
    q.enqueue(5)
    assert q.is_empty() is False

def test_Q9_size():
    q = Queue()
    q.enqueue(5)
    assert q.size() == 1

def test_Q10_clear():
    q = Queue()
    q.enqueue(5)
    q.clear()
    assert q.size() == 0
    assert q.is_empty() is True

def test_Q11_len():
    q = Queue()
    q.enqueue(5)
    assert len(q) == 1

def test_Q12_contains_true():
    q = Queue()
    q.enqueue(5)
    assert (5 in q) is True

def test_Q13_contains_false():
    q = Queue()
    q.enqueue(5)
    assert (10 in q) is False