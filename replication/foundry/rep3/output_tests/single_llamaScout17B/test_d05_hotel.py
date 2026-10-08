import pytest
from datetime import date, timedelta
from data.input_code.d05_hotel import (
    HotelReservationSystem,
    RoomNotFoundError,
    RoomUnavailableError,
    InvalidDateError,
    ReservationNotFoundError
)

def test_add_room_valid():
    hotel = HotelReservationSystem()
    hotel.add_room(101, "Single", 100.0)
    assert hotel.rooms[101]['type'] == "Single"
    assert hotel.rooms[101]['price_per_night'] == 100.0

def test_add_room_invalid_price():
    hotel = HotelReservationSystem()
    with pytest.raises(ValueError):
        hotel.add_room(101, "Single", -100.0)

def test_add_room_zero_price():
    hotel = HotelReservationSystem()
    with pytest.raises(ValueError):
        hotel.add_room(101, "Single", 0.0)

def test_book_room_room_not_found():
    hotel = HotelReservationSystem()
    with pytest.raises(RoomNotFoundError):
        hotel.book_room(101, "John Doe", date.today() + timedelta(days=1), date.today() + timedelta(days=2))

def test_book_room_invalid_dates():
    hotel = HotelReservationSystem()
    hotel.add_room(101, "Single", 100.0)
    with pytest.raises(InvalidDateError):
        hotel.book_room(101, "John Doe", date.today() + timedelta(days=2), date.today() + timedelta(days=1))

def test_book_room_past_date():
    hotel = HotelReservationSystem()
    hotel.add_room(101, "Single", 100.0)
    with pytest.raises(InvalidDateError):
        hotel.book_room(101, "John Doe", date.today() - timedelta(days=1), date.today() + timedelta(days=1))

def test_book_room_unavailable():
    hotel = HotelReservationSystem()
    hotel.add_room(101, "Single", 100.0)
    hotel.book_room(101, "John Doe", date.today() + timedelta(days=1), date.today() + timedelta(days=2))
    with pytest.raises(RoomUnavailableError):
        hotel.book_room(101, "Jane Doe", date.today() + timedelta(days=1), date.today() + timedelta(days=2))

def test_book_room_success():
    hotel = HotelReservationSystem()
    hotel.add_room(101, "Single", 100.0)
    res_id = hotel.book_room(101, "John Doe", date.today() + timedelta(days=1), date.today() + timedelta(days=2))
    assert res_id.startswith("RES-")
    assert len(res_id) == 8

def test_cancel_reservation_not_found():
    hotel = HotelReservationSystem()
    with pytest.raises(ReservationNotFoundError):
        hotel.cancel_reservation("RES-0001")

def test_cancel_reservation_refund_policy():
    hotel = HotelReservationSystem()
    hotel.add_room(101, "Single", 100.0)
    res_id = hotel.book_room(101, "John Doe", date.today() + timedelta(days=10), date.today() + timedelta(days=12))
    # More than 7 days
    assert hotel.cancel_reservation(res_id) == 200.0
    
    res_id = hotel.book_room(101, "John Doe", date.today() + timedelta(days=5), date.today() + timedelta(days=7))
    # Between 2 and 7 days
    assert hotel.cancel_reservation(res_id) == 100.0
    
    res_id = hotel.book_room(101, "John Doe", date.today() + timedelta(days=1), date.today() + timedelta(days=3))
    # Less than 2 days
    assert hotel.cancel_reservation(res_id) == 0.0

def test_get_room_occupancy():
    hotel = HotelReservationSystem()
    hotel.add_room(101, "Single", 100.0)
    hotel.add_room(102, "Double", 200.0)
    hotel.book_room(101, "John Doe", date.today() + timedelta(days=1), date.today() + timedelta(days=3))
    hotel.book_room(102, "Jane Doe", date.today() + timedelta(days=2), date.today() + timedelta(days=4))
    assert hotel.get_room_occupancy(date.today() + timedelta(days=1)) == [101]
    assert hotel.get_room_occupancy(date.today() + timedelta(days=2)) == [101, 102]
    assert hotel.get_room_occupancy(date.today() + timedelta(days=3)) == [102]
    assert hotel.get_room_occupancy(date.today() + timedelta(days=4)) == []


