import pytest
from data.input_code.d02_stack import *

@pytest.mark.parametrize('target', [
    'Stack.pop', 'Stack.peek', 'Queue.dequeue', 'Queue.front'
])
def test_empty_operations_raise_index_error(target):
    cls_name, method = target.split('.')
    obj = Stack() if cls_name == 'Stack' else Queue()
    with pytest.raises(IndexError):
        getattr(obj, method)()

@pytest.mark.parametrize('target', [
    'Stack.is_empty', 'Queue.is_empty'
])
def test_is_empty_on_empty(target):
    cls_name, method = target.split('.')
    obj = Stack() if cls_name == 'Stack' else Queue()
    assert getattr(obj, method)() == True

@pytest.mark.parametrize('target', [
    ('Stack.size', 0),
    ('Queue.size', 0)
])
def test_size_on_empty(target):
    cls_name, method = target[0].split('.')
    expected = target[1]
    obj = Stack() if cls_name == 'Stack' else Queue()
    assert getattr(obj, method)() == expected

import pytest
from data.input_code.d02_stack import *

@pytest.mark.parametrize('cls_tuple', [
    ('Stack', '__len__', (), 0),
    ('Stack', '__contains__', (5,), False),
    ('Stack', 'clear', (), None),
    ('Queue', '__len__', (), 0),
    ('Queue', '__contains__', (7,), False),
    ('Queue', 'clear', (), None),
])
def test_empty_structures(cls_tuple):
    target_cls, method, input_args, expected = cls_tuple
    obj = Stack() if target_cls == 'Stack' else Queue()
    if input_args:
        result = getattr(obj, method)(*input_args)
    else:
        result = getattr(obj, method)()
    if expected is None:
        assert result is None
    else:
        assert result == expected

import pytest
from data.input_code.d02_stack import *

def test_stack_push_changes_state():
    s = Stack()
    s.push(42)
    assert 42 in s

def test_queue_enqueue_changes_state():
    q = Queue()
    q.enqueue("element")
    assert "element" in q

import pytest
from data.input_code.d02_stack import *

@pytest.mark.parametrize('target, expected', [
    ('Stack.pop', 'Pop from empty stack'),
    ('Stack.peek', 'Peek from empty stack'),
    ('Queue.dequeue', 'Dequeue from empty queue'),
    ('Queue.front', 'Front from empty queue')
])
def test_empty_operations_have_expected_error_message(target, expected):
    cls_name, method = target.split('.')
    obj = Stack() if cls_name == 'Stack' else Queue()
    with pytest.raises(IndexError) as excinfo:
        getattr(obj, method)()
    assert str(excinfo.value) == expected

import pytest
from data.input_code.d02_stack import *

def test_stack_nonempty_pop_returns_last_and_updates_state():
    s = Stack()
    s.push(1)
    s.push(2)
    value = s.pop()
    assert value == 2
    assert 2 not in s
    assert len(s) == 1
    assert 1 in s

def test_stack_nonempty_peek_does_not_remove():
    s = Stack()
    s.push(1)
    s.push(3)
    top = s.peek()
    assert top == 3
    assert len(s) == 2
    assert 3 in s
    assert 1 in s

def test_queue_nonempty_dequeue_returns_first_and_updates_state():
    q = Queue()
    q.enqueue("a")
    q.enqueue("b")
    first = q.dequeue()
    assert first == "a"
    assert len(q) == 1
    assert "a" not in q
    assert "b" in q
    assert q.front() == "b"

def test_queue_nonempty_front_returns_first_without_removing():
    q = Queue()
    q.enqueue("x")
    q.enqueue("y")
    front_item = q.front()
    assert front_item == "x"
    assert len(q) == 2
    assert "x" in q
    assert "y" in q

def test_len_on_nonempty_stack():
    s = Stack()
    s.push(1)
    s.push(2)
    assert len(s) == 2

def test_clear_on_nonempty_stack_empties_structure():
    s = Stack()
    s.push(7)
    s.push(8)
    result = s.clear()
    assert result is None
    assert len(s) == 0
    assert s.is_empty() is True