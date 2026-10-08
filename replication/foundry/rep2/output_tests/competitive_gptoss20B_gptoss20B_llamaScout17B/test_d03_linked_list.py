import pytest
from data.input_code.d03_linked_list import *

@pytest.mark.parametrize('initial, data, expected', [
    ([], 10, [10]),
    ([10], 20, [10, 20]),
])
def test_append(initial, data, expected):
    ll = LinkedList()
    for v in initial:
        ll.append(v)
    ll.append(data)
    assert ll.to_list() == expected
    assert len(ll) == len(expected)

@pytest.mark.parametrize('initial, data, expected', [
    ([], 5, [5]),
    ([10], 5, [5, 10]),
])
def test_prepend(initial, data, expected):
    ll = LinkedList()
    for v in initial:
        ll.append(v)
    ll.prepend(data)
    assert ll.to_list() == expected
    assert len(ll) == len(expected)

def test_len_empty():
    ll = LinkedList()
    assert len(ll) == 0

def test_to_list_empty():
    ll = LinkedList()
    assert ll.to_list() == []

def test_delete_empty_false():
    ll = LinkedList()
    assert ll.delete(1) is False

def test_delete_head_true():
    ll = LinkedList()
    ll.append(10)
    assert ll.delete(10) is True
    assert ll.to_list() == []
    assert len(ll) == 0

def test_delete_middle_true():
    ll = LinkedList()
    ll.append(10)
    ll.append(20)
    ll.append(30)
    assert ll.delete(20) is True
    assert ll.to_list() == [10, 30]
    assert len(ll) == 2

def test_delete_not_found_false():
    ll = LinkedList()
    ll.append(10)
    ll.append(20)
    ll.append(30)
    assert ll.delete(99) is False
    assert ll.to_list() == [10, 20, 30]
    assert len(ll) == 3

def test_find_present():
    ll = LinkedList()
    ll.append(5)
    ll.append(10)
    ll.append(15)
    assert ll.find(5) == 0

def test_find_absent():
    ll = LinkedList()
    ll.append(5)
    ll.append(10)
    ll.append(15)
    assert ll.find(999) == -1

@pytest.mark.parametrize('index', [-1, 1000])
def test_get_out_of_range(index):
    ll = LinkedList()
    with pytest.raises(IndexError):
        ll.get(index)

import pytest  # noqa: F401

@pytest.mark.parametrize('initial, index, expected', [
    ([1, 2, 3], 0, 1),
    ([1, 2, 3], 2, 3),
])
def test_get_valid_first_and_last(initial, index, expected):
    ll = LinkedList()
    for v in initial:
        ll.append(v)
    assert ll.get(index) == expected

def test_get_out_of_range_size():
    ll = LinkedList()
    ll.append(7)
    ll.append(8)
    with pytest.raises(IndexError):
        ll.get(2)

def test_delete_tail_true():
    ll = LinkedList()
    ll.append(10)
    ll.append(20)
    ll.append(30)
    assert ll.delete(30) is True
    assert ll.to_list() == [10, 20]
    assert len(ll) == 2

@pytest.mark.parametrize('initial, data, expected', [
    ([5, 10, 15], 10, 1),
])
def test_find_middle(initial, data, expected):
    ll = LinkedList()
    for v in initial:
        ll.append(v)
    assert ll.find(data) == expected