import pytest
from data.input_code.d03_linked_list import *

def test_T1_OK():
    ll = LinkedList()
    assert len(ll) == 0
    assert ll.to_list() == []

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
    ll.append(1)
    ll.prepend(-1)
    assert ll.to_list() == [-1, 1]
    assert len(ll) == 2

def test_T6_OK():
    ll = LinkedList()
    ll.append(-1)
    ll.append(1)
    assert ll.delete(1) is True
    assert ll.to_list() == [-1]
    assert len(ll) == 1

def test_T7_ERR():
    ll = LinkedList()
    ll.append(5)
    ll.append(6)
    assert ll.delete(10) is False
    assert ll.to_list() == [5, 6]

def test_T8_OK():
    ll = LinkedList()
    ll.append(0)
    ll.append(1)
    assert ll.find(1) == 1

def test_T9_ERR():
    ll = LinkedList()
    ll.append(0)
    ll.append(1)
    assert ll.find(10) == -1

def test_T10_OK():
    ll = LinkedList()
    ll.append(-1)
    ll.append(0)
    ll.append(1)
    ll.append(2)
    assert ll.get(0) == -1

def test_T11_ERR():
    ll = LinkedList()
    ll.append(-1)
    ll.append(0)
    ll.append(1)
    with pytest.raises(IndexError):
        ll.get(-1)

def test_T12_ERR():
    ll = LinkedList()
    ll.append(-1)
    ll.append(0)
    ll.append(1)
    with pytest.raises(IndexError):
        ll.get(10)

def test_T13_OK():
    ll = LinkedList()
    ll.append(-1)
    ll.append(0)
    ll.append(1)
    ll.append(2)
    assert ll.to_list() == [-1, 0, 1, 2]

def test_T14_OK():
    ll = LinkedList()
    ll.append(-1)
    ll.append(0)
    ll.append(1)
    ll.append(2)
    assert len(ll) == 4

def test_T_MISSING_PREPEND_EMPTY():
    ll = LinkedList()
    ll.prepend(5)
    assert ll.to_list() == [5]
    assert len(ll) == 1

def test_T_MISSING_DELETE_HEAD():
    ll = LinkedList()
    ll.append(0)
    ll.append(1)
    assert ll.delete(0) is True
    assert ll.to_list() == [1]
    assert len(ll) == 1

def test_T_MISSING_DELETE_TAIL():
    ll = LinkedList()
    ll.append(0)
    ll.append(2)
    assert ll.delete(2) is True
    assert ll.to_list() == [0]
    assert len(ll) == 1

def test_T_MISSING_GET_MIDDLE():
    ll = LinkedList()
    ll.append(-1)
    ll.append(0)
    ll.append(1)
    ll.append(2)
    assert ll.get(1) == 0

def test_T_MISSING_FIND_HEAD():
    ll = LinkedList()
    ll.append(-1)
    ll.append(0)
    ll.append(1)
    assert ll.find(-1) == 0

def test_T_MISSING_FIND_TAIL():
    ll = LinkedList()
    ll.append(-1)
    ll.append(0)
    ll.append(1)
    ll.append(2)
    assert ll.find(2) == 3

def test_T_MISSING_GET_LAST():
    ll = LinkedList()
    ll.append(-1)
    ll.append(0)
    ll.append(1)
    ll.append(2)
    assert ll.get(3) == 2

@pytest.mark.parametrize("test_input, expected", [
    ({"data": 10, "init_data": [-1, 0, 1]}, False),
    ({"data": -1, "init_data": [-1, 10, 1]}, True),
    ({"data": 1, "init_data": [-1, 0, 1]}, True),
])
def test_T_MISSING_DELETE_NOT_FOUND(test_input, expected):
    ll = LinkedList()
    for data in test_input["init_data"]:
        ll.append(data)
    assert ll.delete(test_input["data"]) == expected

@pytest.mark.parametrize("test_input, expected", [
    ({"data": 10, "init_data": [0, 1]}, -1),
    ({"data": -1, "init_data": [-1, 10, 1]}, 0),
    ({"data": 1, "init_data": [-1, 0, 1]}, 2),
])
def test_T_MISSING_FIND_NOT_FOUND(test_input, expected):
    ll = LinkedList()
    for data in test_input["init_data"]:
        ll.append(data)
    assert ll.find(test_input["data"]) == expected

@pytest.mark.parametrize("index, expected", [
    (-10, "IndexError"),
    (10, "IndexError"),
])
def test_T_MISSING_GET_OUT_OF_RANGE(index, expected):
    ll = LinkedList()
    ll.append(-1)
    ll.append(0)
    ll.append(1)
    if expected == "IndexError":
        with pytest.raises(IndexError):
            ll.get(index)
    else:
        assert ll.get(index) == expected

import pytest
from data.input_code.d03_linked_list import *

def test_T_MISSING_PREPEND_MULTIPLE():
    ll = LinkedList()
    for d in [1, 2, 3]:
        ll.append(d)
    ll.prepend(5)
    assert ll.to_list() == [5, 1, 2, 3]

def test_T_MISSING_DELETE_MIDDLE():
    ll = LinkedList()
    for d in [0, 1, 2]:
        ll.append(d)
    assert ll.delete(1) is True

def test_T_MISSING_FIND_MIDDLE():
    ll = LinkedList()
    for d in [0, 1, 2]:
        ll.append(d)
    assert ll.find(1) == 1

def test_T_MISSING_GET_FIRST():
    ll = LinkedList()
    for d in [0, 1, 2]:
        ll.append(d)
    assert ll.get(0) == 0

def test_T_MISSING_TO_LIST_EMPTY():
    ll = LinkedList()
    assert ll.to_list() == []

def test_T_MISSING_LEN_EMPTY():
    ll = LinkedList()
    assert len(ll) == 0

def test_T_MISSING_DELETE_ALL():
    ll = LinkedList()
    ll.append(1)
    assert ll.delete(1) is True
    assert ll.to_list() == []

def test_T_MISSING_PREPEND_AFTER_DELETE():
    ll = LinkedList()
    ll.append(1)
    ll.append(2)
    ll.delete(1)
    ll.prepend(5)
    assert ll.to_list() == [5, 2]

def test_T_MISSING_FIND_AFTER_DELETE():
    ll = LinkedList()
    ll.append(1)
    ll.append(2)
    ll.delete(1)
    assert ll.find(2) == 0

def test_T_MISSING_GET_AFTER_DELETE():
    ll = LinkedList()
    ll.append(1)
    ll.append(2)
    ll.delete(1)
    assert ll.get(0) == 2

def test_T_MISSING_TO_LIST_AFTER_DELETE():
    ll = LinkedList()
    ll.append(1)
    ll.append(2)
    ll.delete(1)
    assert ll.to_list() == [2]

def test_T_MISSING_LEN_AFTER_DELETE():
    ll = LinkedList()
    ll.append(1)
    ll.append(2)
    ll.delete(1)
    assert len(ll) == 1

def test_T_MISSING_DELETE_NONE():
    ll = LinkedList()
    assert ll.delete(1) is False

def test_T_MISSING_PREPEND_NONE():
    ll = LinkedList()
    result = ll.prepend(1)
    assert result is None
    assert ll.to_list() == [1]
    assert len(ll) == 1

def test_T_MISSING_GET_NONE():
    ll = LinkedList()
    with pytest.raises(IndexError):
        ll.get(0)

def test_T_MISSING_FIND_NONE():
    ll = LinkedList()
    assert ll.find(1) == -1

def test_T_MISSING_TO_LIST_NONE_AFTER_PREPEND():
    ll = LinkedList()
    ll.prepend(1)
    assert ll.to_list() == [1]

def test_T_MISSING_LEN_NONE_AFTER_PREPEND():
    ll = LinkedList()
    ll.prepend(1)
    assert len(ll) == 1

def test_T_MISSING_DELETE_AFTER_PREPEND():
    ll = LinkedList()
    ll.prepend(1)
    assert ll.delete(1) is True
    assert ll.to_list() == []
    assert len(ll) == 0

def test_T_MISSING_FIND_AFTER_PREPEND():
    ll = LinkedList()
    ll.prepend(1)
    assert ll.find(1) == 0

def test_T_MISSING_GET_AFTER_PREPEND():
    ll = LinkedList()
    ll.prepend(1)
    assert ll.get(0) == 1