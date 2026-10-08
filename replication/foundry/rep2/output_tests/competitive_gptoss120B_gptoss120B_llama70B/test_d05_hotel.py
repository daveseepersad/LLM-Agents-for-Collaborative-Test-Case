import pytest
from datetime import date, timedelta
from data.input_code.d05_hotel import (
    HotelReservationSystem,
    RoomNotFoundError,
    RoomUnavailableError,
    InvalidDateError,
    ReservationNotFoundError,
)

@pytest.fixture
def hotel_system():
    return HotelReservationSystem()

def test_add_room_success(hotel_system):
    hotel_system.add_room(101, "Deluxe", 150.0)
    assert 101 in hotel_system.rooms

def test_add_room_invalid_price(hotel_system):
    with pytest.raises(ValueError):
        hotel_system.add_room(102, "Standard", 0.0)

def test_book_room_room_not_found(hotel_system):
    with pytest.raises(RoomNotFoundError):
        hotel_system.book_room(999, "Alice", date(2099, 1, 1), date(2099, 1, 5))

def test_book_room_invalid_dates_same_day(hotel_system):
    hotel_system.add_room(101, "Deluxe", 150.0)
    with pytest.raises(InvalidDateError):
        hotel_system.book_room(101, "Bob", date(2099, 2, 10), date(2099, 2, 10))

def test_book_room_invalid_dates_past(hotel_system):
    hotel_system.add_room(101, "Deluxe", 150.0)
    with pytest.raises(InvalidDateError):
        hotel_system.book_room(101, "Carol", date(2000, 1, 1), date(2000, 1, 5))

def test_book_room_unavailable(hotel_system):
    hotel_system.add_room(101, "Deluxe", 150.0)
    hotel_system.book_room(101, "Eve", date(2099, 3, 1), date(2099, 3, 5))
    with pytest.raises(RoomUnavailableError):
        hotel_system.book_room(101, "Dave", date(2099, 3, 1), date(2099, 3, 5))

def test_book_room_success(hotel_system):
    hotel_system.add_room(101, "Deluxe", 150.0)
    assert hotel_system.book_room(101, "Eve", date(2099, 4, 10), date(2099, 4, 13)) == "RES-0001"

def test_cancel_reservation_not_found(hotel_system):
    with pytest.raises(ReservationNotFoundError):
        hotel_system.cancel_reservation("NONEXISTENT")

def test_cancel_reservation_full_refund(hotel_system):
    hotel_system.add_room(101, "Deluxe", 100.0)
    # Check‑in far in the future (>7 days from today) to trigger full refund
    hotel_system.book_room(101, "Eve", date(2100, 1, 1), date(2100, 1, 3))
    assert hotel_system.cancel_reservation("RES-0001") == 200.0

def test_cancel_reservation_half_refund(hotel_system):
    hotel_system.add_room(101, "Deluxe", 100.0)
    today = date.today()
    # Check‑in 5 days from today (2‑7 days window) for 50% refund
    check_in = today + timedelta(days=5)
    check_out = check_in + timedelta(days=2)  # 2 nights → total 200.0
    hotel_system.book_room(101, "Eve", check_in, check_out)
    assert hotel_system.cancel_reservation("RES-0001") == 100.0

def test_cancel_reservation_no_refund(hotel_system):
    hotel_system.add_room(101, "Deluxe", 100.0)
    today = date.today()
    # Check‑in 1 day from today (<2 days) for no refund
    check_in = today + timedelta(days=1)
    check_out = check_in + timedelta(days=2)  # 2 nights → total 200.0
    hotel_system.book_room(101, "Eve", check_in, check_out)
    assert hotel_system.cancel_reservation("RES-0001") == 0.0

def test_get_room_occupancy(hotel_system):
    hotel_system.add_room(101, "Deluxe", 150.0)
    hotel_system.book_room(101, "Eve", date(2099, 4, 10), date(2099, 4, 13))
    assert hotel_system.get_room_occupancy(date(2099, 4, 11)) == [101]