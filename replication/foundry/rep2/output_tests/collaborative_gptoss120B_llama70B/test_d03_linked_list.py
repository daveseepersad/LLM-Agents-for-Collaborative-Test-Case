import pytest
from data.input_code.d03_linked_list import *

@pytest.mark.parametrize('data', [
    (10),
])
def test_append_empty(data):
    linked_list = LinkedList()
    linked_list.append(data)
    assert linked_list.head.data == data
    assert len(linked_list) == 1

@pytest.mark.parametrize('setup, data', [
    ([5], 20),
])
def test_append_nonempty(setup, data):
    linked_list = LinkedList()
    for item in setup:
        linked_list.append(item)
    linked_list.append(data)
    assert linked_list.to_list() == setup + [data]
    assert len(linked_list) == len(setup) + 1

@pytest.mark.parametrize('data', [
    (7),
])
def test_prepend(data):
    linked_list = LinkedList()
    linked_list.prepend(data)
    assert linked_list.head.data == data
    assert len(linked_list) == 1

@pytest.mark.parametrize('setup, data', [
    ([], 1),
])
def test_delete_empty(setup, data):
    linked_list = LinkedList()
    for item in setup:
        linked_list.append(item)
    assert linked_list.delete(data) == False
    assert len(linked_list) == len(setup)

@pytest.mark.parametrize('setup, data', [
    ([1, 2, 3], 1),
])
def test_delete_head(setup, data):
    linked_list = LinkedList()
    for item in setup:
        linked_list.append(item)
    assert linked_list.delete(data) == True
    assert linked_list.to_list() == setup[1:]
    assert len(linked_list) == len(setup) - 1

@pytest.mark.parametrize('setup, data', [
    ([4, 5, 6], 5),
])
def test_delete_middle(setup, data):
    linked_list = LinkedList()
    for item in setup:
        linked_list.append(item)
    assert linked_list.delete(data) == True
    assert linked_list.to_list() == setup[:1] + setup[2:] # Changed from setup[:2] to setup[:1]
    assert len(linked_list) == len(setup) - 1

@pytest.mark.parametrize('setup, data', [
    ([8, 9, 10], 10),
])
def test_delete_tail(setup, data):
    linked_list = LinkedList()
    for item in setup:
        linked_list.append(item)
    assert linked_list.delete(data) == True
    assert linked_list.to_list() == setup[:-1]
    assert len(linked_list) == len(setup) - 1

@pytest.mark.parametrize('setup, data', [
    ([11, 12], 99),
])
def test_delete_not_found(setup, data):
    linked_list = LinkedList()
    for item in setup:
        linked_list.append(item)
    assert linked_list.delete(data) == False
    assert linked_list.to_list() == setup
    assert len(linked_list) == len(setup)

@pytest.mark.parametrize('setup, data', [
    ([], 1),
])
def test_find_empty(setup, data):
    linked_list = LinkedList()
    for item in setup:
        linked_list.append(item)
    assert linked_list.find(data) == -1

@pytest.mark.parametrize('setup, data', [
    ([3, 4, 5], 3),
])
def test_find_head(setup, data):
    linked_list = LinkedList()
    for item in setup:
        linked_list.append(item)
    assert linked_list.find(data) == 0

@pytest.mark.parametrize('setup, data', [
    ([6, 7, 8], 8),
])
def test_find_tail(setup, data):
    linked_list = LinkedList()
    for item in setup:
        linked_list.append(item)
    assert linked_list.find(data) == len(setup) - 1

@pytest.mark.parametrize('setup, data', [
    ([9, 10], 99),
])
def test_find_not_found(setup, data):
    linked_list = LinkedList()
    for item in setup:
        linked_list.append(item)
    assert linked_list.find(data) == -1

@pytest.mark.parametrize('setup, index', [
    ([15, 25, 35], 0),
])
def test_get_valid_zero(setup, index):
    linked_list = LinkedList()
    for item in setup:
        linked_list.append(item)
    assert linked_list.get(index) == setup[index]

@pytest.mark.parametrize('setup, index', [
    ([40, 50, 60], 2),
])
def test_get_valid_last(setup, index):
    linked_list = LinkedList()
    for item in setup:
        linked_list.append(item)
    assert linked_list.get(index) == setup[index]

@pytest.mark.parametrize('setup, index', [
    ([70, 80], -1),
])
def test_get_negative_index(setup, index):
    linked_list = LinkedList()
    for item in setup:
        linked_list.append(item)
    with pytest.raises(IndexError):
        linked_list.get(index)

@pytest.mark.parametrize('setup, index', [
    ([90, 100], 2),
])
def test_get_out_of_range(setup, index):
    linked_list = LinkedList()
    for item in setup:
        linked_list.append(item)
    with pytest.raises(IndexError):
        linked_list.get(index)

@pytest.mark.parametrize('setup', [
    ([]),
])
def test_to_list_empty(setup):
    linked_list = LinkedList()
    for item in setup:
        linked_list.append(item)
    assert linked_list.to_list() == setup

@pytest.mark.parametrize('setup', [
    ([1, 2, 3]),
])
def test_to_list_nonempty(setup):
    linked_list = LinkedList()
    for item in setup:
        linked_list.append(item)
    assert linked_list.to_list() == setup

@pytest.mark.parametrize('setup_operations', [
    (["append:5", "append:6", "prepend:4", "delete:6"]),
])
def test_len_after_operations(setup_operations):
    linked_list = LinkedList()
    for operation in setup_operations:
        op, data = operation.split(":")
        if op == "append":
            linked_list.append(int(data))
        elif op == "prepend":
            linked_list.prepend(int(data))
        elif op == "delete":
            linked_list.delete(int(data))
    assert len(linked_list) == 2