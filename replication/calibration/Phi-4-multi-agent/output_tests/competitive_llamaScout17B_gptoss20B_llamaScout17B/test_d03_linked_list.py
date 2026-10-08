import pytest
from data.input_code.d03_linked_list import *

def test_T1_append_empty():
    ll = LinkedList()
    result = ll.append(10)
    assert result == None
    assert ll.to_list() == [10]

def test_T2_append_non_empty():
    ll = LinkedList()
    ll.append(10)
    result = ll.append(20)
    assert result == None
    assert ll.to_list() == [10, 20]

def test_T3_prepend_empty():
    ll = LinkedList()
    result = ll.prepend(5)
    assert result == None
    assert ll.to_list() == [5]

def test_T4_prepend_non_empty():
    ll = LinkedList()
    ll.prepend(5)
    result = ll.prepend(15)
    assert result == None
    assert ll.to_list() == [15, 5]

def test_T5_delete_empty():
    ll = LinkedList()
    result = ll.delete(10)
    assert result == False
    assert ll.to_list() == []

def test_T6_delete_head():
    ll = LinkedList()
    ll.append(15)
    result = ll.delete(15)
    assert result == True
    assert ll.to_list() == []

def test_T7_delete_mid():
    ll = LinkedList()
    ll.append(15)
    ll.append(20)
    ll.append(30)
    result = ll.delete(20)
    assert result == True
    assert ll.to_list() == [15, 30]

def test_T8_delete_not_found():
    ll = LinkedList()
    ll.append(15)
    ll.append(20)
    result = ll.delete(99)
    assert result == False
    assert ll.to_list() == [15, 20]

def test_T9_find_empty():
    ll = LinkedList()
    idx = ll.find(10)
    assert idx == -1

def test_T10_find_existing():
    ll = LinkedList()
    ll.append(10)
    ll.append(20)
    idx = ll.find(20)
    assert idx == 1

def test_T11_find_not_found():
    ll = LinkedList()
    ll.append(10)
    ll.append(20)
    idx = ll.find(99)
    assert idx == -1

def test_T12_get_empty():
    ll = LinkedList()
    with pytest.raises(IndexError):
        ll.get(0)

def test_T13_get_valid_index():
    ll = LinkedList()
    ll.append(10)
    ll.append(20)
    val = ll.get(1)
    assert val == 20

def test_T14_get_negative_index():
    ll = LinkedList()
    with pytest.raises(IndexError):
        ll.get(-1)

def test_T15_get_out_of_range_index():
    ll = LinkedList()
    ll.append(10)
    ll.append(20)
    with pytest.raises(IndexError):
        ll.get(5)

def test_T16_to_list_empty():
    ll = LinkedList()
    assert ll.to_list() == []

def test_T17_to_list_non_empty():
    ll = LinkedList()
    ll.append(15)
    ll.append(20)
    assert ll.to_list() == [15, 20]

def test_T_MISSING_DELETE_LAST():
    ll = LinkedList()
    ll.append(10)
    ll.append(20)
    result = ll.delete(20)
    assert result == True
    assert ll.to_list() == [10]

def test_T_MISSING_GET_HEAD():
    ll = LinkedList()
    ll.append(10)
    ll.append(20)
    val = ll.get(0)
    assert val == 10

def test_T_MISSING_FIND_HEAD():
    ll = LinkedList()
    ll.append(10)
    ll.append(20)
    idx = ll.find(10)
    assert idx == 0

def test_T_MISSING_LENGTH():
    ll = LinkedList()
    ll.append(1)
    ll.append(2)
    assert len(ll) == 2