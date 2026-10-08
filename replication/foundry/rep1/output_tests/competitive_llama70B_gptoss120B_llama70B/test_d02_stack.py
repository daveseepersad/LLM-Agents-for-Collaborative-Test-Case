import pytest
from data.input_code.d02_stack import *

# Fixtures for Stack
@pytest.fixture
def empty_stack():
    return Stack()

@pytest.fixture
def stack_one_item():
    s = Stack()
    s.push(5)
    return s

# Fixtures for Queue
@pytest.fixture
def empty_queue():
    return Queue()

@pytest.fixture
def queue_one_item():
    q = Queue()
    q.enqueue(5)
    return q

# ---------- Stack Tests ----------
def test_stack_init(empty_stack):
    # __init__ should create an empty stack
    assert empty_stack.is_empty()
    assert empty_stack.size() == 0

def test_stack_push(empty_stack):
    # push returns None; verify side‑effect
    result = empty_stack.push(5)
    assert result is None
    assert empty_stack.peek() == 5

def test_stack_pop_success(stack_one_item):
    assert stack_one_item.pop() == 5
    assert stack_one_item.is_empty()

def test_stack_pop_error(empty_stack):
    with pytest.raises(IndexError):
        empty_stack.pop()

def test_stack_peek_success(stack_one_item):
    assert stack_one_item.peek() == 5

def test_stack_peek_error(empty_stack):
    with pytest.raises(IndexError):
        empty_stack.peek()

@pytest.mark.parametrize(
    "stack_fixture,expected",
    [
        ("empty_stack", True),
        ("stack_one_item", False),
    ],
)
def request_stack_fixture(request, stack_fixture):
    return request.getfixturevalue(stack_fixture)

@pytest.mark.parametrize(
    "stack_fixture,expected",
    [
        ("empty_stack", True),
        ("stack_one_item", False),
    ],
)
def test_stack_is_empty(request, stack_fixture, expected):
    stack = request.getfixturevalue(stack_fixture)
    assert stack.is_empty() is expected

@pytest.mark.parametrize(
    "stack_fixture,expected",
    [
        ("empty_stack", 0),
        ("stack_one_item", 1),
    ],
)
def test_stack_size(request, stack_fixture, expected):
    stack = request.getfixturevalue(stack_fixture)
    assert stack.size() == expected

def test_stack_clear(stack_one_item):
    stack_one_item.clear()
    assert stack_one_item.is_empty()
    assert stack_one_item.size() == 0

@pytest.mark.parametrize(
    "stack_fixture,expected_len",
    [
        ("empty_stack", 0),
        ("stack_one_item", 1),
    ],
)
def test_stack_len(request, stack_fixture, expected_len):
    stack = request.getfixturevalue(stack_fixture)
    assert len(stack) == expected_len

@pytest.mark.parametrize(
    "stack_fixture,item,expected",
    [
        ("stack_one_item", 5, True),
        ("stack_one_item", 3, False),
    ],
)
def test_stack_contains(request, stack_fixture, item, expected):
    stack = request.getfixturevalue(stack_fixture)
    assert (item in stack) is expected

# ---------- Queue Tests ----------
def test_queue_init(empty_queue):
    # __init__ should create an empty queue
    assert empty_queue.is_empty()
    assert empty_queue.size() == 0

def test_queue_enqueue(empty_queue):
    result = empty_queue.enqueue(5)
    assert result is None
    assert empty_queue.front() == 5

def test_queue_dequeue_success(queue_one_item):
    assert queue_one_item.dequeue() == 5
    assert queue_one_item.is_empty()

def test_queue_dequeue_error(empty_queue):
    with pytest.raises(IndexError):
        empty_queue.dequeue()

def test_queue_front_success(queue_one_item):
    assert queue_one_item.front() == 5

def test_queue_front_error(empty_queue):
    with pytest.raises(IndexError):
        empty_queue.front()

@pytest.mark.parametrize(
    "queue_fixture,expected",
    [
        ("empty_queue", True),
        ("queue_one_item", False),
    ],
)
def test_queue_is_empty(request, queue_fixture, expected):
    queue = request.getfixturevalue(queue_fixture)
    assert queue.is_empty() is expected

@pytest.mark.parametrize(
    "queue_fixture,expected",
    [
        ("empty_queue", 0),
        ("queue_one_item", 1),
    ],
)
def test_queue_size(request, queue_fixture, expected):
    queue = request.getfixturevalue(queue_fixture)
    assert queue.size() == expected

def test_queue_clear(queue_one_item):
    queue_one_item.clear()
    assert queue_one_item.is_empty()
    assert queue_one_item.size() == 0

@pytest.mark.parametrize(
    "queue_fixture,expected_len",
    [
        ("empty_queue", 0),
        ("queue_one_item", 1),
    ],
)
def test_queue_len(request, queue_fixture, expected_len):
    queue = request.getfixturevalue(queue_fixture)
    assert len(queue) == expected_len

@pytest.mark.parametrize(
    "queue_fixture,item,expected",
    [
        ("queue_one_item", 5, True),
        ("queue_one_item", 3, False),
    ],
)
def test_queue_contains(request, queue_fixture, item, expected):
    queue = request.getfixturevalue(queue_fixture)
    assert (item in queue) is expected