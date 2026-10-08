import pytest
from data.input_code.d02_stack import *

def test_S1_PUSH_returns_none():
    s = Stack()
    result = s.push(1)
    assert result is None

def test_S2_POP_returns_pushed_value():
    s = Stack()
    s.push(1)
    assert s.pop() == 1

def test_S3_POP_EMPTY_raises_IndexError():
    s = Stack()
    with pytest.raises(IndexError):
        s.pop()

def test_S4_PEEK_returns_top_without_removing():
    s = Stack()
    s.push('a')
    assert s.peek() == 'a'
    assert len(s) == 1  # ensure not removed

def test_S5_PEEK_EMPTY_raises_IndexError():
    s = Stack()
    with pytest.raises(IndexError):
        s.peek()

def test_S6_ISEMPTY_true_for_new_stack():
    s = Stack()
    assert s.is_empty() is True

def test_S7_ISEMPTY_false_after_push():
    s = Stack()
    s.push(1)
    assert s.is_empty() is False

def test_S8_SIZE_reflects_two_pushes():
    s = Stack()
    s.push(1)
    s.push(2)
    assert s.size() == 2

def test_S9_CLEAR_empties_stack():
    s = Stack()
    s.push(10)
    s.clear()
    assert s.is_empty() is True
    assert len(s) == 0

def test_S10_LEN_matches_number_of_items_after_three_pushes():
    s = Stack()
    s.push('a')
    s.push('b')
    s.push('c')
    assert len(s) == 3

def test_S11_CONTAINS_true_for_existing_item():
    s = Stack()
    s.push(42)
    assert (42 in s) is True

def test_S12_CONTAINS_false_for_missing_item():
    s = Stack()
    s.push(42)
    assert (99 in s) is False

def test_Q1_ENQUEUE_returns_none():
    q = Queue()
    result = q.enqueue("x")
    assert result is None

def test_Q2_DEQUEUE_returns_first_enqueued():
    q = Queue()
    q.enqueue("x")
    assert q.dequeue() == "x"

def test_Q3_DEQUEUE_EMPTY_raises_IndexError():
    q = Queue()
    with pytest.raises(IndexError):
        q.dequeue()

def test_Q4_FRONT_returns_first_without_removing():
    q = Queue()
    q.enqueue("y")
    q.enqueue("z")
    assert q.front() == "y"
    # Ensure front does not remove the item
    assert q.dequeue() == "y"

def test_Q5_FRONT_EMPTY_raises_IndexError():
    q = Queue()
    with pytest.raises(IndexError):
        q.front()

def test_Q6_ISEMPTY_true_for_new_queue():
    q = Queue()
    assert q.is_empty() is True

def test_Q7_ISEMPTY_false_after_one_enqueue():
    q = Queue()
    q.enqueue("item")
    assert q.is_empty() is False

def test_Q8_SIZE_after_two_enqueues():
    q = Queue()
    q.enqueue("a")
    q.enqueue("b")
    assert q.size() == 2

def test_Q9_CLEAR_empties_queue():
    q = Queue()
    q.enqueue("a")
    q.enqueue("b")
    q.clear()
    assert q.is_empty() is True
    assert len(q) == 0

def test_Q10_LEN_matches_number_of_items_after_three_enqueues():
    q = Queue()
    q.enqueue("a")
    q.enqueue("b")
    q.enqueue("c")
    assert len(q) == 3

def test_Q11_CONTAINS_true_for_existing_item():
    q = Queue()
    q.enqueue("z")
    assert ("z" in q) is True

def test_Q12_CONTAINS_false_for_missing_item():
    q = Queue()
    q.enqueue("z")
    assert ("missing" in q) is False