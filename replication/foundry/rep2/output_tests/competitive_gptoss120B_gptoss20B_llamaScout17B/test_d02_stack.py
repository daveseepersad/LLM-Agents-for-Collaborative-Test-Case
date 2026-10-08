import pytest
from data.input_code.d02_stack import *

def test_S1_empty_is_empty():
    s = Stack()
    assert s.is_empty() is True

def test_S2_push_returns_none_and_contains():
    s = Stack()
    result = s.push(42)
    assert result is None
    assert 42 in s

def test_S3_size_after_push():
    s = Stack()
    s.push(42)
    assert s.size() == 1

def test_S4_len_after_push():
    s = Stack()
    s.push(42)
    assert len(s) == 1

def test_S5_contains_true():
    s = Stack()
    s.push(42)
    assert (42 in s) is True

def test_S6_contains_false():
    s = Stack()
    s.push(42)
    assert (99 in s) is False

def test_S7_peek_ok():
    s = Stack()
    s.push(42)
    assert s.peek() == 42

def test_S8_pop_ok():
    s = Stack()
    s.push(42)
    assert s.pop() == 42

def test_S9_pop_empty_raises():
    s = Stack()
    with pytest.raises(IndexError):
        s.pop()

def test_S10_peek_empty_raises():
    s = Stack()
    with pytest.raises(IndexError):
        s.peek()

def test_S11_clear_empties():
    s = Stack()
    s.push(1)
    s.clear()
    assert s.is_empty() is True

def test_S12_size_after_clear():
    s = Stack()
    s.push(1)
    s.clear()
    assert s.size() == 0

def test_Q1_empty_is_empty_q():
    q = Queue()
    assert q.is_empty() is True

def test_Q2_enqueue_returns_none_and_contains():
    q = Queue()
    result = q.enqueue("x")
    assert result is None
    assert "x" in q

def test_Q3_size_after_enqueue():
    q = Queue()
    q.enqueue("x")
    assert q.size() == 1

def test_Q4_len_after_enqueue():
    q = Queue()
    q.enqueue("x")
    assert len(q) == 1

def test_Q5_contains_true():
    q = Queue()
    q.enqueue("x")
    assert ("x" in q) is True

def test_Q6_contains_false():
    q = Queue()
    q.enqueue("x")
    assert ("y" in q) is False

def test_Q7_front_ok():
    q = Queue()
    q.enqueue("x")
    assert q.front() == "x"

def test_Q8_dequeue_ok():
    q = Queue()
    q.enqueue("x")
    assert q.dequeue() == "x"

def test_Q9_dequeue_empty_raises():
    q = Queue()
    with pytest.raises(IndexError):
        q.dequeue()

def test_Q10_front_empty_raises():
    q = Queue()
    with pytest.raises(IndexError):
        q.front()

def test_Q11_clear_empties():
    q = Queue()
    q.enqueue("a")
    q.clear()
    assert q.is_empty() is True

def test_Q12_size_after_clear():
    q = Queue()
    q.enqueue("a")
    q.clear()
    assert q.size() == 0