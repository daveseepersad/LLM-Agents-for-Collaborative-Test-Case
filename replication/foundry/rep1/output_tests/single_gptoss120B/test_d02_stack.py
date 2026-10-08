import pytest
from data.input_code.d02_stack import Stack, Queue

def test_stack_basic_operations_and_containment():
    s = Stack()
    # Initially empty
    assert s.is_empty()
    assert s.size() == 0
    assert len(s) == 0
    # Push various types
    s.push(1)
    s.push(None)
    s.push("")
    s.push("last")
    # State after pushes
    assert not s.is_empty()
    assert s.size() == 4
    assert len(s) == 4
    # Peek returns last pushed item
    assert s.peek() == "last"
    # Contains checks
    assert 1 in s
    assert None in s
    assert "" in s
    assert "last" in s
    assert "missing" not in s
    # Pop items in LIFO order
    assert s.pop() == "last"
    assert s.pop() == ""
    assert s.pop() is None
    assert s.pop() == 1
    # After popping all, stack is empty again
    assert s.is_empty()
    assert s.size() == 0
    assert len(s) == 0

def test_stack_error_on_empty_and_clear():
    s = Stack()
    # Operations on empty stack raise IndexError
    with pytest.raises(IndexError, match="Pop from empty stack"):
        s.pop()
    with pytest.raises(IndexError, match="Peek from empty stack"):
        s.peek()
    # After pushing and clearing, stack behaves as empty again
    s.push(42)
    s.clear()
    assert s.is_empty()
    assert s.size() == 0
    assert len(s) == 0
    with pytest.raises(IndexError):
        s.pop()

def test_queue_basic_operations_and_containment():
    q = Queue()
    # Initially empty
    assert q.is_empty()
    assert q.size() == 0
    assert len(q) == 0
    # Enqueue various items
    q.enqueue(1)
    q.enqueue(None)
    q.enqueue("")
    q.enqueue("last")
    # State after enqueues
    assert not q.is_empty()
    assert q.size() == 4
    assert len(q) == 4
    # Front returns first enqueued item
    assert q.front() == 1
    # Contains checks
    assert 1 in q
    assert None in q
    assert "" in q
    assert "last" in q
    assert "missing" not in q
    # Dequeue items in FIFO order
    assert q.dequeue() == 1
    assert q.dequeue() is None
    assert q.dequeue() == ""
    assert q.dequeue() == "last"
    # After dequeuing all, queue is empty again
    assert q.is_empty()
    assert q.size() == 0
    assert len(q) == 0

def test_queue_error_on_empty_and_clear():
    q = Queue()
    # Operations on empty queue raise IndexError
    with pytest.raises(IndexError, match="Dequeue from empty queue"):
        q.dequeue()
    with pytest.raises(IndexError, match="Front from empty queue"):
        q.front()
    # After enqueuing and clearing, queue behaves as empty again
    q.enqueue("item")
    q.clear()
    assert q.is_empty()
    assert q.size() == 0
    assert len(q) == 0
    with pytest.raises(IndexError):
        q.dequeue()