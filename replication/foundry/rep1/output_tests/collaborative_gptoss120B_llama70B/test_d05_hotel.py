import pytest
from data.input_code.d05_hotel import HotelReservationSystem, RoomNotFoundError, RoomUnavailableError, InvalidDateError, ReservationNotFoundError
from datetime import date, timedelta

@pytest.fixture
def hotel_system():
    return HotelReservationSystem()

def test_add_room_success(hotel_system):
    hotel_system.add_room(101, "Deluxe", 150.0)
    assert 101 in hotel_system.rooms

def test_add_room_invalid_price(hotel_system):
    with pytest.raises(ValueError):
        hotel_system.add_room(102, "Standard", 0.0)

def test_book_room_not_found(hotel_system):
    with pytest.raises(RoomNotFoundError):
        hotel_system.book_room(999, "Alice", date.today() + timedelta(days=1), date.today() + timedelta(days=3))

def test_book_room_invalid_dates_equal(hotel_system):
    hotel_system.add_room(101, "Deluxe", 150.0)
    with pytest.raises(InvalidDateError):
        hotel_system.book_room(101, "Bob", date.today(), date.today())

def test_book_room_invalid_dates_past(hotel_system):
    hotel_system.add_room(101, "Deluxe", 150.0)
    with pytest.raises(InvalidDateError):
        hotel_system.book_room(101, "Carol", date.today() - timedelta(days=1), date.today() + timedelta(days=2))

def test_book_room_unavailable(hotel_system):
    hotel_system.add_room(101, "Deluxe", 150.0)
    hotel_system.book_room(101, "Eve", date.today(), date.today() + timedelta(days=2))
    with pytest.raises(RoomUnavailableError):
        hotel_system.book_room(101, "Dave", date.today() + timedelta(days=1), date.today() + timedelta(days=3))

def test_book_room_success(hotel_system):
    hotel_system.add_room(101, "Deluxe", 150.0)
    res_id = hotel_system.book_room(101, "Eve", date.today(), date.today() + timedelta(days=2))
    assert res_id in hotel_system.reservations

def test_cancel_reservation_not_found(hotel_system):
    with pytest.raises(ReservationNotFoundError):
        hotel_system.cancel_reservation("NON_EXISTENT")

def test_cancel_full_refund(hotel_system):
    hotel_system.add_room(101, "Deluxe", 150.0)
    res_id = hotel_system.book_room(101, "Eve", date.today() + timedelta(days=10), date.today() + timedelta(days=12))
    refund = hotel_system.cancel_reservation(res_id)
    assert refund == 300.0

def test_cancel_half_refund(hotel_system):
    hotel_system.add_room(101, "Deluxe", 150.0)
    res_id = hotel_system.book_room(101, "Eve", date.today() + timedelta(days=4), date.today() + timedelta(days=6))
    refund = hotel_system.cancel_reservation(res_id)
    assert refund == 150.0

def test_cancel_no_refund(hotel_system):
    hotel_system.add_room(101, "Deluxe", 150.0)
    res_id = hotel_system.book_room(101, "Eve", date.today() + timedelta(days=1), date.today() + timedelta(days=3))
    refund = hotel_system.cancel_reservation(res_id)
    assert refund == 0.0

def test_get_occupancy_some(hotel_system):
    hotel_system.add_room(101, "Deluxe", 150.0)
    hotel_system.book_room(101, "Eve", date.today(), date.today() + timedelta(days=2))
    occupied_rooms = hotel_system.get_room_occupancy(date.today() + timedelta(days=1))
    assert occupied_rooms == [101]

def test_get_occupancy_none(hotel_system):
    occupied_rooms = hotel_system.get_room_occupancy(date.today() + timedelta(days=30))
    assert occupied_rooms == []