import pytest
from data.input_code.d02_stack import *

def test_stack_is_empty_new():
    s = Stack()
    assert s.is_empty() is True

def test_stack_pop_empty_raises():
    s = Stack()
    with pytest.raises(IndexError):
        s.pop()

def test_stack_peek_empty_raises():
    s = Stack()
    with pytest.raises(IndexError):
        s.peek()

def test_stack_push_peek():
    s = Stack()
    s.push(42)
    assert s.peek() == 42

def test_stack_push_pop():
    s = Stack()
    s.push(7)
    assert s.pop() == 7

def test_stack_size_after_pushes():
    s = Stack()
    for item in [1, 2, 3]:
        s.push(item)
    assert s.size() == 3

def test_stack_contains_true():
    s = Stack()
    for item in ["a", "b"]:
        s.push(item)
    assert ("b" in s) is True

def test_stack_contains_false():
    s = Stack()
    for item in ["a", "b"]:
        s.push(item)
    assert ("c" in s) is False

def test_stack_clear():
    s = Stack()
    s.push(99)
    s.clear()
    assert s.is_empty() is True

def test_queue_is_empty_new():
    q = Queue()
    assert q.is_empty() is True

def test_queue_dequeue_empty_raises():
    q = Queue()
    with pytest.raises(IndexError):
        q.dequeue()

def test_queue_front_empty_raises():
    q = Queue()
    with pytest.raises(IndexError):
        q.front()

def test_queue_enqueue_front():
    q = Queue()
    q.enqueue(5)
    assert q.front() == 5

def test_queue_enqueue_dequeue():
    q = Queue()
    q.enqueue(10)
    assert q.dequeue() == 10

def test_queue_size_after_enqueues():
    q = Queue()
    for item in [1, 2, 3]:
        q.enqueue(item)
    assert q.size() == 3

def test_queue_contains_true():
    q = Queue()
    for item in ["x", "y"]:
        q.enqueue(item)
    assert ("x" in q) is True

def test_queue_contains_false():
    q = Queue()
    for item in ["x", "y"]:
        q.enqueue(item)
    assert ("z" in q) is False

def test_queue_clear():
    q = Queue()
    q.enqueue(42)
    q.clear()
    assert q.is_empty() is True

def test_stack_not_empty_after_push():
    s = Stack()
    s.push(123)
    assert s.is_empty() is False

def test_stack_len_after_pushes():
    s = Stack()
    s.push(10)
    s.push(20)
    assert s.__len__() == 2

def test_stack_peek_no_remove():
    s = Stack()
    s.push(99)
    top = s.peek()
    assert top == 99
    assert s.size() == 1

def test_stack_pop_lifo_first():
    s = Stack()
    s.push(1)
    s.push(2)
    assert s.pop() == 2

def test_stack_pop_lifo_second():
    s = Stack()
    s.push(1)
    s.push(2)
    s.pop()
    assert s.pop() == 1

def test_stack_size_after_clear():
    s = Stack()
    s.push('a')
    s.push('b')
    s.clear()
    assert s.size() == 0

def test_queue_not_empty_after_enqueue():
    q = Queue()
    q.enqueue(5)
    assert q.is_empty() is False

def test_queue_len_after_enqueues():
    q = Queue()
    q.enqueue(1)
    q.enqueue(2)
    assert q.__len__() == 2

def test_queue_front_no_dequeue():
    q = Queue()
    q.enqueue("x")
    assert q.front() == "x"

def test_queue_dequeue_fifo_first():
    q = Queue()
    q.enqueue("a")
    q.enqueue("b")
    assert q.dequeue() == "a"

def test_queue_dequeue_fifo_second():
    q = Queue()
    q.enqueue("a")
    q.enqueue("b")
    q.dequeue()
    assert q.dequeue() == "b"

def test_queue_size_after_clear():
    q = Queue()
    q.enqueue(1)
    q.enqueue(2)
    q.clear()
    assert q.size() == 0