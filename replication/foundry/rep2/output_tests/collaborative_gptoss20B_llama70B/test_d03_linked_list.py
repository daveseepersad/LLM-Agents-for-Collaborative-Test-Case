import pytest
from data.input_code.d03_linked_list import LinkedList

@pytest.mark.parametrize('data', [
    (1),
    (2)
])
def test_append_and_prepend_empty(data):
    linked_list = LinkedList()
    if data == 1:
        linked_list.append(data)
        assert linked_list.to_list() == [1]
    else:
        linked_list.prepend(data)
        assert linked_list.to_list() == [2]

def test_to_list_empty():
    linked_list = LinkedList()
    assert linked_list.to_list() == []

def test_find_empty():
    linked_list = LinkedList()
    assert linked_list.find(99) == -1

def test_delete_empty():
    linked_list = LinkedList()
    assert linked_list.delete(55) == False

def test_get_out_of_range():
    linked_list = LinkedList()
    with pytest.raises(IndexError):
        linked_list.get(0)

@pytest.mark.parametrize('data', [
    (1),
    (2)
])
def test_append_and_prepend_empty(data):
    linked_list = LinkedList()
    if data == 1:
        linked_list.append(data)
        assert linked_list.to_list() == [1]
    else:
        linked_list.prepend(data)
        assert linked_list.to_list() == [2]

def test_to_list_empty():
    linked_list = LinkedList()
    assert linked_list.to_list() == []

def test_find_empty():
    linked_list = LinkedList()
    assert linked_list.find(99) == -1

def test_delete_empty():
    linked_list = LinkedList()
    assert linked_list.delete(55) == False

def test_get_out_of_range():
    linked_list = LinkedList()
    with pytest.raises(IndexError):
        linked_list.get(0)

def test_len_empty():
    linked_list = LinkedList()
    assert len(linked_list) == 0

def test_get_negative():
    linked_list = LinkedList()
    linked_list.append(1)
    with pytest.raises(IndexError):
        linked_list.get(-1)

def test_append_second_element():
    linked_list = LinkedList()
    linked_list.append(1)
    linked_list.append(2)
    assert linked_list.to_list() == [1, 2]

def test_delete_head_in_nonempty():
    linked_list = LinkedList()
    linked_list.append(1)
    assert linked_list.delete(1) == True
    assert linked_list.to_list() == []

def test_delete_not_found_in_nonempty():
    linked_list = LinkedList()
    linked_list.append(1)
    assert linked_list.delete(99) == False
    assert linked_list.to_list() == [1]

@pytest.mark.parametrize('data, initial_state', [
    (42, [1]),
])
def test_prepend_non_empty(data, initial_state):
    linked_list = LinkedList()
    for element in initial_state:
        linked_list.append(element)
    linked_list.prepend(data)
    assert linked_list.to_list() == [data] + initial_state

@pytest.mark.parametrize('data, initial_state, expected', [
    (2, [1, 2], True),
])
def test_delete_tail_nonhead(data, initial_state, expected):
    linked_list = LinkedList()
    for element in initial_state:
        linked_list.append(element)
    assert linked_list.delete(data) == expected
    assert linked_list.to_list() == [x for x in initial_state if x != data]

@pytest.mark.parametrize('data, initial_state, expected', [
    (2, [1, 2, 3], 1),
])
def test_find_exists_middle(data, initial_state, expected):
    linked_list = LinkedList()
    for element in initial_state:
        linked_list.append(element)
    assert linked_list.find(data) == expected

@pytest.mark.parametrize('index, initial_state, expected', [
    (2, [10, 20, 30], 30),
])
def test_get_last_element(index, initial_state, expected):
    linked_list = LinkedList()
    for element in initial_state:
        linked_list.append(element)
    assert linked_list.get(index) == expected

@pytest.mark.parametrize('initial_state, expected', [
    ([5, 6, 7], 3),
])
def test_len_non_empty(initial_state, expected):
    linked_list = LinkedList()
    for element in initial_state:
        linked_list.append(element)
    assert len(linked_list) == expected