import pytest
import datetime
from data.input_code.d05_hotel import *

SHARED = {}

@pytest.fixture(scope="module")
def system():
    return HotelReservationSystem()

def test_T1_OK_add_room(system):
    system.add_room(1, "single", 100.0)
    assert 1 in system.rooms
    assert system.rooms[1]['price_per_night'] == 100.0
    assert system.rooms[1]['type'] == "single"

def test_T2_ERR_add_room(system):
    with pytest.raises(ValueError):
        system.add_room(5, "double", 0.0)

def test_T3_OK_book_room(system):
    today = datetime.date.today()
    check_in = today + datetime.timedelta(days=30)
    check_out = today + datetime.timedelta(days=31)
    res_id = system.book_room(1, "John Doe", check_in, check_out)
    assert res_id == "RES-0001"
    total_price = 100.0  # 1 night * 100.0
    SHARED['check_in'] = check_in
    SHARED['check_out'] = check_out
    SHARED['res_id'] = res_id
    SHARED['total_price'] = total_price

def test_T4_ERR_book_room_room_not_found(system):
    check_in = SHARED['check_in']
    check_out = SHARED['check_out']
    with pytest.raises(RoomNotFoundError):
        system.book_room(2, "John Doe", check_in, check_out)

def test_T5_ERR_book_room_invalid_dates(system):
    today = datetime.date.today()
    check_in = today + datetime.timedelta(days=5)
    check_out = today + datetime.timedelta(days=4)
    with pytest.raises(InvalidDateError):
        system.book_room(1, "John Doe", check_in, check_out)

def test_T6_ERR_book_room_past_dates(system):
    today = datetime.date.today()
    check_in = today - datetime.timedelta(days=1)
    check_out = today
    with pytest.raises(InvalidDateError):
        system.book_room(1, "John Doe", check_in, check_out)

def test_T7_ERR_book_room_room_unavailable(system):
    check_in = SHARED['check_in']
    check_out = SHARED['check_out']
    with pytest.raises(RoomUnavailableError):
        system.book_room(1, "John Doe", check_in, check_out)

def test_T10_OK_get_room_occupancy(system):
    check_date = SHARED['check_in']
    occupancy = system.get_room_occupancy(check_date)
    assert occupancy == [1]

def test_T8_OK_cancel_reservation(system):
    res_id = SHARED['res_id']
    refund = system.cancel_reservation(res_id)
    assert refund == SHARED['total_price']

def test_T9_ERR_cancel_reservation_not_found(system):
    with pytest.raises(ReservationNotFoundError):
        system.cancel_reservation("RES-0002")

def test_T11_OK_is_room_available(system):
    check_in = SHARED['check_in']
    check_out = SHARED['check_out']
    available = system._is_room_available(1, check_in, check_out)
    assert available is True

def test_T_MISSING_EDGE_1(system):
    system.add_room(1, "single", 100.0)
    system.book_room(1, "John Doe", datetime.date.today() + datetime.timedelta(days=30), datetime.date.today() + datetime.timedelta(days=31))
    system.add_room(2, "double", 0.00001)
    assert 2 in system.rooms
    assert system.rooms[2]['price_per_night'] == 0.00001
    assert system.rooms[2]['type'] == "double"

def test_T_MISSING_EDGE_2(system):
    today = datetime.date.today()
    check_in = today + datetime.timedelta(days=1)
    check_out = today + datetime.timedelta(days=2)
    system.add_room(3, "single", 100.0)
    res_id = system.book_room(3, "John Doe", check_in, check_out)
    assert res_id.startswith("RES-")
    total_price = system.reservations[res_id].total_price
    assert total_price == 100.0

def test_T_MISSING_EDGE_3(system):
    system.add_room(4, "single", 100.0)
    today = datetime.date.today()
    check_in = today + datetime.timedelta(days=5)
    check_out = today + datetime.timedelta(days=6)
    res_id = system.book_room(4, "John Doe", check_in, check_out)
    system.reservations[res_id].check_in = today + datetime.timedelta(days=3)
    refund = system.cancel_reservation(res_id)
    assert refund == 50.0

def test_T_MISSING_EDGE_4(system):
    system.add_room(5, "single", 100.0)
    today = datetime.date.today()
    check_in = today + datetime.timedelta(days=1)
    check_out = today + datetime.timedelta(days=2)
    res_id = system.book_room(5, "John Doe", check_in, check_out)
    refund = system.cancel_reservation(res_id)
    assert refund == 0.0

def test_T_MISSING_EDGE_5(system):
    occupancy = system.get_room_occupancy(datetime.date.today())
    assert occupancy == []

def test_T_MISSING_EDGE_6(system):
    system.add_room(6, "single", 100.0)
    today = datetime.date.today()
    check_in = today + datetime.timedelta(days=30)
    check_out = today + datetime.timedelta(days=31)
    system.book_room(6, "John Doe", check_in, check_out)
    available = system._is_room_available(6, check_in, check_out)
    assert available is False