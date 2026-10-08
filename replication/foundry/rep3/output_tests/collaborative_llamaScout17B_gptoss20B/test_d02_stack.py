import pytest
from data.input_code.d02_stack import *

def test_S1_INIT():
    s = Stack()
    assert s.size() == 0
    assert s.is_empty() is True
    assert len(s) == 0

def test_S2_PUSH():
    s = Stack()
    s.push(5)
    assert s.size() == 1

def test_S3_POP_OK():
    s = Stack()
    s.push(5)
    assert s.pop() == 5

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
    assert len(s) == 0

def test_S8_IS_EMPTY_FALSE():
    s = Stack()
    s.push(5)
    assert s.is_empty() is False

def test_S9_SIZE():
    s = Stack()
    s.push(5)
    assert s.size() == 1

def test_S11_LEN():
    s = Stack()
    s.push(5)
    assert len(s) == 1

@pytest.mark.parametrize("item, expected", [(5, True), (10, False)])
def test_S12_S13_CONTAINS(item, expected):
    s = Stack()
    s.push(5)
    assert (item in s) == expected

def test_Q1_INIT():
    q = Queue()
    assert q.size() == 0
    assert q.is_empty() is True
    assert len(q) == 0

def test_Q2_ENQUEUE():
    q = Queue()
    q.enqueue(5)
    assert q.size() == 1

def test_Q3_DEQUEUE_OK():
    q = Queue()
    q.enqueue(5)
    assert q.dequeue() == 5

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
    assert len(q) == 0

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
    assert q.is_empty() is True
    assert len(q) == 0

def test_Q11_LEN():
    q = Queue()
    q.enqueue(5)
    assert len(q) == 1

@pytest.mark.parametrize("item, expected", [(5, True), (10, False)])
def test_Q12_Q13_CONTAINS(item, expected):
    q = Queue()
    q.enqueue(5)
    assert (item in q) == expected

import pytest
from data.input_code.d02_stack import *

def test_T_STACK_CLEAR():
    s = Stack()
    s.push(1)
    s.clear()
    assert s.is_empty() is True

def test_T_STACK_MULTIPLE_PUSH_POP():
    s = Stack()
    s.push(5)
    s.push(10)
    _ = s.pop()
    s.push(5)
    result = s.pop()
    assert result == 5

def test_T_QUEUE_MULTIPLE_ENQUEUE_DEQUEUE():
    q = Queue()
    q.enqueue(5)
    q.enqueue(5)
    q.dequeue()
    second = q.dequeue()
    assert second == 5