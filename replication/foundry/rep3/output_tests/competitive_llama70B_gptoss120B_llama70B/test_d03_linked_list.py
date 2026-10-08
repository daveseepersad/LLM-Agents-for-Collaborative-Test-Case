import pytest
from data.input_code.d03_linked_list import *

@pytest.fixture
def empty_list():
    return LinkedList()

@pytest.fixture
def list_after_append():
    ll = LinkedList()
    ll.append(1)
    ll.append(2)
    return ll

@pytest.fixture
def list_after_prepend():
    ll = LinkedList()
    ll.prepend(0)   # prepend to empty list
    ll.prepend(3)   # prepend to non‑empty list
    return ll

@pytest.fixture
def full_list():
    ll = LinkedList()
    ll.prepend(0)   # empty prepend
    ll.prepend(3)   # non‑empty prepend
    ll.append(1)
    ll.append(2)
    return ll

def test_init(empty_list):
    assert empty_list.head is None
    assert len(empty_list) == 0

def test_append_to_empty(empty_list):
    empty_list.append(1)
    assert empty_list.head is not None
    assert empty_list.head.data == 1
    assert len(empty_list) == 1

def test_append_to_non_empty(list_after_append):
    # list already has [1, 2]; append another element
    list_after_append.append(3)
    assert list_after_append.head.next.next.data == 3
    assert len(list_after_append) == 3

def test_prepend_to_empty(empty_list):
    empty_list.prepend(0)
    assert empty_list.head is not None
    assert empty_list.head.data == 0
    assert len(empty_list) == 1

def test_prepend_to_non_empty(list_after_prepend):
    # list currently is [3, 0]; prepend another element
    list_after_prepend.prepend(5)
    assert list_after_prepend.head.data == 5
    assert len(list_after_prepend) == 3

@pytest.mark.parametrize('data, expected', [
    (1, True),   # existing node
    (4, False),  # non‑existing node
])
def test_delete(full_list, data, expected):
    result = full_list.delete(data)
    assert result is expected
    # verify size adjustment when deletion succeeds
    if expected:
        assert len(full_list) == 3
    else:
        assert len(full_list) == 4

@pytest.mark.parametrize('data, expected', [
    (2, 1),   # existing in append‑only list
    (5, -1),  # non‑existing
])
def test_find(list_after_append, data, expected):
    assert list_after_append.find(data) == expected

@pytest.mark.parametrize('index, expected', [
    (0, 3),   # valid index in full list
])
def test_get_success(full_list, index, expected):
    assert full_list.get(index) == expected

def test_get_negative_index(full_list):
    with pytest.raises(IndexError):
        full_list.get(-1)

def test_get_out_of_range(full_list):
    with pytest.raises(IndexError):
        full_list.get(10)

def test_to_list(full_list):
    assert full_list.to_list() == [3, 0, 1, 2]

def test_len(full_list):
    assert len(full_list) == 4

import pytest

def test_delete_empty(empty_list):
    result = empty_list.delete(1)
    assert result is False
    assert len(empty_list) == 0

def test_find_empty(empty_list):
    assert empty_list.find(1) == -1

def test_get_empty(empty_list):
    with pytest.raises(IndexError):
        empty_list.get(0)

def test_prepend_twice(list_after_prepend):
    # list_after_prepend initially [3, 0]
    for val in [1, 2]:
        list_after_prepend.prepend(val)
    assert list_after_prepend.to_list() == [2, 1, 3, 0]
    assert len(list_after_prepend) == 4

def test_to_list_empty(empty_list):
    assert empty_list.to_list() == []

def test_delete_head(full_list):
    result = full_list.delete(3)
    assert result is True
    assert len(full_list) == 3
    assert full_list.head.data == 0
    assert full_list.to_list() == [0, 1, 2]

def test_get_last_index(full_list):
    assert full_list.get(3) == 2

def test_find_head(full_list):
    assert full_list.find(3) == 0