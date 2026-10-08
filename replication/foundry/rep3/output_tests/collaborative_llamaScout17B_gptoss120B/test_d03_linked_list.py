import pytest
from data.input_code.d03_linked_list import *

def _make_linked_list(values):
    """Create a LinkedList with the given values without using LinkedList.append."""
    ll = LinkedList()
    if not values:
        return ll
    ll.head = Node(values[0])
    current = ll.head
    for val in values[1:]:
        current.next = Node(val)
        current = current.next
    ll._size = len(values)
    return ll

# ---------- __init__ ----------
def test_init_empty():
    ll = LinkedList()
    assert ll.head is None
    assert ll._size == 0

# ---------- append ----------
@pytest.mark.parametrize(
    "initial, data, expected_head, expected_size",
    [
        ([], 5, (5, None), 1),                     # T2_APPEND_EMPTY
        ([1], 2, (1, (2, None)), 2),               # T3_APPEND_NONEMPTY
    ],
)
def test_append(initial, data, expected_head, expected_size):
    ll = _make_linked_list(initial)
    ll.append(data)

    # verify size
    assert ll._size == expected_size

    # verify structure
    head = ll.head
    assert head is not None
    assert head.data == expected_head[0]
    if expected_head[1] is None:
        assert head.next is None
    else:
        nxt = head.next
        assert nxt is not None
        assert nxt.data == expected_head[1][0]
        assert nxt.next is None

# ---------- prepend ----------
@pytest.mark.parametrize(
    "initial, data, expected_head, expected_size",
    [
        ([], 5, (5, None), 1),                     # T4_PREPEND_EMPTY
        ([1], 2, (2, (1, None)), 2),               # T5_PREPEND_NONEMPTY
    ],
)
def test_prepend(initial, data, expected_head, expected_size):
    ll = _make_linked_list(initial)
    ll.prepend(data)

    assert ll._size == expected_size
    head = ll.head
    assert head is not None
    assert head.data == expected_head[0]
    if expected_head[1] is None:
        assert head.next is None
    else:
        nxt = head.next
        assert nxt is not None
        assert nxt.data == expected_head[1][0]
        assert nxt.next is None

# ---------- delete ----------
@pytest.mark.parametrize(
    "initial, data, expected_result, expected_head, expected_size",
    [
        ([], 5, False, None, 0),                                   # T6_DELETE_EMPTY
        ([1], 1, True, None, 0),                                   # T7_DELETE_HEAD
        ([1, 2], 2, True, (1, None), 1),                            # T8_DELETE_NONHEAD
        ([1], 2, False, (1, None), 1),                              # T9_DELETE_MISSING
    ],
)
def test_delete(initial, data, expected_result, expected_head, expected_size):
    ll = _make_linked_list(initial)
    result = ll.delete(data)

    assert result is expected_result
    assert ll._size == expected_size
    if expected_head is None:
        assert ll.head is None
    else:
        assert ll.head is not None
        assert ll.head.data == expected_head[0]
        assert ll.head.next is expected_head[1]

# ---------- find ----------
@pytest.mark.parametrize(
    "initial, data, expected_index",
    [
        ([1, 2], 2, 1),    # T10_FIND_PRESENT
        ([1], 2, -1),      # T11_FIND_MISSING
    ],
)
def test_find(initial, data, expected_index):
    ll = _make_linked_list(initial)
    assert ll.find(data) == expected_index

# ---------- get ----------
@pytest.mark.parametrize(
    "initial, index, expected",
    [
        ([1, 2], 1, 2),                     # T12_GET_VALID
    ],
)
def test_get_valid(initial, index, expected):
    ll = _make_linked_list(initial)
    assert ll.get(index) == expected

def test_get_invalid_low():
    ll = _make_linked_list([1])
    with pytest.raises(IndexError):
        ll.get(-1)                         # T13_GET_INVALID_LOW

def test_get_invalid_high():
    ll = _make_linked_list([1])
    with pytest.raises(IndexError):
        ll.get(1)                          # T14_GET_INVALID_HIGH

# ---------- to_list ----------
@pytest.mark.parametrize(
    "initial, expected",
    [
        ([], []),                            # T15_TOLIST_EMPTY
        ([1, 2], [1, 2]),                    # T16_TOLIST_NONEMPTY
    ],
)
def test_to_list(initial, expected):
    ll = _make_linked_list(initial)
    assert ll.to_list() == expected

# ---------- __len__ ----------
@pytest.mark.parametrize(
    "initial, expected_len",
    [
        ([], 0),                             # T17_LEN_EMPTY
        ([1], 1),                            # T18_LEN_NONEMPTY
    ],
)
def test_len(initial, expected_len):
    ll = _make_linked_list(initial)
    assert len(ll) == expected_len