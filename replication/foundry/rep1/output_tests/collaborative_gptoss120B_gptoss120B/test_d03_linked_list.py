import pytest
from data.input_code.d03_linked_list import *

def build_linked_list(values):
    """Utility to create a LinkedList populated with the given values."""
    ll = LinkedList()
    for v in values:
        ll.append(v)
    return ll

# ----------------------------------------------------------------------
# Append
# ----------------------------------------------------------------------
@pytest.mark.parametrize(
    "initial,data",
    [
        ([], 5),          # T1_append_empty
        ([1], 2),         # T2_append_nonempty
    ],
    ids=["T1_append_empty", "T2_append_nonempty"]
)
def test_append(initial, data):
    ll = build_linked_list(initial)
    prev_len = len(ll)
    ll.append(data)
    # verify size increment
    assert len(ll) == prev_len + 1
    # verify order of elements
    assert ll.to_list() == initial + [data]

# ----------------------------------------------------------------------
# Prepend
# ----------------------------------------------------------------------
@pytest.mark.parametrize(
    "initial,data,expected_list",
    [
        ([], 3, [3]),                # T3_prepend_empty
        ([1, 2], 0, [0, 1, 2]),      # T4_prepend_nonempty
    ],
    ids=["T3_prepend_empty", "T4_prepend_nonempty"]
)
def test_prepend(initial, data, expected_list):
    ll = build_linked_list(initial)
    prev_len = len(ll)
    ll.prepend(data)
    assert len(ll) == prev_len + 1
    assert ll.to_list() == expected_list

# ----------------------------------------------------------------------
# Delete
# ----------------------------------------------------------------------
@pytest.mark.parametrize(
    "initial,data,expected_ret,expected_list,expected_len",
    [
        ([], 1, False, [], 0),                         # T5_delete_empty
        ([1, 2, 3], 1, True, [2, 3], 2),               # T6_delete_head
        ([1, 2, 3], 3, True, [1, 2], 2),               # T7_delete_tail
        ([1, 2], 5, False, [1, 2], 2),                 # T8_delete_missing
    ],
    ids=["T5_delete_empty", "T6_delete_head", "T7_delete_tail", "T8_delete_missing"]
)
def test_delete(initial, data, expected_ret, expected_list, expected_len):
    ll = build_linked_list(initial)
    ret = ll.delete(data)
    assert ret is expected_ret
    assert ll.to_list() == expected_list
    assert len(ll) == expected_len

# ----------------------------------------------------------------------
# Find
# ----------------------------------------------------------------------
@pytest.mark.parametrize(
    "initial,data,expected_index",
    [
        ([], 1, -1),                     # T9_find_empty
        ([10, 20], 10, 0),               # T10_find_head
        ([5, 6, 7], 6, 1),               # T11_find_middle
        ([1, 2], 3, -1),                 # T12_find_missing
    ],
    ids=["T9_find_empty", "T10_find_head", "T11_find_middle", "T12_find_missing"]
)
def test_find(initial, data, expected_index):
    ll = build_linked_list(initial)
    assert ll.find(data) == expected_index

# ----------------------------------------------------------------------
# Get
# ----------------------------------------------------------------------
@pytest.mark.parametrize(
    "initial,index,expected",
    [
        ([9, 8], 0, 9),          # T13_get_first
        ([9, 8], 1, 8),          # T14_get_last
    ],
    ids=["T13_get_first", "T14_get_last"]
)
def test_get_success(initial, index, expected):
    ll = build_linked_list(initial)
    assert ll.get(index) == expected

@pytest.mark.parametrize(
    "initial,index,exc",
    [
        ([1], -1, IndexError),          # T15_get_negative
        ([1], 1, IndexError),           # T16_get_out_of_range
    ],
    ids=["T15_get_negative", "T16_get_out_of_range"]
)
def test_get_exceptions(initial, index, exc):
    ll = build_linked_list(initial)
    with pytest.raises(exc):
        ll.get(index)

# ----------------------------------------------------------------------
# to_list
# ----------------------------------------------------------------------
@pytest.mark.parametrize(
    "initial,expected",
    [
        ([], []),                     # T17_to_list_empty
        ([1, 2, 3], [1, 2, 3]),       # T18_to_list_populated
    ],
    ids=["T17_to_list_empty", "T18_to_list_populated"]
)
def test_to_list(initial, expected):
    ll = build_linked_list(initial)
    assert ll.to_list() == expected

# ----------------------------------------------------------------------
# __len__
# ----------------------------------------------------------------------
def test_len():
    initial = [1, 2, 3, 4]   # T19_len
    ll = build_linked_list(initial)
    assert len(ll) == 4