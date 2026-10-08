import pytest
from data.input_code.d03_linked_list import *

def test_linked_list_init():
    linked_list = LinkedList()
    assert linked_list.head is None
    assert len(linked_list) == 0

@pytest.mark.parametrize('data', [1, 2])
def test_linked_list_append(data):
    linked_list = LinkedList()
    linked_list.append(data)
    assert linked_list.to_list() == [data]

@pytest.mark.parametrize('data', [0, -1])
def test_linked_list_prepend(data):
    linked_list = LinkedList()
    linked_list.append(1)
    linked_list.prepend(data)
    assert linked_list.to_list() == [data, 1]

def test_linked_list_delete_existing():
    linked_list = LinkedList()
    linked_list.append(1)
    assert linked_list.delete(1) == True
    assert linked_list.to_list() == []

def test_linked_list_delete_non_existing():
    linked_list = LinkedList()
    linked_list.append(1)
    assert linked_list.delete(10) == False
    assert linked_list.to_list() == [1]

def test_linked_list_find_existing():
    linked_list = LinkedList()
    linked_list.append(1)
    linked_list.prepend(0)
    linked_list.prepend(-1)
    assert linked_list.find(1) == 2

def test_linked_list_find_non_existing():
    linked_list = LinkedList()
    linked_list.append(1)
    assert linked_list.find(10) == -1

def test_linked_list_get_valid_index():
    linked_list = LinkedList()
    linked_list.prepend(0)
    linked_list.prepend(-1)
    linked_list.append(1)
    linked_list.append(2)
    assert linked_list.get(0) == -1

def test_linked_list_get_invalid_index():
    linked_list = LinkedList()
    linked_list.append(1)
    with pytest.raises(IndexError):
        linked_list.get(10)

def test_linked_list_to_list():
    linked_list = LinkedList()
    linked_list.prepend(0)
    linked_list.prepend(-1)
    linked_list.append(1)
    linked_list.append(2)
    assert linked_list.to_list() == [-1, 0, 1, 2]

def test_linked_list_len():
    linked_list = LinkedList()
    linked_list.prepend(0)
    linked_list.prepend(-1)
    linked_list.append(1)
    linked_list.append(2)
    assert len(linked_list) == 4

import pytest
from data.input_code.d03_linked_list import *

def test_linked_list_delete_head_node():
    linked_list = LinkedList()
    linked_list.append(1)
    linked_list.append(2)
    assert linked_list.delete(1) == True
    assert linked_list.to_list() == [2]

def test_linked_list_prepend_none():
    linked_list = LinkedList()
    linked_list.prepend(None)
    assert linked_list.to_list() == [None]

def test_linked_list_get_negative_index():
    linked_list = LinkedList()
    linked_list.append(1)
    with pytest.raises(IndexError):
        linked_list.get(-1)

def test_linked_list_find_none():
    linked_list = LinkedList()
    linked_list.append(1)
    assert linked_list.find(None) == -1

def test_linked_list_delete_none():
    linked_list = LinkedList()
    linked_list.append(1)
    assert linked_list.delete(None) == False
    assert linked_list.to_list() == [1]

def test_linked_list_append_none():
    linked_list = LinkedList()
    linked_list.append(None)
    assert linked_list.to_list() == [None]

def test_linked_list_get_index_equal_to_size():
    linked_list = LinkedList()
    linked_list.append(1)
    with pytest.raises(IndexError):
        linked_list.get(1)

import pytest
from data.input_code.d03_linked_list import *

def test_linked_list_delete_empty():
    linked_list = LinkedList()
    assert linked_list.delete(1) == False

def test_linked_list_prepend_none_to_empty():
    linked_list = LinkedList()
    linked_list.prepend(None)
    assert linked_list.to_list() == [None]

def test_linked_list_find_in_empty():
    linked_list = LinkedList()
    assert linked_list.find(1) == -1

def test_linked_list_get_index_zero_from_empty():
    linked_list = LinkedList()
    with pytest.raises(IndexError):
        linked_list.get(0)

def test_linked_list_to_list_empty():
    linked_list = LinkedList()
    assert linked_list.to_list() == []

def test_linked_list_delete_head_with_multiple_nodes():
    linked_list = LinkedList()
    linked_list.append(1)
    linked_list.append(2)
    linked_list.append(3)
    assert linked_list.delete(1) == True
    assert linked_list.to_list() == [2, 3]

def test_linked_list_delete_middle_node():
    linked_list = LinkedList()
    linked_list.append(1)
    linked_list.append(2)
    linked_list.append(3)
    assert linked_list.delete(2) == True
    assert linked_list.to_list() == [1, 3]

def test_linked_list_delete_tail_node():
    linked_list = LinkedList()
    linked_list.append(1)
    linked_list.append(2)
    linked_list.append(3)
    assert linked_list.delete(3) == True
    assert linked_list.to_list() == [1, 2]

import pytest
from data.input_code.d03_linked_list import *

def test_linked_list_delete_head_with_none():
    linked_list = LinkedList()
    linked_list.append(None)
    linked_list.append(1)
    assert linked_list.delete(None) == True
    assert linked_list.to_list() == [1]

def test_linked_list_prepend_after_delete():
    linked_list = LinkedList()
    linked_list.append(1)
    linked_list.delete(1)
    linked_list.prepend(1)
    assert linked_list.to_list() == [1]

def test_linked_list_append_after_delete():
    linked_list = LinkedList()
    linked_list.append(1)
    linked_list.delete(1)
    linked_list.append(1)
    assert linked_list.to_list() == [1]

def test_linked_list_find_after_delete():
    linked_list = LinkedList()
    linked_list.append(1)
    linked_list.delete(1)
    assert linked_list.find(1) == -1

def test_linked_list_get_after_delete():
    linked_list = LinkedList()
    linked_list.append(1)
    linked_list.append(2)
    linked_list.delete(1)
    assert linked_list.get(0) == 2

def test_linked_list_delete_middle_with_none():
    linked_list = LinkedList()
    linked_list.append(1)
    linked_list.append(None)
    linked_list.append(2)
    assert linked_list.delete(None) == True
    assert linked_list.to_list() == [1, 2]

def test_linked_list_delete_tail_with_none():
    linked_list = LinkedList()
    linked_list.append(1)
    linked_list.append(2)
    linked_list.append(None)
    assert linked_list.delete(None) == True
    assert linked_list.to_list() == [1, 2]

def test_linked_list_prepend_none_after_prepend_none():
    linked_list = LinkedList()
    linked_list.prepend(None)
    linked_list.prepend(None)
    assert linked_list.to_list() == [None, None]

def test_linked_list_append_none_after_append_none():
    linked_list = LinkedList()
    linked_list.append(None)
    linked_list.append(None)
    assert linked_list.to_list() == [None, None]

import pytest
from data.input_code.d03_linked_list import *

def test_linked_list_len_empty():
    linked_list = LinkedList()
    assert len(linked_list) == 0

def test_linked_list_get_after_prepend():
    linked_list = LinkedList()
    linked_list.prepend(1)
    assert linked_list.get(0) == 1

def test_linked_list_delete_after_append():
    linked_list = LinkedList()
    linked_list.append(1)
    assert linked_list.delete(None) == False

def test_linked_list_find_after_prepend():
    linked_list = LinkedList()
    linked_list.prepend(1)
    assert linked_list.find(None) == -1

def test_linked_list_to_list_after_delete():
    linked_list = LinkedList()
    assert linked_list.to_list() == []

import pytest
from data.input_code.d03_linked_list import *

def test_linked_list_delete_multiple_nodes():
    linked_list = LinkedList()
    linked_list.append(1)
    linked_list.append(1)
    linked_list.append(2)
    assert linked_list.delete(1) == True
    assert linked_list.to_list() == [1, 2]

def test_linked_list_prepend_after_prepend():
    linked_list = LinkedList()
    linked_list.prepend(1)
    linked_list.prepend(1)
    linked_list.prepend(2)
    assert linked_list.to_list() == [2, 1, 1]

def test_linked_list_append_after_append():
    linked_list = LinkedList()
    linked_list.append(1)
    linked_list.append(1)
    linked_list.append(2)
    assert linked_list.to_list() == [1, 1, 2]

def test_linked_list_get_after_get():
    linked_list = LinkedList()
    linked_list.append(1)
    linked_list.append(2)
    linked_list.append(3)
    linked_list.get(0)
    assert linked_list.get(1) == 2

def test_linked_list_find_after_find():
    linked_list = LinkedList()
    linked_list.append(1)
    linked_list.append(2)
    linked_list.append(3)
    linked_list.find(1)
    assert linked_list.find(2) == 1

def test_linked_list_delete_after_delete():
    linked_list = LinkedList()
    linked_list.append(1)
    linked_list.append(2)
    linked_list.append(2)
    linked_list.delete(1)
    assert linked_list.delete(2) == True
    assert linked_list.to_list() == [2]

def test_linked_list_to_list_after_to_list():
    linked_list = LinkedList()
    linked_list.append(1)
    linked_list.append(2)
    linked_list.append(3)
    linked_list.to_list()
    assert linked_list.to_list() == [1, 2, 3]

def test_linked_list_len_after_len():
    linked_list = LinkedList()
    linked_list.append(1)
    linked_list.append(2)
    linked_list.append(3)
    len(linked_list)
    assert len(linked_list) == 3