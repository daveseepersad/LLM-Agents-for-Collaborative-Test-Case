import pytest
from data.input_code.d03_linked_list import *

@pytest.mark.parametrize('data', [1, 2])
def test_linked_list_append(data):
    linked_list = LinkedList()
    linked_list.append(data)
    assert linked_list.to_list() == [data]

@pytest.mark.parametrize('data', [0])
def test_linked_list_prepend(data):
    linked_list = LinkedList()
    linked_list.prepend(data)
    assert linked_list.to_list() == [data]

@pytest.mark.parametrize('data, expected', [(99, False)])
def test_linked_list_delete_on_empty(data, expected):
    linked_list = LinkedList()
    assert linked_list.delete(data) == expected

@pytest.mark.parametrize('data, expected', [(5, -1)])
def test_linked_list_find_on_empty(data, expected):
    linked_list = LinkedList()
    assert linked_list.find(data) == expected

def test_linked_list_get_index_out_of_bounds():
    linked_list = LinkedList()
    with pytest.raises(IndexError):
        linked_list.get(0)

@pytest.mark.parametrize('expected', [[]])
def test_linked_list_to_list_on_empty(expected):
    linked_list = LinkedList()
    assert linked_list.to_list() == expected

@pytest.mark.parametrize('expected', [0])
def test_linked_list_len_on_empty(expected):
    linked_list = LinkedList()
    assert len(linked_list) == expected

def test_linked_list_append_another_empty():
    linked_list = LinkedList()
    linked_list.append(1)
    linked_list.append(2)
    assert linked_list.to_list() == [1, 2]

@pytest.mark.parametrize('data, expected', [(999, False)])
def test_linked_list_delete_nonexistent(data, expected):
    linked_list = LinkedList()
    linked_list.append(1)
    linked_list.append(2)
    assert linked_list.delete(data) == expected

import pytest
from data.input_code.d03_linked_list import *

@pytest.mark.parametrize('data, expected', [(1, True)])
def test_linked_list_delete_head(data, expected):
    linked_list = LinkedList()
    linked_list.append(1)
    linked_list.append(2)
    linked_list.append(3)
    assert linked_list.delete(data) == expected

@pytest.mark.parametrize('data, expected', [(2, True)])
def test_linked_list_delete_middle(data, expected):
    linked_list = LinkedList()
    linked_list.append(1)
    linked_list.append(2)
    linked_list.append(3)
    assert linked_list.delete(data) == expected

@pytest.mark.parametrize('data, expected', [(3, True)])
def test_linked_list_delete_last(data, expected):
    linked_list = LinkedList()
    linked_list.append(1)
    linked_list.append(2)
    linked_list.append(3)
    assert linked_list.delete(data) == expected

@pytest.mark.parametrize('data, expected', [(2, 1)])
def test_linked_list_find_middle(data, expected):
    linked_list = LinkedList()
    linked_list.append(1)
    linked_list.append(2)
    linked_list.append(3)
    assert linked_list.find(data) == expected

@pytest.mark.parametrize('data, expected', [(4, -1)])
def test_linked_list_find_not_found(data, expected):
    linked_list = LinkedList()
    linked_list.append(1)
    linked_list.append(2)
    linked_list.append(3)
    assert linked_list.find(data) == expected

@pytest.mark.parametrize('index, expected', [(1, 2)])
def test_linked_list_get_valid(index, expected):
    linked_list = LinkedList()
    linked_list.append(1)
    linked_list.append(2)
    linked_list.append(3)
    assert linked_list.get(index) == expected

def test_linked_list_get_neg_index():
    linked_list = LinkedList()
    linked_list.append(5)
    linked_list.append(6)
    with pytest.raises(IndexError):
        linked_list.get(-1)