import pytest
import datetime
from data.input_code.d05_hotel import (
    RoomNotFoundError,
    RoomUnavailableError,
    InvalidDateError,
    ReservationNotFoundError,
    HotelReservationSystem,
    Reservation
)

@pytest.fixture
def hotel_system():
    return HotelReservationSystem()

def test_add_room_success(hotel_system):
    hotel_system.add_room(101, "Deluxe", 150.0)
    assert hotel_system.rooms[101] == {'type': 'Deluxe', 'price_per_night': 150.0}

def test_add_room_negative_price(hotel_system):
    with pytest.raises(ValueError):
        hotel_system.add_room(102, "Suite", -100.0)

def test_book_room_nonexistent(hotel_system):
    with pytest.raises(RoomNotFoundError):
        hotel_system.book_room(999, "John Doe", datetime.date(2023, 10, 1), datetime.date(2023, 10, 5))

def test_book_room_invalid_dates(hotel_system):
    hotel_system.add_room(101, "Deluxe", 150.0)
    with pytest.raises(InvalidDateError):
        hotel_system.book_room(101, "John Doe", datetime.date(2023, 10, 5), datetime.date(2023, 10, 1))

def test_book_room_past_dates(hotel_system):
    hotel_system.add_room(101, "Deluxe", 150.0)
    with pytest.raises(InvalidDateError):
        hotel_system.book_room(101, "John Doe", datetime.date(2022, 10, 1), datetime.date(2022, 10, 5))



def test_cancel_reservation_nonexistent(hotel_system):
    with pytest.raises(ReservationNotFoundError):
        hotel_system.cancel_reservation("RES-0001")




def test_get_room_occupancy_empty(hotel_system):
    assert hotel_system.get_room_occupancy(datetime.date(2023, 10, 1)) == []


