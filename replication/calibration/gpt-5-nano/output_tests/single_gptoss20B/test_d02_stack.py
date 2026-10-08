import pytest

from data.input_code.d02_stack import Stack, Queue

def test_stack_operations_and_contains_and_len_and_clear():
    s = Stack()
    items = [1, None, "", [], -100, 2**60, -2**60, 2**1000, -2**1000]
    for it in items:
        s.push(it)
    assert len(s) == len(items)
    assert s.size() == len(items)
    for it in items:
        assert it in s
    assert 999 not in s
    assert s.peek() == items[-1]
    popped = [s.pop() for _ in range(len(items))]
    assert popped == list(reversed(items))
    assert s.is_empty()
    s.clear()
    assert s.is_empty()
    assert len(s) == 0

def test_stack_exceptions():
    s = Stack()
    with pytest.raises(IndexError, match="Pop from empty stack"):
        s.pop()
    with pytest.raises(IndexError, match="Peek from empty stack"):
        s.peek()

def test_queue_operations_and_contains_and_len_and_clear_and_front():
    q = Queue()
    items = [1, None, "", [], -100, 2**60, -2**60, 2**1000, -2**1000]
    for it in items:
        q.enqueue(it)
    assert len(q) == len(items)
    assert q.front() == items[0]
    assert 1 in q
    assert 2**1000 in q
    dequeued = [q.dequeue() for _ in range(len(items))]
    assert dequeued == items
    assert q.is_empty()
    q.clear()
    assert len(q) == 0
    assert 999 not in q

def test_queue_exceptions():
    q = Queue()
    with pytest.raises(IndexError, match="Dequeue from empty queue"):
        q.dequeue()
    with pytest.raises(IndexError, match="Front from empty queue"):
        q.front()