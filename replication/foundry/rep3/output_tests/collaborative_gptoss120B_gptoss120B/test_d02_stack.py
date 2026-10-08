import pytest
from data.input_code.d02_stack import Stack, Queue


@pytest.fixture
def stack():
    return Stack()


@pytest.fixture
def queue():
    return Queue()


def test_stack_push_and_pop(stack):
    # S1_PUSH
    stack.push(42)
    # S2_POP_OK
    assert stack.pop() == 42


def test_stack_pop_error(stack):
    # S3_POP_ERR
    with pytest.raises(IndexError):
        stack.pop()


def test_stack_peek_error(stack):
    # S4_PEEK_ERR
    with pytest.raises(IndexError):
        stack.peek()


def test_stack_multiple_operations(stack):
    # S5_PUSH_MULTIPLE
    stack.push("a")
    # S6_PUSH_NONE
    stack.push(None)

    # S7_PEEK_OK
    assert stack.peek() is None

    # S8_IS_EMPTY_FALSE
    assert stack.is_empty() is False

    # S9_SIZE
    assert stack.size() == 2

    # S10_LEN
    assert len(stack) == 2

    # S11_CONTAINS_TRUE / S12_CONTAINS_FALSE
    assert ("a" in stack) is True
    assert (99 in stack) is False

    # S13_CLEAR
    stack.clear()

    # S14_IS_EMPTY_TRUE
    assert stack.is_empty() is True


def test_queue_enqueue_and_dequeue(queue):
    # Q1_ENQUEUE
    queue.enqueue(7)
    # Q2_DEQUEUE_OK
    assert queue.dequeue() == 7


def test_queue_dequeue_error(queue):
    # Q3_DEQUEUE_ERR
    with pytest.raises(IndexError):
        queue.dequeue()


def test_queue_front_error(queue):
    # Q4_FRONT_ERR
    with pytest.raises(IndexError):
        queue.front()


def test_queue_multiple_operations(queue):
    # Q5_ENQUEUE_MULTIPLE
    queue.enqueue("")
    # Q6_ENQUEUE_NONE
    queue.enqueue(None)

    # Q7_FRONT_OK
    assert queue.front() == ""

    # Q8_IS_EMPTY_FALSE
    assert queue.is_empty() is False

    # Q9_SIZE
    assert queue.size() == 2

    # Q10_LEN
    assert len(queue) == 2

    # Q11_CONTAINS_TRUE / Q12_CONTAINS_FALSE
    assert (None in queue) is True
    assert (100 in queue) is False

    # Q13_CLEAR
    queue.clear()

    # Q14_IS_EMPTY_TRUE
    assert queue.is_empty() is True