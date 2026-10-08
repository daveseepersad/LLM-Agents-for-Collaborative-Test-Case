import datetime
import pytest
from data.input_code.d05_hotel import (
    HotelReservationSystem,
    RoomNotFoundError,
    RoomUnavailableError,
    InvalidDateError,
    ReservationNotFoundError,
)

# Helper to monkeypatch datetime.date.today()
@pytest.fixture
def fixed_today(monkeypatch):
    fixed = datetime.date(2023, 1, 1)
    class FixedDate(datetime.date):
        @classmethod
        def today(cls):
            return fixed
    monkeypatch.setattr(datetime, "date", FixedDate)
    return fixed

@pytest.fixture
def system(fixed_today):
    sys = HotelReservationSystem()
    # Add two rooms for testing
    sys.add_room(101, "single", 100.0)
    sys.add_room(102, "double", 150.0)
    return sys

def test_add_room_overwrite_and_invalid_price():
    sys = HotelReservationSystem()
    sys.add_room(200, "suite", 200.0)
    assert sys.rooms[200]["type"] == "suite"
    assert sys.rooms[200]["price_per_night"] == 200.0

    # Overwrite same room number
    sys.add_room(200, "deluxe", 250.0)
    assert sys.rooms[200]["type"] == "deluxe"
    assert sys.rooms[200]["price_per_night"] == 250.0

    # Invalid price raises
    with pytest.raises(ValueError):
        sys.add_room(201, "economy", 0)

    with pytest.raises(ValueError):
        sys.add_room(202, "economy", -10)

def test_book_room_success_and_price_calculation(system, fixed_today):
    check_in = fixed_today + datetime.timedelta(days=10)
    check_out = check_in + datetime.timedelta(days=3)  # 3 nights
    res_id = system.book_room(101, "Alice", check_in, check_out)

    # Verify reservation ID format and storage
    assert res_id.startswith("RES-")
    reservation = system.reservations[res_id]
    assert reservation.room_number == 101
    assert reservation.user_name == "Alice"
    assert reservation.check_in == check_in
    assert reservation.check_out == check_out
    # 3 nights * 100 = 300.0
    assert reservation.total_price == 300.0

def test_book_room_errors(system, fixed_today):
    # Room does not exist
    with pytest.raises(RoomNotFoundError):
        system.book_room(999, "Bob", fixed_today + datetime.timedelta(days=1), fixed_today + datetime.timedelta(days=2))

    # Invalid date range (check_in >= check_out)
    with pytest.raises(InvalidDateError):
        system.book_room(101, "Bob", fixed_today + datetime.timedelta(days=5), fixed_today + datetime.timedelta(days=5))
    with pytest.raises(InvalidDateError):
        system.book_room(101, "Bob", fixed_today + datetime.timedelta(days=6), fixed_today + datetime.timedelta(days=5))

    # Booking in the past
    past_day = fixed_today - datetime.timedelta(days=1)
    future_day = fixed_today + datetime.timedelta(days=1)
    with pytest.raises(InvalidDateError):
        system.book_room(101, "Bob", past_day, future_day)

    # Room unavailable due to overlapping reservation
    check_in = fixed_today + datetime.timedelta(days=10)
    check_out = check_in + datetime.timedelta(days=5)
    res_id = system.book_room(101, "Carol", check_in, check_out)
    # Overlap start inside existing reservation
    with pytest.raises(RoomUnavailableError):
        system.book_room(101, "Dave", check_in + datetime.timedelta(days=2), check_out + datetime.timedelta(days=2))
    # Overlap end inside existing reservation
    with pytest.raises(RoomUnavailableError):
        system.book_room(101, "Eve", check_in - datetime.timedelta(days=2), check_in + datetime.timedelta(days=2))
    # Fully encompassing existing reservation
    with pytest.raises(RoomUnavailableError):
        system.book_room(101, "Frank", check_in - datetime.timedelta(days=1), check_out + datetime.timedelta(days=1))

def test_cancel_reservation_refund_policy(system, fixed_today):
    # Helper to create reservation with specific check-in offset
    def make_reservation(days_until_checkin):
        check_in = fixed_today + datetime.timedelta(days=days_until_checkin)
        check_out = check_in + datetime.timedelta(days=2)
        return system.book_room(102, "Grace", check_in, check_out)

    # >7 days -> full refund
    res_id_full = make_reservation(10)
    reservation_full = system.reservations[res_id_full]
    refund_full = system.cancel_reservation(res_id_full)
    assert refund_full == reservation_full.total_price

    # 2-7 days -> 50% refund (choose 5 days)
    res_id_half = make_reservation(5)
    reservation_half = system.reservations[res_id_half]
    refund_half = system.cancel_reservation(res_id_half)
    assert refund_half == round(reservation_half.total_price * 0.5, 2)

    # <2 days -> no refund (choose 1 day)
    res_id_none = make_reservation(1)
    reservation_none = system.reservations[res_id_none]
    refund_none = system.cancel_reservation(res_id_none)
    assert refund_none == 0.0

    # Cancel non‑existent reservation raises
    with pytest.raises(ReservationNotFoundError):
        system.cancel_reservation("NONEXISTENT")

def test_get_room_occupancy(system, fixed_today):
    # Create two reservations on different rooms and overlapping dates
    check_in_a = fixed_today + datetime.timedelta(days=3)
    check_out_a = check_in_a + datetime.timedelta(days=4)  # occupies days 3,4,5,6
    system.book_room(101, "Heidi", check_in_a, check_out_a)

    check_in_b = fixed_today + datetime.timedelta(days=5)
    check_out_b = check_in_b + datetime.timedelta(days=3)  # occupies days 5,6,7
    system.book_room(102, "Ivan", check_in_b, check_out_b)

    # Day 4: only room 101 occupied
    occupied_day4 = system.get_room_occupancy(fixed_today + datetime.timedelta(days=4))
    assert occupied_day4 == [101]

    # Day 5: both rooms occupied
    occupied_day5 = system.get_room_occupancy(fixed_today + datetime.timedelta(days=5))
    assert occupied_day5 == [101, 102]

    # Day 7: only room 102 occupied (room 101 checkout on day 7)
    occupied_day7 = system.get_room_occupancy(fixed_today + datetime.timedelta(days=7))
    assert occupied_day7 == [102]

    # Day after all checkouts: none occupied
    occupied_day9 = system.get_room_occupancy(fixed_today + datetime.timedelta(days=9))
    assert occupied_day9 == []