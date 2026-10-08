import pytest
from data.input_code.d02_stack import Stack, Queue


@pytest.mark.parametrize("items", [
    [1, 2, 3],
    [None, "", 0],
])
def test_stack_operations(items):
    s = Stack()
    assert s.is_empty()
    assert len(s) == 0
    for i, item in enumerate(items):
        s.push(item)
        assert s.peek() == item
        assert item in s
        assert s.size() == i + 1
        assert len(s) == i + 1
        assert not s.is_empty()
    for i, expected in enumerate(reversed(items)):
        assert s.peek() == expected
        popped = s.pop()
        assert popped == expected
        assert s.size() == len(items) - i - 1
        assert len(s) == len(items) - i - 1
    assert s.is_empty()
    assert len(s) == 0
    s.clear()
    assert s.is_empty()


def test_stack_empty_exceptions():
    s = Stack()
    with pytest.raises(IndexError, match="Pop from empty stack"):
        s.pop()
    with pytest.raises(IndexError, match="Peek from empty stack"):
        s.peek()


@pytest.mark.parametrize("items", [
    [1, 2, 3],
    [None, "", 0],
])
def test_queue_operations(items):
    q = Queue()
    assert q.is_empty()
    assert len(q) == 0
    for i, item in enumerate(items):
        q.enqueue(item)
        assert q.front() == items[0]
        assert item in q
        assert q.size() == i + 1
        assert len(q) == i + 1
        assert not q.is_empty()
    for i, expected in enumerate(items):
        assert q.front() == expected
        dequeued = q.dequeue()
        assert dequeued == expected
        assert q.size() == len(items) - i - 1
        assert len(q) == len(items) - i - 1
    assert q.is_empty()
    assert len(q) == 0
    q.clear()
    assert q.is_empty()


def test_queue_empty_exceptions():
    q = Queue()
    with pytest.raises(IndexError, match="Dequeue from empty queue"):
        q.dequeue()
    with pytest.raises(IndexError, match="Front from empty queue"):
        q.front()