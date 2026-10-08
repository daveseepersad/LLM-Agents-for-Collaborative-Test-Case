import pytest
from data.input_code.d02_stack import *

@pytest.fixture
def stack():
    return Stack()

@pytest.fixture
def queue():
    return Queue()


def test_stack_init(stack):
    assert len(stack) == 0
    assert stack._items == []


def test_stack_push_and_pop(stack):
    stack.push(5)
    assert stack.pop() == 5
    assert stack.is_empty()


def test_stack_pop_error(stack):
    with pytest.raises(IndexError):
        stack.pop()


def test_stack_peek_ok(stack):
    stack.push(5)
    assert stack.peek() == 5
    # ensure item still there
    assert not stack.is_empty()


def test_stack_peek_error(stack):
    with pytest.raises(IndexError):
        stack.peek()


@pytest.mark.parametrize(
    "prepush,expected",
    [(False, True), (True, False)]
)
def test_stack_is_empty(stack, prepush, expected):
    if prepush:
        stack.push(5)
    assert stack.is_empty() is expected


def test_stack_size(stack):
    stack.push(5)
    assert stack.size() == 1


def test_stack_clear(stack):
    stack.push(5)
    stack.clear()
    assert stack.is_empty()
    assert len(stack) == 0


def test_stack_len(stack):
    stack.push(5)
    assert len(stack) == 1


@pytest.mark.parametrize(
    "item,expected",
    [(5, True), (10, False)]
)
def test_stack_contains(stack, item, expected):
    stack.push(5)
    assert (item in stack) is expected


def test_queue_init(queue):
    assert len(queue) == 0
    assert queue._items == []


def test_queue_enqueue_and_dequeue(queue):
    queue.enqueue(5)
    assert queue.dequeue() == 5
    assert queue.is_empty()


def test_queue_dequeue_error(queue):
    with pytest.raises(IndexError):
        queue.dequeue()


def test_queue_front_ok(queue):
    queue.enqueue(5)
    assert queue.front() == 5
    # front does not remove the item
    assert not queue.is_empty()


def test_queue_front_error(queue):
    with pytest.raises(IndexError):
        queue.front()


@pytest.mark.parametrize(
    "preenqueue,expected",
    [(False, True), (True, False)]
)
def test_queue_is_empty(queue, preenqueue, expected):
    if preenqueue:
        queue.enqueue(5)
    assert queue.is_empty() is expected


def test_queue_size(queue):
    queue.enqueue(5)
    assert queue.size() == 1


def test_queue_clear(queue):
    queue.enqueue(5)
    queue.clear()
    assert queue.is_empty()
    assert len(queue) == 0


def test_queue_len(queue):
    queue.enqueue(5)
    assert len(queue) == 1


@pytest.mark.parametrize(
    "item,expected",
    [(5, True), (10, False)]
)
def test_queue_contains(queue, item, expected):
    queue.enqueue(5)
    assert (item in queue) is expected