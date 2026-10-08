import pytest
from data.input_code.d03_linked_list import *

def test_init():
    ll = LinkedList()
    assert ll.head is None
    assert len(ll) == 0

def test_append_to_empty():
    ll = LinkedList()
    ll.append(1)
    assert ll.to_list() == [1]
    assert len(ll) == 1

def test_append_to_non_empty():
    ll = LinkedList()
    ll.append(1)
    ll.append(2)
    assert ll.to_list() == [1, 2]
    assert len(ll) == 2

def test_prepend_to_empty():
    ll = LinkedList()
    ll.prepend(0)
    assert ll.to_list() == [0]
    assert len(ll) == 1

def test_prepend_to_non_empty():
    ll = LinkedList()
    ll.append(0)
    ll.prepend(-1)
    assert ll.to_list() == [-1, 0]
    assert len(ll) == 2

@pytest.mark.parametrize(
    "initial, data, expected",
    [
        ([1], 1, True),          # delete existing
        ([1, 2], 10, False),     # delete non‑existing
    ],
)
def test_delete(initial, data, expected):
    ll = LinkedList()
    for d in initial:
        ll.append(d)
    assert ll.delete(data) is expected

@pytest.mark.parametrize(
    "initial, data, expected",
    [
        ([-1, 0, 1, 2], 1, 2),   # find existing
        ([-1, 0, 1, 2], 10, -1), # find non‑existing
    ],
)
def test_find(initial, data, expected):
    ll = LinkedList()
    for d in initial:
        ll.append(d)
    assert ll.find(data) == expected

def test_get_valid():
    ll = LinkedList()
    for d in [-1, 0, 1, 2]:
        ll.append(d)
    assert ll.get(0) == -1

def test_get_invalid():
    ll = LinkedList()
    for d in [-1, 0, 1, 2]:
        ll.append(d)
    with pytest.raises(IndexError):
        ll.get(10)

def test_to_list():
    ll = LinkedList()
    for d in [-1, 0, 1, 2]:
        ll.append(d)
    assert ll.to_list() == [-1, 0, 1, 2]

def test_len():
    ll = LinkedList()
    for d in [-1, 0, 1, 2]:
        ll.append(d)
    assert len(ll) == 4

def test_append_none():
    ll = LinkedList()
    ll.append(None)
    assert ll.get(0) is None

def test_prepend_none():
    ll = LinkedList()
    ll.prepend(None)
    assert ll.get(0) is None

def test_delete_none():
    ll = LinkedList()
    ll.append(1)
    assert ll.delete(None) is False

def test_find_none():
    ll = LinkedList()
    ll.append(1)
    assert ll.find(None) == -1

def test_get_none():
    ll = LinkedList()
    ll.prepend(None)
    assert ll.get(0) is None

import pytest
from data.input_code.d03_linked_list import *

def test_get_index_0_after_prepend_none():
    ll = LinkedList()
    ll.prepend(None)
    assert ll.get(0) is None

@pytest.mark.parametrize(
    "index",
    [
        -1,  # negative index
        4,   # index equal to size
    ],
)
def test_get_invalid_indices(index):
    ll = LinkedList()
    for d in [-1, 0, 1, 2]:
        ll.append(d)
    with pytest.raises(IndexError):
        ll.get(index)

@pytest.mark.parametrize(
    "initial, data, expected",
    [
        ([1, 2, 3], 1, True),  # delete head node
        ([1, 2], 2, True),     # delete tail node
    ],
)
def test_delete_edge_cases(initial, data, expected):
    ll = LinkedList()
    for d in initial:
        ll.append(d)
    assert ll.delete(data) is expected

@pytest.mark.parametrize(
    "initial, data, expected",
    [
        ([-1, 0, 1, 2], -1, 0),  # find node at index 0
        ([-1, 0, 1, 2], 2, 3),   # find node at index size‑1
    ],
)
def test_find_edge_cases(initial, data, expected):
    ll = LinkedList()
    for d in initial:
        ll.append(d)
    assert ll.find(data) == expected

def test_prepend_after_delete():
    ll = LinkedList()
    for d in [1, 2]:
        ll.append(d)
    ll.delete(1)          # delete head
    ll.prepend(0)         # prepend after deletion
    assert ll.to_list() == [0, 2]

def test_append_after_delete():
    ll = LinkedList()
    for d in [1, 2]:
        ll.append(d)
    ll.delete(2)          # delete tail
    ll.append(3)          # append after deletion
    assert ll.to_list() == [1, 3]

import pytest
from data.input_code.d03_linked_list import *

def test_get_index_size_minus_one():
    ll = LinkedList()
    for d in [-1, 0, 1, 2]:
        ll.append(d)
    assert ll.get(3) == 2

def test_delete_after_prepend():
    ll = LinkedList()
    ll.prepend(0)
    assert ll.delete(0) is True

def test_find_after_delete():
    ll = LinkedList()
    ll.append(1)
    ll.append(2)
    ll.delete(1)
    assert ll.find(2) == 0

def test_get_after_delete():
    ll = LinkedList()
    ll.append(1)
    ll.append(2)
    ll.delete(1)
    assert ll.get(0) == 2

def test_to_list_after_delete():
    ll = LinkedList()
    ll.append(1)
    ll.append(2)
    ll.delete(1)
    assert ll.to_list() == [2]

def test_len_after_delete():
    ll = LinkedList()
    ll.append(1)
    ll.append(2)
    ll.delete(1)
    assert len(ll) == 1

def test_prepend_after_append():
    ll = LinkedList()
    ll.append(1)
    ll.prepend(0)
    assert ll.to_list() == [0, 1]
    assert len(ll) == 2

def test_append_after_prepend():
    ll = LinkedList()
    ll.prepend(1)
    ll.append(3)
    assert ll.to_list() == [1, 3]
    assert len(ll) == 2

def test_delete_none_after_prepend():
    ll = LinkedList()
    ll.prepend(1)
    assert ll.delete(None) is False

def test_delete_none_after_append():
    ll = LinkedList()
    ll.append(1)
    assert ll.delete(None) is False

import pytest
from data.input_code.d03_linked_list import *

def test_get_index_1_after_prepend_two():
    ll = LinkedList()
    ll.prepend(0)   # list: [0]
    ll.prepend(1)   # list: [1, 0]
    assert ll.get(1) == 0

def test_delete_none_after_append_none():
    ll = LinkedList()
    ll.append(None)
    assert ll.delete(None) is True

def test_find_none_after_prepend_none():
    ll = LinkedList()
    ll.prepend(None)
    assert ll.find(None) == 0

def test_get_after_prepend_none():
    ll = LinkedList()
    ll.prepend(None)
    assert ll.get(0) is None

def test_to_list_after_prepend_none():
    ll = LinkedList()
    ll.prepend(None)
    assert ll.to_list() == [None]

def test_len_after_prepend_none():
    ll = LinkedList()
    ll.prepend(None)
    assert len(ll) == 1

def test_delete_none_after_prepend_none():
    ll = LinkedList()
    ll.prepend(None)
    assert ll.delete(None) is True

def test_get_index_size_minus_two():
    ll = LinkedList()
    for d in [-1, 0, 1, 2]:
        ll.append(d)
    assert ll.get(2) == 1

def test_find_none_after_append_none():
    ll = LinkedList()
    ll.append(None)
    assert ll.find(None) == 0

def test_to_list_after_append_none():
    ll = LinkedList()
    ll.append(None)
    assert ll.to_list() == [None]

def test_len_after_append_none():
    ll = LinkedList()
    ll.append(None)
    assert len(ll) == 1

import pytest
from data.input_code.d03_linked_list import *

def test_get_index_0_after_delete():
    ll = LinkedList()
    ll.append(1)
    ll.append(2)
    ll.delete(1)
    assert ll.get(0) == 2

def test_delete_after_prepend_none():
    ll = LinkedList()
    ll.prepend(None)
    assert ll.delete(None) is True

def test_find_after_prepend_none():
    ll = LinkedList()
    ll.prepend(None)
    assert ll.find(None) == 0

def test_get_after_prepend_none_and_append():
    ll = LinkedList()
    ll.prepend(None)
    ll.append(1)
    assert ll.get(1) == 1

def test_to_list_after_prepend_none_and_delete():
    ll = LinkedList()
    ll.prepend(None)
    ll.delete(None)
    assert ll.to_list() == []

def test_len_after_prepend_none_and_delete():
    ll = LinkedList()
    ll.prepend(None)
    ll.delete(None)
    assert len(ll) == 0

import pytest
from data.input_code.d03_linked_list import *

def test_get_index_after_delete_tail():
    ll = LinkedList()
    ll.append(0)
    ll.append(1)
    ll.append(2)          # list: [0, 1, 2]
    ll.delete(2)          # delete tail
    assert ll.get(1) == 1

def test_delete_after_prepend_and_append():
    ll = LinkedList()
    ll.prepend(0)         # list: [0]
    ll.append(1)          # list: [0, 1]
    assert ll.delete(0) is True

def test_find_after_prepend_and_append():
    ll = LinkedList()
    ll.prepend(0)         # list: [0]
    ll.append(1)          # list: [0, 1]
    assert ll.find(1) == 1

def test_get_after_prepend_and_delete_head():
    ll = LinkedList()
    ll.prepend(0)         # list: [0]
    ll.append(1)          # list: [0, 1]
    ll.delete(0)          # delete head, list: [1]
    assert ll.get(0) == 1

def test_to_list_after_prepend_and_delete_tail():
    ll = LinkedList()
    ll.prepend(1)         # list: [1]
    ll.prepend(0)         # list: [0, 1]
    ll.delete(1)          # delete tail, list: [0]
    assert ll.to_list() == [0]

def test_len_after_prepend_and_delete_tail():
    ll = LinkedList()
    ll.prepend(1)         # list: [1]
    ll.prepend(0)         # list: [0, 1]
    ll.delete(1)          # delete tail, list: [0]
    assert len(ll) == 1

import pytest
from data.input_code.d03_linked_list import *

def test_get_index_0_after_delete_head_and_append():
    ll = LinkedList()
    ll.append(0)          # initial list: [0]
    ll.delete(0)          # delete head, list becomes []
    ll.append(1)          # append after deletion, list: [1]
    assert ll.get(0) == 1

def test_delete_after_prepend_and_delete_tail():
    ll = LinkedList()
    ll.prepend(0)         # list: [0]
    ll.append(1)          # list: [0, 1]
    ll.delete(1)          # delete tail, list: [0]
    assert ll.delete(0) is True

def test_find_after_prepend_and_delete_head_and_tail():
    ll = LinkedList()
    ll.prepend(1)         # list: [1]
    ll.append(2)          # list: [1, 2]
    ll.delete(1)          # delete head, list: [2]
    ll.delete(2)          # delete tail, list: []
    assert ll.find(1) == -1

def test_get_after_prepend_and_delete_head_and_tail_raises():
    ll = LinkedList()
    ll.prepend(1)         # list: [1]
    ll.append(2)          # list: [1, 2]
    ll.delete(1)          # delete head, list: [2]
    ll.delete(2)          # delete tail, list: []
    with pytest.raises(IndexError):
        ll.get(0)

def test_to_list_after_prepend_and_delete_head_and_tail():
    ll = LinkedList()
    ll.prepend(1)         # list: [1]
    ll.append(2)          # list: [1, 2]
    ll.delete(1)          # delete head, list: [2]
    ll.delete(2)          # delete tail, list: []
    assert ll.to_list() == []

def test_len_after_prepend_and_delete_head_and_tail():
    ll = LinkedList()
    ll.prepend(1)         # list: [1]
    ll.append(2)          # list: [1, 2]
    ll.delete(1)          # delete head, list: [2]
    ll.delete(2)          # delete tail, list: []
    assert len(ll) == 0

import pytest
from data.input_code.d03_linked_list import *

def test_delete_middle():
    ll = LinkedList()
    for d in [0, 1, 2]:
        ll.append(d)
    assert ll.delete(1) is True
    assert ll.to_list() == [0, 2]

def test_find_middle():
    ll = LinkedList()
    for d in [0, 1, 2]:
        ll.append(d)
    assert ll.find(1) == 1

def test_get_middle():
    ll = LinkedList()
    for d in [0, 1, 2]:
        ll.append(d)
    assert ll.get(1) == 1

def test_prepend_after_delete_middle():
    ll = LinkedList()
    for d in [0, 1, 2]:
        ll.append(d)
    ll.delete(1)          # list becomes [0, 2]
    ll.prepend(0)         # prepend 0 -> [0, 0, 2]
    assert ll.to_list() == [0, 0, 2]

def test_append_after_delete_middle():
    ll = LinkedList()
    for d in [0, 1, 2]:
        ll.append(d)
    ll.delete(1)          # list becomes [0, 2]
    ll.append(3)          # append 3 -> [0, 2, 3]
    assert ll.to_list() == [0, 2, 3]

def test_delete_after_prepend_and_append():
    ll = LinkedList()
    ll.prepend(0)         # list: [0]
    ll.append(1)          # list: [0, 1]
    assert ll.delete(1) is True
    assert ll.to_list() == [0]

def test_find_after_prepend_and_append():
    ll = LinkedList()
    ll.prepend(0)         # list: [0]
    ll.append(1)          # list: [0, 1]
    assert ll.find(1) == 1

def test_get_after_prepend_and_append():
    ll = LinkedList()
    ll.prepend(0)         # list: [0]
    ll.append(1)          # list: [0, 1]
    assert ll.get(1) == 1

import pytest
from data.input_code.d03_linked_list import *

def test_delete_head_none_on_empty():
    ll = LinkedList()
    assert ll.delete(None) is False

def test_delete_middle_none_not_present():
    ll = LinkedList()
    for d in [1, 2, 3]:
        ll.append(d)
    assert ll.delete(None) is False

def test_get_after_delete_head_none():
    ll = LinkedList()
    ll.append(None)
    ll.append(None)
    ll.append(1)
    ll.delete(None)  # delete head None
    assert ll.get(0) is None

def test_get_after_delete_middle_none():
    ll = LinkedList()
    ll.append(0)
    ll.append(None)
    ll.append(None)
    ll.append(1)
    ll.delete(None)  # delete first middle None
    assert ll.get(1) is None

def test_find_after_delete_head_none():
    ll = LinkedList()
    ll.append(None)
    ll.append(1)
    ll.delete(None)  # delete head None
    assert ll.find(None) == -1

def test_find_after_delete_middle_none():
    ll = LinkedList()
    ll.append(0)
    ll.append(None)
    ll.append(1)
    ll.delete(None)  # delete middle None
    assert ll.find(None) == -1

def test_prepend_after_delete_head_none():
    ll = LinkedList()
    ll.append(None)
    ll.append(2)
    ll.delete(None)  # delete head None
    ll.prepend(0)
    assert ll.to_list() == [0, 2]

def test_prepend_after_delete_middle_none():
    ll = LinkedList()
    ll.append(0)
    ll.append(None)
    ll.append(2)
    ll.delete(None)  # delete middle None
    ll.prepend(0)
    assert ll.to_list() == [0, 0, 2]

def test_append_after_delete_head_none():
    ll = LinkedList()
    ll.append(None)
    ll.append(2)
    ll.delete(None)  # delete head None
    ll.append(0)
    assert ll.to_list() == [2, 0]

def test_append_after_delete_middle_none():
    ll = LinkedList()
    ll.append(0)
    ll.append(None)
    ll.append(2)
    ll.delete(None)  # delete middle None
    ll.append(0)
    assert ll.to_list() == [0, 2, 0]