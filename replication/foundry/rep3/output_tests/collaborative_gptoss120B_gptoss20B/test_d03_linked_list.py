import pytest
from data.input_code.d03_linked_list import *

@pytest.fixture
def empty_list():
    return LinkedList()

@pytest.mark.parametrize(
    "data, expected_head_data, expected_size",
    [
        (5, 5, 1),
        (None, None, 1),
        ("", "", 1),
        ([], [], 1),
    ],
)
def test_append_on_empty(data, expected_head_data, expected_size):
    ll = LinkedList()
    ll.append(data)
    assert ll.head is not None
    assert ll.head.data == expected_head_data
    assert len(ll) == expected_size
    assert ll.to_list() == [expected_head_data]

@pytest.mark.parametrize(
    "data, expected_head_data, expected_size",
    [
        (5, 5, 1),
        (None, None, 1),
        ("", "", 1),
        ([], [], 1),
    ],
)
def test_prepend_on_empty(data, expected_head_data, expected_size):
    ll = LinkedList()
    ll.prepend(data)
    assert ll.head is not None
    assert ll.head.data == expected_head_data
    assert len(ll) == expected_size
    assert ll.to_list() == [expected_head_data]

@pytest.mark.parametrize(
    "method, args, expected",
    [
        ("delete", (5,), False),
        ("find", (5,), -1),
    ],
)
def test_operations_on_empty_list(empty_list, method, args, expected):
    func = getattr(empty_list, method)
    assert func(*args) == expected

@pytest.mark.parametrize(
    "index, exception",
    [
        (-1, IndexError),
        (1, IndexError),
    ],
)
def test_get_on_empty_raises_index_error(empty_list, index, exception):
    with pytest.raises(exception):
        empty_list.get(index)

def test_to_list_and_len_on_empty(empty_list):
    assert empty_list.to_list() == []
    assert len(empty_list) == 0

def test_delete_nonexistent_on_empty_after_inserts():
    ll = LinkedList()
    # Insert a few elements first
    ll.append(1)
    ll.append(2)
    ll.append(3)
    # Attempt to delete a value not present
    result = ll.delete(999)
    assert result is False
    # Ensure list remains unchanged
    assert ll.to_list() == [1, 2, 3]
    assert len(ll) == 3

import pytest
from data.input_code.d03_linked_list import *

@pytest.fixture
def three_element_list():
    ll = LinkedList()
    ll.append(1)
    ll.append(2)
    ll.append(3)
    return ll

@pytest.mark.parametrize(
    "data, expected",
    [
        (1, True),  # delete head
        (2, True),  # delete middle
        (3, True),  # delete tail
    ],
)
def test_delete_various_positions(three_element_list, data, expected):
    result = three_element_list.delete(data)
    assert result is expected

def test_find_existing_tail(three_element_list):
    index = three_element_list.find(3)
    assert index == 2

@pytest.mark.parametrize(
    "index, expected",
    [
        (2, 3),  # valid index, tail element
        (0, 1),  # head element
    ],
)
def test_get_valid_indices(three_element_list, index, expected):
    value = three_element_list.get(index)
    assert value == expected