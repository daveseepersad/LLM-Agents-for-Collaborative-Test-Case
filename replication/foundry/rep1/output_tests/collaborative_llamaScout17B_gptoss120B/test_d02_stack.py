import pytest
from data.input_code.d02_stack import Stack, Queue


@pytest.fixture
def stack():
    return Stack()


@pytest.fixture
def queue():
    return Queue()


def test_stack_initial_state(stack):
    assert stack.is_empty() is True
    assert stack.size() == 0
    assert len(stack) == 0


def test_stack_push_and_state(stack):
    stack.push(5)
    assert stack.is_empty() is False
    assert stack.size() == 1
    assert len(stack) == 1
    assert stack.peek() == 5
    assert 5 in stack


def test_stack_pop_success(stack):
    stack.push(5)
    popped = stack.pop()
    assert popped == 5
    assert stack.is_empty() is True
    assert stack.size() == 0
    assert len(stack) == 0


def test_stack_pop_error(stack):
    with pytest.raises(IndexError):
        stack.pop()


def test_stack_peek_error(stack):
    with pytest.raises(IndexError):
        stack.peek()


def test_stack_clear(stack):
    stack.push(5)
    stack.clear()
    assert stack.is_empty() is True
    assert stack.size() == 0
    assert len(stack) == 0
    assert 5 not in stack


@pytest.mark.parametrize(
    "item,expected",
    [
        (5, True),
        (10, False),
    ],
)
def test_stack_contains(stack, item, expected):
    stack.push(5)
    assert (item in stack) is expected


def test_queue_initial_state(queue):
    assert queue.is_empty() is True
    assert queue.size() == 0
    assert len(queue) == 0


def test_queue_enqueue_and_state(queue):
    queue.enqueue(5)
    assert queue.is_empty() is False
    assert queue.size() == 1
    assert len(queue) == 1
    assert queue.front() == 5
    assert 5 in queue


def test_queue_dequeue_success(queue):
    queue.enqueue(5)
    dequeued = queue.dequeue()
    assert dequeued == 5
    assert queue.is_empty() is True
    assert queue.size() == 0
    assert len(queue) == 0


def test_queue_dequeue_error(queue):
    with pytest.raises(IndexError):
        queue.dequeue()


def test_queue_front_error(queue):
    with pytest.raises(IndexError):
        queue.front()


def test_queue_clear(queue):
    queue.enqueue(5)
    queue.clear()
    assert queue.is_empty() is True
    assert queue.size() == 0
    assert len(queue) == 0
    assert 5 not in queue


@pytest.mark.parametrize(
    "item,expected",
    [
        (5, True),
        (10, False),
    ],
)
def test_queue_contains(queue, item, expected):
    queue.enqueue(5)
    assert (item in queue) is expected