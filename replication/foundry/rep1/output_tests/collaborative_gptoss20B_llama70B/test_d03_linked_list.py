import pytest
from data.input_code.d03_linked_list import *

@pytest.mark.parametrize('data', [
    (1),
    (2)
])
def test_ll_append_and_prepend(data):
    ll = LinkedList()
    ll.append(data)
    assert ll.head.data == data
    ll.prepend(data + 1)
    assert ll.head.data == data + 1

def test_ll_delete_empty():
    ll = LinkedList()
    assert ll.delete(3) == False

def test_ll_find_empty():
    ll = LinkedList()
    assert ll.find(4) == -1

def test_ll_get_empty_oor():
    ll = LinkedList()
    with pytest.raises(IndexError):
        ll.get(0)

def test_ll_to_list_empty():
    ll = LinkedList()
    assert ll.to_list() == []

def test_ll_len_empty():
    ll = LinkedList()
    assert len(ll) == 0

def test_ll_get_negative_oor():
    ll = LinkedList()
    ll.append(1)
    with pytest.raises(IndexError):
        ll.get(-1)

@pytest.mark.parametrize('initial, delete, expected', [
    ([1, 2], 1, True),
    ([1, 2, 3], 2, True),
    ([1, 2], 2, True),
    ([1, 2], 3, False)
])
def test_ll_delete(initial, delete, expected):
    ll = LinkedList()
    for data in initial:
        ll.append(data)
    assert ll.delete(delete) == expected

def test_ll_get_upper_oor():
    ll = LinkedList()
    ll.append(1)
    ll.append(2)
    with pytest.raises(IndexError):
        ll.get(2)

def test_ll_find_exist():
    ll = LinkedList()
    ll.append(5)
    ll.append(10)
    ll.append(15)
    assert ll.find(10) == 1

def test_ll_to_list_nonempty():
    ll = LinkedList()
    ll.append(7)
    ll.append(8)
    ll.append(9)
    assert ll.to_list() == [7, 8, 9]

@pytest.mark.parametrize('initial, data, expected', [
    ([5, 6], 7, -1)
])
def test_ll_find_not_found_nonempty(initial, data, expected):
    ll = LinkedList()
    for value in initial:
        ll.append(value)
    assert ll.find(data) == expected

@pytest.mark.parametrize('initial, index, expected', [
    ([11, 22, 33], 2, 33),
    ([11, 22, 33], 1, 22)
])
def test_ll_get_valid_index_nonempty(initial, index, expected):
    ll = LinkedList()
    for value in initial:
        ll.append(value)
    assert ll.get(index) == expected

def test_ll_delete_single_element():
    ll = LinkedList()
    ll.append(42)
    assert ll.delete(42) == True
    assert len(ll) == 0