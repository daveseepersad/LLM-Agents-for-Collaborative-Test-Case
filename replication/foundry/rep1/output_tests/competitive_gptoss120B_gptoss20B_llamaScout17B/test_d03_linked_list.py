import pytest
from data.input_code.d03_linked_list import *

@pytest.mark.parametrize("initial, data, expected", [
    ([], 42, [42]),
    ([1], 2, [1, 2]),
])
def test_append(initial, data, expected):
    ll = LinkedList()
    for v in initial:
        ll.append(v)
    ll.append(data)
    assert ll.to_list() == expected

@pytest.mark.parametrize("initial, data, expected", [
    ([], 99, [99]),
])
def test_prepend(initial, data, expected):
    ll = LinkedList()
    for v in initial:
        ll.append(v)
    ll.prepend(data)
    assert ll.to_list() == expected

@pytest.mark.parametrize("initial, data, expected_res, expected_list", [
    ([], 5, False, []),
    ([10, 20, 30], 10, True, [20, 30]),
    ([10, 20, 30], 20, True, [10, 30]),
    ([1, 2], 99, False, [1, 2]),
])
def test_delete(initial, data, expected_res, expected_list):
    ll = LinkedList()
    for v in initial:
        ll.append(v)
    res = ll.delete(data)
    assert res == expected_res
    assert ll.to_list() == expected_list

@pytest.mark.parametrize("initial, data, expected_index", [
    ([5, 6, 7], 6, 1),
    ([5, 6, 7], 9, -1),
    ([], 1, -1),
])
def test_find(initial, data, expected_index):
    ll = LinkedList()
    for v in initial:
        ll.append(v)
    assert ll.find(data) == expected_index

@pytest.mark.parametrize("initial, index, expected", [
    ([100, 200, 300], 2, 300),
])
def test_get_success(initial, index, expected):
    ll = LinkedList()
    for v in initial:
        ll.append(v)
    assert ll.get(index) == expected

@pytest.mark.parametrize("initial, index", [
    ([1, 2], -1),
    ([1, 2], 2),
])
def test_get_index_error(initial, index):
    ll = LinkedList()
    for v in initial:
        ll.append(v)
    with pytest.raises(IndexError):
        ll.get(index)

@pytest.mark.parametrize("initial, expected", [
    ([], []),
    ([8, 9, 10], [8, 9, 10]),
])
def test_to_list(initial, expected):
    ll = LinkedList()
    for v in initial:
        ll.append(v)
    assert ll.to_list() == expected

@pytest.mark.parametrize("initial, expected_len", [
    ([1, 2, 3, 4], 4),
])
def test_len(initial, expected_len):
    ll = LinkedList()
    for v in initial:
        ll.append(v)
    assert len(ll) == expected_len