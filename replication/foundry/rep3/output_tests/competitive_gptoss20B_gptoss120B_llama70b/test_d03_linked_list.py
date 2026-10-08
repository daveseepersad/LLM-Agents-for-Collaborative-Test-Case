import pytest
from data.input_code.d03_linked_list import LinkedList

def build_linked_list(values):
    ll = LinkedList()
    for v in values:
        ll.append(v)
    return ll

# ---------- Append ----------
@pytest.mark.parametrize(
    "initial,data,expected",
    [
        ([], 1, [1]),                     # T1_LL_APPEND_EMPTY
        ([1], 2, [1, 2]),                 # T2_LL_APPEND_SECOND
        ([1, 2], 3, [1, 2, 3]),           # T3_LL_APPEND_THIRD
        ([], None, [None]),               # T14_LL_APPEND_NONE
        ([], "", [""]),                   # T15_LL_APPEND_EMPTY_STRING
    ],
    ids=[
        "empty",
        "second",
        "third",
        "append_none",
        "append_empty_string",
    ]
)
def test_append(initial, data, expected):
    ll = build_linked_list(initial)
    ll.append(data)
    assert ll.to_list() == expected
    assert len(ll) == len(expected)

# ---------- Prepend ----------
def test_prepend():
    ll = build_linked_list([1, 2, 3])
    ll.prepend(0)
    assert ll.to_list() == [0, 1, 2, 3]
    assert len(ll) == 4

# ---------- Delete ----------
@pytest.mark.parametrize(
    "initial,data,expected_ret,expected_list",
    [
        ([0, 1, 2, 3], 0, True, [1, 2, 3]),   # T5_LL_DELETE_HEAD
        ([1, 2, 3], 3, True, [1, 2]),        # T6_LL_DELETE_TAIL
        ([1, 2], 99, False, [1, 2]),         # T7_LL_DELETE_NOT_FOUND
    ],
    ids=["delete_head", "delete_tail", "delete_not_found"]
)
def test_delete(initial, data, expected_ret, expected_list):
    ll = build_linked_list(initial)
    ret = ll.delete(data)
    assert ret is expected_ret
    assert ll.to_list() == expected_list
    assert len(ll) == len(expected_list)

# ---------- Find ----------
@pytest.mark.parametrize(
    "initial,data,expected",
    [
        ([1, 2], 2, 1),          # T8_LL_FIND_EXISTING
        ([5, 6, 7], 100, -1),    # T17_LL_FIND_NOT_PRESENT
    ],
    ids=["find_existing", "find_not_present"]
)
def test_find(initial, data, expected):
    ll = build_linked_list(initial)
    assert ll.find(data) == expected

# ---------- Get ----------
@pytest.mark.parametrize(
    "initial,index,expected",
    [
        ([1, 2], 0, 1),          # T9_LL_GET_VALID
        ([5, 6, 7], 2, 7),       # T18_LL_GET_LAST
    ],
    ids=["get_first", "get_last"]
)
def test_get_valid(initial, index, expected):
    ll = build_linked_list(initial)
    assert ll.get(index) == expected

@pytest.mark.parametrize(
    "initial,index,exc",
    [
        ([1, 2], -1, IndexError),   # T10_LL_GET_NEG_INDEX
        ([1, 2], 2, IndexError),    # T11_LL_GET_OOB
    ],
    ids=["get_negative_index", "get_out_of_bounds"]
)
def test_get_exceptions(initial, index, exc):
    ll = build_linked_list(initial)
    with pytest.raises(exc):
        ll.get(index)

# ---------- to_list ----------
@pytest.mark.parametrize(
    "initial,expected",
    [
        ([1, 2, 3], [1, 2, 3]),   # T12_LL_TO_LIST
        ([], []),                 # T16_LL_TO_LIST_EMPTY
        ([], []),                 # T20_LL_TO_LIST_EMPTY_FINAL
    ],
    ids=["to_list_normal", "to_list_empty_1", "to_list_empty_2"]
)
def test_to_list(initial, expected):
    ll = build_linked_list(initial)
    assert ll.to_list() == expected

# ---------- __len__ ----------
@pytest.mark.parametrize(
    "initial,expected",
    [
        ([1, 2, 3], 3),   # T13_LL_LEN
        ([], 0),          # T19_LL_LEN_EMPTY
    ],
    ids=["len_nonempty", "len_empty"]
)
def test_len(initial, expected):
    ll = build_linked_list(initial)
    assert len(ll) == expected

import pytest
from data.input_code.d03_linked_list import LinkedList

def build_linked_list(values):
    ll = LinkedList()
    for v in values:
        ll.append(v)
    return ll

# ---------- Delete (additional cases) ----------
@pytest.mark.parametrize(
    "initial,data,expected_ret,expected_list",
    [
        ([5], 5, True, []),                     # T21_LL_DELETE_SINGLE_ELEMENT
        ([1, 2, 3, 4], 2, True, [1, 3, 4]),     # T22_LL_DELETE_MIDDLE
    ],
    ids=["delete_single_element", "delete_middle"]
)
def test_delete_additional(initial, data, expected_ret, expected_list):
    ll = build_linked_list(initial)
    ret = ll.delete(data)
    assert ret is expected_ret
    assert ll.to_list() == expected_list
    assert len(ll) == len(expected_list)

# ---------- Get (exception on empty list) ----------
def test_get_on_empty_raises():
    ll = build_linked_list([])
    with pytest.raises(IndexError):
        ll.get(0)  # T23_LL_GET_ON_EMPTY

# ---------- Delete (on empty list) ----------
def test_delete_on_empty_returns_false():
    ll = build_linked_list([])
    ret = ll.delete(1)  # T24_LL_DELETE_ON_EMPTY
    assert ret is False
    assert ll.to_list() == []
    assert len(ll) == 0

# ---------- Find (duplicate first occurrence) ----------
def test_find_duplicate_first():
    ll = build_linked_list([1, 2, 2, 3])
    assert ll.find(2) == 1  # T25_LL_FIND_DUPLICATE_FIRST