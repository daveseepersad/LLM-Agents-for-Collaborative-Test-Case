import pytest
from data.input_code.d03_linked_list import *

def test_T1_append_empty():
    ll = LinkedList()
    ll.append(10)
    assert ll.to_list() == [10]
    assert len(ll) == 1

def test_T2_append_nonempty():
    ll = LinkedList()
    ll.append(1)
    ll.append(2)
    assert ll.to_list() == [1, 2]
    assert len(ll) == 2

def test_T3_prepend_empty():
    ll = LinkedList()
    ll.prepend(5)
    assert ll.to_list() == [5]
    assert len(ll) == 1

def test_T4_prepend_nonempty():
    ll = LinkedList()
    ll.append(7)
    ll.prepend(3)
    assert ll.to_list() == [3, 7]
    assert len(ll) == 2

def test_T5_delete_empty():
    ll = LinkedList()
    res = ll.delete(99)
    assert res is False
    assert ll.to_list() == []
    assert len(ll) == 0

def test_T6_delete_head():
    ll = LinkedList()
    ll.append(4)
    ll.append(8)
    res = ll.delete(4)
    assert res is True
    assert ll.to_list() == [8]
    assert len(ll) == 1

def test_T7_delete_middle():
    ll = LinkedList()
    for v in [1, 2, 3]:
        ll.append(v)
    res = ll.delete(2)
    assert res is True
    assert ll.to_list() == [1, 3]
    assert len(ll) == 2

def test_T8_delete_notfound():
    ll = LinkedList()
    ll.append(5)
    ll.append(6)
    res = ll.delete(10)
    assert res is False
    assert ll.to_list() == [5, 6]
    assert len(ll) == 2

def test_T9_find_empty():
    ll = LinkedList()
    idx = ll.find(1)
    assert idx == -1

def test_T10_find_head():
    ll = LinkedList()
    ll.append(9)
    ll.append(4)
    ll.append(7)
    assert ll.find(9) == 0

def test_T11_find_tail():
    ll = LinkedList()
    for v in [2, 3, 5]:
        ll.append(v)
    assert ll.find(5) == 2

def test_T12_get_first():
    ll = LinkedList()
    for v in [11, 22]:
        ll.append(v)
    assert ll.get(0) == 11

def test_T13_get_last():
    ll = LinkedList()
    for v in [33, 44, 55]:
        ll.append(v)
    assert ll.get(2) == 55

def test_T14_get_negative_index():
    ll = LinkedList()
    ll.append(1)
    with pytest.raises(IndexError):
        ll.get(-1)

def test_T15_get_out_of_range():
    ll = LinkedList()
    ll.append(7)
    ll.append(8)
    with pytest.raises(IndexError):
        ll.get(2)