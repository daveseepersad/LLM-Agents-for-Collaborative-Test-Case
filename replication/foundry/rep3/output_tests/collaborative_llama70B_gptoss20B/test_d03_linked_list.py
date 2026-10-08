import pytest
from data.input_code.d03_linked_list import *

def test_T1_OK_init():
    ll = LinkedList()
    assert ll.to_list() == []
    assert len(ll) == 0

def test_T2_OK_append_single():
    ll = LinkedList()
    ll.append(1)
    assert ll.to_list() == [1]
    assert len(ll) == 1

def test_T3_OK_append_multiple():
    ll = LinkedList()
    ll.append(1)
    ll.append(2)
    assert ll.to_list() == [1, 2]
    assert len(ll) == 2

def test_T4_OK_prepend_single():
    ll = LinkedList()
    ll.prepend(0)
    assert ll.to_list() == [0]
    assert len(ll) == 1

def test_T5_OK_prepend_multiple():
    ll = LinkedList()
    ll.prepend(-1)
    assert ll.to_list() == [-1]
    assert len(ll) == 1

def test_T6_OK_delete_existing():
    ll = LinkedList()
    ll.append(-1)
    ll.append(0)
    ll.append(1)
    ll.append(2)
    assert ll.delete(1) is True
    assert ll.to_list() == [-1, 0, 2]

def test_T7_ERR_delete_non_existing():
    ll = LinkedList()
    ll.append(-1)
    ll.append(0)
    ll.append(2)
    assert ll.delete(1) is False

def test_T8_OK_find_existing():
    ll = LinkedList()
    ll.append(-1)
    ll.append(0)
    ll.append(1)
    ll.append(2)
    assert ll.find(1) == 2

def test_T9_ERR_find_non_existing():
    ll = LinkedList()
    ll.append(-1)
    ll.append(0)
    ll.append(1)
    ll.append(2)
    assert ll.find(10) == -1

def test_T10_OK_get_valid_index():
    ll = LinkedList()
    ll.append(-1)
    ll.append(0)
    ll.append(1)
    ll.append(2)
    assert ll.get(0) == -1

def test_T11_ERR_get_invalid_index():
    ll = LinkedList()
    ll.append(-1)
    ll.append(0)
    ll.append(1)
    ll.append(2)
    with pytest.raises(IndexError):
        ll.get(10)

def test_T12_OK_to_list():
    ll = LinkedList()
    ll.append(-1)
    ll.append(0)
    ll.append(1)
    ll.append(2)
    assert ll.to_list() == [-1, 0, 1, 2]

def test_T13_OK_len():
    ll = LinkedList()
    ll.append(-1)
    ll.append(0)
    ll.append(1)
    ll.append(2)
    assert len(ll) == 4

import pytest
from data.input_code.d03_linked_list import *

def test_T_MISSING_PREPEND_MULTIPLE():
    ll = LinkedList()
    ll.append(0)
    ll.prepend(1)
    assert ll.to_list() == [1, 0]
    assert len(ll) == 2

def test_T_MISSING_DELETE_HEAD():
    ll = LinkedList()
    ll.append(0)
    result = ll.delete(0)
    assert result is True
    assert ll.to_list() == []
    assert len(ll) == 0

def test_T_MISSING_GET_LAST_INDEX():
    ll = LinkedList()
    ll.append(-1)
    ll.append(0)
    ll.append(1)
    ll.append(2)
    assert ll.get(3) == 2

def test_T_MISSING_GET_NEGATIVE_INDEX():
    ll = LinkedList()
    ll.append(-1)
    ll.append(0)
    ll.append(1)
    ll.append(2)
    with pytest.raises(IndexError):
        ll.get(-1)

def test_T_MISSING_FIND_HEAD():
    ll = LinkedList()
    ll.append(0)
    assert ll.find(0) == 0

def test_T_MISSING_DELETE_NON_EXISTING_HEAD():
    ll = LinkedList()
    ll.append(0)
    result = ll.delete(1)
    assert result is False

def test_T_MISSING_PREPEND_EMPTY():
    ll = LinkedList()
    result = ll.prepend(0)
    assert result is None
    assert ll.to_list() == [0]
    assert len(ll) == 1