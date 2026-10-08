import pytest
from data.input_code.d02_stack import *

STACK_CASES = [
    {"id": "T1(Stack)_init", "target": "Stack.__init__", "input": {}, "expected": None, "setup": None},
    {"id": "T2(Stack)_push", "target": "Stack.push", "input": {"item": 1}, "expected": None, "setup": None},
    {"id": "T3(Stack)_pop", "target": "Stack.pop", "input": {}, "expected": 1, "setup": "Stack.push(1)"},
    {"id": "T4(Stack)_pop_err", "target": "Stack.pop", "input": {}, "expected": "IndexError", "setup": None},
    {"id": "T5(Stack)_peek", "target": "Stack.peek", "input": {}, "expected": 1, "setup": "Stack.push(1)"},
    {"id": "T6(Stack)_peek_err", "target": "Stack.peek", "input": {}, "expected": "IndexError", "setup": None},
    {"id": "T7(Stack)_is_empty", "target": "Stack.is_empty", "input": {}, "expected": True, "setup": None},
    {"id": "T8(Stack)_is_empty_false", "target": "Stack.is_empty", "input": {}, "expected": False, "setup": "Stack.push(1)"},
    {"id": "T9(Stack)_size", "target": "Stack.size", "input": {}, "expected": 0, "setup": None},
    {"id": "T10(Stack)_size_non_empty", "target": "Stack.size", "input": {}, "expected": 1, "setup": "Stack.push(1)"},
    {"id": "T11(Stack)_clear", "target": "Stack.clear", "input": {}, "expected": None, "setup": "Stack.push(1)"},
    {"id": "T12(Stack)_len", "target": "Stack.__len__", "input": {}, "expected": 0, "setup": None},
    {"id": "T13(Stack)_len_non_empty", "target": "Stack.__len__", "input": {}, "expected": 1, "setup": "Stack.push(1)"},
    {"id": "T14(Stack)_contains", "target": "Stack.__contains__", "input": {"item": 1}, "expected": False, "setup": None},
    {"id": "T15(Stack)_contains_true", "target": "Stack.__contains__", "input": {"item": 1}, "expected": True, "setup": "Stack.push(1)"},
]

QUEUE_CASES = [
    {"id": "T16(Queue)_init", "target": "Queue.__init__", "input": {}, "expected": None, "setup": None},
    {"id": "T17(Queue)_enqueue", "target": "Queue.enqueue", "input": {"item": 1}, "expected": None, "setup": None},
    {"id": "T18(Queue)_dequeue", "target": "Queue.dequeue", "input": {}, "expected": 1, "setup": "Queue.enqueue(1)"},
    {"id": "T19(Queue)_dequeue_err", "target": "Queue.dequeue", "input": {}, "expected": "IndexError", "setup": None},
    {"id": "T20(Queue)_front", "target": "Queue.front", "input": {}, "expected": 1, "setup": "Queue.enqueue(1)"},
    {"id": "T21(Queue)_front_err", "target": "Queue.front", "input": {}, "expected": "IndexError", "setup": None},
    {"id": "T22(Queue)_is_empty", "target": "Queue.is_empty", "input": {}, "expected": True, "setup": None},
    {"id": "T23(Queue)_is_empty_false", "target": "Queue.is_empty", "input": {}, "expected": False, "setup": "Queue.enqueue(1)"},
    {"id": "T24(Queue)_size", "target": "Queue.size", "input": {}, "expected": 0, "setup": None},
    {"id": "T25(Queue)_size_non_empty", "target": "Queue.size", "input": {}, "expected": 1, "setup": "Queue.enqueue(1)"},
    {"id": "T26(Queue)_clear", "target": "Queue.clear", "input": {}, "expected": None, "setup": "Queue.enqueue(1)"},
    {"id": "T27(Queue)_len", "target": "Queue.__len__", "input": {}, "expected": 0, "setup": None},
    {"id": "T28(Queue)_len_non_empty", "target": "Queue.__len__", "input": {}, "expected": 1, "setup": "Queue.enqueue(1)"},
    {"id": "T29(Queue)_contains", "target": "Queue.__contains__", "input": {"item": 1}, "expected": False, "setup": None},
    {"id": "T30(Queue)_contains_true", "target": "Queue.__contains__", "input": {"item": 1}, "expected": True, "setup": "Queue.enqueue(1)"},
]

@pytest.mark.parametrize("case", STACK_CASES)
def test_stack_plan(case):
    s = Stack()
    setup = case.get("setup")
    if setup == "Stack.push(1)":
        s.push(1)
    target = case["target"]
    expected = case.get("expected")

    if target == "Stack.__init__":
        assert isinstance(s, Stack)
        assert len(s) == 0
        return

    if target == "Stack.push":
        s.push(case["input"]["item"])
        assert (case["input"]["item"] in s)
        assert len(s) == 1
        return

    if target == "Stack.pop":
        if expected == "IndexError":
            with pytest.raises(IndexError):
                s.pop()
        else:
            res = s.pop()
            assert res == expected
        return

    if target == "Stack.peek":
        if expected == "IndexError":
            with pytest.raises(IndexError):
                s.peek()
        else:
            res = s.peek()
            assert res == expected
        return

    if target == "Stack.is_empty":
        assert s.is_empty() == expected
        return

    if target == "Stack.size":
        assert s.size() == expected
        return

    if target == "Stack.clear":
        s.clear()
        assert len(s) == 0
        return

    if target == "Stack.__len__":
        assert len(s) == expected
        return

    if target == "Stack.__contains__":
        item = case["input"]["item"]
        assert (item in s) == expected
        return

    pytest.fail("Unknown stack target")

@pytest.mark.parametrize("case", QUEUE_CASES)
def test_queue_plan(case):
    q = Queue()
    setup = case.get("setup")
    if setup == "Queue.enqueue(1)":
        q.enqueue(1)
    target = case["target"]
    expected = case.get("expected")

    if target == "Queue.__init__":
        assert isinstance(q, Queue)
        assert len(q) == 0
        return

    if target == "Queue.enqueue":
        q.enqueue(case["input"]["item"])
        assert (case["input"]["item"] in q)
        assert len(q) == 1
        return

    if target == "Queue.dequeue":
        if expected == "IndexError":
            with pytest.raises(IndexError):
                q.dequeue()
        else:
            res = q.dequeue()
            assert res == expected
        return

    if target == "Queue.front":
        if expected == "IndexError":
            with pytest.raises(IndexError):
                q.front()
        else:
            res = q.front()
            assert res == expected
        return

    if target == "Queue.is_empty":
        assert q.is_empty() == expected
        return

    if target == "Queue.size":
        assert q.size() == expected
        return

    if target == "Queue.clear":
        q.clear()
        assert len(q) == 0
        return

    if target == "Queue.__len__":
        assert len(q) == expected
        return

    if target == "Queue.__contains__":
        item = case["input"]["item"]
        assert (item in q) == expected
        return

    pytest.fail("Unknown queue target")