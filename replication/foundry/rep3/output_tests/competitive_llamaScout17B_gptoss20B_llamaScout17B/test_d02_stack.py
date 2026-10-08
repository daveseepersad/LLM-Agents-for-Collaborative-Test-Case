import pytest
from data.input_code.d02_stack import *

# Stack tests
def test_S1_init_stack():
    s = Stack()
    assert s.size() == 0
    assert s._items == []

def test_S2_push_stack():
    s = Stack()
    res = s.push(5)
    assert res is None

def test_S3_pop_ok():
    s = Stack()
    s.push(5)
    assert s.pop() == 5

def test_S4_pop_err():
    s = Stack()
    with pytest.raises(IndexError):
        s.pop()

def test_S5_peek_ok():
    s = Stack()
    s.push(5)
    assert s.peek() == 5

def test_S6_peek_err():
    s = Stack()
    with pytest.raises(IndexError):
        s.peek()

def test_S7_is_empty_true():
    s = Stack()
    assert s.is_empty() == True

def test_S8_is_empty_false():
    s = Stack()
    s.push(5)
    assert s.is_empty() == False

def test_S9_size():
    s = Stack()
    s.push(5)
    assert s.size() == 1

def test_S10_clear():
    s = Stack()
    s.push(5)
    res = s.clear()
    assert res is None
    assert s.size() == 0
    assert s._items == []

def test_S11_len():
    assert len(Stack()) == 0

def test_S12_contains_true():
    s = Stack()
    s.push(5)
    assert (5 in s) == True

def test_S13_contains_false():
    s = Stack()
    s.push(5)
    assert (10 in s) == False

# Queue tests
def test_Q1_init_queue():
    q = Queue()
    assert q.size() == 0
    assert q._items == []

def test_Q2_enqueue():
    q = Queue()
    res = q.enqueue(5)
    assert res is None

def test_Q3_dequeue_ok():
    q = Queue()
    q.enqueue(5)
    assert q.dequeue() == 5

def test_Q4_dequeue_err():
    q = Queue()
    with pytest.raises(IndexError):
        q.dequeue()

def test_Q5_front_ok():
    q = Queue()
    q.enqueue(5)
    assert q.front() == 5

def test_Q6_front_err():
    q = Queue()
    with pytest.raises(IndexError):
        q.front()

def test_Q7_is_empty_true():
    q = Queue()
    assert q.is_empty() == True

def test_Q8_is_empty_false():
    q = Queue()
    q.enqueue(5)
    assert q.is_empty() == False

def test_Q9_size():
    q = Queue()
    q.enqueue(5)
    assert q.size() == 1

def test_Q10_clear():
    q = Queue()
    q.enqueue(5)
    res = q.clear()
    assert res is None
    assert q.size() == 0
    assert q._items == []

def test_Q11_len():
    assert len(Queue()) == 0

def test_Q12_contains_true():
    q = Queue()
    q.enqueue(5)
    assert (5 in q) == True

def test_Q13_contains_false():
    q = Queue()
    q.enqueue(5)
    assert (10 in q) == False