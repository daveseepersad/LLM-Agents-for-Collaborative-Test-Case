import pytest
from data.input_code.d03_linked_list import *

def test_T1_append_empty():
    ll = LinkedList()
    res = ll.append(1)
    assert res is None
    assert ll.head is not None and ll.head.data == 1
    assert ll._size == 1
    assert ll.to_list() == [1]

def test_T2_append_nonempty():
    ll = LinkedList()
    ll.append(1)
    ll.append(2)
    res = ll.append(3)
    assert res is None
    assert ll.to_list() == [1, 2, 3]
    assert ll._size == 3

@pytest.mark.parametrize("init, delete_target, expected, final_list, final_size", [
    ([], 1, False, [], 0),
    ([1, 2, 3], 1, True, [2, 3], 2),
    ([1, 2, 3], 2, True, [1, 3], 2),
    ([1, 2, 3], 4, False, [1, 2, 3], 3),
])
def test_T3_to_T6_delete_variants(init, delete_target, expected, final_list, final_size):
    ll = LinkedList()
    for v in init:
        ll.append(v)
    result = ll.delete(delete_target)
    assert result == expected
    assert ll.to_list() == final_list
    assert ll._size == final_size

def test_T7_find_existing():
    ll = LinkedList()
    ll.append(0)
    ll.append(1)
    ll.append(2)
    assert ll.find(1) == 1

def test_T8_find_missing():
    ll = LinkedList()
    ll.append(0)
    ll.append(1)
    ll.append(2)
    assert ll.find(3) == -1

def test_T9_get_valid():
    ll = LinkedList()
    ll.append(10)
    ll.append(20)
    ll.append(30)
    assert ll.get(1) == 20

def test_T10_get_negative_index():
    ll = LinkedList()
    ll.append(1)
    ll.append(2)
    ll.append(3)
    with pytest.raises(IndexError):
        ll.get(-1)

def test_T11_get_out_of_range():
    ll = LinkedList()
    ll.append(1)
    ll.append(2)
    ll.append(3)
    with pytest.raises(IndexError):
        ll.get(3)

def test_T12_to_list_empty():
    ll = LinkedList()
    assert ll.to_list() == []

def test_T13_to_list_nonempty():
    ll = LinkedList()
    ll.append(1)
    ll.append(2)
    ll.append(3)
    assert ll.to_list() == [1, 2, 3]

def test_T14_len_empty():
    ll = LinkedList()
    assert len(ll) == 0

def test_T15_len_nonempty():
    ll = LinkedList()
    ll.append(1)
    ll.append(2)
    ll.append(3)
    assert len(ll) == 3

import pytest
from data.input_code.d03_linked_list import *

def test_T16_PREPEND_EMPTY():
    ll = LinkedList()
    ll.prepend(10)
    assert ll.head is not None
    assert ll.head.data == 10
    assert ll._size == 1
    assert ll.to_list() == [10]

def test_T17_DELETE_TAIL():
    ll = LinkedList()
    ll.append(1)
    ll.append(2)
    ll.append(3)
    result = ll.delete(3)
    assert result is True
    assert ll.to_list() == [1, 2]
    assert ll._size == 2

def test_T18_DELETE_ONLY_ELEMENT():
    ll = LinkedList()
    ll.append(5)
    result = ll.delete(5)
    assert result is True
    assert ll.to_list() == []
    assert ll._size == 0
    assert ll.head is None

def test_T19_GET_LAST_INDEX():
    ll = LinkedList()
    ll.append(9)
    ll.append(8)
    with pytest.raises(IndexError):
        ll.get(2)