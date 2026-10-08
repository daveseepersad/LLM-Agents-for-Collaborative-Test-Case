import pytest
from data.input_code.d05_hotel import HotelReservationSystem, RoomNotFoundError, RoomUnavailableError, InvalidDateError, ReservationNotFoundError
from datetime import date, timedelta

@pytest.fixture
def hotel_system():
    return HotelReservationSystem()

def test_add_room(hotel_system):
    hotel_system.add_room(1, 'single', 100.0)
    assert hotel_system.rooms == {1: {'type': 'single', 'price_per_night': 100.0}}

def test_add_room_invalid_price(hotel_system):
    with pytest.raises(ValueError):
        hotel_system.add_room(1, 'single', -100.0)

def test_book_room(hotel_system):
    hotel_system.add_room(1, 'single', 100.0)
    res_id = hotel_system.book_room(1, 'John Doe', date.today() + timedelta(days=1), date.today() + timedelta(days=3))
    assert res_id in hotel_system.reservations

def test_book_room_non_existent_room(hotel_system):
    with pytest.raises(RoomNotFoundError):
        hotel_system.book_room(1, 'John Doe', date.today() + timedelta(days=1), date.today() + timedelta(days=3))

def test_book_room_invalid_dates(hotel_system):
    hotel_system.add_room(1, 'single', 100.0)
    with pytest.raises(InvalidDateError):
        hotel_system.book_room(1, 'John Doe', date.today() + timedelta(days=3), date.today() + timedelta(days=1))

def test_book_room_past_dates(hotel_system):
    hotel_system.add_room(1, 'single', 100.0)
    with pytest.raises(InvalidDateError):
        hotel_system.book_room(1, 'John Doe', date.today() - timedelta(days=1), date.today() + timedelta(days=1))

def test_book_room_unavailable_room(hotel_system):
    hotel_system.add_room(1, 'single', 100.0)
    hotel_system.book_room(1, 'John Doe', date.today() + timedelta(days=1), date.today() + timedelta(days=3))
    with pytest.raises(RoomUnavailableError):
        hotel_system.book_room(1, 'Jane Doe', date.today() + timedelta(days=1), date.today() + timedelta(days=3))


def test_cancel_reservation_non_existent_reservation(hotel_system):
    with pytest.raises(ReservationNotFoundError):
        hotel_system.cancel_reservation('RES-0001')

def test_get_room_occupancy(hotel_system):
    hotel_system.add_room(1, 'single', 100.0)
    hotel_system.book_room(1, 'John Doe', date.today() + timedelta(days=1), date.today() + timedelta(days=3))
    occupied_rooms = hotel_system.get_room_occupancy(date.today() + timedelta(days=2))
    assert occupied_rooms == [1]

def test_get_room_occupancy_empty(hotel_system):
    occupied_rooms = hotel_system.get_room_occupancy(date.today())
    assert occupied_rooms == []

def test_is_room_available(hotel_system):
    hotel_system.add_room(1, 'single', 100.0)
    assert hotel_system._is_room_available(1, date.today() + timedelta(days=1), date.today() + timedelta(days=3))

def test_is_room_available_unavailable(hotel_system):
    hotel_system.add_room(1, 'single', 100.0)
    hotel_system.book_room(1, 'John Doe', date.today() + timedelta(days=1), date.today() + timedelta(days=3))
    assert not hotel_system._is_room_available(1, date.today() + timedelta(days=1), date.today() + timedelta(days=3))