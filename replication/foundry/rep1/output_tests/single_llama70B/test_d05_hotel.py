import pytest
from data.input_code.d05_hotel import HotelReservationSystem, RoomNotFoundError, RoomUnavailableError, InvalidDateError, ReservationNotFoundError
from datetime import date, timedelta

def test_init():
    hotel = HotelReservationSystem()
    assert hotel.rooms == {}
    assert hotel.reservations == {}
    assert hotel._reservation_counter == 0

def test_add_room():
    hotel = HotelReservationSystem()
    hotel.add_room(1, 'single', 100.0)
    assert hotel.rooms == {1: {'type': 'single', 'price_per_night': 100.0}}

def test_add_room_overwrite():
    hotel = HotelReservationSystem()
    hotel.add_room(1, 'single', 100.0)
    hotel.add_room(1, 'double', 200.0)
    assert hotel.rooms == {1: {'type': 'double', 'price_per_night': 200.0}}

def test_add_room_invalid_price():
    hotel = HotelReservationSystem()
    with pytest.raises(ValueError):
        hotel.add_room(1, 'single', -100.0)

def test_is_room_available():
    hotel = HotelReservationSystem()
    hotel.add_room(1, 'single', 100.0)
    assert hotel._is_room_available(1, date.today() + timedelta(days=1), date.today() + timedelta(days=3)) == True

def test_is_room_available_booked():
    hotel = HotelReservationSystem()
    hotel.add_room(1, 'single', 100.0)
    hotel.book_room(1, 'user', date.today() + timedelta(days=1), date.today() + timedelta(days=3))
    assert hotel._is_room_available(1, date.today() + timedelta(days=1), date.today() + timedelta(days=3)) == False

def test_book_room():
    hotel = HotelReservationSystem()
    hotel.add_room(1, 'single', 100.0)
    res_id = hotel.book_room(1, 'user', date.today() + timedelta(days=1), date.today() + timedelta(days=3))
    assert res_id in hotel.reservations

def test_book_room_room_not_found():
    hotel = HotelReservationSystem()
    with pytest.raises(RoomNotFoundError):
        hotel.book_room(1, 'user', date.today() + timedelta(days=1), date.today() + timedelta(days=3))

def test_book_room_invalid_dates():
    hotel = HotelReservationSystem()
    hotel.add_room(1, 'single', 100.0)
    with pytest.raises(InvalidDateError):
        hotel.book_room(1, 'user', date.today() + timedelta(days=3), date.today() + timedelta(days=1))

def test_book_room_past_dates():
    hotel = HotelReservationSystem()
    hotel.add_room(1, 'single', 100.0)
    with pytest.raises(InvalidDateError):
        hotel.book_room(1, 'user', date.today() - timedelta(days=1), date.today() + timedelta(days=1))

def test_book_room_room_unavailable():
    hotel = HotelReservationSystem()
    hotel.add_room(1, 'single', 100.0)
    hotel.book_room(1, 'user', date.today() + timedelta(days=1), date.today() + timedelta(days=3))
    with pytest.raises(RoomUnavailableError):
        hotel.book_room(1, 'user', date.today() + timedelta(days=1), date.today() + timedelta(days=3))


def test_cancel_reservation_not_found():
    hotel = HotelReservationSystem()
    with pytest.raises(ReservationNotFoundError):
        hotel.cancel_reservation('RES-0001')


def test_cancel_reservation_no_refund():
    hotel = HotelReservationSystem()
    hotel.add_room(1, 'single', 100.0)
    res_id = hotel.book_room(1, 'user', date.today() + timedelta(days=1), date.today() + timedelta(days=3))
    refund = hotel.cancel_reservation(res_id)
    assert refund == 0.0

def test_get_room_occupancy():
    hotel = HotelReservationSystem()
    hotel.add_room(1, 'single', 100.0)
    hotel.add_room(2, 'double', 200.0)
    hotel.book_room(1, 'user', date.today(), date.today() + timedelta(days=1))
    hotel.book_room(2, 'user', date.today(), date.today() + timedelta(days=1))
    occupied_rooms = hotel.get_room_occupancy(date.today())
    assert occupied_rooms == [1, 2]

def test_get_room_occupancy_empty():
    hotel = HotelReservationSystem()
    occupied_rooms = hotel.get_room_occupancy(date.today())
    assert occupied_rooms == []