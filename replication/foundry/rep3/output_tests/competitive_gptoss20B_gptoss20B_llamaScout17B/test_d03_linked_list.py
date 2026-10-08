import pytest
from data.input_code.d03_linked_list import *

def test_linked_list_plan():
    ll = LinkedList()

    # T1: delete on empty list should return False
    assert ll.delete(10) is False

    # T2: find on empty list should return -1
    assert ll.find(10) == -1

    # T3: get on empty list should raise IndexError
    with pytest.raises(IndexError):
        ll.get(0)

    # T4: to_list on empty list should return []
    assert ll.to_list() == []

    # T5: len on empty list should be 0
    assert len(ll) == 0

    # T6: first append should take the head path
    assert ll.append(1) is None

    # T7: second append should create a two-node list
    assert ll.append(2) is None

    # T8: third append should trigger traversal (three nodes now)
    assert ll.append(3) is None

    # T9: verify list contents after multiple appends
    assert ll.to_list() == [1, 2, 3]

    # T10: prepend should update head correctly
    assert ll.prepend(0) is None

    # T11: find should locate the new head value at index 0
    assert ll.find(0) == 0

    # T12: delete the head value should adjust head and size
    ll.delete(0)  # no assertion on return value per plan (expected None)

    # T13: to_list after deleting head should reflect new order
    assert ll.to_list() == [1, 2, 3]

    # T14: delete the last element to test non-head removal
    ll.delete(3)

    # T15: to_list should reflect removal of last item
    assert ll.to_list() == [1, 2]

    # T16: delete a non-existent value should return false
    assert ll.delete(99) is False

    # T17: append another value to create a longer list for further tests
    assert ll.append(4) is None

    # T18: delete a middle element to exercise non-head deletion path
    ll.delete(2)

    # T19: to_list after middle deletion shows updated order
    assert ll.to_list() == [1, 4]

    # T20: find an existing value near the start
    assert ll.find(1) == 0

    # T21: find a non-existent value returns -1
    assert ll.find(99) == -1

    # T22: get a valid non-first index
    assert ll.get(1) == 4

    # T23: get with negative index should raise IndexError
    with pytest.raises(IndexError):
        ll.get(-1)

    # T24: get with out-of-range index should raise IndexError
    with pytest.raises(IndexError):
        ll.get(2)

    # T25: final length should reflect two items remaining
    assert len(ll) == 2