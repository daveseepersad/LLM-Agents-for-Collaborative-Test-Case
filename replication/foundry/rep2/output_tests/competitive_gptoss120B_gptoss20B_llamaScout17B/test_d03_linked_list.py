import pytest
from data.input_code.d03_linked_list import *

def test_T1_append_empty():
    ll = LinkedList()
    ll.append(10)
    assert ll.head is not None
    assert ll.head.data == 10
    assert ll._size == 1

def test_T2_append_nonempty():
    ll = LinkedList()
    ll.append(1)
    ll.append(2)
    assert ll._size == 2
    assert ll.head.data == 1
    assert ll.head.next.data == 2

def test_T3_prepend_empty():
    ll = LinkedList()
    ll.prepend(5)
    assert ll.head is not None
    assert ll.head.data == 5
    assert ll._size == 1

def test_T4_prepend_nonempty():
    ll = LinkedList()
    ll.append(7)
    ll.prepend(3)
    assert ll.head.data == 3
    assert ll.head.next.data == 7
    assert ll._size == 2

def test_T5_delete_empty():
    ll = LinkedList()
    result = ll.delete(99)
    assert result is False
    assert ll._size == 0

def test_T6_delete_head():
    ll = LinkedList()
    ll.append(4)
    ll.append(8)
    result = ll.delete(4)
    assert result is True
    assert ll.head.data == 8
    assert ll._size == 1

def test_T7_delete_tail():
    ll = LinkedList()
    ll.append(11)
    ll.append(22)
    ll.append(33)
    result = ll.delete(33)
    assert result is True
    assert ll.to_list() == [11, 22]
    assert ll._size == 2

def test_T8_delete_not_found():
    ll = LinkedList()
    ll.append(100)
    ll.append(200)
    result = ll.delete(300)
    assert result is False
    assert ll.to_list() == [100, 200]
    assert ll._size == 2

def test_T9_find_empty():
    ll = LinkedList()
    assert ll.find(1) == -1

def test_T10_find_head():
    ll = LinkedList()
    ll.append(42)
    assert ll.find(42) == 0

def test_T11_find_middle():
    ll = LinkedList()
    ll.append("a")
    ll.append("b")
    ll.append("c")
    assert ll.find("b") == 1

def test_T12_find_not_found():
    ll = LinkedList()
    ll.append("x")
    ll.append("y")
    assert ll.find("z") == -1

def test_T13_get_valid_index_zero():
    ll = LinkedList()
    ll.append(9)
    ll.append(8)
    assert ll.get(0) == 9

def test_T14_get_valid_last_index():
    ll = LinkedList()
    ll.append("first")
    ll.append("second")
    ll.append("third")
    assert ll.get(2) == "third"

def test_T15_get_negative_index():
    ll = LinkedList()
    ll.append(0)
    with pytest.raises(IndexError):
        ll.get(-1)

def test_T16_get_out_of_range():
    ll = LinkedList()
    ll.append(1)
    ll.append(2)
    with pytest.raises(IndexError):
        ll.get(5)

def test_T17_to_list_empty():
    ll = LinkedList()
    assert ll.to_list() == []

def test_T18_to_list_multiple():
    ll = LinkedList()
    ll.prepend(3)
    ll.append(4)
    ll.append(5)
    assert ll.to_list() == [3, 4, 5]

def test_T19_len_after_operations():
    ll = LinkedList()
    ll.append("a")
    ll.prepend("b")
    ll.delete("a")
    assert len(ll) == 1