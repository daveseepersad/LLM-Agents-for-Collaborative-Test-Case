import pytest
from data.input_code.d03_linked_list import LinkedList, Node

def test_append_and_len_and_to_list():
    ll = LinkedList()
    # Append first element, head should be set
    ll.append(10)
    assert ll.head is not None
    assert ll.head.data == 10
    assert len(ll) == 1
    assert ll.to_list() == [10]

    # Append second element, should be added at tail
    ll.append(20)
    assert len(ll) == 2
    # Verify order via to_list and traversal
    assert ll.to_list() == [10, 20]
    # Verify internal linking
    assert ll.head.next is not None
    assert ll.head.next.data == 20
    assert ll.head.next.next is None

def test_prepend_and_combination():
    ll = LinkedList()
    # Prepend on empty list
    ll.prepend('first')
    assert ll.head.data == 'first'
    assert len(ll) == 1
    assert ll.to_list() == ['first']

    # Prepend another element, should become new head
    ll.prepend('new_head')
    assert ll.head.data == 'new_head'
    assert ll.head.next.data == 'first'
    assert len(ll) == 2
    assert ll.to_list() == ['new_head', 'first']

def test_delete_various_cases():
    ll = LinkedList()
    # Deleting from empty list returns False
    assert ll.delete(99) is False

    # Setup list: [1, 2, 3]
    ll.append(1)
    ll.append(2)
    ll.append(3)

    # Delete head
    assert ll.delete(1) is True
    assert ll.to_list() == [2, 3]
    assert len(ll) == 2

    # Delete middle (now head is 2, tail is 3, delete 3 which is tail)
    assert ll.delete(3) is True
    assert ll.to_list() == [2]
    assert len(ll) == 1

    # Delete remaining head (also tail)
    assert ll.delete(2) is True
    assert ll.to_list() == []
    assert len(ll) == 0

    # Rebuild list and attempt to delete non‑existent element
    ll.append('a')
    ll.append('b')
    ll.append('c')
    assert ll.delete('z') is False
    assert ll.to_list() == ['a', 'b', 'c']
    assert len(ll) == 3

def test_find_cases():
    ll = LinkedList()
    # Empty list returns -1 for any find
    assert ll.find('anything') == -1

    # Populate list with diverse data types
    ll.append(None)
    ll.append('')
    ll.append(0)
    ll.append('test')

    # Verify indices
    assert ll.find(None) == 0
    assert ll.find('') == 1
    assert ll.find(0) == 2
    assert ll.find('test') == 3
    # Not present
    assert ll.find('missing') == -1

def test_get_valid_and_invalid_indices():
    ll = LinkedList()
    elements = [5, 10, 15]
    for e in elements:
        ll.append(e)

    # Valid indices
    for idx, val in enumerate(elements):
        assert ll.get(idx) == val

    # Negative index raises
    with pytest.raises(IndexError):
        ll.get(-1)

    # Index equal to size raises
    with pytest.raises(IndexError):
        ll.get(len(ll))

    # Index greater than size raises
    with pytest.raises(IndexError):
        ll.get(len(ll) + 5)

def test_edge_data_types_in_operations():
    ll = LinkedList()
    # Append None and empty string
    ll.append(None)
    ll.append('')
    ll.append('data')
    assert ll.to_list() == [None, '', 'data']
    assert len(ll) == 3

    # Prepend after some appends
    ll.prepend('start')
    assert ll.to_list() == ['start', None, '', 'data']
    assert len(ll) == 4

    # Delete empty string and verify list integrity
    assert ll.delete('') is True
    assert ll.to_list() == ['start', None, 'data']
    assert len(ll) == 3

    # Find None after deletions
    assert ll.find(None) == 1

    # Get each remaining element by index
    assert ll.get(0) == 'start'
    assert ll.get(1) is None
    assert ll.get(2) == 'data'