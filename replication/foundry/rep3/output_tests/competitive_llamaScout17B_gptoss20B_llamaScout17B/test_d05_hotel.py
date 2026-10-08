import pytest
from data.input_code.d05_hotel import *
import datetime

def test_T1_INIT():
    system = HotelReservationSystem()
    assert system.rooms == {}
    assert system.reservations == {}

def test_T2_ADD_ROOM_VALID():
    system = HotelReservationSystem()
    system.add_room(101, "Single", 100.0)
    assert 101 in system.rooms
    assert system.rooms[101]['type'] == "Single"
    assert system.rooms[101]['price_per_night'] == 100.0

def test_T3_ADD_ROOM_INVALID_PRICE():
    system = HotelReservationSystem()
    with pytest.raises(ValueError):
        system.add_room(102, "Double", -50.0)

def test_T4_BOOK_ROOM_NONEXISTENT():
    system = HotelReservationSystem()
    today = datetime.date.today()
    check_in = today + datetime.timedelta(days=1)
    check_out = today + datetime.timedelta(days=3)
    with pytest.raises(RoomNotFoundError):
        system.book_room(103, "John", check_in, check_out)

def test_T5_BOOK_ROOM_INVALID_DATES():
    system = HotelReservationSystem()
    system.add_room(101, "Single", 100.0)
    today = datetime.date.today()
    check_in = today + datetime.timedelta(days=3)
    check_out = today + datetime.timedelta(days=1)
    with pytest.raises(InvalidDateError):
        system.book_room(101, "John", check_in, check_out)

def test_T6_BOOK_ROOM_PAST():
    system = HotelReservationSystem()
    system.add_room(101, "Single", 100.0)
    today = datetime.date.today()
    check_in = today - datetime.timedelta(days=1)
    check_out = today + datetime.timedelta(days=1)
    with pytest.raises(InvalidDateError):
        system.book_room(101, "John", check_in, check_out)

def test_T7_BOOK_ROOM_SUCCESS():
    system = HotelReservationSystem()
    system.add_room(101, "Single", 100.0)
    today = datetime.date.today()
    check_in = today + datetime.timedelta(days=1)
    check_out = today + datetime.timedelta(days=3)
    res_id = system.book_room(101, "John", check_in, check_out)
    assert res_id == "RES-0001"
    assert res_id in system.reservations
    assert system.reservations[res_id].room_number == 101

def test_T8_BOOK_ROOM_UNAVAILABLE():
    system = HotelReservationSystem()
    system.add_room(101, "Single", 100.0)
    today = datetime.date.today()
    res_id = system.book_room(101, "John", today + datetime.timedelta(days=1), today + datetime.timedelta(days=3))
    assert res_id == "RES-0001"
    with pytest.raises(RoomUnavailableError):
        system.book_room(101, "Jane", today + datetime.timedelta(days=2), today + datetime.timedelta(days=4))

def test_T9_CANCEL_NONEXISTENT():
    system = HotelReservationSystem()
    with pytest.raises(ReservationNotFoundError):
        system.cancel_reservation("RES-9999")

def test_T10_CANCEL_FULL_REFUND():
    system = HotelReservationSystem()
    system.add_room(101, "Single", 100.0)
    today = datetime.date.today()
    res_id = system.book_room(101, "John", today + datetime.timedelta(days=10), today + datetime.timedelta(days=12))
    assert res_id == "RES-0001"
    refund = system.cancel_reservation(res_id)
    assert refund == 200.0

def test_T11_GET_OCCUPANCY():
    system = HotelReservationSystem()
    system.add_room(101, "Single", 100.0)
    today = datetime.date.today()
    system.book_room(101, "John", today + datetime.timedelta(days=2), today + datetime.timedelta(days=4))
    occupancy = system.get_room_occupancy(today + datetime.timedelta(days=3))
    assert occupancy == [101]

def test_T_MISSING_PARTIAL_REFUND():
    system = HotelReservationSystem()
    system.add_room(101, "Single", 100.0)
    today = datetime.date.today()
    res_id = system.book_room(101, "Alice", today + datetime.timedelta(days=5), today + datetime.timedelta(days=7))
    assert res_id == "RES-0001"
    refund = system.cancel_reservation(res_id)
    assert refund == 100.0

def test_T_MISSING_NO_REFUND():
    system = HotelReservationSystem()
    system.add_room(101, "Single", 100.0)
    today = datetime.date.today()
    res_id = system.book_room(101, "Bob", today + datetime.timedelta(days=1), today + datetime.timedelta(days=3))
    assert res_id == "RES-0001"
    refund = system.cancel_reservation(res_id)
    assert refund == 0.0

def test_T_MISSING_MULTIPLE_ROOMS_OCCUPANCY():
    system = HotelReservationSystem()
    system.add_room(101, "Single", 100.0)
    system.add_room(102, "Double", 150.0)
    today = datetime.date.today()
    system.book_room(101, "A", today + datetime.timedelta(days=2), today + datetime.timedelta(days=4))
    system.book_room(102, "B", today + datetime.timedelta(days=1), today + datetime.timedelta(days=5))
    occupancy = system.get_room_occupancy(today + datetime.timedelta(days=3))
    assert occupancy == [101, 102]

def test_T_MISSING_EDGE_CASE_CHECKIN_TODAY():
    system = HotelReservationSystem()
    system.add_room(101, "Single", 100.0)
    today = datetime.date.today()
    res_id = system.book_room(101, "John", today, today + datetime.timedelta(days=1))
    assert res_id == "RES-0001"
    assert res_id in system.reservations

def test_T_MISSING_OVERWRITE_ROOM():
    system = HotelReservationSystem()
    system.add_room(101, "Single", 100.0)
    result = system.add_room(101, "Double", 200.0)
    assert result is None
    assert system.rooms[101]['type'] == "Double"
    assert system.rooms[101]['price_per_night'] == 200.0