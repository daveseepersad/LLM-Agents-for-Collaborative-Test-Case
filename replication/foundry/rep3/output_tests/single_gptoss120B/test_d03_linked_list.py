import pytest
from data.input_code.d03_linked_list import LinkedList, Node

def test_append_and_len_and_to_list():
    ll = LinkedList()
    assert len(ll) == 0
    assert ll.to_list() == []

    # Append first element (head is None branch)
    ll.append(10)
    assert len(ll) == 1
    assert ll.to_list() == [10]

    # Append additional elements (traverse loop)
    ll.append(20)
    ll.append(30)
    assert len(ll) == 3
    assert ll.to_list() == [10, 20, 30]

def test_prepend_and_len_and_order():
    ll = LinkedList()
    ll.prepend('c')
    ll.prepend('b')
    ll.prepend('a')
    # After prepends, order should be a, b, c
    assert ll.to_list() == ['a', 'b', 'c']
    assert len(ll) == 3

def test_delete_head_and_middle_and_not_found():
    ll = LinkedList()
    # Delete on empty list returns False
    assert ll.delete(1) is False

    # Build list [1, 2, 3]
    ll.append(1)
    ll.append(2)
    ll.append(3)

    # Delete head
    assert ll.delete(1) is True
    assert ll.to_list() == [2, 3]
    assert len(ll) == 2

    # Delete middle (now head is 2, delete 3 which is tail)
    assert ll.delete(3) is True
    assert ll.to_list() == [2]
    assert len(ll) == 1

    # Delete non‑existent element
    assert ll.delete(99) is False
    assert ll.to_list() == [2]
    assert len(ll) == 1

def test_find_existing_and_missing():
    ll = LinkedList()
    # Empty list returns -1
    assert ll.find('x') == -1

    # Populate list
    items = ['a', 'b', 'c', 'd']
    for item in items:
        ll.append(item)

    # Find each element
    for idx, val in enumerate(items):
        assert ll.find(val) == idx

    # Not present
    assert ll.find('z') == -1

def test_get_valid_and_invalid_indices():
    ll = LinkedList()
    for i in range(5):
        ll.append(i * 10)  # [0,10,20,30,40]

    # Valid indices
    for idx in range(5):
        assert ll.get(idx) == idx * 10

    # Negative index raises
    with pytest.raises(IndexError):
        ll.get(-1)

    # Index equal to size raises
    with pytest.raises(IndexError):
        ll.get(5)

    # Index greater than size raises
    with pytest.raises(IndexError):
        ll.get(100)

def test_combined_operations_consistency():
    ll = LinkedList()
    # Mix prepend and append
    ll.append('end')
    ll.prepend('start')
    ll.append('middle')
    # Expected order: start, end, middle
    assert ll.to_list() == ['start', 'end', 'middle']
    assert len(ll) == 3

    # Delete middle element
    assert ll.delete('end') is True
    assert ll.to_list() == ['start', 'middle']
    assert len(ll) == 2

    # Find after deletions
    assert ll.find('start') == 0
    assert ll.find('middle') == 1
    assert ll.find('end') == -1

    # Get by index after deletions
    assert ll.get(0) == 'start'
    assert ll.get(1) == 'middle'