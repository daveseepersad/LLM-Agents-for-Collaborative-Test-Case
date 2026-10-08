import pytest
from data.input_code.d02_stack import *

def _apply_setup(obj, actions):
    """Execute a sequence of method calls on obj."""
    for act in actions:
        method = getattr(obj, act["method"])
        method(**act.get("args", {}))

# ---------- Stack Tests ----------

@pytest.mark.parametrize(
    "item",
    [42],
)
def test_stack_push_returns_none(item):
    s = Stack()
    assert s.push(item) is None
    assert item in s

@pytest.mark.parametrize(
    "setup, expected",
    [
        ([{"method": "push", "args": {"item": 42}}], 42),
    ],
)
def test_stack_pop_success(setup, expected):
    s = Stack()
    _apply_setup(s, setup)
    assert s.pop() == expected

def test_stack_pop_empty_raises():
    s = Stack()
    with pytest.raises(IndexError):
        s.pop()

def test_stack_peek_empty_raises():
    s = Stack()
    with pytest.raises(IndexError):
        s.peek()

@pytest.mark.parametrize(
    "setup, expected",
    [
        ([{"method": "push", "args": {"item": "a"}},
          {"method": "push", "args": {"item": "b"}}], "b"),
    ],
)
def test_stack_peek_success(setup, expected):
    s = Stack()
    _apply_setup(s, setup)
    assert s.peek() == expected

@pytest.mark.parametrize(
    "setup, expected_len",
    [
        ([{"method": "push", "args": {"item": 1}},
          {"method": "push", "args": {"item": 2}},
          {"method": "push", "args": {"item": 3}}], 3),
    ],
)
def test_stack_len_reflects_items(setup, expected_len):
    s = Stack()
    _apply_setup(s, setup)
    assert len(s) == expected_len

@pytest.mark.parametrize(
    "setup, expected_size",
    [
        ([{"method": "push", "args": {"item": 1}},
          {"method": "push", "args": {"item": 2}}], 2),
    ],
)
def test_stack_size_returns_correct_value(setup, expected_size):
    s = Stack()
    _apply_setup(s, setup)
    assert s.size() == expected_size

@pytest.mark.parametrize(
    "setup, query, expected",
    [
        ([{"method": "push", "args": {"item": None}},
          {"method": "push", "args": {"item": ""}},
          {"method": "push", "args": {"item": 0}}], "", True),
    ],
)
def test_stack_contains_behavior(setup, query, expected):
    s = Stack()
    _apply_setup(s, setup)
    assert (query in s) is expected

def test_stack_clear_empties():
    s = Stack()
    s.push(5)
    s.clear()
    assert s.is_empty()
    assert len(s) == 0

def test_stack_is_empty_on_new():
    s = Stack()
    assert s.is_empty()

# ---------- Queue Tests ----------

@pytest.mark.parametrize(
    "item",
    ["x"],
)
def test_queue_enqueue_returns_none(item):
    q = Queue()
    assert q.enqueue(item) is None
    assert item in q

@pytest.mark.parametrize(
    "setup, expected",
    [
        ([{"method": "enqueue", "args": {"item": "x"}}], "x"),
    ],
)
def test_queue_dequeue_success(setup, expected):
    q = Queue()
    _apply_setup(q, setup)
    assert q.dequeue() == expected

def test_queue_dequeue_empty_raises():
    q = Queue()
    with pytest.raises(IndexError):
        q.dequeue()

def test_queue_front_empty_raises():
    q = Queue()
    with pytest.raises(IndexError):
        q.front()

@pytest.mark.parametrize(
    "setup, expected",
    [
        ([{"method": "enqueue", "args": {"item": "first"}},
          {"method": "enqueue", "args": {"item": "second"}}], "first"),
    ],
)
def test_queue_front_success(setup, expected):
    q = Queue()
    _apply_setup(q, setup)
    assert q.front() == expected

@pytest.mark.parametrize(
    "setup, expected_len",
    [
        ([{"method": "enqueue", "args": {"item": 1}},
          {"method": "enqueue", "args": {"item": 2}},
          {"method": "enqueue", "args": {"item": 3}}], 3),
    ],
)
def test_queue_len_reflects_items(setup, expected_len):
    q = Queue()
    _apply_setup(q, setup)
    assert len(q) == expected_len

@pytest.mark.parametrize(
    "setup, expected_size",
    [
        ([{"method": "enqueue", "args": {"item": "a"}},
          {"method": "enqueue", "args": {"item": "b"}}], 2),
    ],
)
def test_queue_size_returns_correct_value(setup, expected_size):
    q = Queue()
    _apply_setup(q, setup)
    assert q.size() == expected_size

@pytest.mark.parametrize(
    "setup, query, expected",
    [
        ([{"method": "enqueue", "args": {"item": None}},
          {"method": "enqueue", "args": {"item": ""}},
          {"method": "enqueue", "args": {"item": 0}}], 0, True),
    ],
)
def test_queue_contains_behavior(setup, query, expected):
    q = Queue()
    _apply_setup(q, setup)
    assert (query in q) is expected

def test_queue_clear_empties():
    q = Queue()
    q.enqueue("temp")
    q.clear()
    assert q.is_empty()
    assert len(q) == 0

def test_queue_is_empty_on_new():
    q = Queue()
    assert q.is_empty()