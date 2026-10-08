import pytest
from data.input_code.d03_linked_list import *

# T1 and T2: append
@pytest.mark.parametrize('initial, data, expected', [
    ([], 10, [10]),
    ([1], 2, [1, 2]),
])
def test_append(initial, data, expected):
    ll = LinkedList()
    for v in initial:
        ll.append(v)
    ll.append(data)
    assert ll.to_list() == expected
    assert len(ll) == len(expected)

# T3 and T4: prepend
@pytest.mark.parametrize('initial, data, expected', [
    ([], 5, [5]),
    ([1, 2], 0, [0, 1, 2]),
])
def test_prepend(initial, data, expected):
    ll = LinkedList()
    for v in initial:
        ll.append(v)
    ll.prepend(data)
    assert ll.to_list() == expected
    assert len(ll) == len(expected)

# T5-T9: delete
@pytest.mark.parametrize('initial, data, expected_bool, expected_list', [
    ([], 99, False, []),
    ([7, 8, 9], 7, True, [8, 9]),
    ([1, 2, 3, 4], 3, True, [1, 2, 4]),
    ([5, 6, 7], 7, True, [5, 6]),
    ([1, 2, 3], 99, False, [1, 2, 3]),
])
def test_delete(initial, data, expected_bool, expected_list):
    ll = LinkedList()
    for v in initial:
        ll.append(v)
    result = ll.delete(data)
    assert result == expected_bool
    assert ll.to_list() == expected_list
    assert len(ll) == len(expected_list)

# T10-T13: find
@pytest.mark.parametrize('initial, data, expected', [
    ([10, 20, 30], 10, 0),
    ([5, 6, 7, 8], 7, 2),
    ([1, 2, 3], 3, 2),
    ([4, 5, 6], 99, -1),
])
def test_find(initial, data, expected):
    ll = LinkedList()
    for v in initial:
        ll.append(v)
    assert ll.find(data) == expected

# T14-T18: get
@pytest.mark.parametrize('initial, index, expected', [
    ([100, 200, 300], 1, 200),
    ([42], 0, 42),
    ([9, 8, 7], 2, 7),
    ([1, 2, 3], -1, "IndexError"),
    ([1, 2, 3], 3, "IndexError"),
])
def test_get(initial, index, expected):
    ll = LinkedList()
    for v in initial:
        ll.append(v)
    if isinstance(expected, str):
        with pytest.raises(IndexError):
            ll.get(index)
    else:
        assert ll.get(index) == expected

# T19-T20: to_list
@pytest.mark.parametrize('initial, expected', [
    ([], []),
    ([1, 2, 3], [1, 2, 3]),
])
def test_to_list(initial, expected):
    ll = LinkedList()
    for v in initial:
        ll.append(v)
    assert ll.to_list() == expected

# T21: len after creation
def test_len_empty():
    ll = LinkedList()
    assert len(ll) == 0

# T22: len with complex operations
def test_len_complex():
    initial = [1, 2, 3]
    operations = ["append", 4, "prepend", 0, "delete", 2]
    ll = LinkedList()
    for v in initial:
        ll.append(v)
    for i in range(0, len(operations), 2):
        op = operations[i]
        val = operations[i + 1]
        if op == "append":
            ll.append(val)
        elif op == "prepend":
            ll.prepend(val)
        elif op == "delete":
            ll.delete(val)
    assert len(ll) == 4