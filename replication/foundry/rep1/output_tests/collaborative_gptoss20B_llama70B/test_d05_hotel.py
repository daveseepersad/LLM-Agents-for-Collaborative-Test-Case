import pytest
from data.input_code.d05_hotel import *
from datetime import date, timedelta

@pytest.fixture
def hotel_system():
    return HotelReservationSystem()

def test_add_room_valid(hotel_system):
    hotel_system.add_room(101, "Deluxe", 120.0)
    assert 101 in hotel_system.rooms

def test_add_room_invalid_price(hotel_system):
    with pytest.raises(ValueError):
        hotel_system.add_room(102, "Standard", 0)

def test_book_room_room_not_found(hotel_system):
    with pytest.raises(RoomNotFoundError):
        hotel_system.book_room(999, "Alice", date.today() + timedelta(days=1), date.today() + timedelta(days=3))

def test_book_room_invalid_dates(hotel_system):
    hotel_system.add_room(101, "Deluxe", 120.0)
    with pytest.raises(InvalidDateError):
        hotel_system.book_room(101, "Bob", date.today() + timedelta(days=3), date.today() + timedelta(days=3))

def test_book_room_past_date(hotel_system):
    hotel_system.add_room(101, "Deluxe", 120.0)
    with pytest.raises(InvalidDateError):
        hotel_system.book_room(101, "Charlie", date.today() - timedelta(days=1), date.today() + timedelta(days=1))

def test_cancel_reservation_not_found(hotel_system):
    with pytest.raises(ReservationNotFoundError):
        hotel_system.cancel_reservation("RES-9999")

def test_get_room_occupancy_empty(hotel_system):
    assert hotel_system.get_room_occupancy(date.today() + timedelta(days=1)) == []

@pytest.mark.parametrize("room_number, user_name, check_in, check_out, expected", [
    (201, "Alice", date.today() + timedelta(days=5), date.today() + timedelta(days=7), "RES-0001")
])
def test_book_room_success(hotel_system, room_number, user_name, check_in, check_out, expected):
    hotel_system.add_room(room_number, "Deluxe", 120.0)
    assert hotel_system.book_room(room_number, user_name, check_in, check_out) == expected

def test_book_room_overlapping_dates(hotel_system):
    hotel_system.add_room(203, "Standard", 100.0)
    hotel_system.book_room(203, "Charlie", date.today() + timedelta(days=3), date.today() + timedelta(days=5))
    with pytest.raises(RoomUnavailableError):
        hotel_system.book_room(203, "Bob", date.today() + timedelta(days=4), date.today() + timedelta(days=6))

def test_get_room_occupancy(hotel_system):
    hotel_system.add_room(203, "Standard", 100.0)
    hotel_system.book_room(203, "Bob", date.today() + timedelta(days=3), date.today() + timedelta(days=6))
    assert hotel_system.get_room_occupancy(date.today() + timedelta(days=4)) == [203]

def test_add_room_overwrite(hotel_system):
    hotel_system.add_room(301, "Suite", 150.0)
    hotel_system.add_room(301, "Suite", 180.0)
    assert hotel_system.rooms[301]['price_per_night'] == 180.0

@pytest.fixture
def hotel_system_with_reservation():
    hotel_system = HotelReservationSystem()
    hotel_system.add_room(101, "Deluxe", 100.0)
    return hotel_system

def test_cancel_reservation_full_refund(hotel_system_with_reservation):
    reservation_id = hotel_system_with_reservation.book_room(101, "Alice", date.today() + timedelta(days=10), date.today() + timedelta(days=12))
    refund = hotel_system_with_reservation.cancel_reservation(reservation_id)
    assert refund == 200.0

def test_cancel_reservation_half_refund(hotel_system):
    hotel_system.add_room(101, "Deluxe", 100.0)
    reservation_id = hotel_system.book_room(101, "Alice", date.today() + timedelta(days=5), date.today() + timedelta(days=7))
    refund = hotel_system.cancel_reservation(reservation_id)
    assert refund == 100.0

def test_cancel_reservation_no_refund(hotel_system):
    hotel_system.add_room(101, "Deluxe", 100.0)
    reservation_id = hotel_system.book_room(101, "Alice", date.today() + timedelta(days=1), date.today() + timedelta(days=3))
    refund = hotel_system.cancel_reservation(reservation_id)
    assert refund == 0.0