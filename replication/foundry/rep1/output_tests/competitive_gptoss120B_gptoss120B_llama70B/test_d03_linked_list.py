import pytest
from data.input_code.d03_linked_list import *

def _apply_setup(ll, actions):
    """Execute a sequence of method calls on a LinkedList instance."""
    for act in actions:
        method = getattr(ll, act["method"])
        method(**act["args"])

# ---------- append ----------
@pytest.mark.parametrize(
    "setup_actions, input_data, expected_list",
    [
        ([], 1, [1]),                                   # T1_append_empty
        ([{"method": "append", "args": {"data": 1}}], 2, [1, 2]),  # T2_append_nonempty
    ],
    ids=["T1_append_empty", "T2_append_nonempty"]
)
def test_append(setup_actions, input_data, expected_list):
    ll = LinkedList()
    _apply_setup(ll, setup_actions)
    ll.append(input_data)
    assert ll.to_list() == expected_list
    assert len(ll) == len(expected_list)

# ---------- prepend ----------
def test_prepend():
    ll = LinkedList()
    ll.prepend(10)  # T3_prepend
    assert ll.to_list() == [10]
    assert len(ll) == 1

# ---------- delete ----------
@pytest.mark.parametrize(
    "setup_actions, del_data, expected_result, expected_list",
    [
        ([], 5, False, []),                                 # T4_delete_empty
        (
            [
                {"method": "append", "args": {"data": 1}},
                {"method": "append", "args": {"data": 2}},
                {"method": "append", "args": {"data": 3}},
            ],
            1,
            True,
            [2, 3],
        ),                                                  # T5_delete_head
        (
            [
                {"method": "append", "args": {"data": 1}},
                {"method": "append", "args": {"data": 2}},
                {"method": "append", "args": {"data": 3}},
            ],
            2,
            True,
            [1, 3],
        ),                                                  # T6_delete_nonhead
        (
            [
                {"method": "append", "args": {"data": 1}},
                {"method": "append", "args": {"data": 2}},
                {"method": "append", "args": {"data": 3}},
            ],
            99,
            False,
            [1, 2, 3],
        ),                                                  # T7_delete_notfound
    ],
    ids=[
        "T4_delete_empty",
        "T5_delete_head",
        "T6_delete_nonhead",
        "T7_delete_notfound",
    ],
)
def test_delete(setup_actions, del_data, expected_result, expected_list):
    ll = LinkedList()
    _apply_setup(ll, setup_actions)
    result = ll.delete(del_data)
    assert result is expected_result
    assert ll.to_list() == expected_list
    assert len(ll) == len(expected_list)

# ---------- find ----------
@pytest.mark.parametrize(
    "setup_actions, find_data, expected_index",
    [
        (
            [
                {"method": "append", "args": {"data": 5}},
                {"method": "append", "args": {"data": 6}},
                {"method": "append", "args": {"data": 7}},
            ],
            5,
            0,
        ),  # T8_find_head
        (
            [
                {"method": "append", "args": {"data": 5}},
                {"method": "append", "args": {"data": 6}},
                {"method": "append", "args": {"data": 7}},
            ],
            99,
            -1,
        ),  # T9_find_notfound
    ],
    ids=["T8_find_head", "T9_find_notfound"],
)
def test_find(setup_actions, find_data, expected_index):
    ll = LinkedList()
    _apply_setup(ll, setup_actions)
    assert ll.find(find_data) == expected_index

# ---------- get ----------
@pytest.mark.parametrize(
    "setup_actions, index, expected",
    [
        (
            [
                {"method": "append", "args": {"data": 10}},
                {"method": "append", "args": {"data": 20}},
                {"method": "append", "args": {"data": 30}},
            ],
            0,
            10,
        ),  # T10_get_first
        (
            [
                {"method": "append", "args": {"data": 10}},
                {"method": "append", "args": {"data": 20}},
                {"method": "append", "args": {"data": 30}},
            ],
            2,
            30,
        ),  # T11_get_last
    ],
    ids=["T10_get_first", "T11_get_last"],
)
def test_get_success(setup_actions, index, expected):
    ll = LinkedList()
    _apply_setup(ll, setup_actions)
    assert ll.get(index) == expected

@pytest.mark.parametrize(
    "setup_actions, index",
    [
        ([{"method": "append", "args": {"data": 1}}], -1),  # T12_get_negative
        ([{"method": "append", "args": {"data": 1}}], 1),   # T13_get_out_of_range
    ],
    ids=["T12_get_negative", "T13_get_out_of_range"],
)
def test_get_errors(setup_actions, index):
    ll = LinkedList()
    _apply_setup(ll, setup_actions)
    with pytest.raises(IndexError):
        ll.get(index)

# ---------- to_list ----------
def test_to_list():
    ll = LinkedList()
    _apply_setup(
        ll,
        [
            {"method": "append", "args": {"data": 1}},
            {"method": "append", "args": {"data": 2}},
            {"method": "append", "args": {"data": 3}},
        ],
    )
    assert ll.to_list() == [1, 2, 3]  # T14_to_list

# ---------- __len__ ----------
def test_len():
    ll = LinkedList()
    _apply_setup(
        ll,
        [
            {"method": "append", "args": {"data": 1}},
            {"method": "append", "args": {"data": 2}},
        ],
    )
    assert len(ll) == 2  # T15_len