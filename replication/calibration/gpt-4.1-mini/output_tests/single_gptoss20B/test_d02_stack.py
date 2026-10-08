import pytest
from data.input_code.d02_stack import Stack, Queue

def test_stack_push_pop_peek_size_is_empty_clear_contains_len():
    s = Stack()
    # Initially empty
    assert s.is_empty() is True
    assert s.size() == 0
    assert len(s) == 0
    # Push items
    s.push(1)
    s.push(2)
    s.push(None)
    assert s.is_empty() is False
    assert s.size() == 3
    assert len(s) == 3
    # Contains check
    assert 1 in s
    assert 2 in s
    assert None in s
    assert 3 not in s
    # Peek returns last pushed item
    assert s.peek() is None
    # Pop returns last pushed item and removes it
    assert s.pop() is None
    assert s.size() == 2
    # Peek after pop
    assert s.peek() == 2
    # Pop remaining items
    assert s.pop() == 2
    assert s.pop() == 1
    # Now empty again
    assert s.is_empty() is True
    # Pop from empty raises
    with pytest.raises(IndexError, match="Pop from empty stack"):
        s.pop()
    # Peek from empty raises
    with pytest.raises(IndexError, match="Peek from empty stack"):
        s.peek()
    # Clear on empty stack
    s.clear()
    assert s.is_empty() is True
    # Clear on non-empty stack
    s.push(10)
    s.clear()
    assert s.is_empty() is True

def test_queue_enqueue_dequeue_front_size_is_empty_clear_contains_len():
    q = Queue()
    # Initially empty
    assert q.is_empty() is True
    assert q.size() == 0
    assert len(q) == 0
    # Enqueue items
    q.enqueue(1)
    q.enqueue(2)
    q.enqueue("")
    q.enqueue(None)
    assert q.is_empty() is False
    assert q.size() == 4
    assert len(q) == 4
    # Contains check
    assert 1 in q
    assert 2 in q
    assert "" in q
    assert None in q
    assert 3 not in q
    # Front returns first enqueued item
    assert q.front() == 1
    # Dequeue returns first enqueued item and removes it
    assert q.dequeue() == 1
    assert q.size() == 3
    # Front after dequeue
    assert q.front() == 2
    # Dequeue remaining items
    assert q.dequeue() == 2
    assert q.dequeue() == ""
    assert q.dequeue() is None
    # Now empty again
    assert q.is_empty() is True
    # Dequeue from empty raises
    with pytest.raises(IndexError, match="Dequeue from empty queue"):
        q.dequeue()
    # Front from empty raises
    with pytest.raises(IndexError, match="Front from empty queue"):
        q.front()
    # Clear on empty queue
    q.clear()
    assert q.is_empty() is True
    # Clear on non-empty queue
    q.enqueue(10)
    q.clear()
    assert q.is_empty() is True