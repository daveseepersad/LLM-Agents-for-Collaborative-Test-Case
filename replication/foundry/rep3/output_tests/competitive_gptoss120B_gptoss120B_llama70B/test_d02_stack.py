import pytest
from data.input_code.d02_stack import *

# ---------- Stack Tests ----------

@pytest.mark.parametrize(
    "initial_items, item",
    [
        ([], 42),
    ],
)
def test_stack_push(initial_items, item):
    s = Stack()
    s._items = list(initial_items)
    s.push(item)
    assert s._items[-1] == item
    assert s.size() == len(initial_items) + 1

@pytest.mark.parametrize(
    "initial_items, expected",
    [
        ([1, 2, 3], 3),
    ],
)
def test_stack_pop_success(initial_items, expected):
    s = Stack()
    s._items = list(initial_items)
    result = s.pop()
    assert result == expected
    assert s.size() == len(initial_items) - 1

def test_stack_pop_empty():
    s = Stack()
    s._items = []
    with pytest.raises(IndexError):
        s.pop()

@pytest.mark.parametrize(
    "initial_items, expected",
    [
        ([7, 8], 8),
    ],
)
def test_stack_peek_success(initial_items, expected):
    s = Stack()
    s._items = list(initial_items)
    assert s.peek() == expected
    # ensure peek does not remove the item
    assert s.size() == len(initial_items)

def test_stack_peek_empty():
    s = Stack()
    s._items = []
    with pytest.raises(IndexError):
        s.peek()

@pytest.mark.parametrize(
    "initial_items, expected",
    [
        ([], True),
        ([0], False),
    ],
)
def test_stack_is_empty(initial_items, expected):
    s = Stack()
    s._items = list(initial_items)
    assert s.is_empty() is expected

@pytest.mark.parametrize(
    "initial_items, expected",
    [
        ([1, 2, 3, 4], 4),
    ],
)
def test_stack_size(initial_items, expected):
    s = Stack()
    s._items = list(initial_items)
    assert s.size() == expected

def test_stack_clear():
    s = Stack()
    s._items = [9, 10]
    s.clear()
    assert s.size() == 0
    assert s.is_empty()

@pytest.mark.parametrize(
    "initial_items, expected",
    [
        ([5, 6], 2),
    ],
)
def test_stack_len(initial_items, expected):
    s = Stack()
    s._items = list(initial_items)
    assert len(s) == expected

@pytest.mark.parametrize(
    "initial_items, item, expected",
    [
        ([1, 2, 3], 2, True),
        ([1, 2, 3], 4, False),
    ],
)
def test_stack_contains(initial_items, item, expected):
    s = Stack()
    s._items = list(initial_items)
    assert (item in s) is expected

# ---------- Queue Tests ----------

@pytest.mark.parametrize(
    "initial_items, item",
    [
        ([], "a"),
    ],
)
def test_queue_enqueue(initial_items, item):
    q = Queue()
    q._items = list(initial_items)
    q.enqueue(item)
    assert q._items[-1] == item
    assert q.size() == len(initial_items) + 1

@pytest.mark.parametrize(
    "initial_items, expected",
    [
        (["x", "y", "z"], "x"),
    ],
)
def test_queue_dequeue_success(initial_items, expected):
    q = Queue()
    q._items = list(initial_items)
    result = q.dequeue()
    assert result == expected
    assert q.size() == len(initial_items) - 1

def test_queue_dequeue_empty():
    q = Queue()
    q._items = []
    with pytest.raises(IndexError):
        q.dequeue()

@pytest.mark.parametrize(
    "initial_items, expected",
    [
        ([10, 20], 10),
    ],
)
def test_queue_front_success(initial_items, expected):
    q = Queue()
    q._items = list(initial_items)
    assert q.front() == expected
    # ensure front does not remove the item
    assert q.size() == len(initial_items)

def test_queue_front_empty():
    q = Queue()
    q._items = []
    with pytest.raises(IndexError):
        q.front()

@pytest.mark.parametrize(
    "initial_items, expected",
    [
        ([], True),
        (["item"], False),
    ],
)
def test_queue_is_empty(initial_items, expected):
    q = Queue()
    q._items = list(initial_items)
    assert q.is_empty() is expected

@pytest.mark.parametrize(
    "initial_items, expected",
    [
        ([1, 2, 3], 3),
    ],
)
def test_queue_size(initial_items, expected):
    q = Queue()
    q._items = list(initial_items)
    assert q.size() == expected

def test_queue_clear():
    q = Queue()
    q._items = [5, 6]
    q.clear()
    assert q.size() == 0
    assert q.is_empty()

@pytest.mark.parametrize(
    "initial_items, expected",
    [
        (["a", "b"], 2),
    ],
)
def test_queue_len(initial_items, expected):
    q = Queue()
    q._items = list(initial_items)
    assert len(q) == expected

@pytest.mark.parametrize(
    "initial_items, item, expected",
    [
        ([1, 2, 3], 2, True),
        ([1, 2, 3], 4, False),
    ],
)
def test_queue_contains(initial_items, item, expected):
    q = Queue()
    q._items = list(initial_items)
    assert (item in q) is expected