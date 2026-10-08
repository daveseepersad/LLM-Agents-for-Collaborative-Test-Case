import pytest
from data.input_code.d05_hotel import *
from datetime import date, timedelta

@pytest.fixture
def hotel_system():
    return HotelReservationSystem()

def test_add_room_ok(hotel_system):
    hotel_system.add_room(101, "Deluxe", 150.0)
    assert 101 in hotel_system.rooms

def test_add_room_invalid_price(hotel_system):
    with pytest.raises(ValueError):
        hotel_system.add_room(102, "Standard", -10.0)

@pytest.mark.parametrize('room_number, user_name, check_in, check_out, expected', [
    (101, "Alice", date(2026, 10, 20), date(2026, 10, 22), "RES-0001")
])
def test_book_room_ok(hotel_system, room_number, user_name, check_in, check_out, expected):
    hotel_system.add_room(room_number, "Deluxe", 150.0)
    assert hotel_system.book_room(room_number, user_name, check_in, check_out) == expected

@pytest.mark.parametrize('room_number, user_name, check_in, check_out, expected_exception', [
    (9999, "Bob", date(2026, 10, 24), date(2026, 10, 26), RoomNotFoundError),
    (101, "Carol", date(2026, 10, 25), date(2026, 10, 25), InvalidDateError),
    (101, "Dan", date(2020, 1, 1), date(2020, 1, 2), InvalidDateError)
])
def test_book_room_error(hotel_system, room_number, user_name, check_in, check_out, expected_exception):
    hotel_system.add_room(101, "Deluxe", 150.0)
    with pytest.raises(expected_exception):
        hotel_system.book_room(room_number, user_name, check_in, check_out)

def test_cancel_reservation_not_found(hotel_system):
    with pytest.raises(ReservationNotFoundError):
        hotel_system.cancel_reservation("RES-UNKNOWN")

def test_get_room_occupancy_empty(hotel_system):
    assert hotel_system.get_room_occupancy(date(2026, 10, 21)) == []

def test_add_room_zero_price(hotel_system):
    with pytest.raises(ValueError):
        hotel_system.add_room(301, "Standard", 0.0)

@pytest.mark.parametrize('check_in, expected_refund', [
    (date.today() + timedelta(days=8), 360.0),
    (date.today() + timedelta(days=5), 180.0),
    (date.today() + timedelta(days=1), 0.0)
])
def test_cancel_reservation_refund(hotel_system, check_in, expected_refund):
    hotel_system.add_room(101, "Deluxe", 120.0)
    reservation_id = hotel_system.book_room(101, "TestUser", check_in, check_in + timedelta(days=3))
    assert hotel_system.cancel_reservation(reservation_id) == expected_refund

@pytest.mark.parametrize('room_number, user_name, check_in, check_out, expected_exception', [
    (102, "Alice", date(2026, 10, 20), date(2026, 10, 22), RoomUnavailableError)
])
def test_book_room_overlap_error(hotel_system, room_number, user_name, check_in, check_out, expected_exception):
    hotel_system.add_room(room_number, "Deluxe", 150.0)
    hotel_system.book_room(room_number, user_name, check_in, check_out)
    with pytest.raises(expected_exception):
        hotel_system.book_room(room_number, "Charlie", check_in, check_out)

def test_get_room_occupancy_with_reservation(hotel_system):
    hotel_system.add_room(103, "Deluxe", 150.0)
    hotel_system.book_room(103, "David", date(2026, 10, 20), date(2026, 10, 22))
    assert hotel_system.get_room_occupancy(date(2026, 10, 21)) == [103]

def test_book_room_boundary_ok(hotel_system):
    hotel_system.add_room(103, "Deluxe", 150.0)
    hotel_system.book_room(103, "Eve", date(2026, 10, 20), date(2026, 10, 22))
    assert hotel_system.book_room(103, "Bob", date(2026, 10, 22), date(2026, 10, 24)) == "RES-0002"