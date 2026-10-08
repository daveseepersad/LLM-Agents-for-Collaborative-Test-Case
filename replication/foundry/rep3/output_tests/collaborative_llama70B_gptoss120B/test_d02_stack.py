import pytest
from data.input_code.d02_stack import *

# ---------- Stack Tests ----------

def test_stack_init():
    Stack()  # should initialize without error


def test_stack_push():
    s = Stack()
    s.push(1)
    assert s._items == [1]  # internal state check


def test_stack_pop_empty():
    s = Stack()
    with pytest.raises(IndexError):
        s.pop()


@pytest.mark.parametrize("item", [1])
def test_stack_pop_nonempty(item):
    s = Stack()
    s.push(item)
    assert s.pop() == item
    assert s.is_empty()


@pytest.mark.parametrize("item", [1])
def test_stack_peek_nonempty(item):
    s = Stack()
    s.push(item)
    assert s.peek() == item
    # ensure item still present
    assert not s.is_empty()


def test_stack_peek_empty():
    s = Stack()
    with pytest.raises(IndexError):
        s.peek()


@pytest.mark.parametrize(
    "setup,expected",
    [
        (False, True),   # empty stack
        (True, False),   # after push
    ],
)
def test_stack_is_empty(setup, expected):
    s = Stack()
    if setup:
        s.push(1)
    assert s.is_empty() is expected


@pytest.mark.parametrize(
    "setup,expected",
    [
        (False, 0),   # empty
        (True, 1),    # one element
    ],
)
def test_stack_size(setup, expected):
    s = Stack()
    if setup:
        s.push(1)
    assert s.size() == expected


def test_stack_clear():
    s = Stack()
    s.push(1)
    s.clear()
    assert s.is_empty()
    assert s.size() == 0


@pytest.mark.parametrize(
    "setup,expected",
    [
        (False, 0),   # empty length
        (True, 1),    # one element
    ],
)
def test_stack_len(setup, expected):
    s = Stack()
    if setup:
        s.push(1)
    assert len(s) == expected


@pytest.mark.parametrize(
    "setup,item,expected",
    [
        (False, 1, False),  # empty stack
        (True, 1, True),    # after push
    ],
)
def test_stack_contains(setup, item, expected):
    s = Stack()
    if setup:
        s.push(item)
    assert (item in s) is expected


# ---------- Queue Tests ----------

def test_queue_init():
    Queue()  # should initialize without error


def test_queue_enqueue():
    q = Queue()
    q.enqueue(1)
    assert q._items == [1]  # internal state check


def test_queue_dequeue_empty():
    q = Queue()
    with pytest.raises(IndexError):
        q.dequeue()


@pytest.mark.parametrize("item", [1])
def test_queue_dequeue_nonempty(item):
    q = Queue()
    q.enqueue(item)
    assert q.dequeue() == item
    assert q.is_empty()


def test_queue_front_empty():
    q = Queue()
    with pytest.raises(IndexError):
        q.front()


@pytest.mark.parametrize("item", [1])
def test_queue_front_nonempty(item):
    q = Queue()
    q.enqueue(item)
    assert q.front() == item
    # front should not remove the item
    assert not q.is_empty()


@pytest.mark.parametrize(
    "setup,expected",
    [
        (False, True),   # empty queue
        (True, False),   # after enqueue
    ],
)
def test_queue_is_empty(setup, expected):
    q = Queue()
    if setup:
        q.enqueue(1)
    assert q.is_empty() is expected


@pytest.mark.parametrize(
    "setup,expected",
    [
        (False, 0),   # empty
        (True, 1),    # one element
    ],
)
def test_queue_size(setup, expected):
    q = Queue()
    if setup:
        q.enqueue(1)
    assert q.size() == expected


def test_queue_clear():
    q = Queue()
    q.enqueue(1)
    q.clear()
    assert q.is_empty()
    assert q.size() == 0


@pytest.mark.parametrize(
    "setup,expected",
    [
        (False, 0),   # empty length
        (True, 1),    # one element
    ],
)
def test_queue_len(setup, expected):
    q = Queue()
    if setup:
        q.enqueue(1)
    assert len(q) == expected


@pytest.mark.parametrize(
    "setup,item,expected",
    [
        (False, 1, False),  # empty queue
        (True, 1, True),    # after enqueue
    ],
)
def test_queue_contains(setup, item, expected):
    q = Queue()
    if setup:
        q.enqueue(item)
    assert (item in q) is expected