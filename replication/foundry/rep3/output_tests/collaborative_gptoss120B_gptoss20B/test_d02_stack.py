import pytest
from data.input_code.d02_stack import Stack, Queue


def _make_stack(initial):
    s = Stack()
    for item in initial:
        s.push(item)
    return s


def _make_queue(initial):
    q = Queue()
    for item in initial:
        q.enqueue(item)
    return q


@pytest.mark.parametrize(
    "initial,expected",
    [
        ([], True),          # S3_STACK_IS_EMPTY_INITIAL
        ([1], False),       # non‑empty case for completeness
    ],
)
def test_stack_is_empty(initial, expected):
    stack = _make_stack(initial)
    assert stack.is_empty() is expected


@pytest.mark.parametrize(
    "initial,expected",
    [
        ([], True),          # Q3_QUEUE_IS_EMPTY_INITIAL
        ([1], False),       # non‑empty case for completeness
    ],
)
def test_queue_is_empty(initial, expected):
    queue = _make_queue(initial)
    assert queue.is_empty() is expected


@pytest.mark.parametrize(
    "initial,expected",
    [
        ([], 0),   # S4_STACK_LEN_INITIAL_ZERO
        ([1], 1),  # S7_STACK_LEN_ONE
        ([1, 2, 3], 3),  # S8_STACK_LEN_THREE
    ],
)
def test_stack_len(initial, expected):
    stack = _make_stack(initial)
    assert len(stack) == expected


@pytest.mark.parametrize(
    "initial,expected",
    [
        ([], 0),   # Q4_QUEUE_LEN_INITIAL_ZERO
        ([1, 2, 3], 3),  # Q7_QUEUE_LEN_THREE
    ],
)
def test_queue_len(initial, expected):
    queue = _make_queue(initial)
    assert len(queue) == expected


@pytest.mark.parametrize(
    "initial,item,expected",
    [
        ([], None, False),          # S5_STACK_CONTAINS_NONE_NOT_IN_EMPTY
        ([None], None, True),       # S9_STACK_CONTAINS_NONE_IN_STACK
        ([1, 2, 3], 2, True),       # extra positive case
    ],
)
def test_stack_contains(initial, item, expected):
    stack = _make_stack(initial)
    assert (item in stack) is expected


@pytest.mark.parametrize(
    "initial,item,expected",
    [
        ([], None, False),          # Q5_QUEUE_CONTAINS_NONE_NOT_IN_EMPTY
        ([None], None, True),       # extra positive case for queue
        ([1, 2, 3], 2, True),       # extra positive case
    ],
)
def test_queue_contains(initial, item, expected):
    queue = _make_queue(initial)
    assert (item in queue) is expected


def test_stack_clear_on_empty():
    stack = _make_stack([])
    result = stack.clear()
    assert result is None
    assert stack.is_empty()


def test_queue_clear_on_empty():
    queue = _make_queue([])
    result = queue.clear()
    assert result is None
    assert queue.is_empty()


def test_stack_pop_empty_raises():
    stack = _make_stack([])
    with pytest.raises(IndexError):
        stack.pop()


def test_stack_peek_empty_raises():
    stack = _make_stack([])
    with pytest.raises(IndexError):
        stack.peek()


def test_queue_dequeue_empty_raises():
    queue = _make_queue([])
    with pytest.raises(IndexError):
        queue.dequeue()


def test_queue_front_empty_raises():
    queue = _make_queue([])
    with pytest.raises(IndexError):
        queue.front()

import pytest
from data.input_code.d02_stack import *

def test_stack_pop_on_nonempty():
    stack = _make_stack([1, 2, 3])
    result = stack.pop()
    assert result == 3
    assert len(stack) == 2

def test_stack_peek_on_nonempty():
    stack = _make_stack([1, 2, 3])
    result = stack.peek()
    assert result == 3
    assert len(stack) == 3

def test_stack_clear_on_nonempty():
    stack = _make_stack([1, 2, 3])
    result = stack.clear()
    assert result is None
    assert stack.is_empty()

def test_stack_contains_false_missing():
    stack = _make_stack([1, 2, 3])
    assert (4 in stack) is False

def test_queue_dequeue_on_nonempty():
    queue = _make_queue([1, 2, 3])
    result = queue.dequeue()
    assert result == 1
    assert len(queue) == 2

def test_queue_front_on_nonempty():
    queue = _make_queue([1, 2, 3])
    result = queue.front()
    assert result == 1
    assert len(queue) == 3

def test_queue_enqueue_on_nonempty():
    queue = _make_queue([1, 2])
    result = queue.enqueue(3)
    assert result is None
    assert len(queue) == 3
    assert queue._items[-1] == 3

import pytest
from data.input_code.d02_stack import *

@pytest.mark.parametrize(
    "initial,expected",
    [
        ([1, 2, 3], 3),
    ],
)
def test_stack_size_matches_len(initial, expected):
    stack = _make_stack(initial)
    assert stack.size() == expected
    assert len(stack) == expected

@pytest.mark.parametrize(
    "initial,expected",
    [
        ([1, 2, 3], 3),
    ],
)
def test_queue_size_matches_len(initial, expected):
    queue = _make_queue(initial)
    assert queue.size() == expected
    assert len(queue) == expected

def test_queue_clear_on_nonempty():
    queue = _make_queue([1, 2, 3])
    result = queue.clear()
    assert result is None
    assert queue.is_empty()
    assert len(queue) == 0

@pytest.mark.parametrize(
    "initial,item,expected",
    [
        ([1, 2, 3], 4, False),
    ],
)
def test_queue_contains_false_missing_nonempty(initial, item, expected):
    queue = _make_queue(initial)
    assert (item in queue) is expected