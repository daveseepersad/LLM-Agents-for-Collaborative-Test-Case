import pytest
from data.input_code.d02_stack import Stack, Queue

def test_stack_operations_and_exceptions():
    s = Stack()
    assert s.is_empty() is True
    # Push multiple items including None and empty string
    s.push(10)
    s.push(None)
    s.push("")
    assert s.size() == 3
    assert len(s) == 3
    assert 10 in s and None in s and "" in s
    assert s.peek() == ""
    assert s.pop() == ""
    assert s.pop() is None
    assert s.pop() == 10
    assert s.is_empty()
    assert len(s) == 0
    with pytest.raises(IndexError):
        s.pop()
    with pytest.raises(IndexError):
        s.peek()
    # Clear should reset the stack
    s.push("a")
    s.clear()
    assert s.is_empty()
    with pytest.raises(IndexError):
        s.peek()
    with pytest.raises(IndexError):
        s.pop()

def test_queue_operations_and_exceptions():
    q = Queue()
    assert q.is_empty() is True
    q.enqueue(1)
    q.enqueue(None)
    q.enqueue("")
    assert q.size() == 3
    assert len(q) == 3
    assert None in q and "" in q and 1 in q
    assert q.front() == 1
    assert q.dequeue() == 1
    assert q.front() is None
    assert q.dequeue() is None
    assert q.dequeue() == ""
    assert q.is_empty()
    with pytest.raises(IndexError):
        q.dequeue()
    with pytest.raises(IndexError):
        q.front()