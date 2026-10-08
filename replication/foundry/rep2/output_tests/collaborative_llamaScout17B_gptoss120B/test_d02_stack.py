import pytest
from data.input_code.d02_stack import *

@pytest.fixture
def empty_stack():
    return Stack()

@pytest.fixture
def stack_with_one():
    s = Stack()
    s.push(5)
    return s

@pytest.fixture
def empty_queue():
    return Queue()

@pytest.fixture
def queue_with_one():
    q = Queue()
    q.enqueue(5)
    return q

def test_stack_init(empty_stack):
    assert empty_stack.size() == 0
    assert empty_stack.is_empty() is True

def test_stack_push(stack_with_one):
    assert stack_with_one.size() == 1
    assert stack_with_one.is_empty() is False

@pytest.mark.parametrize("method,expected", [
    ("pop", 5),
    ("peek", 5),
])
def test_stack_success_operations(stack_with_one, method, expected):
    if method == "pop":
        assert stack_with_one.pop() == expected
    else:  # peek
        assert stack_with_one.peek() == expected

def test_stack_pop_error(empty_stack):
    with pytest.raises(IndexError):
        empty_stack.pop()

def test_stack_peek_error(empty_stack):
    with pytest.raises(IndexError):
        empty_stack.peek()

def test_stack_is_empty_true(empty_stack):
    assert empty_stack.is_empty() is True

def test_stack_is_empty_false(stack_with_one):
    assert stack_with_one.is_empty() is False

def test_stack_size(stack_with_one):
    assert stack_with_one.size() == 1

def test_stack_len(stack_with_one):
    assert len(stack_with_one) == 1

def test_stack_contains_true(stack_with_one):
    assert 5 in stack_with_one

def test_stack_contains_false(stack_with_one):
    assert 10 not in stack_with_one

def test_stack_clear(stack_with_one):
    stack_with_one.clear()
    assert stack_with_one.size() == 0
    assert stack_with_one.is_empty() is True

def test_queue_init(empty_queue):
    assert empty_queue.size() == 0
    assert empty_queue.is_empty() is True

def test_queue_enqueue(queue_with_one):
    assert queue_with_one.size() == 1
    assert queue_with_one.is_empty() is False

@pytest.mark.parametrize("method,expected", [
    ("dequeue", 5),
    ("front", 5),
])
def test_queue_success_operations(queue_with_one, method, expected):
    if method == "dequeue":
        assert queue_with_one.dequeue() == expected
    else:  # front
        assert queue_with_one.front() == expected

def test_queue_dequeue_error(empty_queue):
    with pytest.raises(IndexError):
        empty_queue.dequeue()

def test_queue_front_error(empty_queue):
    with pytest.raises(IndexError):
        empty_queue.front()

def test_queue_is_empty_true(empty_queue):
    assert empty_queue.is_empty() is True

def test_queue_is_empty_false(queue_with_one):
    assert queue_with_one.is_empty() is False

def test_queue_size(queue_with_one):
    assert queue_with_one.size() == 1

def test_queue_len(queue_with_one):
    assert len(queue_with_one) == 1

def test_queue_contains_true(queue_with_one):
    assert 5 in queue_with_one

def test_queue_contains_false(queue_with_one):
    assert 10 not in queue_with_one

def test_queue_clear(queue_with_one):
    queue_with_one.clear()
    assert queue_with_one.size() == 0
    assert queue_with_one.is_empty() is True