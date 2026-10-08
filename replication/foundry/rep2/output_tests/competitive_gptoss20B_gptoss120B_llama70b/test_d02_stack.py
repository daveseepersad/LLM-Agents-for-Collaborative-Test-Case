import pytest
from data.input_code.d02_stack import *

# ---------- Stack Tests ----------

def test_stack_pop_empty():
    s = Stack()
    with pytest.raises(IndexError):
        s.pop()

def test_stack_peek_empty():
    s = Stack()
    with pytest.raises(IndexError):
        s.peek()

def test_stack_is_empty_true():
    s = Stack()
    assert s.is_empty() is True

def test_stack_size_on_new():
    s = Stack()
    assert s.size() == 0

def test_stack_len_on_new():
    s = Stack()
    assert len(s) == 0

def test_stack_contains_on_empty_false():
    s = Stack()
    assert (1 in s) is False

def test_stack_clear_no_exception():
    s = Stack()
    # should not raise any exception
    s.clear()
    assert s.is_empty() is True

@pytest.mark.parametrize('item', [
    9223372036854775807,          # MAX
    -9223372036854775808,         # MIN
    -9223372036854775809,         # MIN-1
    9223372036854775808,          # MAX+1
    None,                         # NONE
])
def test_stack_push_various_items(item):
    s = Stack()
    s.push(item)                     # no exception expected
    assert s.size() == 1
    assert s.peek() == item
    assert item in s

# ---------- Queue Tests ----------

def test_queue_dequeue_empty():
    q = Queue()
    with pytest.raises(IndexError):
        q.dequeue()

def test_queue_front_empty():
    q = Queue()
    with pytest.raises(IndexError):
        q.front()

def test_queue_is_empty_true():
    q = Queue()
    assert q.is_empty() is True

def test_queue_size_on_new():
    q = Queue()
    assert q.size() == 0

def test_queue_len_on_new():
    q = Queue()
    assert len(q) == 0

def test_queue_contains_on_empty_false():
    q = Queue()
    assert ("a" in q) is False

def test_queue_clear_no_exception():
    q = Queue()
    # should not raise any exception
    q.clear()
    assert q.is_empty() is True

@pytest.mark.parametrize('item', [
    9223372036854775807,   # MAX
    None,                  # NONE
])
def test_queue_enqueue_various_items(item):
    q = Queue()
    q.enqueue(item)                # no exception expected
    assert q.size() == 1
    assert q.front() == item
    assert item in q

def test_stack_pop_non_empty():
    s = Stack()
    for i in [1, 2]:
        s.push(i)
    result = s.pop()
    assert result == 2
    assert s.size() == 1
    assert s.peek() == 1


def test_stack_peek_non_empty():
    s = Stack()
    for i in [1, 2]:
        s.push(i)
    result = s.peek()
    assert result == 2
    # ensure peek does not remove the item
    assert s.size() == 2
    assert s.pop() == 2


def test_stack_clear_state():
    s = Stack()
    for i in [1, 2]:
        s.push(i)
    s.clear()
    assert s.is_empty() is True
    assert s.size() == 0


def test_queue_dequeue_order():
    q = Queue()
    for i in [1, 2]:
        q.enqueue(i)
    result = q.dequeue()
    assert result == 1
    assert q.size() == 1
    assert q.front() == 2


def test_queue_contains_non_empty_true():
    q = Queue()
    for i in [5]:
        q.enqueue(i)
    assert (5 in q) is True