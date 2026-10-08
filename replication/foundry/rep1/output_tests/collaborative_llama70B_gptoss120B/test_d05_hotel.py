import pytest
import datetime
from data.input_code.d05_hotel import *

def future_date(days: int) -> datetime.date:
    """Helper to get a date `days` days from today."""
    return datetime.date.today() + datetime.timedelta(days=days)

@pytest.fixture
def system():
    """Provides a fresh HotelReservationSystem for each test."""
    return HotelReservationSystem()

def test_add_room_success(system):
    system.add_room(room_number=101, room_type="single", price_per_night=100.0)
    assert 101 in system.rooms
    assert system.rooms[101]["type"] == "single"
    assert system.rooms[101]["price_per_night"] == 100.0

def test_add_room_invalid_price(system):
    with pytest.raises(ValueError):
        system.add_room(room_number=102, room_type="double", price_per_night=-50.0)

def test_book_room_success(system):
    system.add_room(room_number=101, room_type="single", price_per_night=100.0)
    res_id = system.book_room(
        room_number=101,
        user_name="John Doe",
        check_in=future_date(20),
        check_out=future_date(25),
    )
    assert res_id == "RES-0001"
    reservation = system.reservations[res_id]
    # 5 nights * 100.0
    assert reservation.total_price == 500.0

def test_book_room_not_found(system):
    with pytest.raises(RoomNotFoundError):
        system.book_room(
            room_number=103,
            user_name="Jane Doe",
            check_in=future_date(20),
            check_out=future_date(25),
        )

def test_book_room_invalid_dates(system):
    system.add_room(room_number=101, room_type="single", price_per_night=100.0)
    with pytest.raises(InvalidDateError):
        system.book_room(
            room_number=101,
            user_name="John Doe",
            check_in=future_date(25),
            check_out=future_date(20),  # checkout before check‑in
        )

def test_book_room_unavailable(system):
    system.add_room(room_number=101, room_type="single", price_per_night=100.0)
    # First reservation occupies the dates
    system.book_room(
        room_number=101,
        user_name="John Doe",
        check_in=future_date(20),
        check_out=future_date(25),
    )
    # Overlapping reservation should fail
    with pytest.raises(RoomUnavailableError):
        system.book_room(
            room_number=101,
            user_name="Jane Doe",
            check_in=future_date(22),
            check_out=future_date(27),
        )

def test_cancel_reservation_success(system):
    system.add_room(room_number=101, room_type="single", price_per_night=100.0)
    # Book far enough in the future to guarantee >7 days until check‑in
    res_id = system.book_room(
        room_number=101,
        user_name="John Doe",
        check_in=future_date(30),
        check_out=future_date(35),
    )
    refund = system.cancel_reservation(reservation_id=res_id)
    # Full refund expected (>7 days before check‑in)
    assert refund == 500.0

def test_cancel_reservation_not_found(system):
    with pytest.raises(ReservationNotFoundError):
        system.cancel_reservation(reservation_id="RES-0002")

def test_get_room_occupancy(system):
    system.add_room(room_number=101, room_type="single", price_per_night=100.0)
    system.book_room(
        room_number=101,
        user_name="John Doe",
        check_in=future_date(20),
        check_out=future_date(25),
    )
    # Choose a date within the reservation window
    occupied = system.get_room_occupancy(date=future_date(22))
    assert occupied == [101]

def test_get_room_occupancy_empty(system):
    # No reservations at all
    occupied = system.get_room_occupancy(date=future_date(1))
    assert occupied == []

import pytest
import datetime
from data.input_code.d05_hotel import *

def test_book_room_past_date(system):
    """Booking a room with a check‑in date in the past should raise InvalidDateError."""
    system.add_room(room_number=101, room_type="single", price_per_night=100.0)
    past_check_in = datetime.date.today() - datetime.timedelta(days=1)
    future_check_out = datetime.date.today() + datetime.timedelta(days=1)
    with pytest.raises(InvalidDateError):
        system.book_room(
            room_number=101,
            user_name="John Doe",
            check_in=past_check_in,
            check_out=future_check_out,
        )

def test_cancel_reservation_refund_50_percent(system):
    """Cancel a reservation that is 7 days away from check‑in (50% refund)."""
    system.add_room(room_number=101, room_type="single", price_per_night=100.0)
    # Booking from day 7 to day 12 (5 nights, total 500.0)
    system.book_room(
        room_number=101,
        user_name="John Doe",
        check_in=future_date(7),
        check_out=future_date(12),
    )
    # The reservation ID generated is RES-0001
    refund = system.cancel_reservation(reservation_id="RES-0001")
    # 50% of 500.0 = 250.0
    assert refund == 250.0

def test_cancel_reservation_refund_0_percent(system):
    """Cancel a reservation that is less than 2 days away from check‑in (0% refund)."""
    system.add_room(room_number=101, room_type="single", price_per_night=100.0)
    # Booking from day 1 to day 6 (5 nights, total 500.0)
    system.book_room(
        room_number=101,
        user_name="John Doe",
        check_in=future_date(1),
        check_out=future_date(6),
    )
    refund = system.cancel_reservation(reservation_id="RES-0001")
    assert refund == 0.0

def test_get_room_occupancy_multiple_rooms(system):
    """Occupancy query should list all rooms occupied on a given date."""
    system.add_room(room_number=101, room_type="single", price_per_night=100.0)
    system.add_room(room_number=102, room_type="double", price_per_night=200.0)
    system.book_room(
        room_number=101,
        user_name="John Doe",
        check_in=future_date(5),
        check_out=future_date(15),
    )
    system.book_room(
        room_number=102,
        user_name="Jane Doe",
        check_in=future_date(5),
        check_out=future_date(15),
    )
    occupied = system.get_room_occupancy(date=future_date(10))
    assert occupied == [101, 102]

def test_book_room_single_night(system):
    """Booking a room for exactly one night should succeed."""
    system.add_room(room_number=101, room_type="single", price_per_night=100.0)
    check_in = datetime.date.today() + datetime.timedelta(days=1)
    check_out = datetime.date.today() + datetime.timedelta(days=2)  # one night later
    res_id = system.book_room(
        room_number=101,
        user_name="John Doe",
        check_in=check_in,
        check_out=check_out,
    )
    assert res_id == "RES-0001"
    reservation = system.reservations[res_id]
    # One night * 100.0 = 100.0
    assert reservation.total_price == 100.0