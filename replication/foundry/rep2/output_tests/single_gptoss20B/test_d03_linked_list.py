import pytest
from data.input_code.d03_linked_list import LinkedList

def test_basic_operations_and_boundaries():
    ll = LinkedList()
    data = ["", None, 0, "end"]
    for v in data:
        ll.append(v)
    assert ll.to_list() == data
    assert len(ll) == 4
    assert ll.get(0) == ""
    assert ll.get(3) == "end"
    assert ll.get(2) == 0
    with pytest.raises(IndexError):
        ll.get(-1)
    with pytest.raises(IndexError):
        ll.get(4)
    assert ll.find("") == 0
    assert ll.find("not there") == -1

def test_prepend_and_find_and_delete_middle_head():
    ll = LinkedList()
    ll.append("A")
    ll.append("B")
    ll.append("C")
    ll.prepend("START")
    assert ll.to_list() == ["START", "A", "B", "C"]
    assert ll.find("B") == 2
    # delete head
    assert ll.delete("START") is True
    assert ll.to_list() == ["A", "B", "C"]
    assert len(ll) == 3
    # delete middle
    assert ll.delete("B") is True
    assert ll.to_list() == ["A", "C"]
    assert len(ll) == 2
    # delete non-existent
    assert ll.delete("X") is False

def test_empty_list_behavior_and_get_errors():
    ll = LinkedList()
    assert ll.to_list() == []
    assert len(ll) == 0
    # deleting from empty should be False (branch where head is None)
    assert ll.delete("anything") is False
    with pytest.raises(IndexError):
        ll.get(0)
    ll.append(None)
    ll.append("")
    assert ll.to_list() == [None, ""]
    assert ll.get(0) is None
    assert ll.get(1) == ""