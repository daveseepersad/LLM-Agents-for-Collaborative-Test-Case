import pytest
from data.input_code.d02_stack import Stack, Queue

def test_stack_basic_operations_and_edge_cases():
    s = Stack()
    # Initially empty and operations on empty should raise
    assert s.is_empty() is True
    with pytest.raises(IndexError):
        s.pop()
    with pytest.raises(IndexError):
        s.peek()

    # Push a mix of items including None to test data type handling and containment
    s.push('a')
    s.push(None)
    s.push(123)

    # Basic state and access
    assert len(s) == 3
    assert s.size() == 3
    assert s.peek() is 123
    assert None in s
    assert 'not_in' not in s

    # Pop order
    assert s.pop() == 123
    assert s.pop() is None
    assert s.peek() == 'a'

    # Clear and verify state
    s.clear()
    assert s.is_empty()
    assert len(s) == 0
    with pytest.raises(IndexError):
        s.pop()

def test_queue_basic_operations_and_edge_cases():
    q = Queue()
    # Operations on empty queue should raise
    assert q.is_empty() is True
    with pytest.raises(IndexError):
        q.dequeue()
    with pytest.raises(IndexError):
        q.front()

    # Enqueue items including None
    q.enqueue(1)
    q.enqueue(None)
    q.enqueue(5)

    # Basic state and access
    assert len(q) == 3
    assert q.size() == 3
    assert q.front() == 1
    assert None in q

    # Dequeue order
    assert q.dequeue() == 1
    assert q.dequeue() is None
    assert q.front() == 5

    # Remaining state
    assert len(q) == 1
    q.dequeue()
    assert q.is_empty()
    with pytest.raises(IndexError):
        q.dequeue()