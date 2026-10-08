import pytest
from data.input_code.d02_stack import Stack, Queue

@pytest.mark.parametrize('instance_method, instance_method_args, expected', [
    (None, None, True),
    ('push', [1], False)
])
def test_stack_is_empty(instance_method, instance_method_args, expected):
    stack = Stack()
    if instance_method:
        method = getattr(stack, instance_method)
        method(*instance_method_args)
    assert stack.is_empty() == expected

@pytest.mark.parametrize('instance_method, instance_method_args, expected', [
    (None, None, 0),
    ('push', [1], 1)
])
def test_stack_size(instance_method, instance_method_args, expected):
    stack = Stack()
    if instance_method:
        method = getattr(stack, instance_method)
        method(*instance_method_args)
    assert stack.size() == expected

def test_stack_push():
    stack = Stack()
    stack.push(1)
    assert 1 in stack

def test_stack_pop():
    stack = Stack()
    stack.push(1)
    assert stack.pop() == 1

def test_stack_pop_error():
    stack = Stack()
    with pytest.raises(IndexError):
        stack.pop()

def test_stack_peek():
    stack = Stack()
    stack.push(1)
    assert stack.peek() == 1

def test_stack_peek_error():
    stack = Stack()
    with pytest.raises(IndexError):
        stack.peek()

def test_stack_clear():
    stack = Stack()
    stack.push(1)
    stack.clear()
    assert stack.is_empty()

def test_stack_contains():
    stack = Stack()
    stack.push(1)
    assert 1 in stack

def test_stack_contains_false():
    stack = Stack()
    stack.push(1)
    assert 2 not in stack

@pytest.mark.parametrize('instance_method, instance_method_args, expected', [
    (None, None, True),
    ('enqueue', [1], False)
])
def test_queue_is_empty(instance_method, instance_method_args, expected):
    queue = Queue()
    if instance_method:
        method = getattr(queue, instance_method)
        method(*instance_method_args)
    assert queue.is_empty() == expected

@pytest.mark.parametrize('instance_method, instance_method_args, expected', [
    (None, None, 0),
    ('enqueue', [1], 1)
])
def test_queue_size(instance_method, instance_method_args, expected):
    queue = Queue()
    if instance_method:
        method = getattr(queue, instance_method)
        method(*instance_method_args)
    assert queue.size() == expected

def test_queue_enqueue():
    queue = Queue()
    queue.enqueue(1)
    assert 1 in queue

def test_queue_dequeue():
    queue = Queue()
    queue.enqueue(1)
    assert queue.dequeue() == 1

def test_queue_dequeue_error():
    queue = Queue()
    with pytest.raises(IndexError):
        queue.dequeue()

def test_queue_front():
    queue = Queue()
    queue.enqueue(1)
    assert queue.front() == 1

def test_queue_front_error():
    queue = Queue()
    with pytest.raises(IndexError):
        queue.front()

def test_queue_clear():
    queue = Queue()
    queue.enqueue(1)
    queue.clear()
    assert queue.is_empty()

def test_queue_contains():
    queue = Queue()
    queue.enqueue(1)
    assert 1 in queue

def test_queue_contains_false():
    queue = Queue()
    queue.enqueue(1)
    assert 2 not in queue

def test_stack_len():
    stack = Stack()
    assert len(stack) == 0

def test_queue_len():
    queue = Queue()
    assert len(queue) == 0

def test_stack_pop_after_clear():
    stack = Stack()
    stack.push(1)
    stack.clear()
    with pytest.raises(IndexError):
        stack.pop()

def test_queue_dequeue_after_clear():
    queue = Queue()
    queue.enqueue(1)
    queue.clear()
    with pytest.raises(IndexError):
        queue.dequeue()

def test_stack_peek_after_clear():
    stack = Stack()
    stack.push(1)
    stack.clear()
    with pytest.raises(IndexError):
        stack.peek()

def test_queue_front_after_clear():
    queue = Queue()
    queue.enqueue(1)
    queue.clear()
    with pytest.raises(IndexError):
        queue.front()

def test_stack_clear_twice():
    stack = Stack()
    stack.push(1)
    stack.clear()
    stack.clear()
    assert stack.is_empty()

def test_queue_clear_twice():
    queue = Queue()
    queue.enqueue(1)
    queue.clear()
    queue.clear()
    assert queue.is_empty()