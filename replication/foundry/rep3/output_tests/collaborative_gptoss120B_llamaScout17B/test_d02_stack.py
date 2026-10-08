import pytest
from data.input_code.d02_stack import *

@pytest.mark.parametrize('item', [42])
def test_stack_push(item):
    stack = Stack()
    stack.push(item)
    assert stack._items == [item]

def test_stack_pop_empty():
    stack = Stack()
    with pytest.raises(IndexError):
        stack.pop()

@pytest.mark.parametrize('pre_items, expected', [([7], 7)])
def test_stack_pop_nonempty(pre_items, expected):
    stack = Stack()
    for item in pre_items:
        stack.push(item)
    assert stack.pop() == expected

def test_stack_peek_empty():
    stack = Stack()
    with pytest.raises(IndexError):
        stack.peek()

@pytest.mark.parametrize('pre_items, expected', [(['alpha'], 'alpha')])
def test_stack_peek_nonempty(pre_items, expected):
    stack = Stack()
    for item in pre_items:
        stack.push(item)
    assert stack.peek() == expected

def test_stack_is_empty_true():
    stack = Stack()
    assert stack.is_empty() == True

@pytest.mark.parametrize('pre_items', [[1]])
def test_stack_is_empty_false(pre_items):
    stack = Stack()
    for item in pre_items:
        stack.push(item)
    assert stack.is_empty() == False

@pytest.mark.parametrize('pre_items, expected', [([1, 2, 3], 3)])
def test_stack_size(pre_items, expected):
    stack = Stack()
    for item in pre_items:
        stack.push(item)
    assert stack.size() == expected

@pytest.mark.parametrize('pre_items', [[9]])
def test_stack_clear(pre_items):
    stack = Stack()
    for item in pre_items:
        stack.push(item)
    stack.clear()
    assert stack._items == []

@pytest.mark.parametrize('pre_items, expected', [(['x', 'y'], 2)])
def test_stack_len(pre_items, expected):
    stack = Stack()
    for item in pre_items:
        stack.push(item)
    assert len(stack) == expected

@pytest.mark.parametrize('pre_items, item, expected', [([5, 6], 6, True), ([], 10, False)])
def test_stack_contains(pre_items, item, expected):
    stack = Stack()
    for i in pre_items:
        stack.push(i)
    assert (item in stack) == expected

@pytest.mark.parametrize('item', ['data'])
def test_queue_enqueue(item):
    queue = Queue()
    queue.enqueue(item)
    assert queue._items == [item]

def test_queue_dequeue_empty():
    queue = Queue()
    with pytest.raises(IndexError):
        queue.dequeue()

@pytest.mark.parametrize('pre_items, expected', [([99], 99)])
def test_queue_dequeue_nonempty(pre_items, expected):
    queue = Queue()
    for item in pre_items:
        queue.enqueue(item)
    assert queue.dequeue() == expected

def test_queue_front_empty():
    queue = Queue()
    with pytest.raises(IndexError):
        queue.front()

@pytest.mark.parametrize('pre_items, expected', [(['first', 'second'], 'first')])
def test_queue_front_nonempty(pre_items, expected):
    queue = Queue()
    for item in pre_items:
        queue.enqueue(item)
    assert queue.front() == expected

def test_queue_is_empty_true():
    queue = Queue()
    assert queue.is_empty() == True

@pytest.mark.parametrize('pre_items', [[1]])
def test_queue_is_empty_false(pre_items):
    queue = Queue()
    for item in pre_items:
        queue.enqueue(item)
    assert queue.is_empty() == False

@pytest.mark.parametrize('pre_items, expected', [([1, 2, 3, 4], 4)])
def test_queue_size(pre_items, expected):
    queue = Queue()
    for item in pre_items:
        queue.enqueue(item)
    assert queue.size() == expected

@pytest.mark.parametrize('pre_items', [['x']])
def test_queue_clear(pre_items):
    queue = Queue()
    for item in pre_items:
        queue.enqueue(item)
    queue.clear()
    assert queue._items == []

@pytest.mark.parametrize('pre_items, expected', [([10, 20], 2)])
def test_queue_len(pre_items, expected):
    queue = Queue()
    for item in pre_items:
        queue.enqueue(item)
    assert len(queue) == expected

@pytest.mark.parametrize('pre_items, item, expected', [([7, 8], 8, True), ([], 5, False)])
def test_queue_contains(pre_items, item, expected):
    queue = Queue()
    for i in pre_items:
        queue.enqueue(i)
    assert (item in queue) == expected