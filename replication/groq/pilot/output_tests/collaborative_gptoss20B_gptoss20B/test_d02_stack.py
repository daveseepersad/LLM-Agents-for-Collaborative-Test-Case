import pytest
from data.input_code.d02_stack import Stack, Queue

# ---------- Stack Tests ----------

@pytest.mark.parametrize("item", [5, None, "", []])
def test_stack_push(item):
    s = Stack()
    s.push(item)
    # No exception should be raised; verify the item is in the stack
    assert item in s._items

def test_stack_is_empty():
    s = Stack()
    assert s.is_empty() is True

def test_stack_size_empty():
    s = Stack()
    assert s.size() == 0

def test_stack_pop_success():
    s = Stack()
    s.push(10)
    assert s.pop() == 10
    assert s.is_empty() is True

def test_stack_pop_empty():
    s = Stack()
    with pytest.raises(IndexError):
        s.pop()

def test_stack_peek_success():
    s = Stack()
    s.push(20)
    assert s.peek() == 20
    # Peek should not remove the item
    assert s.size() == 1

def test_stack_peek_empty():
    s = Stack()
    with pytest.raises(IndexError):
        s.peek()

def test_stack_clear():
    s = Stack()
    s.push(1)
    s.push(2)
    s.clear()
    assert s.is_empty() is True
    assert s.size() == 0

def test_stack_len_after_push():
    s = Stack()
    s.push(3)
    s.push(4)
    assert len(s) == 2

def test_stack_len_after_clear():
    s = Stack()
    s.push(5)
    s.push(6)
    s.clear()
    assert len(s) == 0

@pytest.mark.parametrize(
    "setup_items, item, expected",
    [
        ([7], 7, True),
        ([5], 6, False),
        ([None], None, True),
        ([""], "", True),
        ([[]], [], True),
    ],
)
def test_stack_contains(setup_items, item, expected):
    s = Stack()
    for it in setup_items:
        s.push(it)
    assert (item in s) is expected

# ---------- Queue Tests ----------

@pytest.mark.parametrize("item", ["a", None, "", []])
def test_queue_enqueue(item):
    q = Queue()
    q.enqueue(item)
    # No exception should be raised; verify the item is in the queue
    assert item in q._items

def test_queue_is_empty():
    q = Queue()
    assert q.is_empty() is True

def test_queue_size_empty():
    q = Queue()
    assert q.size() == 0

def test_queue_dequeue_success():
    q = Queue()
    q.enqueue("b")
    assert q.dequeue() == "b"
    assert q.is_empty() is True

def test_queue_dequeue_empty():
    q = Queue()
    with pytest.raises(IndexError):
        q.dequeue()

def test_queue_front_success():
    q = Queue()
    q.enqueue("c")
    assert q.front() == "c"
    # Front should not remove the item
    assert q.size() == 1

def test_queue_front_empty():
    q = Queue()
    with pytest.raises(IndexError):
        q.front()

def test_queue_clear():
    q = Queue()
    q.enqueue(1)
    q.enqueue(2)
    q.clear()
    assert q.is_empty() is True
    assert q.size() == 0

def test_queue_len_after_enqueue():
    q = Queue()
    q.enqueue(3)
    q.enqueue(4)
    assert len(q) == 2

def test_queue_len_after_clear():
    q = Queue()
    q.enqueue(5)
    q.enqueue(6)
    q.clear()
    assert len(q) == 0

@pytest.mark.parametrize(
    "setup_items, item, expected",
    [
        (["7"], "7", True),
        (["5"], "6", False),
        ([None], None, True),
        ([""], "", True),
        ([[]], [], True),
    ],
)
def test_queue_contains(setup_items, item, expected):
    q = Queue()
    for it in setup_items:
        q.enqueue(it)
    assert (item in q) is expected