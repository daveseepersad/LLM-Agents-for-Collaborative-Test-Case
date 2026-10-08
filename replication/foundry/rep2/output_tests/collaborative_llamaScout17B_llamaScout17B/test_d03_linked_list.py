import pytest
from data.input_code.d03_linked_list import *

@pytest.mark.parametrize('expected_head, expected_size', [
    (None, 0)
])
def test_linked_list_init(expected_head, expected_size):
    linked_list = LinkedList()
    assert linked_list.head == expected_head
    assert linked_list._size == expected_size

@pytest.mark.parametrize('data', [
    5
])
def test_linked_list_append_empty(data):
    linked_list = LinkedList()
    linked_list.append(data)
    assert linked_list.head.data == data
    assert linked_list._size == 1

@pytest.mark.parametrize('data, expected_size', [
    (10, 2)
])
def test_linked_list_append_nonempty(data, expected_size):
    linked_list = LinkedList()
    linked_list.append(5)
    linked_list.append(data)
    assert linked_list._size == expected_size

@pytest.mark.parametrize('data', [
    5
])
def test_linked_list_prepend_empty(data):
    linked_list = LinkedList()
    linked_list.prepend(data)
    assert linked_list.head.data == data
    assert linked_list._size == 1

@pytest.mark.parametrize('data, expected_size', [
    (10, 2)
])
def test_linked_list_prepend_nonempty(data, expected_size):
    linked_list = LinkedList()
    linked_list.append(5)
    linked_list.prepend(data)
    assert linked_list.head.data == data
    assert linked_list._size == expected_size

@pytest.mark.parametrize('data, expected', [
    (5, False)
])
def test_linked_list_delete_empty(data, expected):
    linked_list = LinkedList()
    assert linked_list.delete(data) == expected

@pytest.mark.parametrize('data, expected', [
    (5, True)
])
def test_linked_list_delete_head(data, expected):
    linked_list = LinkedList()
    linked_list.append(data)
    assert linked_list.delete(data) == expected
    assert linked_list.head is None

@pytest.mark.parametrize('data, expected', [
    (10, True)
])
def test_linked_list_delete_nonhead(data, expected):
    linked_list = LinkedList()
    linked_list.append(5)
    linked_list.append(data)
    assert linked_list.delete(data) == expected

@pytest.mark.parametrize('data, expected', [
    (15, False)
])
def test_linked_list_delete_notfound(data, expected):
    linked_list = LinkedList()
    linked_list.append(5)
    assert linked_list.delete(data) == expected

@pytest.mark.parametrize('data, expected', [
    (5, -1)
])
def test_linked_list_find_empty(data, expected):
    linked_list = LinkedList()
    assert linked_list.find(data) == expected

@pytest.mark.parametrize('data, expected', [
    (10, 1)
])
def test_linked_list_find_found(data, expected):
    linked_list = LinkedList()
    linked_list.append(5)
    linked_list.append(data)
    assert linked_list.find(data) == expected

@pytest.mark.parametrize('data, expected', [
    (15, -1)
])
def test_linked_list_find_notfound(data, expected):
    linked_list = LinkedList()
    linked_list.append(5)
    assert linked_list.find(data) == expected

@pytest.mark.parametrize('index, expected', [
    (1, 10)
])
def test_linked_list_get_valid(index, expected):
    linked_list = LinkedList()
    linked_list.append(5)
    linked_list.append(expected)
    assert linked_list.get(index) == expected

@pytest.mark.parametrize('index, expected_exception', [
    (-1, IndexError),
    (2, IndexError)
])
def test_linked_list_get_invalid(index, expected_exception):
    linked_list = LinkedList()
    linked_list.append(5)
    linked_list.append(10)
    with pytest.raises(expected_exception):
        linked_list.get(index)

@pytest.mark.parametrize('expected', [
    []
])
def test_linked_list_to_list_empty(expected):
    linked_list = LinkedList()
    assert linked_list.to_list() == expected

@pytest.mark.parametrize('expected', [
    [5, 10]
])
def test_linked_list_to_list_nonempty(expected):
    linked_list = LinkedList()
    linked_list.append(5)
    linked_list.append(10)
    assert linked_list.to_list() == expected

@pytest.mark.parametrize('expected', [
    0
])
def test_linked_list_len_empty(expected):
    linked_list = LinkedList()
    assert len(linked_list) == expected

@pytest.mark.parametrize('expected', [
    2
])
def test_linked_list_len_nonempty(expected):
    linked_list = LinkedList()
    linked_list.append(5)
    linked_list.append(10)
    assert len(linked_list) == expected

import pytest
from data.input_code.d03_linked_list import *

@pytest.mark.parametrize('data, expected', [
    (5, True)
])
def test_linked_list_delete_multiple(data, expected):
    linked_list = LinkedList()
    linked_list.append(data)
    linked_list.append(data)
    linked_list.append(10)
    assert linked_list.delete(data) == expected

@pytest.mark.parametrize('index, expected', [
    (0, 5)
])
def test_linked_list_get_edge(index, expected):
    linked_list = LinkedList()
    linked_list.append(expected)
    linked_list.append(10)
    assert linked_list.get(index) == expected

@pytest.mark.parametrize('expected', [
    1
])
def test_linked_list_len_after_delete(expected):
    linked_list = LinkedList()
    linked_list.append(5)
    linked_list.append(10)
    linked_list.delete(5)
    assert len(linked_list) == expected

import pytest
from data.input_code.d03_linked_list import *

@pytest.mark.parametrize('data, expected', [
    (10, True)
])
def test_linked_list_delete_multiple_nonhead(data, expected):
    linked_list = LinkedList()
    linked_list.append(5)
    linked_list.append(data)
    linked_list.append(data)
    linked_list.append(15)
    assert linked_list.delete(data) == expected

@pytest.mark.parametrize('data, expected', [
    (5, 0)
])
def test_linked_list_find_multiple_occurrences(data, expected):
    linked_list = LinkedList()
    linked_list.append(data)
    linked_list.append(data)
    linked_list.append(10)
    assert linked_list.find(data) == expected

@pytest.mark.parametrize('data', [
    10
])
def test_linked_list_prepend_multiple_times(data):
    linked_list = LinkedList()
    linked_list.append(5)
    linked_list.prepend(data)
    linked_list.prepend(data)
    assert linked_list.head.data == data
    assert linked_list._size == 3

@pytest.mark.parametrize('data', [
    15
])
def test_linked_list_append_multiple_times(data):
    linked_list = LinkedList()
    linked_list.append(5)
    linked_list.append(data)
    linked_list.append(data)
    assert linked_list._size == 3

@pytest.mark.parametrize('expected', [
    0
])
def test_linked_list_len_after_multiple_deletes(expected):
    linked_list = LinkedList()
    linked_list.append(5)
    linked_list.append(10)
    linked_list.append(15)
    linked_list.delete(5)
    linked_list.delete(10)
    linked_list.delete(15)
    assert len(linked_list) == expected

import pytest
from data.input_code.d03_linked_list import *

@pytest.mark.parametrize('data, expected', [
    (5, True)
])
def test_linked_list_delete_head_multiple(data, expected):
    linked_list = LinkedList()
    linked_list.append(data)
    linked_list.append(data)
    linked_list.append(10)
    assert linked_list.delete(data) == expected
    assert linked_list.head.data == data

@pytest.mark.parametrize('index, expected', [
    (1, 10)
])
def test_linked_list_get_middle_index(index, expected):
    linked_list = LinkedList()
    linked_list.append(5)
    linked_list.append(expected)
    linked_list.append(15)
    assert linked_list.get(index) == expected

@pytest.mark.parametrize('expected', [
    1
])
def test_linked_list_len_after_prepend(expected):
    linked_list = LinkedList()
    linked_list.prepend(5)
    assert len(linked_list) == expected

@pytest.mark.parametrize('expected', [
    [5]
])
def test_linked_list_to_list_single_element(expected):
    linked_list = LinkedList()
    linked_list.append(5)
    assert linked_list.to_list() == expected

@pytest.mark.parametrize('data, expected', [
    (5, 0)
])
def test_linked_list_find_head(data, expected):
    linked_list = LinkedList()
    linked_list.append(data)
    linked_list.append(10)
    assert linked_list.find(data) == expected

import pytest
from data.input_code.d03_linked_list import *

@pytest.mark.parametrize('data, expected', [
    (10, True)
])
def test_linked_list_delete_last_node(data, expected):
    linked_list = LinkedList()
    linked_list.append(5)
    linked_list.append(data)
    assert linked_list.delete(data) == expected

@pytest.mark.parametrize('index, expected', [
    (2, 15)
])
def test_linked_list_get_last_index(index, expected):
    linked_list = LinkedList()
    linked_list.append(5)
    linked_list.append(10)
    linked_list.append(expected)
    assert linked_list.get(index) == expected

@pytest.mark.parametrize('expected', [
    1
])
def test_linked_list_len_after_append(expected):
    linked_list = LinkedList()
    linked_list.append(5)
    assert len(linked_list) == expected

@pytest.mark.parametrize('data', [
    5
])
def test_linked_list_prepend_empty_list_size_check(data):
    linked_list = LinkedList()
    linked_list.prepend(data)
    assert linked_list._size == 1

@pytest.mark.parametrize('data', [
    20
])
def test_linked_list_append_multiple_times_different_data(data):
    linked_list = LinkedList()
    linked_list.append(5)
    linked_list.append(10)
    linked_list.append(data)
    assert linked_list._size == 3

@pytest.mark.parametrize('data, expected', [
    (20, -1)
])
def test_linked_list_find_not_found_in_multiple_occurrences(data, expected):
    linked_list = LinkedList()
    linked_list.append(5)
    linked_list.append(10)
    linked_list.append(10)
    linked_list.append(15)
    assert linked_list.find(data) == expected

@pytest.mark.parametrize('expected', [
    [10]
])
def test_linked_list_to_list_after_delete(expected):
    linked_list = LinkedList()
    linked_list.append(5)
    linked_list.append(10)
    linked_list.delete(5)
    assert linked_list.to_list() == expected

@pytest.mark.parametrize('data, expected', [
    (5, False)
])
def test_linked_list_delete_non_existent_in_empty_list(data, expected):
    linked_list = LinkedList()
    assert linked_list.delete(data) == expected

import pytest
from data.input_code.d03_linked_list import *

@pytest.mark.parametrize('data, expected', [
    (5, True)
])
def test_linked_list_delete_single_element_list(data, expected):
    linked_list = LinkedList()
    linked_list.append(data)
    assert linked_list.delete(data) == expected
    assert linked_list.head is None

@pytest.mark.parametrize('index, expected', [
    (0, 5)
])
def test_linked_list_get_single_element_list(index, expected):
    linked_list = LinkedList()
    linked_list.append(expected)
    assert linked_list.get(index) == expected

@pytest.mark.parametrize('expected', [
    1
])
def test_linked_list_len_after_single_append(expected):
    linked_list = LinkedList()
    linked_list.append(5)
    assert len(linked_list) == expected

@pytest.mark.parametrize('expected', [
    []
])
def test_linked_list_to_list_single_element_after_delete(expected):
    linked_list = LinkedList()
    linked_list.append(5)
    linked_list.delete(5)
    assert linked_list.to_list() == expected

@pytest.mark.parametrize('data, expected_size', [
    (5, 3)
])
def test_linked_list_prepend_same_data_multiple_times_size_check(data, expected_size):
    linked_list = LinkedList()
    linked_list.prepend(data)
    linked_list.prepend(data)
    linked_list.prepend(data)
    assert linked_list._size == expected_size

@pytest.mark.parametrize('data, expected_size', [
    (5, 3)
])
def test_linked_list_append_same_data_multiple_times_size_check(data, expected_size):
    linked_list = LinkedList()
    linked_list.append(data)
    linked_list.append(data)
    linked_list.append(data)
    assert linked_list._size == expected_size

@pytest.mark.parametrize('data, expected', [
    (10, 1)
])
def test_linked_list_find_multiple_occurrences_edge_case(data, expected):
    linked_list = LinkedList()
    linked_list.append(5)
    linked_list.append(data)
    linked_list.append(data)
    assert linked_list.find(data) == expected

@pytest.mark.parametrize('data, expected', [
    (10, True)
])
def test_linked_list_delete_multiple_occurrences_edge_case(data, expected):
    linked_list = LinkedList()
    linked_list.append(5)
    linked_list.append(data)
    linked_list.append(data)
    assert linked_list.delete(data) == expected

import pytest
from data.input_code.d03_linked_list import *

@pytest.mark.parametrize('data, expected', [
    (10, True)
])
def test_linked_list_delete_size_check(data, expected):
    linked_list = LinkedList()
    linked_list.append(5)
    linked_list.append(data)
    assert linked_list.delete(data) == expected
    assert len(linked_list) == 1

@pytest.mark.parametrize('data, expected', [
    (5, 0)
])
def test_linked_list_find_edge_case_head(data, expected):
    linked_list = LinkedList()
    linked_list.append(data)
    assert linked_list.find(data) == expected

@pytest.mark.parametrize('data, expected', [
    (5, True)
])
def test_linked_list_get_size_check_after_delete_head(data, expected):
    linked_list = LinkedList()
    linked_list.append(data)
    linked_list.append(10)
    assert linked_list.delete(data) == expected
    assert len(linked_list) == 1

@pytest.mark.parametrize('data, expected', [
    (10, 3)
])
def test_linked_list_prepend_size_check_multiple(data, expected):
    linked_list = LinkedList()
    linked_list.append(5)
    linked_list.prepend(data)
    linked_list.prepend(data)
    assert linked_list._size == expected

@pytest.mark.parametrize('data, expected', [
    (5, 1)
])
def test_linked_list_append_size_check_single_element(data, expected):
    linked_list = LinkedList()
    linked_list.append(data)
    assert linked_list._size == expected

@pytest.mark.parametrize('expected', [
    [5, 10, 15]
])
def test_linked_list_to_list_after_multiple_appends(expected):
    linked_list = LinkedList()
    linked_list.append(5)
    linked_list.append(10)
    linked_list.append(15)
    assert linked_list.to_list() == expected

@pytest.mark.parametrize('expected', [
    3
])
def test_linked_list_len_after_multiple_prepends(expected):
    linked_list = LinkedList()
    linked_list.prepend(5)
    linked_list.prepend(10)
    linked_list.prepend(15)
    assert len(linked_list) == expected

@pytest.mark.parametrize('data, expected', [
    (10, False)
])
def test_linked_list_delete_not_found_in_single_element_list(data, expected):
    linked_list = LinkedList()
    linked_list.append(5)
    assert linked_list.delete(data) == expected

@pytest.mark.parametrize('index, expected_exception', [
    (0, IndexError)
])
def test_linked_list_get_invalid_index_zero_in_empty_list(index, expected_exception):
    linked_list = LinkedList()
    with pytest.raises(expected_exception):
        linked_list.get(index)

@pytest.mark.parametrize('data, expected', [
    (10, -1)
])
def test_linked_list_find_in_single_element_list_not_found(data, expected):
    linked_list = LinkedList()
    linked_list.append(5)
    assert linked_list.find(data) == expected

import pytest
from data.input_code.d03_linked_list import *

@pytest.mark.parametrize('data, expected', [
    (5, True)
])
def test_linked_list_delete_size_check_head(data, expected):
    linked_list = LinkedList()
    linked_list.append(data)
    linked_list.append(10)
    assert linked_list.delete(data) == expected
    assert len(linked_list) == 1

@pytest.mark.parametrize('index, expected', [
    (0, 5)
])
def test_linked_list_get_boundary_zero(index, expected):
    linked_list = LinkedList()
    linked_list.append(expected)
    linked_list.append(10)
    assert linked_list.get(index) == expected

@pytest.mark.parametrize('data', [
    5
])
def test_linked_list_prepend_size_update(data):
    linked_list = LinkedList()
    linked_list.prepend(data)
    assert linked_list._size == 1

@pytest.mark.parametrize('data', [
    5
])
def test_linked_list_append_size_update(data):
    linked_list = LinkedList()
    linked_list.append(data)
    assert linked_list._size == 1

@pytest.mark.parametrize('expected', [
    0
])
def test_linked_list_len_after_single_delete(expected):
    linked_list = LinkedList()
    linked_list.append(5)
    linked_list.delete(5)
    assert len(linked_list) == expected

@pytest.mark.parametrize('expected', [
    [15, 10, 5]
])
def test_linked_list_to_list_after_prepend(expected):
    linked_list = LinkedList()
    linked_list.append(5)
    linked_list.prepend(10)
    linked_list.prepend(15)
    assert linked_list.to_list() == expected

import pytest
from data.input_code.d03_linked_list import *

@pytest.mark.parametrize('data, expected', [
    (5, True)
])
def test_linked_list_delete_last_element_size_check(data, expected):
    linked_list = LinkedList()
    linked_list.append(data)
    assert linked_list.delete(data) == expected
    assert len(linked_list) == 0

@pytest.mark.parametrize('index, expected', [
    (2, 15)
])
def test_linked_list_get_last_index_size_check(index, expected):
    linked_list = LinkedList()
    linked_list.append(5)
    linked_list.append(10)
    linked_list.append(expected)
    assert linked_list.get(index) == expected
    assert len(linked_list) == 3

@pytest.mark.parametrize('data, expected', [
    (5, 5)
])
def test_linked_list_prepend_empty_list_head_check(data, expected):
    linked_list = LinkedList()
    linked_list.prepend(data)
    assert linked_list.head.data == expected

@pytest.mark.parametrize('data, expected', [
    (10, 2)
])
def test_linked_list_append_single_element_list_size_check(data, expected):
    linked_list = LinkedList()
    linked_list.append(5)
    linked_list.append(data)
    assert linked_list._size == expected

@pytest.mark.parametrize('data, expected', [
    (5, 0)
])
def test_linked_list_find_single_occurrence_edge_case(data, expected):
    linked_list = LinkedList()
    linked_list.append(data)
    assert linked_list.find(data) == expected

@pytest.mark.parametrize('expected', [
    0
])
def test_linked_list_len_after_append_and_delete(expected):
    linked_list = LinkedList()
    linked_list.append(5)
    linked_list.delete(5)
    assert len(linked_list) == expected

import pytest
from data.input_code.d03_linked_list import *

@pytest.mark.parametrize('data, expected', [
    (10, True)
])
def test_linked_list_delete_non_consecutive_duplicates(data, expected):
    linked_list = LinkedList()
    linked_list.append(5)
    linked_list.append(data)
    linked_list.append(15)
    linked_list.append(data)
    assert linked_list.delete(data) == expected

@pytest.mark.parametrize('index, expected', [
    (0, 10)
])
def test_linked_list_get_after_delete(index, expected):
    linked_list = LinkedList()
    linked_list.append(5)
    linked_list.append(expected)
    linked_list.delete(5)
    assert linked_list.get(index) == expected

@pytest.mark.parametrize('expected', [
    2
])
def test_linked_list_len_after_multiple_appends_and_deletes(expected):
    linked_list = LinkedList()
    linked_list.append(5)
    linked_list.append(10)
    linked_list.append(15)
    linked_list.delete(5)
    assert len(linked_list) == expected

@pytest.mark.parametrize('data, expected', [
    (5, -1)
])
def test_linked_list_find_after_delete(data, expected):
    linked_list = LinkedList()
    linked_list.append(data)
    linked_list.append(10)
    linked_list.delete(data)
    assert linked_list.find(data) == expected

@pytest.mark.parametrize('expected', [
    [10, 15]
])
def test_linked_list_to_list_after_multiple_operations(expected):
    linked_list = LinkedList()
    linked_list.append(5)
    linked_list.append(10)
    linked_list.append(15)
    linked_list.delete(5)
    assert linked_list.to_list() == expected

import pytest
from data.input_code.d03_linked_list import *

@pytest.mark.parametrize('data, expected', [
    (20, False)
])
def test_linked_list_delete_missing_node_in_multiple_element_list(data, expected):
    linked_list = LinkedList()
    linked_list.append(5)
    linked_list.append(10)
    linked_list.append(15)
    assert linked_list.delete(data) == expected

@pytest.mark.parametrize('index, expected_exception', [
    (1, IndexError)
])
def test_linked_list_get_invalid_index_in_single_element_list(index, expected_exception):
    linked_list = LinkedList()
    linked_list.append(5)
    with pytest.raises(expected_exception):
        linked_list.get(index)



@pytest.mark.parametrize('data, expected', [
    (None, -1)
])
def test_linked_list_find_null_data(data, expected):
    linked_list = LinkedList()
    linked_list.append(5)
    linked_list.append(10)
    assert linked_list.find(data) == expected

@pytest.mark.parametrize('data, expected', [
    (None, False)
])
def test_linked_list_delete_null_data(data, expected):
    linked_list = LinkedList()
    linked_list.append(5)
    linked_list.append(10)
    assert linked_list.delete(data) == expected

@pytest.mark.parametrize('expected', [
    0
])
def test_linked_list_len_after_clear(expected):
    linked_list = LinkedList()
    linked_list.append(5)
    linked_list.append(10)
    linked_list.append(15)
    linked_list.delete(5)
    linked_list.delete(10)
    linked_list.delete(15)
    assert len(linked_list) == expected