import pytest
from data.input_code.d03_linked_list import *

def test_T1_LL_append_first():
    ll = LinkedList()
    ll.append(1)
    assert ll.to_list() == [1]
    assert len(ll) == 1

def test_T2_LL_prepend_first():
    ll = LinkedList()
    ll.prepend(1)
    assert ll.to_list() == [1]
    assert len(ll) == 1

@pytest.mark.parametrize('data', [99])
def test_T3_LL_delete_empty(data):
    ll = LinkedList()
    assert ll.delete(data) is False

def test_T4_LL_find_empty():
    ll = LinkedList()
    assert ll.find(99) == -1

def test_T5_LL_get_negative_empty():
    ll = LinkedList()
    with pytest.raises(IndexError):
        ll.get(-1)

def test_T6_LL_get_out_of_bounds_empty():
    ll = LinkedList()
    with pytest.raises(IndexError):
        ll.get(1)

def test_T7_LL_to_list_empty():
    ll = LinkedList()
    assert ll.to_list() == []

def test_T8_LL_len_empty():
    ll = LinkedList()
    assert len(ll) == 0

import pytest
from data.input_code.d03_linked_list import *

def test_T9_LL_APPEND_NON_EMPTY():
    ll = LinkedList()
    ll.append(1)
    ll.append(2)
    assert ll.to_list() == [1, 2]
    assert len(ll) == 2

def test_T10_LL_DELETE_HEAD_NON_EMPTY():
    ll = LinkedList()
    ll.append(1)
    ll.append(2)
    ll.append(3)
    result = ll.delete(1)
    assert result is True
    assert ll.to_list() == [2, 3]
    assert len(ll) == 2

def test_T11_LL_GET_IN_BOUNDS_NON_EMPTY():
    ll = LinkedList()
    ll.append(5)
    ll.append(6)
    ll.append(7)
    assert ll.get(0) == 5

import pytest
from data.input_code.d03_linked_list import *

def test_T12_LL_DELETE_TAIL_NON_EMPTY():
    ll = LinkedList()
    ll.append(1)
    ll.append(2)
    ll.append(3)
    result = ll.delete(3)
    assert result is True
    assert ll.to_list() == [1, 2]
    assert len(ll) == 2

def test_T13_LL_DELETE_NOT_FOUND_NON_EMPTY():
    ll = LinkedList()
    ll.append(1)
    ll.append(2)
    result = ll.delete(99)
    assert result is False

def test_T14_LL_FIND_MIDDLE():
    ll = LinkedList()
    ll.append(10)
    ll.append(20)
    ll.append(30)
    assert ll.find(20) == 1

def test_T15_LL_GET_MIDDLE():
    ll = LinkedList()
    ll.append(5)
    ll.append(6)
    ll.append(7)
    assert ll.get(1) == 6

def test_T16_LL_GET_NEGATIVE_NON_EMPTY():
    ll = LinkedList()
    ll.append(1)
    ll.append(2)
    with pytest.raises(IndexError):
        ll.get(-1)

def test_T17_LL_GET_OUT_OF_BOUNDS_NON_EMPTY():
    ll = LinkedList()
    ll.append(1)
    ll.append(2)
    with pytest.raises(IndexError):
        ll.get(2)