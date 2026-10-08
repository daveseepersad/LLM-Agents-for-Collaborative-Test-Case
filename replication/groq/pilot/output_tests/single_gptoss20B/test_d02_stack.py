import pytest
from data.input_code.d02_stack import Stack, Queue


def test_stack_basic_operations():
    s = Stack()
    # Initially empty
    assert s.is_empty()
    assert s.size() == 0
    assert len(s) == 0
    assert "a" not in s

    # Push elements
    s.push(1)
    s.push(2)
    s.push(3)
    assert not s.is_empty()
    assert s.size() == 3
    assert len(s) == 3
    assert s.peek() == 3
    assert s._items == [1, 2, 3]
    assert 2 in s
    assert 4 not in s

    # Pop elements
    assert s.pop() == 3
    assert s.size() == 2
    assert len(s) == 2
    assert s.pop() == 2
    assert s.pop() == 1
    assert s.is_empty()
    assert len(s) == 0
    assert s.size() == 0
    assert 1 not in s


def test_stack_exceptions():
    s = Stack()
    with pytest.raises(IndexError, match="Pop from empty stack"):
        s.pop()
    with pytest.raises(IndexError, match="Peek from empty stack"):
        s.peek()


def test_stack_clear_and_contains():
    s = Stack()
    s.push("x")
    s.push("y")
    assert not s.is_empty()
    s.clear()
    assert s.is_empty()
    assert s.size() == 0
    assert len(s) == 0
    assert "x" not in s
    assert "y" not in s


def test_stack_push_none_and_empty_string():
    s = Stack()
    s.push(None)
    s.push("")
    s.push(0)
    s.push(-1)
    assert s.peek() == -1
    assert s.pop() == -1
    assert s.pop() == 0
    assert s.pop() == ""
    assert s.pop() is None
    assert s.is_empty()


def test_queue_basic_operations():
    q = Queue()
    # Initially empty
    assert q.is_empty()
    assert q.size() == 0
    assert len(q) == 0
    assert "a" not in q

    # Enqueue elements
    q.enqueue(1)
    q.enqueue(2)
    q.enqueue(3)
    assert not q.is_empty()
    assert q.size() == 3
    assert len(q) == 3
    assert q.front() == 1
    assert q._items == [1, 2, 3]
    assert 2 in q
    assert 4 not in q

    # Dequeue elements
    assert q.dequeue() == 1
    assert q.size() == 2
    assert len(q) == 2
    assert q.dequeue() == 2
    assert q.dequeue() == 3
    assert q.is_empty()
    assert len(q) == 0
    assert q.size() == 0
    assert 1 not in q


def test_queue_exceptions():
    q = Queue()
    with pytest.raises(IndexError, match="Dequeue from empty queue"):
        q.dequeue()
    with pytest.raises(IndexError, match="Front from empty queue"):
        q.front()


def test_queue_clear_and_contains():
    q = Queue()
    q.enqueue("x")
    q.enqueue("y")
    assert not q.is_empty()
    q.clear()
    assert q.is_empty()
    assert q.size() == 0
    assert len(q) == 0
    assert "x" not in q
    assert "y" not in q


def test_queue_push_none_and_empty_string():
    q = Queue()
    q.enqueue(None)
    q.enqueue("")
    q.enqueue(0)
    q.enqueue(-1)
    assert q.front() == None
    assert q.dequeue() is None
    assert q.dequeue() == ""
    assert q.dequeue() == 0
    assert q.dequeue() == -1
    assert q.is_empty()
    assert len(q) == 0
    assert q.size() == 0
    assert None not in q
    assert "" not in q
    assert 0 not in q
    assert -1 not in q