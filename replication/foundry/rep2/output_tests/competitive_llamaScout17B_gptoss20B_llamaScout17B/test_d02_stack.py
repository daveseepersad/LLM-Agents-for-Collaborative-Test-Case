import pytest
from data.input_code.d02_stack import *

class TestStack:
    def test_S1_INIT(self):
        s = Stack()
        assert s.size() == 0
        assert s._items == []

    def test_S2_PUSH(self):
        s = Stack()
        s.push(5)
        assert s._items == [5]
        assert s.size() == 1

    def test_S3_POP_OK(self):
        s = Stack()
        s.push(5)
        result = s.pop()
        assert result == 5
        assert s._items == []

    def test_S4_POP_ERR(self):
        s = Stack()
        with pytest.raises(IndexError):
            s.pop()

    def test_S5_PEEK_OK(self):
        s = Stack()
        s.push(5)
        assert s.peek() == 5

    def test_S6_PEEK_ERR(self):
        s = Stack()
        with pytest.raises(IndexError):
            s.peek()

    def test_S7_IS_EMPTY_TRUE(self):
        s = Stack()
        assert s.is_empty() is True

    def test_S8_IS_EMPTY_FALSE(self):
        s = Stack()
        s.push(5)
        assert s.is_empty() is False

    def test_S9_SIZE(self):
        s = Stack()
        s.push(5)
        assert s.size() == 1

    def test_S10_CLEAR(self):
        s = Stack()
        s.push(5)
        s.clear()
        assert s.size() == 0
        assert s._items == []

    def test_S11_LEN(self):
        s = Stack()
        assert len(s) == 0

    @pytest.mark.parametrize("item", [5])
    def test_S12_CONTAINS_TRUE(self, item):
        s = Stack()
        s.push(5)
        assert (item in s) is True

    @pytest.mark.parametrize("item", [10])
    def test_S13_CONTAINS_FALSE(self, item):
        s = Stack()
        s.push(5)
        assert (item in s) is False

class TestQueue:
    def test_Q1_INIT(self):
        q = Queue()
        assert q.size() == 0
        assert q._items == []

    def test_Q2_ENQUEUE(self):
        q = Queue()
        q.enqueue(5)
        assert q._items == [5]
        assert q.size() == 1

    def test_Q3_DEQUEUE_OK(self):
        q = Queue()
        q.enqueue(5)
        result = q.dequeue()
        assert result == 5
        assert q._items == []

    def test_Q4_DEQUEUE_ERR(self):
        q = Queue()
        with pytest.raises(IndexError):
            q.dequeue()

    def test_Q5_FRONT_OK(self):
        q = Queue()
        q.enqueue(5)
        assert q.front() == 5

    def test_Q6_FRONT_ERR(self):
        q = Queue()
        with pytest.raises(IndexError):
            q.front()

    def test_Q7_IS_EMPTY_TRUE(self):
        q = Queue()
        assert q.is_empty() is True

    def test_Q8_IS_EMPTY_FALSE(self):
        q = Queue()
        q.enqueue(5)
        assert q.is_empty() is False

    def test_Q9_SIZE(self):
        q = Queue()
        q.enqueue(5)
        assert q.size() == 1

    def test_Q10_CLEAR(self):
        q = Queue()
        q.enqueue(5)
        q.clear()
        assert q.size() == 0
        assert q._items == []

    def test_Q11_LEN(self):
        q = Queue()
        assert len(q) == 0

    def test_Q12_CONTAINS_TRUE(self):
        q = Queue()
        q.enqueue(5)
        assert (5 in q) is True

    def test_Q13_CONTAINS_FALSE(self):
        q = Queue()
        q.enqueue(5)
        assert (10 in q) is False