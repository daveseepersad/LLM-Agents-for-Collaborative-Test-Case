import pytest
from data.input_code.d02_stack import *

# ---------- Fixtures ----------
@pytest.fixture
def empty_stack():
    return Stack()

@pytest.fixture
def stack_one_item():
    s = Stack()
    s.push(42)
    return s

@pytest.fixture
def stack_three_items():
    s = Stack()
    s.push(1)
    s.push(None)
    s.push("")
    return s

@pytest.fixture
def empty_queue():
    return Queue()

@pytest.fixture
def queue_one_item():
    q = Queue()
    q.enqueue("x")
    return q

@pytest.fixture
def queue_three_items():
    q = Queue()
    q.enqueue(1)
    q.enqueue(None)
    q.enqueue("")
    return q

# ---------- Stack Tests ----------
def test_stack_is_empty_initial(empty_stack):
    assert empty_stack.is_empty() is True

def test_stack_push_returns_none(stack_one_item):
    # push already performed in fixture; ensure method returns None
    result = stack_one_item.push(99)  # extra push to test return value
    assert result is None

def test_stack_peek(stack_one_item):
    assert stack_one_item.peek() == 42

def test_stack_pop(stack_one_item):
    assert stack_one_item.pop() == 42

def test_stack_pop_raises_on_empty(empty_stack):
    with pytest.raises(IndexError):
        empty_stack.pop()

def test_stack_peek_raises_on_empty(empty_stack):
    with pytest.raises(IndexError):
        empty_stack.peek()

def test_stack_size(stack_three_items):
    assert stack_three_items.size() == 3

def test_stack_len(stack_three_items):
    assert len(stack_three_items) == 3

def test_stack_contains_none(stack_three_items):
    assert None in stack_three_items

def test_stack_not_contains_missing(stack_three_items):
    assert "missing" not in stack_three_items

def test_stack_clear(stack_three_items):
    stack_three_items.clear()
    assert stack_three_items.is_empty() is True

def test_stack_is_empty_after_clear(empty_stack):
    empty_stack.clear()  # should remain empty without error
    assert empty_stack.is_empty() is True

# ---------- Queue Tests ----------
def test_queue_is_empty_initial(empty_queue):
    assert empty_queue.is_empty() is True

def test_queue_enqueue_returns_none(queue_one_item):
    result = queue_one_item.enqueue("y")
    assert result is None

def test_queue_front(queue_one_item):
    assert queue_one_item.front() == "x"

def test_queue_dequeue(queue_one_item):
    assert queue_one_item.dequeue() == "x"

def test_queue_dequeue_raises_on_empty(empty_queue):
    with pytest.raises(IndexError):
        empty_queue.dequeue()

def test_queue_front_raises_on_empty(empty_queue):
    with pytest.raises(IndexError):
        empty_queue.front()

def test_queue_size(queue_three_items):
    assert queue_three_items.size() == 3

def test_queue_len(queue_three_items):
    assert len(queue_three_items) == 3

def test_queue_contains_none(queue_three_items):
    assert None in queue_three_items

def test_queue_not_contains_missing(queue_three_items):
    assert "missing" not in queue_three_items

def test_queue_clear(queue_three_items):
    queue_three_items.clear()
    assert queue_three_items.is_empty() is True

def test_queue_is_empty_after_clear(empty_queue):
    empty_queue.clear()
    assert empty_queue.is_empty() is True