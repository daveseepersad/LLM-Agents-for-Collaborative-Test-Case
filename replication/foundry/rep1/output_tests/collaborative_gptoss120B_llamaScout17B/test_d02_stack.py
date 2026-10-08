import pytest
from data.input_code.d02_stack import *

# Stack tests
@pytest.mark.parametrize('push_items, expected', [
    ([42], 42),
])
def test_stack_peek(push_items, expected):
    stack = Stack()
    for item in push_items:
        stack.push(item)
    assert stack.peek() == expected

@pytest.mark.parametrize('push_items, expected', [
    ([99], 99),
])
def test_stack_pop(push_items, expected):
    stack = Stack()
    for item in push_items:
        stack.push(item)
    assert stack.pop() == expected

@pytest.mark.parametrize('push_items, expected_exception', [
    ([], IndexError),
])
def test_stack_pop_empty(push_items, expected_exception):
    stack = Stack()
    for item in push_items:
        stack.push(item)
    with pytest.raises(expected_exception):
        stack.pop()

@pytest.mark.parametrize('push_items, expected', [
    ([], True),
    ([1], False),
])
def test_stack_is_empty(push_items, expected):
    stack = Stack()
    for item in push_items:
        stack.push(item)
    assert stack.is_empty() == expected

@pytest.mark.parametrize('push_items, expected', [
    ([1, 2, 3], 3),
])
def test_stack_size(push_items, expected):
    stack = Stack()
    for item in push_items:
        stack.push(item)
    assert stack.size() == expected

@pytest.mark.parametrize('push_items', [
    ([5, 6],),
])
def test_stack_clear(push_items):
    stack = Stack()
    for item in push_items:
        stack.push(item)
    stack.clear()
    assert stack.is_empty()

@pytest.mark.parametrize('push_items, expected', [
    ([7, 8], 2),
])
def test_stack_len(push_items, expected):
    stack = Stack()
    for item in push_items:
        stack.push(item)
    assert len(stack) == expected

@pytest.mark.parametrize('push_items, item, expected', [
    ([10, 20], 20, True),
    ([10, 20], 30, False),
])
def test_stack_contains(push_items, item, expected):
    stack = Stack()
    for i in push_items:
        stack.push(i)
    assert (item in stack) == expected

# Queue tests
@pytest.mark.parametrize('enqueue_items, expected', [
    ([55], 55),
])
def test_queue_front(enqueue_items, expected):
    queue = Queue()
    for item in enqueue_items:
        queue.enqueue(item)
    assert queue.front() == expected

@pytest.mark.parametrize('enqueue_items, expected', [
    ([77], 77),
])
def test_queue_dequeue(enqueue_items, expected):
    queue = Queue()
    for item in enqueue_items:
        queue.enqueue(item)
    assert queue.dequeue() == expected

@pytest.mark.parametrize('enqueue_items, expected_exception', [
    ([], IndexError),
])
def test_queue_dequeue_empty(enqueue_items, expected_exception):
    queue = Queue()
    for item in enqueue_items:
        queue.enqueue(item)
    with pytest.raises(expected_exception):
        queue.dequeue()

@pytest.mark.parametrize('enqueue_items, expected', [
    ([], True),
    ([1], False),
])
def test_queue_is_empty(enqueue_items, expected):
    queue = Queue()
    for item in enqueue_items:
        queue.enqueue(item)
    assert queue.is_empty() == expected

@pytest.mark.parametrize('enqueue_items, expected', [
    ([1, 2, 3, 4], 4),
])
def test_queue_size(enqueue_items, expected):
    queue = Queue()
    for item in enqueue_items:
        queue.enqueue(item)
    assert queue.size() == expected

@pytest.mark.parametrize('enqueue_items', [
    ([9, 10],),
])
def test_queue_clear(enqueue_items):
    queue = Queue()
    for item in enqueue_items:
        queue.enqueue(item)
    queue.clear()
    assert queue.is_empty()

@pytest.mark.parametrize('enqueue_items, expected', [
    ([3, 4, 5], 3),
])
def test_queue_len(enqueue_items, expected):
    queue = Queue()
    for item in enqueue_items:
        queue.enqueue(item)
    assert len(queue) == expected

@pytest.mark.parametrize('enqueue_items, item, expected', [
    ([11, 22], 22, True),
    ([11, 22], 33, False),
])
def test_queue_contains(enqueue_items, item, expected):
    queue = Queue()
    for i in enqueue_items:
        queue.enqueue(i)
    assert (item in queue) == expected

import pytest
from data.input_code.d02_stack import *

@pytest.mark.parametrize('initial_items, expected_exception', [
    ([], IndexError),
])
def test_stack_peek_empty(initial_items, expected_exception):
    stack = Stack()
    for item in initial_items:
        stack.push(item)
    with pytest.raises(expected_exception):
        stack.peek()

@pytest.mark.parametrize('push_items, expected', [
    ([1, 2, 3], {'peek': 3, 'pop_sequence': [3, 2], 'final_size': 1}),
])
def test_stack_multiple_push_pop(push_items, expected):
    stack = Stack()
    for item in push_items:
        stack.push(item)
    assert stack.peek() == expected['peek']
    for expected_pop in expected['pop_sequence']:
        assert stack.pop() == expected_pop
    assert stack.size() == expected['final_size']

@pytest.mark.parametrize('initial_items, expected_exception', [
    ([], IndexError),
])
def test_queue_front_empty(initial_items, expected_exception):
    queue = Queue()
    for item in initial_items:
        queue.enqueue(item)
    with pytest.raises(expected_exception):
        queue.front()

@pytest.mark.parametrize('enqueue_items, expected', [
    ([1, 2, 3], {'front_initial': 1, 'dequeue_sequence': [1, 2], 'final_size': 1}),
])
def test_queue_multiple_enqueue_dequeue(enqueue_items, expected):
    queue = Queue()
    for item in enqueue_items:
        queue.enqueue(item)
    assert queue.front() == expected['front_initial']
    for expected_dequeue in expected['dequeue_sequence']:
        assert queue.dequeue() == expected_dequeue
    assert queue.size() == expected['final_size']

@pytest.mark.parametrize('push_items, expected', [
    ([5, 6], 0),
])
def test_stack_len_after_clear(push_items, expected):
    stack = Stack()
    for item in push_items:
        stack.push(item)
    stack.clear()
    assert len(stack) == expected

@pytest.mark.parametrize('enqueue_items, expected', [
    ([9, 10], 0),
])
def test_queue_len_after_clear(enqueue_items, expected):
    queue = Queue()
    for item in enqueue_items:
        queue.enqueue(item)
    queue.clear()
    assert len(queue) == expected