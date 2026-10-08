import pytest
from data.input_code.d03_linked_list import *

def test_T1_OK():
    ll = LinkedList()
    assert isinstance(ll, LinkedList)

def test_T2_OK():
    ll = LinkedList()
    ll.append(1)
    assert ll.to_list() == [1]

def test_T3_OK():
    ll = LinkedList()
    ll.append(1)
    ll.append(2)
    assert ll.to_list() == [1, 2]

def test_T4_OK():
    ll = LinkedList()
    ll.prepend(0)
    assert ll.to_list() == [0]

def test_T5_OK():
    ll = LinkedList()
    ll.prepend(3)
    assert ll.to_list() == [3]

def test_T6_OK():
    ll = LinkedList()
    ll.append(1)
    assert ll.delete(1) is True
    assert ll.to_list() == []

def test_T7_ERR():
    ll = LinkedList()
    assert ll.delete(4) is False

def test_T8_OK():
    ll = LinkedList()
    ll.append(2)
    assert ll.find(2) == 0

def test_T9_ERR():
    ll = LinkedList()
    ll.append(1)
    assert ll.find(5) == -1

def test_T10_OK():
    ll = LinkedList()
    ll.append(3)
    assert ll.get(0) == 3

def test_T11_ERR():
    ll = LinkedList()
    with pytest.raises(IndexError):
        ll.get(-1)

def test_T12_ERR():
    ll = LinkedList()
    with pytest.raises(IndexError):
        ll.get(10)

def test_T13_OK():
    ll = LinkedList()
    ll.append(3)
    ll.append(0)
    ll.append(1)
    ll.append(2)
    assert ll.to_list() == [3, 0, 1, 2]

def test_T14_OK():
    ll = LinkedList()
    ll.append(1)
    ll.append(2)
    ll.append(3)
    ll.append(4)
    assert len(ll) == 4

import pytest
from data.input_code.d03_linked_list import *

def test_T_MISSING_PREPEND_MULTIPLE_OK():
    ll = LinkedList()
    ll.append(2)
    ll.prepend(1)
    assert ll.to_list() == [1, 2]

def test_T_MISSING_DELETE_HEAD_OK():
    ll = LinkedList()
    ll.append(1)
    ll.append(2)
    assert ll.delete(1) is True
    assert ll.to_list() == [2]

def test_T_MISSING_DELETE_TAIL_OK():
    ll = LinkedList()
    ll.append(1)
    ll.append(2)
    assert ll.delete(2) is True
    assert ll.to_list() == [1]

def test_T_MISSING_DELETE_MIDDLE_OK():
    ll = LinkedList()
    ll.append(1)
    ll.append(2)
    ll.append(3)
    assert ll.delete(2) is True
    assert ll.to_list() == [1, 3]

def test_T_MISSING_FIND_MULTIPLE_OK():
    ll = LinkedList()
    ll.append(1)
    ll.append(2)
    ll.append(3)
    assert ll.find(2) == 1

def test_T_MISSING_GET_MIDDLE_OK():
    ll = LinkedList()
    ll.append(1)
    ll.append(2)
    ll.append(3)
    assert ll.get(1) == 2

def test_T_MISSING_GET_TAIL_OK():
    ll = LinkedList()
    ll.append(1)
    ll.append(2)
    ll.append(3)
    assert ll.get(2) == 3

def test_T_MISSING_LEN_EMPTY_OK():
    ll = LinkedList()
    assert len(ll) == 0