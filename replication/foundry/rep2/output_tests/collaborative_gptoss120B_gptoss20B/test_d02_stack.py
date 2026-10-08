import pytest
from data.input_code.d02_stack import *

def test_stack_pop_empty():
    s = Stack()
    with pytest.raises(IndexError):
        s.pop()

def test_stack_peek_empty():
    s = Stack()
    with pytest.raises(IndexError):
        s.peek()

def test_stack_len_initial():
    s = Stack()
    assert len(s) == 0

@pytest.mark.parametrize(
    "prepopulate,item,expected",
    [
        ([1, 2], 2, True),
        ([1, 2], 3, False),
    ]
)
def test_stack_contains(prepopulate, item, expected):
    s = Stack()
    for i in prepopulate:
        s.push(i)
    assert (item in s) is expected

def test_queue_dequeue_empty():
    q = Queue()
    with pytest.raises(IndexError):
        q.dequeue()

def test_queue_front_empty():
    q = Queue()
    with pytest.raises(IndexError):
        q.front()

def test_queue_len_initial():
    q = Queue()
    assert len(q) == 0

def test_queue_enqueue():
    q = Queue()
    q.enqueue(7)
    assert 7 in q
    assert len(q) == 1

@pytest.mark.parametrize(
    "prepopulate,item,expected",
    [
        ([7, 8], 7, True),
        ([7, 8], 9, False),
    ]
)
def test_queue_contains(prepopulate, item, expected):
    q = Queue()
    for i in prepopulate:
        q.enqueue(i)
    assert (item in q) is expected

import pytest
from data.input_code.d02_stack import *

def test_stack_pop_nonempty():
    s = Stack()
    for i in [1, 2]:
        s.push(i)
    assert s.pop() == 2

def test_stack_peek_nonempty():
    s = Stack()
    for i in [1, 2]:
        s.push(i)
    assert s.peek() == 2

def test_stack_is_empty_after_push():
    s = Stack()
    for i in [42]:
        s.push(i)
    assert s.is_empty() is False

def test_stack_size_after_push():
    s = Stack()
    for i in [1, 2]:
        s.push(i)
    assert s.size() == 2

def test_queue_dequeue_nonempty():
    q = Queue()
    for i in [10, 20]:
        q.enqueue(i)
    assert q.dequeue() == 10

def test_queue_front_nonempty():
    q = Queue()
    for i in [5, 6]:
        q.enqueue(i)
    assert q.front() == 5

def test_queue_size_after_prepop():
    q = Queue()
    for i in [1, 2]:
        q.enqueue(i)
    assert q.size() == 2

import pytest
from data.input_code.d02_stack import *

def test_stack_pop_three():
    s = Stack()
    for i in [1, 2, 3]:
        s.push(i)
    assert s.pop() == 3

def test_stack_size_three():
    s = Stack()
    for i in [1, 2, 3]:
        s.push(i)
    assert s.size() == 3

def test_queue_dequeue_three():
    q = Queue()
    for i in [100, 200, 300]:
        q.enqueue(i)
    assert q.dequeue() == 100

def test_queue_front_three():
    q = Queue()
    for i in [101, 202, 303]:
        q.enqueue(i)
    assert q.front() == 101

def test_queue_size_three():
    q = Queue()
    for i in [5, 6, 7]:
        q.enqueue(i)
    assert q.size() == 3

import pytest
from data.input_code.d02_stack import *

def test_stack_is_empty_initial():
    s = Stack()
    assert s.is_empty() is True

def test_stack_size_initial():
    s = Stack()
    assert s.size() == 0

def test_queue_is_empty_initial():
    q = Queue()
    assert q.is_empty() is True

def test_queue_size_initial():
    q = Queue()
    assert q.size() == 0

import pytest
from data.input_code.d02_stack import *

def test_stack_clear():
    s = Stack()
    for i in [1, 2, 3]:
        s.push(i)
    s.clear()
    assert s.is_empty() is True
    assert s.size() == 0
    assert len(s) == 0
    assert 1 not in s

def test_queue_clear():
    q = Queue()
    for i in [4, 5, 6]:
        q.enqueue(i)
    q.clear()
    assert q.is_empty() is True
    assert q.size() == 0
    assert len(q) == 0
    assert 4 not in q