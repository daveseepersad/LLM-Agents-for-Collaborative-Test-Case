import pytest
from data.input_code.d03_linked_list import *

# Tests for append
@pytest.mark.parametrize('case', [
    {'initial': [], 'data': 1},
    {'initial': [1], 'data': 2},
])
def test_append(case):
    ll = LinkedList()
    for v in case['initial']:
        ll.append(v)
    ll.append(case['data'])
    # No explicit assertion per plan (expected=None)

# Tests for prepend
@pytest.mark.parametrize('case', [
    {'initial': [], 'data': 3},
    {'initial': [1], 'data': 0},
])
def test_prepend(case):
    ll = LinkedList()
    for v in case['initial']:
        ll.append(v)
    ll.prepend(case['data'])
    # No explicit assertion per plan (expected=None)

# Tests for delete
@pytest.mark.parametrize('case', [
    {'initial': [], 'data': 1, 'expected': False},
    {'initial': [5], 'data': 5, 'expected': True},
    {'initial': [1, 2, 3], 'data': 2, 'expected': True},
    {'initial': [1, 2, 3], 'data': 4, 'expected': False},
])
def test_delete(case):
    ll = LinkedList()
    for v in case['initial']:
        ll.append(v)
    assert ll.delete(case['data']) == case['expected']

# Tests for find
@pytest.mark.parametrize('case', [
    {'initial': [10, 20], 'data': 10, 'expected': 0},
    {'initial': [10, 20, 30], 'data': 20, 'expected': 1},
    {'initial': [1, 2, 3], 'data': 5, 'expected': -1},
])
def test_find(case):
    ll = LinkedList()
    for v in case['initial']:
        ll.append(v)
    assert ll.find(case['data']) == case['expected']

# Tests for get
@pytest.mark.parametrize('case', [
    {'initial': [7, 8], 'index': 0, 'expected': 7},
    {'initial': [7, 8, 9], 'index': 2, 'expected': 9},
    {'initial': [1], 'index': -1, 'expected': 'IndexError'},
    {'initial': [1], 'index': 1, 'expected': 'IndexError'},
])
def test_get(case):
    ll = LinkedList()
    for v in case['initial']:
        ll.append(v)
    if case['expected'] == 'IndexError':
        with pytest.raises(IndexError):
            ll.get(case['index'])
    else:
        assert ll.get(case['index']) == case['expected']

# Test to_list
@pytest.mark.parametrize('case', [
    {'initial': [1, 2, 3], 'expected': [1, 2, 3]},
])
def test_to_list(case):
    ll = LinkedList()
    for v in case['initial']:
        ll.append(v)
    assert ll.to_list() == case['expected']

# Test __len__
@pytest.mark.parametrize('case', [
    {'initial': [1, 2, 3, 4], 'expected': 4},
])
def test_len(case):
    ll = LinkedList()
    for v in case['initial']:
        ll.append(v)
    assert len(ll) == case['expected']