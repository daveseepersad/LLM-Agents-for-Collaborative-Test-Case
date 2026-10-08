import pytest
from data.input_code.d02_stack import *

# ---------- Stack Tests ----------

def test_stack_init():
    s = Stack()
    assert s.size() == 0
    assert s.is_empty() is True

def test_stack_push():
    s = Stack()
    s.push(5)
    assert s.size() == 1
    assert s.is_empty() is False

def test_stack_pop_success():
    s = Stack()
    s.push(5)
    assert s.pop() == 5
    assert s.is_empty() is True

def test_stack_pop_error():
    s = Stack()
    with pytest.raises(IndexError):
        s.pop()

def test_stack_peek_success():
    s = Stack()
    s.push(5)
    assert s.peek() == 5
    # peek should not remove the item
    assert s.size() == 1

def test_stack_peek_error():
    s = Stack()
    with pytest.raises(IndexError):
        s.peek()

@pytest.mark.parametrize(
    "operations,expected_is_empty,expected_size",
    [
        ([], True, 0),                     # empty stack
        ([5], False, 1),                   # one element
        ([5, 10], False, 2),               # two elements
    ],
)
def test_stack_is_empty_and_size(operations, expected_is_empty, expected_size):
    s = Stack()
    for item in operations:
        s.push(item)
    assert s.is_empty() is expected_is_empty
    assert s.size() == expected_size

def test_stack_clear():
    s = Stack()
    s.push(1)
    s.push(2)
    s.clear()
    assert s.size() == 0
    assert s.is_empty() is True

@pytest.mark.parametrize(
    "operations,expected_len",
    [
        ([], 0),
        ([1], 1),
        ([1, 2, 3], 3),
    ],
)
def test_stack_len(operations, expected_len):
    s = Stack()
    for item in operations:
        s.push(item)
    assert len(s) == expected_len

@pytest.mark.parametrize(
    "push_items,query_item,expected_contains",
    [
        ([1, 2, 3], 2, True),
        ([1, 2, 3], 5, False),
    ],
)
def test_stack_contains(push_items, query_item, expected_contains):
    s = Stack()
    for item in push_items:
        s.push(item)
    assert (query_item in s) is expected_contains

# ---------- Queue Tests ----------

def test_queue_init():
    q = Queue()
    assert q.size() == 0
    assert q.is_empty() is True

def test_queue_enqueue():
    q = Queue()
    q.enqueue(5)
    assert q.size() == 1
    assert q.is_empty() is False

def test_queue_dequeue_success():
    q = Queue()
    q.enqueue(5)
    assert q.dequeue() == 5
    assert q.is_empty() is True

def test_queue_dequeue_error():
    q = Queue()
    with pytest.raises(IndexError):
        q.dequeue()

def test_queue_front_success():
    q = Queue()
    q.enqueue(5)
    assert q.front() == 5
    # front should not remove the item
    assert q.size() == 1

def test_queue_front_error():
    q = Queue()
    with pytest.raises(IndexError):
        q.front()

@pytest.mark.parametrize(
    "operations,expected_is_empty,expected_size",
    [
        ([], True, 0),
        ([5], False, 1),
        ([5, 10], False, 2),
    ],
)
def test_queue_is_empty_and_size(operations, expected_is_empty, expected_size):
    q = Queue()
    for item in operations:
        q.enqueue(item)
    assert q.is_empty() is expected_is_empty
    assert q.size() == expected_size

def test_queue_clear():
    q = Queue()
    q.enqueue(1)
    q.enqueue(2)
    q.clear()
    assert q.size() == 0
    assert q.is_empty() is True

@pytest.mark.parametrize(
    "operations,expected_len",
    [
        ([], 0),
        ([1], 1),
        ([1, 2, 3], 3),
    ],
)
def test_queue_len(operations, expected_len):
    q = Queue()
    for item in operations:
        q.enqueue(item)
    assert len(q) == expected_len

@pytest.mark.parametrize(
    "enqueue_items,query_item,expected_contains",
    [
        ([1, 2, 3], 2, True),
        ([1, 2, 3], 5, False),
    ],
)
def test_queue_contains(enqueue_items, query_item, expected_contains):
    q = Queue()
    for item in enqueue_items:
        q.enqueue(item)
    assert (query_item in q) is expected_contains