import pytest
from data.input_code.d03_linked_list import *

# Helper to manually build a small 2-node chain without defining new helpers at module scope
def _build_two_node_chain(head_dict):
    if head_dict is None:
        return None
    head = Node(head_dict['data'])
    next_dict = head_dict.get('next')
    if next_dict is not None:
        head.next = Node(next_dict['data'])
    return head

def test_T1_INIT():
    ll = LinkedList()
    assert ll.head is None
    assert ll._size == 0

# Tests for append/prepend on various initial conditions
cases_A = [
    {"id":"T2_APPEND_EMPTY","initial":{"head": None, "_size": 0}, "method":"append","data":5, "expected":[5],"size":1},
    {"id":"T3_APPEND_NONEMPTY","initial":{"head":{"data":1,"next": None}, "_size": 1}, "method":"append","data":2, "expected":[1,2], "size":2},
    {"id":"T4_PREPEND_EMPTY","initial":{"head": None, "_size": 0}, "method":"prepend","data":5, "expected":[5],"size":1},
    {"id":"T5_PREPEND_NONEMPTY","initial":{"head":{"data":1,"next": None}, "_size":1}, "method":"prepend","data":2, "expected":[2,1], "size":2},
]

@pytest.mark.parametrize("case", cases_A, ids=[case["id"] for case in cases_A])
def test_T_append_prepend(case):
    ll = LinkedList()
    init = case["initial"]
    # Build initial list state without introducing new helpers at module scope
    head = None
    if init["head"] is not None:
        head_dict = init["head"]
        head = Node(head_dict["data"])
        if head_dict.get("next") is not None:
            head.next = Node(head_dict["next"]["data"])
    ll.head = head
    ll._size = init["_size"]

    # Perform operation
    getattr(ll, case["method"])(case["data"])

    # Assertions
    assert ll.to_list() == case["expected"]
    assert len(ll) == case["size"]

# Tests for delete
cases_B = [
    {"id":"T6_DELETE_EMPTY","initial":{"head": None, "_size":0}, "data":5, "expected": False, "expected_list": [], "expected_size":0},
    {"id":"T7_DELETE_HEAD","initial":{"head":{"data":1,"next": None}, "_size":1}, "data":1, "expected": True, "expected_list": [], "expected_size":0},
    {"id":"T8_DELETE_NONHEAD","initial":{"head":{"data":1,"next": {"data":2,"next": None}}, "_size":2}, "data":2, "expected": True, "expected_list":[1], "expected_size":1},
    {"id":"T9_DELETE_MISSING","initial":{"head":{"data":1,"next": None}, "_size":1}, "data":2, "expected": False, "expected_list":[1], "expected_size":1},
]

@pytest.mark.parametrize("case", cases_B, ids=[case["id"] for case in cases_B])
def test_T_delete(case):
    ll = LinkedList()
    init = case["initial"]
    head = None
    if init["head"] is not None:
        head_dict = init["head"]
        head = Node(head_dict["data"])
        if head_dict.get("next") is not None:
            head.next = Node(head_dict["next"]["data"])
    ll.head = head
    ll._size = init["_size"]

    res = ll.delete(case["data"])
    assert res == case["expected"]
    assert ll.to_list() == case["expected_list"]
    assert len(ll) == case["expected_size"]

# Tests for find
cases_C = [
    {"id":"T10_FIND_PRESENT", "initial":{"head":{"data":1,"next":{"data":2,"next": None}}, "_size":2}, "data":2, "expected":1},
    {"id":"T11_FIND_MISSING", "initial":{"head":{"data":1,"next": None}, "_size":1}, "data":2, "expected": -1},
]

@pytest.mark.parametrize("case", cases_C, ids=[case["id"] for case in cases_C])
def test_T_find(case):
    ll = LinkedList()
    init = case["initial"]
    head = None
    if init["head"] is not None:
        head_dict = init["head"]
        head = Node(head_dict["data"])
        if head_dict.get("next") is not None:
            head.next = Node(head_dict["next"]["data"])
    ll.head = head
    ll._size = init["_size"]

    assert ll.find(case["data"]) == case["expected"]

# Tests for get
cases_D = [
    {"id":"T12_GET_VALID","initial":{"head":{"data":1,"next":{"data":2,"next": None}}, "_size":2}, "index":1, "expected":2},
    {"id":"T13_GET_INVALID_LOW","initial":{"head":{"data":1,"next": None}, "_size":1}, "index": -1, "expected":"IndexError"},
    {"id":"T14_GET_INVALID_HIGH","initial":{"head":{"data":1,"next": None}, "_size":1}, "index": 1, "expected":"IndexError"},
]

@pytest.mark.parametrize("case", cases_D, ids=[case["id"] for case in cases_D])
def test_T_get(case):
    ll = LinkedList()
    init = case["initial"]
    head = None
    if init["head"] is not None:
        head_dict = init["head"]
        head = Node(head_dict["data"])
        if head_dict.get("next") is not None:
            head.next = Node(head_dict["next"]["data"])
    ll.head = head
    ll._size = init["_size"]

    idx = case["index"]
    expected = case["expected"]
    if isinstance(expected, str) and expected == "IndexError":
        with pytest.raises(IndexError):
            ll.get(idx)
    else:
        assert ll.get(idx) == expected

# Tests for to_list
cases_E = [
    {"id":"T15_TOLIST_EMPTY","initial":{"head": None, "_size":0}, "expected": []},
    {"id":"T16_TOLIST_NONEMPTY","initial":{"head":{"data":1,"next": {"data":2,"next": None}}, "_size":2}, "expected":[1,2]},
]

@pytest.mark.parametrize("case", cases_E, ids=[case["id"] for case in cases_E])
def test_T_to_list(case):
    ll = LinkedList()
    init = case["initial"]
    head = None
    if init["head"] is not None:
        head_dict = init["head"]
        head = Node(head_dict["data"])
        if head_dict.get("next") is not None:
            head.next = Node(head_dict["next"]["data"])
    ll.head = head
    ll._size = init["_size"]

    assert ll.to_list() == case["expected"]

# Tests for __len__
cases_F = [
    {"id":"T17_LEN_EMPTY","initial":{"head": None, "_size":0}, "expected":0},
    {"id":"T18_LEN_NONEMPTY","initial":{"head":{"data":1,"next": None}, "_size":1}, "expected":1},
]

@pytest.mark.parametrize("case", cases_F, ids=[case["id"] for case in cases_F])
def test_T_len(case):
    ll = LinkedList()
    init = case["initial"]
    head = None
    if init["head"] is not None:
        head_dict = init["head"]
        head = Node(head_dict["data"])
        if head_dict.get("next") is not None:
            head.next = Node(head_dict["next"]["data"])
    ll.head = head
    ll._size = init["_size"]

    assert len(ll) == case["expected"]

import pytest
from data.input_code.d03_linked_list import *

def test_T_missing_delete_multiple():
    ll = LinkedList()
    ll.head = Node(1)
    ll.head.next = Node(2)
    ll.head.next.next = Node(3)
    ll._size = 3
    res = ll.delete(2)
    assert res is True
    assert ll.to_list() == [1, 3]
    assert len(ll) == 2

def test_T_missing_find_empty():
    ll = LinkedList()
    assert ll.find(1) == -1

def test_T_missing_get_edge():
    ll = LinkedList()
    ll.head = Node(1)
    ll._size = 1
    assert ll.get(0) == 1

def test_T_missing_append_multiple():
    ll = LinkedList()
    ll.head = Node(1)
    ll.head.next = Node(2)
    ll._size = 2
    ll.append(3)
    assert ll.to_list() == [1, 2, 3]
    assert len(ll) == 3

def test_T_missing_prepend_multiple():
    ll = LinkedList()
    ll.head = Node(1)
    ll.head.next = Node(2)
    ll._size = 2
    ll.prepend(0)
    assert ll.to_list() == [0, 1, 2]
    assert len(ll) == 3

import pytest
from data.input_code.d03_linked_list import *

def test_T_MISSING_DELETE_HEAD_MULTIPLE():
    ll = LinkedList()
    ll.head = Node(1)
    ll.head.next = Node(2)
    ll.head.next.next = Node(3)
    ll._size = 3
    res = ll.delete(1)
    assert res is True
    assert ll.to_list() == [2, 3]
    assert len(ll) == 2

def test_T_MISSING_FIND_HEAD():
    ll = LinkedList()
    ll.head = Node(1)
    ll.head.next = Node(2)
    ll._size = 2
    assert ll.find(1) == 0

import pytest
from data.input_code.d03_linked_list import *

def test_T_MISSING_1_delete_middle_not_head():
    ll = LinkedList()
    ll.head = Node(1)
    ll.head.next = Node(3)
    ll.head.next.next = Node(2)
    ll._size = 3

    res = ll.delete(2)
    assert res is True
    assert ll.to_list() == [1, 3]
    assert len(ll) == 2

def test_T_MISSING_2_find_last():
    ll = LinkedList()
    ll.head = Node(1)
    ll.head.next = Node(2)
    ll.head.next.next = Node(3)
    ll._size = 3

    assert ll.find(3) == 2

def test_T_MISSING_3_get_last():
    ll = LinkedList()
    ll.head = Node(1)
    ll.head.next = Node(2)
    ll.head.next.next = Node(3)
    ll._size = 3

    assert ll.get(2) == 3

def test_T_MISSING_4_to_list():
    ll = LinkedList()
    ll.head = Node(1)
    ll.head.next = Node(2)
    ll.head.next.next = Node(3)
    ll._size = 3

    assert ll.to_list() == [1, 2, 3]

def test_T_MISSING_5_len():
    ll = LinkedList()
    ll.head = Node(1)
    ll.head.next = Node(2)
    ll.head.next.next = Node(3)
    ll._size = 3

    assert len(ll) == 3