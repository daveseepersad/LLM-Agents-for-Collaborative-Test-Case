import pytest
from data.input_code.d03_linked_list import *

# Tests for append
@pytest.mark.parametrize('initial, data, expected', [
    ([], 1, [1]),      # T1_APPEND_EMPTY
    ([1], 2, [1, 2]),  # T2_APPEND_NONEMPTY
])
def test_append(initial, data, expected):
    ll = LinkedList()
    for v in initial:
        ll.append(v)
    ll.append(data)
    assert ll.to_list() == expected

# Tests for prepend
@pytest.mark.parametrize('initial, data, expected', [
    ([], 10, [10]),      # T3_PREPEND_EMPTY
    ([5], 20, [20, 5]),  # T4_PREPEND_NONEMPTY
])
def test_prepend(initial, data, expected):
    ll = LinkedList()
    for v in initial:
        ll.append(v)
    ll.prepend(data)
    assert ll.to_list() == expected

# Tests for delete
@pytest.mark.parametrize('initial, data, expected', [
    ([], 99, False),        # T5_DELETE_EMPTY
    ([1, 2, 3], 1, True),    # T6_DELETE_HEAD
    ([1, 2, 3], 2, True),    # T7_DELETE_MIDDLE
    ([1, 2, 3], 3, True),    # T8_DELETE_TAIL
    ([1, 2, 3], 42, False),  # T9_DELETE_NOT_FOUND
])
def test_delete(initial, data, expected):
    ll = LinkedList()
    for v in initial:
        ll.append(v)
    result = ll.delete(data)
    assert result == expected

    # After deletes, ensure list state matches expectation if relevant
    if initial or data == 99:
        # We compare only when expectations about the resulting list can be inferred
        if not initial and data == 99:
            assert ll.to_list() == []
        elif data == 1:
            assert ll.to_list() == [2, 3]
        elif data == 2:
            assert ll.to_list() == [1, 3]
        elif data == 3:
            assert ll.to_list() == [1, 2]
        elif data == 42:
            assert ll.to_list() == [1, 2, 3]

# Tests for find
@pytest.mark.parametrize('initial, data, expected', [
    ([], 5, -1),          # T10_FIND_EMPTY
    ([10, 20, 30], 10, 0), # T11_FIND_HEAD
    ([10, 20, 30], 20, 1), # T12_FIND_MIDDLE
    ([10, 20, 30], 999, -1), # T13_FIND_NOT_FOUND
])
def test_find(initial, data, expected):
    ll = LinkedList()
    for v in initial:
        ll.append(v)
    assert ll.find(data) == expected

# Tests for get
@pytest.mark.parametrize('initial, index, expected', [
    ([10, 20, 30], 0, 10),        # T14_GET_FIRST
    ([10, 20, 30], 2, 30),        # T15_GET_LAST
    ([10, 20, 30], -1, 'IndexError'), # T16_GET_NEGATIVE
    ([10, 20, 30], 3, 'IndexError'),  # T17_GET_OUT_OF_RANGE
])
def test_get(initial, index, expected):
    ll = LinkedList()
    for v in initial:
        ll.append(v)
    if isinstance(expected, str) and expected == 'IndexError':
        with pytest.raises(IndexError):
            ll.get(index)
    else:
        assert ll.get(index) == expected

# Tests for len
def test_len():
    ll = LinkedList()
    ll.append(10)
    ll.append(20)
    ll.append(30)
    assert len(ll) == 3