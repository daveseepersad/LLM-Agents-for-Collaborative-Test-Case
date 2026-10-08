import pytest
from data.input_code.d02_stack import Stack, Queue

def test_stack_basic_and_edge_operations():
    s = Stack()
    # initially empty
    assert s.is_empty()
    assert s.size() == 0
    assert len(s) == 0
    # push various types
    s.push(1)
    s.push(None)
    s.push("")
    s.push(0)
    # after pushes
    assert not s.is_empty()
    assert s.size() == 4
    assert len(s) == 4
    # contains checks
    assert 1 in s
    assert None in s
    assert "" in s
    assert 0 in s
    # peek returns last pushed (LIFO)
    assert s.peek() == 0
    # pop returns items in reverse order
    assert s.pop() == 0
    assert s.pop() == ""
    assert s.pop() == None
    assert s.pop() == 1
    # now empty again
    assert s.is_empty()
    assert s.size() == 0
    assert len(s) == 0

def test_stack_exceptions_and_clear():
    s = Stack()
    # pop and peek on empty should raise
    with pytest.raises(IndexError) as e_pop:
        s.pop()
    assert "Pop from empty stack" in str(e_pop.value)
    with pytest.raises(IndexError) as e_peek:
        s.peek()
    assert "Peek from empty stack" in str(e_peek.value)
    # push then clear
    s.push('a')
    s.push('b')
    assert s.size() == 2
    s.clear()
    # after clear, behaves as empty
    assert s.is_empty()
    assert s.size() == 0
    assert len(s) == 0
    assert 'a' not in s

def test_queue_basic_and_edge_operations():
    q = Queue()
    # initially empty
    assert q.is_empty()
    assert q.size() == 0
    assert len(q) == 0
    # enqueue various types
    q.enqueue(1)
    q.enqueue(None)
    q.enqueue("")
    q.enqueue(0)
    # after enqueues
    assert not q.is_empty()
    assert q.size() == 4
    assert len(q) == 4
    # contains checks
    assert 1 in q
    assert None in q
    assert "" in q
    assert 0 in q
    # front returns first enqueued (FIFO)
    assert q.front() == 1
    # dequeue returns items in order
    assert q.dequeue() == 1
    assert q.dequeue() == None
    assert q.dequeue() == ""
    assert q.dequeue() == 0
    # now empty again
    assert q.is_empty()
    assert q.size() == 0
    assert len(q) == 0

def test_queue_exceptions_and_clear():
    q = Queue()
    # dequeue and front on empty should raise
    with pytest.raises(IndexError) as e_deq:
        q.dequeue()
    assert "Dequeue from empty queue" in str(e_deq.value)
    with pytest.raises(IndexError) as e_front:
        q.front()
    assert "Front from empty queue" in str(e_front.value)
    # enqueue then clear
    q.enqueue('x')
    q.enqueue('y')
    assert q.size() == 2
    q.clear()
    # after clear, behaves as empty
    assert q.is_empty()
    assert q.size() == 0
    assert len(q) == 0
    assert 'x' not in q