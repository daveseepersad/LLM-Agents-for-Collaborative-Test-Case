import pytest
import datetime
import data.input_code.d05_hotel as hotel_mod
from data.input_code.d05_hotel import *

def test_T1_OK_add_room():
    system = HotelReservationSystem()
    result = system.add_room(1, "single", 100.0)
    assert result is None
    assert 1 in system.rooms
    assert system.rooms[1] == {'type': 'single', 'price_per_night': 100.0}

def test_T2_ERR_add_room():
    system = HotelReservationSystem()
    with pytest.raises(ValueError):
        system.add_room(1, "single", 0.0)

def test_T3_OK_book_room():
    system = HotelReservationSystem()
    system.add_room(1, "single", 100.0)
    base = datetime.date.today()
    check_in = base + datetime.timedelta(days=10)
    check_out = base + datetime.timedelta(days=15)
    res_id = system.book_room(1, "John", check_in, check_out)
    assert res_id == "RES-0001"
    assert res_id in system.reservations
    assert system.reservations[res_id].total_price == 500.0

def test_T4_ERR_book_room_room_not_found():
    system = HotelReservationSystem()
    system.add_room(1, "single", 100.0)
    base = datetime.date.today()
    check_in = base + datetime.timedelta(days=10)
    check_out = base + datetime.timedelta(days=15)
    with pytest.raises(RoomNotFoundError):
        system.book_room(2, "John", check_in, check_out)

def test_T5_ERR_book_room_invalid_dates():
    system = HotelReservationSystem()
    system.add_room(1, "single", 100.0)
    base = datetime.date.today()
    check_in = base + datetime.timedelta(days=10)
    check_out = base + datetime.timedelta(days=5)  # invalid: check_out before check_in
    with pytest.raises(InvalidDateError):
        system.book_room(1, "John", check_in, check_out)

def test_T6_ERR_book_room_room_unavailable():
    system = HotelReservationSystem()
    system.add_room(1, "single", 100.0)
    base = datetime.date.today()
    s = base + datetime.timedelta(days=20)
    e = base + datetime.timedelta(days=25)
    system.book_room(1, "Alice", s, e)
    with pytest.raises(RoomUnavailableError):
        system.book_room(1, "John", s, e)

def test_T7_OK_cancel_reservation():
    system = HotelReservationSystem()
    system.add_room(1, "single", 100.0)
    base = datetime.date.today()
    s = base + datetime.timedelta(days=25)
    e = base + datetime.timedelta(days=30)
    res_id = system.book_room(1, "John", s, e)
    refund = system.cancel_reservation(res_id)
    assert refund == 500.0

def test_T8_ERR_cancel_reservation_not_found():
    system = HotelReservationSystem()
    with pytest.raises(ReservationNotFoundError):
        system.cancel_reservation("RES-0001")

def test_T9_OK_get_room_occupancy():
    system = HotelReservationSystem()
    system.add_room(1, "single", 100.0)
    base = datetime.date.today()
    si = base + datetime.timedelta(days=20)
    so = base + datetime.timedelta(days=23)
    system.book_room(1, "John", si, so)
    occupancy = system.get_room_occupancy(base + datetime.timedelta(days=22))
    assert occupancy == [1]

def test_T10_OK_is_room_available():
    system = HotelReservationSystem()
    system.add_room(1, "single", 100.0)
    base = datetime.date.today()
    assert system._is_room_available(1, base + datetime.timedelta(days=20), base + datetime.timedelta(days=25)) is True

def test_T11_ERR_is_room_available():
    system = HotelReservationSystem()
    system.add_room(1, "single", 100.0)
    base = datetime.date.today()
    s = base + datetime.timedelta(days=20)
    e = base + datetime.timedelta(days=25)
    system.book_room(1, "John", s, e)
    assert system._is_room_available(1, s, e) is False

import pytest
import datetime
from data.input_code.d05_hotel import *

def test_T_MISSING_EDGE_BOOK_PAST():
    system = HotelReservationSystem()
    system.add_room(1, "single", 100.0)
    check_in = datetime.date.today() - datetime.timedelta(days=1)
    check_out = datetime.date.today() + datetime.timedelta(days=1)
    with pytest.raises(InvalidDateError):
        system.book_room(1, "John", check_in, check_out)

def test_T_MISSING_EDGE_CANCEL_REFUND_50():
    system = HotelReservationSystem()
    system.add_room(1, "single", 100.0)
    base = datetime.date.today()
    s = base + datetime.timedelta(days=5)
    e = base + datetime.timedelta(days=10)
    res_id = system.book_room(1, "John", s, e)
    refund = system.cancel_reservation(res_id)
    assert refund == 250.0

def test_T_MISSING_EDGE_CANCEL_REFUND_0():
    system = HotelReservationSystem()
    system.add_room(1, "single", 100.0)
    base = datetime.date.today()
    s = base + datetime.timedelta(days=1)
    e = base + datetime.timedelta(days=6)
    res_id = system.book_room(1, "John", s, e)
    refund = system.cancel_reservation(res_id)
    assert refund == 0.0

def test_T_MISSING_EDGE_GET_ROOM_OCCUPANCY_EMPTY():
    system = HotelReservationSystem()
    date = datetime.date.today()
    occupancy = system.get_room_occupancy(date)
    assert occupancy == []

def test_T_MISSING_EDGE_GET_ROOM_OCCUPANCY_MULTIPLE():
    system = HotelReservationSystem()
    system.add_room(1, "single", 100.0)
    system.add_room(2, "single", 100.0)
    base = datetime.date.today()
    s = base + datetime.timedelta(days=10)
    e = base + datetime.timedelta(days=15)
    system.book_room(1, "John", s, e)
    system.book_room(2, "Jane", s, e)
    occupancy = system.get_room_occupancy(base + datetime.timedelta(days=10))
    assert occupancy == [1, 2]