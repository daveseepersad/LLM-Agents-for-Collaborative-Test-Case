import pytest
from data.input_code.d02_stack import *

def test_stack_empty_is_empty():
    s = Stack()
    assert s.is_empty() == True

def test_stack_size_empty():
    s = Stack()
    assert s.size() == 0

def test_stack_len_empty():
    s = Stack()
    assert len(s) == 0

def test_stack_contains_empty():
    s = Stack()
    assert (42 in s) == False

def test_stack_push_peek():
    s = Stack()
    s.push(99)
    assert s.peek() == 99

def test_stack_push_pop():
    s = Stack()
    s.push("alpha")
    assert s.pop() == "alpha"
    assert s.is_empty() == True

def test_stack_pop_empty():
    s = Stack()
    with pytest.raises(IndexError):
        s.pop()

def test_stack_peek_empty():
    s = Stack()
    with pytest.raises(IndexError):
        s.peek()

def test_stack_clear():
    s = Stack()
    s.push(1)
    s.push(2)
    s.push(3)
    assert s.clear() is None
    assert s.is_empty() == True

def test_queue_empty_is_empty():
    q = Queue()
    assert q.is_empty() == True

def test_queue_size_empty():
    q = Queue()
    assert q.size() == 0

def test_queue_len_empty():
    q = Queue()
    assert len(q) == 0

def test_queue_contains_empty():
    q = Queue()
    assert ("x" in q) == False

def test_queue_front_after_enqueue():
    q = Queue()
    q.enqueue(7)
    assert q.front() == 7

def test_queue_enqueue_dequeue():
    q = Queue()
    q.enqueue("beta")
    assert q.dequeue() == "beta"
    assert q.is_empty() == True

def test_queue_dequeue_empty():
    q = Queue()
    with pytest.raises(IndexError):
        q.dequeue()

def test_queue_front_empty():
    q = Queue()
    with pytest.raises(IndexError):
        q.front()

def test_queue_clear():
    q = Queue()
    q.enqueue(4)
    q.enqueue(5)
    assert q.clear() is None
    assert q.is_empty() == True