import pytest
from data.input_code.d02_stack import *

@pytest.fixture
def empty_stack():
    return Stack()

@pytest.fixture
def empty_queue():
    return Queue()


def test_stack_push_and_basic_operations(empty_stack):
    empty_stack.push(1)
    assert empty_stack.peek() == 1
    assert empty_stack.size() == 1
    assert len(empty_stack) == 1
    assert 1 in empty_stack


def test_stack_pop_and_is_empty(empty_stack):
    empty_stack.push(1)
    assert empty_stack.pop() == 1
    assert empty_stack.is_empty()


@pytest.mark.parametrize("method,exc", [
    ("pop", IndexError),
    ("peek", IndexError),
])
def test_stack_empty_exceptions(empty_stack, method, exc):
    with pytest.raises(exc):
        getattr(empty_stack, method)()


@pytest.mark.parametrize("item", [None, ""])
def test_stack_push_falsy_and_contains(empty_stack, item):
    empty_stack.push(item)
    assert item in empty_stack


def test_stack_clear_and_is_empty(empty_stack):
    empty_stack.push(1)
    empty_stack.push(2)
    empty_stack.clear()
    assert empty_stack.is_empty()


def test_queue_enqueue_and_basic_operations(empty_queue):
    empty_queue.enqueue("a")
    assert empty_queue.front() == "a"
    assert empty_queue.size() == 1
    assert len(empty_queue) == 1
    assert "a" in empty_queue


def test_queue_dequeue_and_is_empty(empty_queue):
    empty_queue.enqueue("a")
    assert empty_queue.dequeue() == "a"
    assert empty_queue.is_empty()


@pytest.mark.parametrize("method,exc", [
    ("dequeue", IndexError),
    ("front", IndexError),
])
def test_queue_empty_exceptions(empty_queue, method, exc):
    with pytest.raises(exc):
        getattr(empty_queue, method)()


@pytest.mark.parametrize("item", [None, 0])
def test_queue_enqueue_falsy_and_contains(empty_queue, item):
    empty_queue.enqueue(item)
    assert item in empty_queue


def test_queue_clear_and_is_empty(empty_queue):
    empty_queue.enqueue("x")
    empty_queue.enqueue("y")
    empty_queue.clear()
    assert empty_queue.is_empty()