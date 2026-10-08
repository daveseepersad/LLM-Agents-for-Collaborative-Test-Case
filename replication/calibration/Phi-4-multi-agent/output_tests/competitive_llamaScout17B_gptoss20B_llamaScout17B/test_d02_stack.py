import pytest
from data.input_code.d02_stack import *

def test_S1_INIT_stack():
    s = Stack()
    assert isinstance(s, Stack)
    assert s._items == []

def test_S2_PUSH_stack():
    s = Stack()
    s.push(1)
    assert s._items == [1]

def test_S3_POP_stack():
    s = Stack()
    s.push(1)
    val = s.pop()
    assert val == 1
    assert s._items == []

def test_S4_POP_ERR_stack():
    s = Stack()
    with pytest.raises(IndexError):
        s.pop()

def test_S5_PEEK_stack():
    s = Stack()
    s.push(1)
    assert s.peek() == 1

def test_S6_PEEK_ERR_stack():
    s = Stack()
    with pytest.raises(IndexError):
        s.peek()

def test_S7_IS_EMPTY_stack():
    s = Stack()
    assert s.is_empty() is True

def test_S8_SIZE_stack():
    s = Stack()
    assert s.size() == 0

def test_S9_CLEAR_stack():
    s = Stack()
    s.push(1)
    s.clear()
    assert s._items == []

def test_S10_LEN_stack():
    s = Stack()
    assert len(s) == 0

def test_S11_CONTAINS_stack():
    s = Stack()
    assert (1 in s) is False

def test_Q1_INIT_queue():
    q = Queue()
    assert isinstance(q, Queue)
    assert q._items == []

def test_Q2_ENQUEUE_queue():
    q = Queue()
    q.enqueue(1)
    assert q._items == [1]

def test_Q3_DEQUEUE_queue():
    q = Queue()
    q.enqueue(1)
    val = q.dequeue()
    assert val == 1
    assert q._items == []

def test_Q4_DEQUEUE_ERR_queue():
    q = Queue()
    with pytest.raises(IndexError):
        q.dequeue()

def test_Q5_FRONT_queue():
    q = Queue()
    q.enqueue(1)
    assert q.front() == 1

def test_Q6_FRONT_ERR_queue():
    q = Queue()
    with pytest.raises(IndexError):
        q.front()

def test_Q7_IS_EMPTY_queue():
    q = Queue()
    assert q.is_empty() is True

def test_Q8_SIZE_queue():
    q = Queue()
    assert q.size() == 0

def test_Q9_CLEAR_queue():
    q = Queue()
    q.enqueue(1)
    q.clear()
    assert q._items == []

def test_Q10_LEN_queue():
    q = Queue()
    assert len(q) == 0

def test_Q11_CONTAINS_queue():
    q = Queue()
    assert (1 in q) is False