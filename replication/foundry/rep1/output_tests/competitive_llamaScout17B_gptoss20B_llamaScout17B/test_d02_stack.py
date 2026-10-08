import pytest
from data.input_code.d02_stack import *

def test_S1_INIT():
    s = Stack()
    assert s.size() == 0
    assert s._items == []

def test_S2_PUSH():
    s = Stack()
    s.push(5)
    assert s._items == [5]
    assert s.size() == 1

def test_S3_POP_OK():
    s = Stack()
    s.push(5)
    assert s.pop() == 5
    assert s.is_empty() is True

def test_S4_POP_ERR():
    s = Stack()
    with pytest.raises(IndexError):
        s.pop()

def test_S5_PEEK_OK():
    s = Stack()
    s.push(5)
    assert s.peek() == 5

def test_S6_PEEK_ERR():
    s = Stack()
    with pytest.raises(IndexError):
        s.peek()

def test_S7_IS_EMPTY_TRUE():
    s = Stack()
    assert s.is_empty() is True

def test_S8_IS_EMPTY_FALSE():
    s = Stack()
    s.push(5)
    assert s.is_empty() is False

def test_S9_SIZE():
    s = Stack()
    s.push(5)
    assert s.size() == 1

def test_S10_CLEAR():
    s = Stack()
    s.push(5)
    s.clear()
    assert s._items == []
    assert s.size() == 0

def test_S11_LEN():
    s = Stack()
    assert len(s) == 0

def test_S12_CONTAINS_TRUE():
    s = Stack()
    s.push(5)
    assert (5 in s) is True

def test_S13_CONTAINS_FALSE():
    s = Stack()
    assert (5 in s) is False

def test_Q1_INIT():
    q = Queue()
    assert q.size() == 0
    assert q._items == []

def test_Q2_ENQUEUE():
    q = Queue()
    q.enqueue(5)
    assert q._items == [5]
    assert q.size() == 1

def test_Q3_DEQUEUE_OK():
    q = Queue()
    q.enqueue(5)
    assert q.dequeue() == 5
    assert q.is_empty() is True

def test_Q4_DEQUEUE_ERR():
    q = Queue()
    with pytest.raises(IndexError):
        q.dequeue()

def test_Q5_FRONT_OK():
    q = Queue()
    q.enqueue(5)
    assert q.front() == 5

def test_Q6_FRONT_ERR():
    q = Queue()
    with pytest.raises(IndexError):
        q.front()

def test_Q7_IS_EMPTY_TRUE():
    q = Queue()
    assert q.is_empty() is True

def test_Q8_IS_EMPTY_FALSE():
    q = Queue()
    q.enqueue(5)
    assert q.is_empty() is False

def test_Q9_SIZE():
    q = Queue()
    q.enqueue(5)
    assert q.size() == 1

def test_Q10_CLEAR():
    q = Queue()
    q.enqueue(5)
    q.clear()
    assert q._items == []
    assert q.size() == 0

def test_Q11_LEN():
    q = Queue()
    assert len(q) == 0

def test_Q12_CONTAINS_TRUE():
    q = Queue()
    q.enqueue(5)
    assert (5 in q) is True

def test_Q13_CONTAINS_FALSE():
    q = Queue()
    assert (5 in Queue()) is False