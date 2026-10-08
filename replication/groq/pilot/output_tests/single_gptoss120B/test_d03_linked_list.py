import pytest
from data.input_code.d03_linked_list import LinkedList

def test_append_and_len_and_to_list():
    ll = LinkedList()
    # Append to empty list
    ll.append(10)
    assert ll.head is not None
    assert ll.head.data == 10
    assert len(ll) == 1
    assert ll.to_list() == [10]
    # Append to non‑empty list
    ll.append(20)
    ll.append(30)
    assert len(ll) == 3
    # Verify order via to_list
    assert ll.to_list() == [10, 20, 30]
    # Verify internal linking
    assert ll.head.next.next.data == 30

def test_prepend_and_order():
    ll = LinkedList()
    ll.prepend('a')
    assert ll.head.data == 'a'
    assert len(ll) == 1
    ll.prepend('b')
    ll.prepend('c')
    # List should be c -> b -> a
    assert ll.to_list() == ['c', 'b', 'a']
    assert len(ll) == 3

def test_delete_empty_returns_false():
    ll = LinkedList()
    assert ll.delete(123) is False
    assert len(ll) == 0

def test_delete_head_and_middle_and_nonexistent():
    ll = LinkedList()
    ll.append('first')
    ll.append('second')
    ll.append('third')
    # Delete head
    result_head = ll.delete('first')
    assert result_head is True
    assert ll.head.data == 'second'
    assert len(ll) == 2
    # Delete middle (now 'second' is head, 'third' is next)
    ll.append('fourth')
    result_mid = ll.delete('third')
    assert result_mid is True
    # Ensure 'fourth' follows 'second'
    assert ll.head.next.data == 'fourth'
    assert len(ll) == 2
    # Attempt to delete non‑existent value
    result_none = ll.delete('nonexistent')
    assert result_none is False
    assert len(ll) == 2

def test_find_various_data_and_not_found():
    ll = LinkedList()
    ll.append(None)
    ll.append('')
    ll.append(0)
    ll.append('test')
    # Find each existing element
    assert ll.find(None) == 0
    assert ll.find('') == 1
    assert ll.find(0) == 2
    assert ll.find('test') == 3
    # Not found
    assert ll.find('absent') == -1

def test_get_valid_and_invalid_indices():
    ll = LinkedList()
    values = [5, 10, 15]
    for v in values:
        ll.append(v)
    # Valid indices
    for idx, val in enumerate(values):
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

def test_len_and_to_list_consistency():
    ll = LinkedList()
    assert len(ll) == 0
    assert ll.to_list() == []
    items = ['x', 'y', 'z']
    for i, item in enumerate(items, 1):
        ll.append(item)
        assert len(ll) == i
        assert ll.to_list() == items[:i]"""