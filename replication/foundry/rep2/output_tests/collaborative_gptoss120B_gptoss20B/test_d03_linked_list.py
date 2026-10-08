import pytest
from data.input_code.d03_linked_list import *

@pytest.mark.parametrize('data,expected', [
    (1, [1]),
])
def test_append_on_empty(data, expected):
    ll = LinkedList()
    ll.append(data)
    assert ll.to_list() == expected

def test_to_list_on_empty():
    ll = LinkedList()
    assert ll.to_list() == []

@pytest.mark.parametrize('data,expected', [
    (5, [5]),
])
def test_prepend_on_empty(data, expected):
    ll = LinkedList()
    ll.prepend(data)
    assert ll.to_list() == expected

def test_delete_on_empty():
    ll = LinkedList()
    assert ll.delete("x") is False

def test_find_on_empty():
    ll = LinkedList()
    assert ll.find(10) == -1

@pytest.mark.parametrize('index,exception', [
    (-1, IndexError),
    (1, IndexError),
])
def test_get_raises_index_error(index, exception):
    ll = LinkedList()  # empty list, size = 0
    with pytest.raises(exception):
        ll.get(index)

def test_len_on_empty():
    ll = LinkedList()
    assert len(ll) == 0

import pytest
from data.input_code.d03_linked_list import *

def test_append_on_non_empty():
    ll = LinkedList()
    ll.append(1)          # initial element
    ll.append(2)          # append the test input
    assert ll.to_list() == [1, 2]

def test_delete_head_non_empty():
    ll = LinkedList()
    ll.append(1)
    ll.append(2)
    ll.append(3)
    result = ll.delete(1)
    assert result is True
    assert ll.to_list() == [2, 3]

def test_delete_middle_non_empty():
    ll = LinkedList()
    ll.append(1)
    ll.append(2)
    ll.append(3)
    result = ll.delete(3)   # deleting tail (as per plan)
    assert result is True
    assert ll.to_list() == [1, 2]

def test_delete_not_found_non_empty():
    ll = LinkedList()
    ll.append(1)
    ll.append(2)
    ll.append(3)
    result = ll.delete(999)
    assert result is False
    assert ll.to_list() == [1, 2, 3]

def test_find_non_empty():
    ll = LinkedList()
    ll.append(1)
    ll.append(2)
    ll.append(3)
    index = ll.find(2)
    assert index == 1

def test_get_0_on_non_empty():
    ll = LinkedList()
    ll.append(1)
    ll.append(2)
    ll.append(3)
    value = ll.get(0)
    assert value == 1

def test_get_out_of_range_non_empty():
    ll = LinkedList()
    ll.append(1)
    ll.append(2)
    ll.append(3)
    with pytest.raises(IndexError):
        ll.get(5)

import pytest
from data.input_code.d03_linked_list import *

def test_delete_middle_non_head():
    ll = LinkedList()
    ll.append(1)
    ll.append(2)
    ll.append(3)
    result = ll.delete(2)
    assert result is True
    assert ll.to_list() == [1, 3]

@pytest.mark.parametrize('setup,data,expected', [
    (["append 5", "append 6", "append 7"], 5, 0),
    (["append 1", "append 2", "append 3"], 99, -1),
])
def test_find_various(setup, data, expected):
    ll = LinkedList()
    for action in setup:
        cmd, val = action.split()
        if cmd == "append":
            ll.append(int(val))
        elif cmd == "prepend":
            ll.prepend(int(val))
    assert ll.find(data) == expected

@pytest.mark.parametrize('setup,index,expected', [
    (["append 1", "append 2", "append 3"], 2, 3),
    (["append 1", "append 2", "append 3"], -1, IndexError),
])
def test_get_various(setup, index, expected):
    ll = LinkedList()
    for action in setup:
        cmd, val = action.split()
        if cmd == "append":
            ll.append(int(val))
        elif cmd == "prepend":
            ll.prepend(int(val))
    if isinstance(expected, type) and issubclass(expected, Exception):
        with pytest.raises(expected):
            ll.get(index)
    else:
        assert ll.get(index) == expected

def test_len_after_operations():
    ll = LinkedList()
    ll.append(1)
    ll.append(2)
    ll.prepend(0)
    ll.delete(1)
    assert len(ll) == 2