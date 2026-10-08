import pytest
from data.input_code.d02_stack import Stack, Queue

def test_stack_operations_and_edge_cases():
    s = Stack()
    # Initially empty
    assert s.is_empty()
    assert len(s) == 0
    assert s.size() == 0
    assert not (1 in s)

    # Push various types including None and empty string
    items = [42, None, "", "last"]
    for item in items:
        s.push(item)
        assert s.peek() == item  # peek should return the most recent item
        assert item in s

    # Size checks
    assert s.size() == len(items)
    assert len(s) == len(items)

    # Pop items and verify order (LIFO)
    for expected in reversed(items):
        popped = s.pop()
        assert popped is expected
    # After popping all, stack should be empty again
    assert s.is_empty()
    assert s.size() == 0
    assert len(s) == 0

    # Clear on already empty stack should keep it empty
    s.clear()
    assert s.is_empty()
    assert s.size() == 0

def test_stack_exceptions():
    s = Stack()
    # Pop from empty raises IndexError
    with pytest.raises(IndexError, match="Pop from empty stack"):
        s.pop()
    # Peek from empty raises IndexError
    with pytest.raises(IndexError, match="Peek from empty stack"):
        s.peek()
    # After pushing then clearing, exceptions still raise
    s.push(1)
    s.clear()
    with pytest.raises(IndexError):
        s.pop()
    with pytest.raises(IndexError):
        s.peek()

def test_queue_operations_and_edge_cases():
    q = Queue()
    # Initially empty
    assert q.is_empty()
    assert len(q) == 0
    assert q.size() == 0
    assert not ("x" in q)

    # Enqueue various types
    items = ["first", None, "", 99]
    for item in items:
        q.enqueue(item)
        assert q.front() == items[0]  # front should always be the first enqueued
        assert item in q

    # Size checks
    assert q.size() == len(items)
    assert len(q) == len(items)

    # Dequeue items and verify order (FIFO)
    for expected in items:
        front = q.front()
        assert front == expected
        dequeued = q.dequeue()
        assert dequeued is expected
    # After dequeuing all, queue should be empty again
    assert q.is_empty()
    assert q.size() == 0
    assert len(q) == 0

    # Clear on already empty queue should keep it empty
    q.clear()
    assert q.is_empty()
    assert q.size() == 0

def test_queue_exceptions():
    q = Queue()
    # Dequeue from empty raises IndexError
    with pytest.raises(IndexError, match="Dequeue from empty queue"):
        q.dequeue()
    # Front from empty raises IndexError
    with pytest.raises(IndexError, match="Front from empty queue"):
        q.front()
    # After enqueue and clear, exceptions still raise
    q.enqueue("temp")
    q.clear()
    with pytest.raises(IndexError):
        q.dequeue()
    with pytest.raises(IndexError):
        q.front()