import pytest
from data.input_code.d03_linked_list import *

@pytest.mark.parametrize('action, expected', [
    ('len', 0),
    ('to_list', [])
])
def test_empty_actions(action, expected):
    ll = LinkedList()
    if action == 'len':
        assert len(ll) == expected
    else:
        assert ll.to_list() == expected

def test_append_on_empty():
    ll = LinkedList()
    ll.append(1)
    assert ll.head is not None and ll.head.data == 1
    assert len(ll) == 1

def test_prepend_on_empty():
    ll = LinkedList()
    ll.prepend(2)
    assert ll.head is not None and ll.head.data == 2
    assert len(ll) == 1

def test_delete_on_empty_false():
    ll = LinkedList()
    assert ll.delete(3) is False

@pytest.mark.parametrize('index', [-1, 100])
def test_get_out_of_bounds(index):
    ll = LinkedList()
    with pytest.raises(IndexError):
        ll.get(index)

def test_delete_head_true():
    ll = LinkedList()
    ll.append(1)
    assert ll.delete(1) is True
    assert len(ll) == 0
    assert ll.head is None

def test_delete_not_found_false():
    ll = LinkedList()
    assert ll.delete(999) is False

def test_find_not_found():
    ll = LinkedList()
    assert ll.find(5) == -1

def test_find_found_head():
    ll = LinkedList()
    ll.append(1)
    assert ll.find(1) == 0

def test_get_valid_head():
    ll = LinkedList()
    ll.append(1)
    assert ll.get(0) == 1

import pytest
from data.input_code.d03_linked_list import *

@pytest.mark.parametrize('initial, delete_value, expected_list, expected_len', [
    ([1, 2, 3], 3, [1, 2], 2),  # delete tail
    ([1, 2, 3], 2, [1, 3], 2),  # delete middle
])
def test_delete_tail_and_middle(initial, delete_value, expected_list, expected_len):
    ll = LinkedList()
    for v in initial:
        ll.append(v)
    result = ll.delete(delete_value)
    assert result is True
    assert len(ll) == expected_len
    assert ll.to_list() == expected_list

def test_get_middle():
    ll = LinkedList()
    ll.append(10)
    ll.append(20)
    ll.append(30)
    assert ll.get(1) == 20

def test_to_list_mix():
    ll = LinkedList()
    ll.append(2)
    ll.prepend(1)
    ll.prepend(0)
    assert ll.to_list() == [0, 1, 2]

def test_get_out_of_bounds_equal_size():
    ll = LinkedList()
    ll.append(1)
    ll.append(2)
    with pytest.raises(IndexError):
        ll.get(2)

import pytest
from data.input_code.d03_linked_list import *

@pytest.mark.parametrize('initial, data, expected_result, expected_head, expected_len, expected_list', [
    ([1, 2, 3], 1, True, 2, 2, [2, 3]),
    ([5, 6, 7], 999, False, 5, 3, [5, 6, 7]),
])
def test_delete_head_or_not_found_in_multi(initial, data, expected_result, expected_head, expected_len, expected_list):
    ll = LinkedList()
    for v in initial:
        ll.append(v)
    result = ll.delete(data)
    assert result is expected_result
    assert len(ll) == expected_len
    if ll.head is None:
        assert expected_head is None
    else:
        assert ll.head.data == expected_head
    assert ll.to_list() == expected_list

@pytest.mark.parametrize('initial, target, expected', [
    ([1, 2, 3], 2, 1),
])
def test_find_middle(initial, target, expected):
    ll = LinkedList()
    for v in initial:
        ll.append(v)
    assert ll.find(target) == expected

@pytest.mark.parametrize('initial, index, expected', [
    ([7, 8, 9], 2, 9),
])
def test_get_last_element(initial, index, expected):
    ll = LinkedList()
    for v in initial:
        ll.append(v)
    assert ll.get(index) == expected