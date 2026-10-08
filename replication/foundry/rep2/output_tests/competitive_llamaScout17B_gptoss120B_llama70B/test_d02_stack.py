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
    assert empty_stack.size() == 0
    assert len(empty_stack) == 0
    assert empty_stack._items == []

def test_stack_push(stack_one_item):
    # push already performed in fixture; verify state
    assert stack_one_item._items == [5]
    assert stack_one_item.size() == 1

def test_stack_pop_success(stack_one_item):
    result = stack_one_item.pop()
    assert result == 5
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
    "stack_fixture, expected",
    [
        ("empty_stack", True),
        ("stack_one_item", False),
    ],
)
def request_stack_fixture(request, stack_fixture):
    return request.getfixturevalue(stack_fixture)

@pytest.mark.parametrize(
    "stack_fixture, expected",
    [
        ("empty_stack", True),
        ("stack_one_item", False),
    ],
)
def test_stack_is_empty(request, stack_fixture, expected):
    stack = request.getfixturevalue(stack_fixture)
    assert stack.is_empty() is expected

def test_stack_size(stack_one_item):
    assert stack_one_item.size() == 1

def test_stack_clear(stack_one_item):
    stack_one_item.clear()
    assert stack_one_item.is_empty()
    assert stack_one_item._items == []

def test_stack_len(stack_one_item):
    assert len(stack_one_item) == 1

@pytest.mark.parametrize(
    "stack_fixture, item, expected",
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
    assert empty_queue.size() == 0
    assert len(empty_queue) == 0
    assert empty_queue._items == []

def test_queue_enqueue(queue_one_item):
    # enqueue already performed in fixture; verify state
    assert queue_one_item._items == [5]
    assert queue_one_item.size() == 1

def test_queue_dequeue_success(queue_one_item):
    result = queue_one_item.dequeue()
    assert result == 5
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
    "queue_fixture, expected",
    [
        ("empty_queue", True),
        ("queue_one_item", False),
    ],
)
def test_queue_is_empty(request, queue_fixture, expected):
    queue = request.getfixturevalue(queue_fixture)
    assert queue.is_empty() is expected

def test_queue_size(queue_one_item):
    assert queue_one_item.size() == 1

def test_queue_clear(queue_one_item):
    queue_one_item.clear()
    assert queue_one_item.is_empty()
    assert queue_one_item._items == []

def test_queue_len(queue_one_item):
    assert len(queue_one_item) == 1

@pytest.mark.parametrize(
    "queue_fixture, item, expected",
    [
        ("queue_one_item", 5, True),
        ("queue_one_item", 3, False),
    ],
)
def test_queue_contains(request, queue_fixture, item, expected):
    queue = request.getfixturevalue(queue_fixture)
    assert (item in queue) is expected