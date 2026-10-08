import pytest
from data.input_code.d02_stack import *

# ---------- Stack Tests ----------

@pytest.mark.parametrize(
    "initial_items, expected",
    [
        ([1, 2], 2),                                   # SPOP_NonEmpty
        ([-9223372036854775808, 9223372036854775807], 9223372036854775807),  # S_BOUNDARY
    ],
)
def test_stack_pop_success(initial_items, expected):
    s = Stack()
    for item in initial_items:
        s.push(item)
    assert s.pop() == expected


@pytest.mark.parametrize(
    "initial_items, expected",
    [
        ([1, 2], 2),  # SPEEK_NonEmpty
    ],
)
def test_stack_peek_success(initial_items, expected):
    s = Stack()
    for item in initial_items:
        s.push(item)
    assert s.peek() == expected


def test_stack_pop_empty():
    s = Stack()
    with pytest.raises(IndexError):
        s.pop()  # SPOP_Empty


def test_stack_peek_empty():
    s = Stack()
    with pytest.raises(IndexError):
        s.peek()  # SPEEK_Empty


@pytest.mark.parametrize(
    "initial_items, item, expected",
    [
        ([None, 1], None, True),  # S_CONTAINS_None
    ],
)
def test_stack_contains(initial_items, item, expected):
    s = Stack()
    for i in initial_items:
        s.push(i)
    assert (item in s) is expected


@pytest.mark.parametrize(
    "initial_items, expected",
    [
        ([1, 2, 3], 3),  # S_LEN_Init
    ],
)
def test_stack_len(initial_items, expected):
    s = Stack()
    for i in initial_items:
        s.push(i)
    assert len(s) == expected


# ---------- Queue Tests ----------

@pytest.mark.parametrize(
    "initial_items, expected",
    [
        ([1, 2], 1),                                   # QDEQ_NonEmpty
        ([-9223372036854775808, 9223372036854775807], 9223372036854775807),  # Q_BOUNDARY
    ],
)
def test_queue_dequeue_success(initial_items, expected):
    q = Queue()
    # For the boundary case we need the first element to be the large integer,
    # so we reverse the list when initializing.
    items_to_enqueue = (
        list(initial_items)[::-1]
        if initial_items == [-9223372036854775808, 9223372036854775807]
        else initial_items
    )
    for item in items_to_enqueue:
        q.enqueue(item)
    assert q.dequeue() == expected


@pytest.mark.parametrize(
    "initial_items, expected",
    [
        ([1, 2], 1),  # Q_FRONT_NonEmpty
    ],
)
def test_queue_front_success(initial_items, expected):
    q = Queue()
    for item in initial_items:
        q.enqueue(item)
    assert q.front() == expected


def test_queue_dequeue_empty():
    q = Queue()
    with pytest.raises(IndexError):
        q.dequeue()  # QDEQ_Empty


def test_queue_front_empty():
    q = Queue()
    with pytest.raises(IndexError):
        q.front()  # Q_FRONT_Empty


@pytest.mark.parametrize(
    "initial_items, item, expected",
    [
        ([1, None], None, True),  # Q_CONTAINS_None
    ],
)
def test_queue_contains(initial_items, item, expected):
    q = Queue()
    for i in initial_items:
        q.enqueue(i)
    assert (item in q) is expected


@pytest.mark.parametrize(
    "initial_items, expected",
    [
        ([1, 2, 3], 3),  # Q_LEN_Init
    ],
)
def test_queue_len(initial_items, expected):
    q = Queue()
    for i in initial_items:
        q.enqueue(i)
    assert len(q) == expected

import pytest

@pytest.mark.parametrize(
    "initial_items, expected",
    [
        ([1, 2], 2),  # T_MISSING_STACK_SIZE
    ],
)
def test_stack_size(initial_items, expected):
    s = Stack()
    for item in initial_items:
        s.push(item)
    assert s.size() == expected


@pytest.mark.parametrize(
    "initial_items, expected",
    [
        ([42], False),  # T_MISSING_STACK_IS_EMPTY_NONEMPTY
    ],
)
def test_stack_is_empty_nonempty(initial_items, expected):
    s = Stack()
    for item in initial_items:
        s.push(item)
    assert s.is_empty() is expected


def test_stack_clear():
    s = Stack()
    for item in [1, 2, 3]:
        s.push(item)
    s.clear()
    assert s.is_empty()
    assert s.size() == 0
    assert len(s) == 0


@pytest.mark.parametrize(
    "initial_items, item, expected",
    [
        ([1, 2], 99, False),  # T_MISSING_STACK_CONTAINS_NOT_PRESENT
    ],
)
def test_stack_contains_not_present(initial_items, item, expected):
    s = Stack()
    for i in initial_items:
        s.push(i)
    assert (item in s) is expected


@pytest.mark.parametrize(
    "initial_items, expected",
    [
        ([1, 2, 3], 3),  # T_MISSING_QUEUE_SIZE
    ],
)
def test_queue_size(initial_items, expected):
    q = Queue()
    for item in initial_items:
        q.enqueue(item)
    assert q.size() == expected


def test_queue_clear():
    q = Queue()
    for item in [1, 2, 3, 4]:
        q.enqueue(item)
    q.clear()
    assert q.is_empty()
    assert q.size() == 0
    assert len(q) == 0


@pytest.mark.parametrize(
    "initial_items, item, expected",
    [
        ([5, 6], -1, False),  # T_MISSING_QUEUE_CONTAINS_NOT_PRESENT
    ],
)
def test_queue_contains_not_present(initial_items, item, expected):
    q = Queue()
    for i in initial_items:
        q.enqueue(i)
    assert (item in q) is expected