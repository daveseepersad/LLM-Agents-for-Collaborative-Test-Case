import pytest
from data.input_code.d02_stack import *

def test_S1_PUSH():
    s = Stack()
    s.push(42)
    assert 42 in s
    assert len(s) == 1

def test_S2_POP_NONEMPTY():
    s = Stack()
    s.push(42)
    assert s.pop() == 42

def test_S3_POP_EMPTY():
    s = Stack()
    with pytest.raises(IndexError):
        s.pop()

def test_S4_PEEK_NONEMPTY():
    s = Stack()
    s.push(42)
    assert s.peek() == 42

def test_S5_PEEK_EMPTY():
    s = Stack()
    with pytest.raises(IndexError):
        s.peek()

def test_S6_ISEMPTY_TRUE():
    s = Stack()
    assert s.is_empty()

def test_S7_ISEMPTY_FALSE():
    s = Stack()
    s.push(1)
    assert not s.is_empty()

def test_S8_SIZE():
    s = Stack()
    s.push(1)
    assert s.size() == 1

def test_S9_CLEAR():
    s = Stack()
    s.push(10)
    s.clear()
    assert len(s) == 0

def test_S10_LEN():
    s = Stack()
    s.push(5)
    s.clear()
    assert len(s) == 0

def test_S11_CONTAINS_TRUE():
    s = Stack()
    s.push(99)
    assert 99 in s

def test_S12_CONTAINS_FALSE():
    s = Stack()
    s.push(99)
    assert 100 not in s

def test_Q1_ENQUEUE():
    q = Queue()
    q.enqueue("a")
    assert ("a" in q)
    assert len(q) == 1

def test_Q2_DEQUEUE_NONEMPTY():
    q = Queue()
    q.enqueue("a")
    assert q.dequeue() == "a"

def test_Q3_DEQUEUE_EMPTY():
    q = Queue()
    with pytest.raises(IndexError):
        q.dequeue()

def test_Q4_FRONT_NONEMPTY():
    q = Queue()
    q.enqueue("b")
    assert q.front() == "b"

def test_Q5_FRONT_EMPTY():
    q = Queue()
    with pytest.raises(IndexError):
        q.front()

def test_Q6_ISEMPTY_TRUE():
    q = Queue()
    assert q.is_empty()

def test_Q7_ISEMPTY_FALSE():
    q = Queue()
    q.enqueue(1)
    assert not q.is_empty()

def test_Q8_SIZE():
    q = Queue()
    q.enqueue(1)
    assert q.size() == 1

def test_Q9_CLEAR():
    q = Queue()
    q.enqueue(2)
    q.clear()
    assert len(q) == 0

def test_Q10_LEN():
    q = Queue()
    q.clear()
    assert len(q) == 0

def test_Q11_CONTAINS_TRUE():
    q = Queue()
    q.enqueue(5)
    assert 5 in q

def test_Q12_CONTAINS_FALSE():
    q = Queue()
    q.enqueue(5)
    assert 6 not in q