import pytest
from data.input_code.d05_hotel import *
import datetime

def test_T_MISSING_CANCEL_EDGE_2DAYS():
    system = HotelReservationSystem()
    system.add_room(101, "Standard", 50.0)
    base = datetime.date.today()
    check_in = base + datetime.timedelta(days=2)
    check_out = check_in + datetime.timedelta(days=1)
    res_id = system.book_room(101, "Bob", check_in, check_out)
    assert res_id == "RES-0001"
    refund = system.cancel_reservation(res_id)
    assert refund == 25.0

def test_T_MISSING_ROOM_UNAVAILABLE():
    system = HotelReservationSystem()
    system.add_room(101, "Standard", 50.0)
    today = datetime.date.today()
    day1 = today + datetime.timedelta(days=1)
    day3 = today + datetime.timedelta(days=3)
    # First booking should succeed
    res1 = system.book_room(101, "Alice", day1, day3)
    assert res1 == "RES-0001"
    # Second booking overlapping should raise RoomUnavailableError
    with pytest.raises(RoomUnavailableError):
        system.book_room(101, "Alice", day1, day3 + datetime.timedelta(days=1))

def test_T_MISSING_CANCEL_EDGE_7DAYS():
    system = HotelReservationSystem()
    system.add_room(101, "Standard", 1.0)
    base = datetime.date.today()
    check_in = base + datetime.timedelta(days=7)
    check_out = check_in + datetime.timedelta(days=1)
    res_id = system.book_room(101, "Bob", check_in, check_out)
    assert res_id == "RES-0001"
    refund = system.cancel_reservation(res_id)
    assert refund == 0.5

def test_T_MISSING_INVALID_PRICE():
    system = HotelReservationSystem()
    with pytest.raises(ValueError):
        system.add_room(102, "Deluxe", -10.0)

def test_T_MISSING_GET_OCCUPANCY():
    system = HotelReservationSystem()
    system.add_room(101, "Standard", 50.0)
    base = datetime.date.today()
    check_in = base + datetime.timedelta(days=1)
    check_out = check_in + datetime.timedelta(days=2)
    system.book_room(101, "Alice", check_in, check_out)
    check_date = check_in + datetime.timedelta(days=1)
    occupancy = system.get_room_occupancy(check_date)
    assert occupancy == [101]

def test_T_MISSING_CHECKIN_TODAY():
    system = HotelReservationSystem()
    system.add_room(101, "Standard", 50.0)
    with pytest.raises(InvalidDateError):
        system.book_room(101, "Charlie", datetime.date.today(), datetime.date.today())

import pytest
import datetime
from data.input_code.d05_hotel import *

import pytest
from data.input_code.d05_hotel import *
import datetime

def test_T_MISSING_CANCEL_EDGE_0DAYS():
    system = HotelReservationSystem()
    system.add_room(101, "Standard", 50.0)
    today = datetime.date.today()
    res_id = system.book_room(101, "Alice", today, today + datetime.timedelta(days=1))
    assert res_id == "RES-0001"
    refund = system.cancel_reservation(res_id)
    assert refund == 0.0

def test_T_MISSING_BOOK_PAST_ERROR():
    system = HotelReservationSystem()
    system.add_room(101, "Standard", 50.0)
    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    today = datetime.date.today()
    with pytest.raises(InvalidDateError):
        system.book_room(101, "Alice", yesterday, today)

def test_T_MISSING_ROOM_OVERLAP_PARTIAL():
    system = HotelReservationSystem()
    system.add_room(101, "Standard", 50.0)
    base = datetime.date.today()
    check_in1 = base + datetime.timedelta(days=2)
    check_out1 = base + datetime.timedelta(days=5)
    res1 = system.book_room(101, "Bob", check_in1, check_out1)
    assert res1 == "RES-0001"
    with pytest.raises(RoomUnavailableError):
        system.book_room(101, "Bob", base + datetime.timedelta(days=4), base + datetime.timedelta(days=6))

def test_T_MISSING_GET_OCCUPANCY_EMPTY():
    system = HotelReservationSystem()
    system.add_room(101, "Standard", 50.0)
    date = datetime.date.today()
    occupancy = system.get_room_occupancy(date)
    assert occupancy == []

def test_T_MISSING_CANCEL_NONEXISTENT():
    system = HotelReservationSystem()
    with pytest.raises(ReservationNotFoundError):
        system.cancel_reservation("RES-9999")

def test_T_MISSING_ADD_ROOM_DUPLICATE():
    system = HotelReservationSystem()
    system.add_room(101, "Standard", 50.0)
    system.add_room(101, "Deluxe", 100.0)
    assert system.rooms[101]['type'] == "Deluxe"
    assert system.rooms[101]['price_per_night'] == 100.0