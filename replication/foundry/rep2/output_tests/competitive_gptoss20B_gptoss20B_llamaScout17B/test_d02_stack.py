import pytest
from data.input_code.d02_stack import *

@pytest.mark.parametrize('initial_items, expected', [
    ([1, 2, 3], 3)
])
def test_S_POP_NonEmpty(initial_items, expected):
    s = Stack()
    for item in initial_items:
        s.push(item)
    assert s.pop() == expected

def test_S_POP_Empty():
    s = Stack()
    with pytest.raises(IndexError):
        s.pop()

@pytest.mark.parametrize('initial_items, expected', [
    ([7, 8, 9], 9)
])
def test_S_PEEK_NonEmpty(initial_items, expected):
    s = Stack()
    for item in initial_items:
        s.push(item)
    assert s.peek() == expected

def test_S_PEEK_Empty():
    s = Stack()
    with pytest.raises(IndexError):
        s.peek()

@pytest.mark.parametrize('initial_items, expected', [
    ([1, 2, 3], 3)
])
def test_S_LEN_NonEmpty(initial_items, expected):
    s = Stack()
    for item in initial_items:
        s.push(item)
    assert len(s) == expected

@pytest.mark.parametrize('initial_items, expected', [
    ([1, 2, 3], 1)
])
def test_Q_DEQUEUE_NonEmpty(initial_items, expected):
    q = Queue()
    for item in initial_items:
        q.enqueue(item)
    assert q.dequeue() == expected

def test_Q_DEQUEUE_Empty():
    q = Queue()
    with pytest.raises(IndexError):
        q.dequeue()

@pytest.mark.parametrize('initial_items, expected', [
    ([4, 5], 4)
])
def test_Q_FRONT_NonEmpty(initial_items, expected):
    q = Queue()
    for item in initial_items:
        q.enqueue(item)
    assert q.front() == expected

def test_Q_FRONT_Empty():
    q = Queue()
    with pytest.raises(IndexError):
        q.front()

def test_T_MISSING_S_CLEAR():
    s = Stack()
    actions = [
        {"action": "push", "value": 1},
        {"action": "push", "value": 2},
        {"action": "clear", "value": None},
    ]
    for act in actions:
        if act["action"] == "push":
            s.push(act["value"])
        elif act["action"] == "clear":
            s.clear()
    assert s.is_empty() is True
    assert s.size() == 0

def test_T_MISSING_S_CONTAINS():
    s = Stack()
    actions = [
        {"action": "push", "value": 5}
    ]
    for act in actions:
        if act["action"] == "push":
            s.push(act["value"])
    assert (5 in s) is True
    assert (7 in s) is False

def test_T_MISSING_S_POP_REDUCES():
    s = Stack()
    for v in [1, 2, 3]:
        s.push(v)
    s.pop()
    assert s.size() == 2
    assert s.peek() == 2

def test_T_MISSING_Q_CLEAR():
    q = Queue()
    actions = [
        {"action": "enqueue", "value": 10},
        {"action": "enqueue", "value": 20},
        {"action": "clear", "value": None},
    ]
    for act in actions:
        if act["action"] == "enqueue":
            q.enqueue(act["value"])
        elif act["action"] == "clear":
            q.clear()
    assert q.is_empty() is True
    assert q.size() == 0

def test_T_MISSING_Q_CONTAINS():
    q = Queue()
    actions = [
        {"action": "enqueue", "value": 42}
    ]
    for act in actions:
        if act["action"] == "enqueue":
            q.enqueue(act["value"])
    assert (42 in q) is True
    assert (99 in q) is False

@pytest.mark.parametrize('initial_items, expected', [
    ([], 0)
])
def test_S_LEN_EMPTY(initial_items, expected):
    s = Stack()
    for item in initial_items:
        s.push(item)
    assert len(s) == expected
    assert s.size() == expected

@pytest.mark.parametrize('initial_items, expected', [
    ([], 0)
])
def test_Q_LEN_EMPTY(initial_items, expected):
    q = Queue()
    for item in initial_items:
        q.enqueue(item)
    assert len(q) == expected
    assert q.size() == expected

@pytest.mark.parametrize('initial_items, item, expected', [
    ([], 5, False)
])
def test_S_CONTAINS_EMPTY_FALSE(initial_items, item, expected):
    s = Stack()
    for v in initial_items:
        s.push(v)
    assert (item in s) is expected

@pytest.mark.parametrize('initial_items, expected', [
    ([10, 20], 10)
])
def test_Q_DEQUEUE_ORDER(initial_items, expected):
    q = Queue()
    for it in initial_items:
        q.enqueue(it)
    assert q.dequeue() == expected