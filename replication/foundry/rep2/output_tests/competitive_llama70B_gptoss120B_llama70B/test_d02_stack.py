import pytest
from data.input_code.d02_stack import Stack, Queue

def test_stack_init():
    stack = Stack()
    assert stack._items == []

@pytest.mark.parametrize('item, expected', [
    (1, None)
])
def test_stack_push(item, expected):
    stack = Stack()
    result = stack.push(item)
    assert result == expected
    assert stack._items == [item]

def test_stack_pop_ok():
    stack = Stack()
    stack.push(1)
    result = stack.pop()
    assert result == 1
    assert stack._items == []

def test_stack_pop_err():
    stack = Stack()
    with pytest.raises(IndexError):
        stack.pop()

def test_stack_peek_ok():
    stack = Stack()
    stack.push(1)
    result = stack.peek()
    assert result == 1
    assert stack._items == [1]

def test_stack_peek_err():
    stack = Stack()
    with pytest.raises(IndexError):
        stack.peek()

@pytest.mark.parametrize('expected', [
    (True)
])
def test_stack_is_empty_ok(expected):
    stack = Stack()
    result = stack.is_empty()
    assert result == expected

def test_stack_is_empty_err():
    stack = Stack()
    stack.push(1)
    result = stack.is_empty()
    assert result == False

@pytest.mark.parametrize('expected', [
    (0)
])
def test_stack_size_ok(expected):
    stack = Stack()
    result = stack.size()
    assert result == expected

def test_stack_size_err():
    stack = Stack()
    stack.push(1)
    result = stack.size()
    assert result == 1

def test_stack_clear():
    stack = Stack()
    stack.push(1)
    stack.clear()
    assert stack._items == []

@pytest.mark.parametrize('expected', [
    (0)
])
def test_stack_len_ok(expected):
    stack = Stack()
    result = len(stack)
    assert result == expected

def test_stack_len_err():
    stack = Stack()
    stack.push(1)
    result = len(stack)
    assert result == 1

@pytest.mark.parametrize('item, expected', [
    (1, False)
])
def test_stack_contains_ok(item, expected):
    stack = Stack()
    result = item in stack
    assert result == expected

def test_stack_contains_err():
    stack = Stack()
    stack.push(1)
    result = 1 in stack
    assert result == True

def test_queue_init():
    queue = Queue()
    assert queue._items == []

@pytest.mark.parametrize('item, expected', [
    (1, None)
])
def test_queue_enqueue(item, expected):
    queue = Queue()
    result = queue.enqueue(item)
    assert result == expected
    assert queue._items == [item]

def test_queue_dequeue_ok():
    queue = Queue()
    queue.enqueue(1)
    result = queue.dequeue()
    assert result == 1
    assert queue._items == []

def test_queue_dequeue_err():
    queue = Queue()
    with pytest.raises(IndexError):
        queue.dequeue()

def test_queue_front_ok():
    queue = Queue()
    queue.enqueue(1)
    result = queue.front()
    assert result == 1
    assert queue._items == [1]

def test_queue_front_err():
    queue = Queue()
    with pytest.raises(IndexError):
        queue.front()

@pytest.mark.parametrize('expected', [
    (True)
])
def test_queue_is_empty_ok(expected):
    queue = Queue()
    result = queue.is_empty()
    assert result == expected

def test_queue_is_empty_err():
    queue = Queue()
    queue.enqueue(1)
    result = queue.is_empty()
    assert result == False

@pytest.mark.parametrize('expected', [
    (0)
])
def test_queue_size_ok(expected):
    queue = Queue()
    result = queue.size()
    assert result == expected

def test_queue_size_err():
    queue = Queue()
    queue.enqueue(1)
    result = queue.size()
    assert result == 1

def test_queue_clear():
    queue = Queue()
    queue.enqueue(1)
    queue.clear()
    assert queue._items == []

@pytest.mark.parametrize('expected', [
    (0)
])
def test_queue_len_ok(expected):
    queue = Queue()
    result = len(queue)
    assert result == expected

def test_queue_len_err():
    queue = Queue()
    queue.enqueue(1)
    result = len(queue)
    assert result == 1

@pytest.mark.parametrize('item, expected', [
    (1, False)
])
def test_queue_contains_ok(item, expected):
    queue = Queue()
    result = item in queue
    assert result == expected

def test_queue_contains_err():
    queue = Queue()
    queue.enqueue(1)
    result = 1 in queue
    assert result == True