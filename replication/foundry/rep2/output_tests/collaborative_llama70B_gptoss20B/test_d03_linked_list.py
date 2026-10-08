import pytest
from data.input_code.d03_linked_list import *

def test_T1_OK():
    ll = LinkedList()
    assert len(ll) == 0
    assert ll.head is None

def test_T2_OK():
    ll = LinkedList()
    ll.append(1)
    assert ll.to_list() == [1]
    assert len(ll) == 1

def test_T3_OK():
    ll = LinkedList()
    ll.append(1)
    ll.append(2)
    assert ll.to_list() == [1, 2]
    assert len(ll) == 2

def test_T4_OK():
    ll = LinkedList()
    ll.prepend(0)
    assert ll.to_list() == [0]
    assert len(ll) == 1

def test_T5_OK():
    ll = LinkedList()
    ll.prepend(-1)
    assert ll.to_list() == [-1]
    assert len(ll) == 1

def test_T6_OK():
    ll = LinkedList()
    ll.append(1)
    ll.append(2)
    ll.append(3)
    result = ll.delete(1)
    assert result is True
    assert ll.to_list() == [2, 3]
    assert len(ll) == 2

def test_T7_ERR():
    ll = LinkedList()
    ll.append(1)
    ll.append(2)
    ll.append(3)
    result = ll.delete(10)
    assert result is False
    assert ll.to_list() == [1, 2, 3]
    assert len(ll) == 3

def test_T8_OK():
    ll = LinkedList()
    ll.append(0)
    ll.append(2)
    ll.append(1)
    assert ll.find(1) == 2

def test_T9_ERR():
    ll = LinkedList()
    ll.append(0)
    ll.append(2)
    ll.append(1)
    assert ll.find(10) == -1

def test_T10_OK():
    ll = LinkedList()
    ll.append(-1)
    assert ll.get(0) == -1

def test_T11_ERR():
    ll = LinkedList()
    ll.append(1)
    ll.append(2)
    ll.append(3)
    with pytest.raises(IndexError):
        ll.get(10)

def test_T12_OK():
    ll = LinkedList()
    ll.append(-1)
    ll.append(0)
    ll.append(1)
    ll.append(2)
    assert ll.to_list() == [-1, 0, 1, 2]

def test_T13_OK():
    ll = LinkedList()
    ll.append(-1)
    ll.append(0)
    ll.append(1)
    ll.append(2)
    assert len(ll) == 4

import pytest
from data.input_code.d03_linked_list import *

def test_T_MISSING_PREPEND_MULTIPLE_OK():
    ll = LinkedList()
    ll.append(2)
    ll.prepend(1)
    assert ll.to_list() == [1, 2]
    assert len(ll) == 2

def test_T_MISSING_DELETE_HEAD_OK():
    ll = LinkedList()
    ll.append(1)
    ll.append(2)
    result = ll.delete(1)
    assert result is True
    assert ll.to_list() == [2]
    assert len(ll) == 1

def test_T_MISSING_DELETE_TAIL_OK():
    ll = LinkedList()
    ll.append(1)
    ll.append(2)
    result = ll.delete(2)
    assert result is True
    assert ll.to_list() == [1]
    assert len(ll) == 1

def test_T_MISSING_GET_MIDDLE_OK():
    ll = LinkedList()
    ll.append(0)
    ll.append(1)
    ll.append(2)
    assert ll.get(1) == 1

def test_T_MISSING_FIND_HEAD_OK():
    ll = LinkedList()
    ll.append(1)
    ll.append(2)
    assert ll.find(1) == 0

def test_T_MISSING_FIND_TAIL_OK():
    ll = LinkedList()
    ll.append(1)
    ll.append(2)
    assert ll.find(2) == 1

def test_T_MISSING_EMPTY_DELETE_OK():
    ll = LinkedList()
    result = ll.delete(1)
    assert result is False
    assert ll.to_list() == []
    assert len(ll) == 0

def test_T_MISSING_EMPTY_FIND_OK():
    ll = LinkedList()
    assert ll.find(1) == -1

def test_T_MISSING_EMPTY_GET_ERR():
    ll = LinkedList()
    with pytest.raises(IndexError):
        ll.get(0)

def test_T_MISSING_NEGATIVE_GET_ERR():
    ll = LinkedList()
    ll.append(1)
    with pytest.raises(IndexError):
        ll.get(-1)