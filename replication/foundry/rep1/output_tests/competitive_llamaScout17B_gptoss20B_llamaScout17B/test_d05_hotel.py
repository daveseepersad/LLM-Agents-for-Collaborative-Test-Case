import pytest
import datetime
from data.input_code.d05_hotel import *

def test_T1_ADD_ROOM_OK():
    system = HotelReservationSystem()
    result = system.add_room(101, 'Single', 100.0)
    assert result is None

def test_T2_ADD_ROOM_ERR_PRICE():
    system = HotelReservationSystem()
    with pytest.raises(ValueError):
        system.add_room(102, 'Double', 0.0)

def test_T3_BOOK_ROOM_OK():
    system = HotelReservationSystem()
    system.add_room(101, 'Single', 100.0)
    today = datetime.date.today()
    res_id = system.book_room(101, 'John Doe', today + datetime.timedelta(days=1), today + datetime.timedelta(days=3))
    assert res_id == "RES-0001"

def test_T4_BOOK_ROOM_ERR_ROOM_NOT_FOUND():
    system = HotelReservationSystem()
    with pytest.raises(RoomNotFoundError):
        system.book_room(103, 'Jane Doe', datetime.date.today() + datetime.timedelta(days=1), datetime.date.today() + datetime.timedelta(days=3))

def test_T5_BOOK_ROOM_ERR_INVALID_DATES():
    system = HotelReservationSystem()
    system.add_room(101, 'Single', 100.0)
    with pytest.raises(InvalidDateError):
        system.book_room(101, 'John Doe', datetime.date.today() + datetime.timedelta(days=3), datetime.date.today() + datetime.timedelta(days=1))

def test_T6_BOOK_ROOM_ERR_PAST_DATES():
    system = HotelReservationSystem()
    system.add_room(101, 'Single', 100.0)
    today = datetime.date.today()
    with pytest.raises(InvalidDateError):
        system.book_room(101, 'John Doe', today - datetime.timedelta(days=1), today + datetime.timedelta(days=3))

def test_T7_BOOK_ROOM_ERR_ROOM_UNAVAILABLE():
    system = HotelReservationSystem()
    system.add_room(101, 'Single', 100.0)
    today = datetime.date.today()
    system.book_room(101, 'John Doe', today + datetime.timedelta(days=1), today + datetime.timedelta(days=3))
    with pytest.raises(RoomUnavailableError):
        system.book_room(101, 'Jane Doe', today + datetime.timedelta(days=2), today + datetime.timedelta(days=4))

def test_T8_CANCEL_RESERVATION_OK_FULL_REFUND():
    system = HotelReservationSystem()
    system.add_room(101, 'Single', 100.0)
    today = datetime.date.today()
    # Book with a check-in sufficiently far in the future to trigger full refund on cancel
    res_id = system.book_room(101, 'John Doe', today + datetime.timedelta(days=10), today + datetime.timedelta(days=12))
    refund = system.cancel_reservation(res_id)
    assert refund == 200.0

def test_T9_CANCEL_RESERVATION_OK_PARTIAL_REFUND():
    system = HotelReservationSystem()
    system.add_room(101, 'Single', 100.0)
    today = datetime.date.today()
    # Reservation 1: far in future (to avoid overlap with Reservation 2)
    system.book_room(101, 'John Doe', today + datetime.timedelta(days=10), today + datetime.timedelta(days=12))
    # Reservation 2: 2-7 days from today to yield partial refund upon cancellation
    res2 = system.book_room(101, 'John Doe', today + datetime.timedelta(days=6), today + datetime.timedelta(days=8))
    refund = system.cancel_reservation(res2)
    assert refund == 100.0

def test_T10_CANCEL_RESERVATION_OK_NO_REFUND():
    system = HotelReservationSystem()
    system.add_room(101, 'Single', 100.0)
    today = datetime.date.today()
    res = system.book_room(101, 'John Doe', today + datetime.timedelta(days=1), today + datetime.timedelta(days=3))
    refund = system.cancel_reservation(res)
    assert refund == 0.0

def test_T11_CANCEL_RESERVATION_ERR_NOT_FOUND():
    system = HotelReservationSystem()
    with pytest.raises(ReservationNotFoundError):
        system.cancel_reservation("RES-9999")

def test_T12_GET_ROOM_OCCUPANCY_OK():
    system = HotelReservationSystem()
    system.add_room(101, 'Single', 100.0)
    today = datetime.date.today()
    system.book_room(101, 'John Doe', today + datetime.timedelta(days=2), today + datetime.timedelta(days=4))
    occupied = system.get_room_occupancy(today + datetime.timedelta(days=2))
    assert occupied == [101]

def test_T13_GET_ROOM_OCCUPANCY_EMPTY():
    system = HotelReservationSystem()
    occupied = system.get_room_occupancy(datetime.date.today() + datetime.timedelta(days=10))
    assert occupied == []