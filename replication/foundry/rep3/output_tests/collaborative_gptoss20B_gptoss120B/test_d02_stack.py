import pytest
from data.input_code.d02_stack import *

# Stack tests

def test_S1_PUSH():
    s = Stack()
    assert s.push(42) is None

def test_S2_POP_OK():
    s = Stack()
    s.push(42)
    assert s.pop() == 42

def test_S3_POP_ERR():
    s = Stack()
    with pytest.raises(IndexError):
        s.pop()

def test_S4_PEEK_OK():
    s = Stack()
    s.push("test")
    assert s.peek() == "test"

def test_S5_PEEK_ERR():
    s = Stack()
    with pytest.raises(IndexError):
        s.peek()

def test_S6_ISEMPTY_TRUE():
    s = Stack()
    assert s.is_empty() is True

def test_S7_ISEMPTY_FALSE():
    s = Stack()
    s.push(1)
    assert s.is_empty() is False

def test_S8_SIZE():
    s = Stack()
    s.push(1)
    s.push(2)
    s.push(3)
    assert s.size() == 3

def test_S9_CLEAR():
    s = Stack()
    s.push(1)
    s.push(2)
    s.push(3)
    s.clear()
    assert len(s) == 0

def test_S10_LEN():
    s = Stack()
    s.push(10)
    s.clear()
    assert len(s) == 0

def test_S11_CONTAINS_TRUE():
    s = Stack()
    s.push("alpha")
    assert ("alpha" in s) is True

def test_S12_CONTAINS_FALSE():
    s = Stack()
    assert ("beta" in s) is False

# Queue tests

def test_Q1_ENQUEUE():
    q = Queue()
    assert q.enqueue(None) is None

def test_Q2_DEQUEUE_OK():
    q = Queue()
    q.enqueue("first")
    q.enqueue("second")
    q.enqueue("third")
    assert q.dequeue() == "first"

def test_Q3_DEQUEUE_ERR():
    q = Queue()
    with pytest.raises(IndexError):
        q.dequeue()

def test_Q4_FRONT_OK():
    q = Queue()
    q.enqueue("first")
    q.enqueue("second")
    q.enqueue("third")
    assert q.front() == "first"

def test_Q5_FRONT_ERR():
    q = Queue()
    with pytest.raises(IndexError):
        q.front()

def test_Q6_ISEMPTY_TRUE():
    q = Queue()
    assert q.is_empty() is True

def test_Q7_ISEMPTY_FALSE():
    q = Queue()
    q.enqueue("item")
    assert q.is_empty() is False

def test_Q8_SIZE():
    q = Queue()
    q.enqueue("a")
    q.enqueue("b")
    assert q.size() == 2

def test_Q9_CLEAR():
    q = Queue()
    q.enqueue(1)
    q.enqueue(2)
    q.clear()
    assert len(q) == 0

def test_Q10_LEN():
    q = Queue()
    q.enqueue(1)
    q.clear()
    assert len(q) == 0

def test_Q11_CONTAINS_TRUE():
    q = Queue()
    q.enqueue("x")
    assert ("x" in q) is True

def test_Q12_CONTAINS_FALSE():
    q = Queue()
    assert ("y" in q) is False