import pytest
from data.input_code.d02_stack import *

# ---------- Stack Tests ----------
@pytest.fixture
def stack():
    return Stack()

def test_stack_push_and_size(stack):
    stack.push(10)
    assert stack.size() == 1

def test_stack_pop(stack):
    stack.push(10)
    assert stack.pop() == 10

def test_stack_pop_empty(stack):
    with pytest.raises(IndexError):
        stack.pop()

def test_stack_peek(stack):
    stack.push(20)
    assert stack.peek() == 20

def test_stack_peek_empty(stack):
    with pytest.raises(IndexError):
        stack.peek()

@pytest.mark.parametrize(
    "item,expected",
    [
        (30, True),
        (99, False),
    ],
)
def test_stack_contains(stack, item, expected):
    # Ensure the stack has 30 before testing contains
    stack.push(30)
    assert (item in stack) is expected

def test_stack_clear_and_len(stack):
    stack.push(1)
    stack.clear()
    assert len(stack) == 0

# ---------- Queue Tests ----------
@pytest.fixture
def queue():
    return Queue()

def test_queue_enqueue_and_size(queue):
    queue.enqueue("a")
    assert queue.size() == 1

def test_queue_dequeue(queue):
    queue.enqueue("a")
    assert queue.dequeue() == "a"

def test_queue_dequeue_empty(queue):
    with pytest.raises(IndexError):
        queue.dequeue()

def test_queue_front(queue):
    queue.enqueue("b")
    assert queue.front() == "b"

def test_queue_front_empty(queue):
    with pytest.raises(IndexError):
        queue.front()

@pytest.mark.parametrize(
    "item,expected",
    [
        ("c", True),
        ("z", False),
    ],
)
def test_queue_contains(queue, item, expected):
    # Ensure the queue has "c" before testing contains
    queue.enqueue("c")
    assert (item in queue) is expected

def test_queue_clear_and_len(queue):
    queue.enqueue("x")
    queue.clear()
    assert len(queue) == 0