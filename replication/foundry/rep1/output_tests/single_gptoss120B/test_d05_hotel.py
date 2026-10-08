import datetime
import pytest
from datetime import timedelta

from data.input_code.d05_hotel import (
    HotelReservationSystem,
    RoomNotFoundError,
    RoomUnavailableError,
    InvalidDateError,
    ReservationNotFoundError,
)


@pytest.fixture
def system():
    sys = HotelReservationSystem()
    # Add a sample room
    sys.add_room(room_number=101, room_type="single", price_per_night=100.0)
    return sys


def test_add_room_invalid_price_raises():
    sys = HotelReservationSystem()
    with pytest.raises(ValueError):
        sys.add_room(room_number=1, room_type="double", price_per_night=0)
    with pytest.raises(ValueError):
        sys.add_room(room_number=2, room_type="double", price_per_night=-10)


def test_add_room_overwrites_existing():
    sys = HotelReservationSystem()
    sys.add_room(101, "single", 80.0)
    assert sys.rooms[101]["price_per_night"] == 80.0
    # Overwrite with new price
    sys.add_room(101, "single", 120.0)
    assert sys.rooms[101]["price_per_night"] == 120.0


def test_book_room_success_price_and_id(system):
    today = datetime.date.today()
    check_in = today + timedelta(days=1)
    check_out = check_in + timedelta(days=3)  # 3 nights
    res_id = system.book_room(
        room_number=101,
        user_name="Alice",
        check_in=check_in,
        check_out=check_out,
    )
    assert res_id == "RES-0001"
    reservation = system.reservations[res_id]
    assert reservation.total_price == round(3 * 100.0, 2)
    # Booking same room non‑overlapping (adjacent) should succeed
    next_check_in = check_out
    next_check_out = next_check_in + timedelta(days=2)
    res_id2 = system.book_room(
        room_number=101,
        user_name="Bob",
        check_in=next_check_in,
        check_out=next_check_out,
    )
    assert res_id2 == "RES-0002"


def test_book_room_errors(system):
    today = datetime.date.today()
    future = today + timedelta(days=5)
    # Room not found
    with pytest.raises(RoomNotFoundError):
        system.book_room(999, "User", future, future + timedelta(days=1))
    # Invalid dates: check_in == check_out
    with pytest.raises(InvalidDateError):
        system.book_room(101, "User", future, future)
    # Invalid dates: check_in > check_out
    with pytest.raises(InvalidDateError):
        system.book_room(101, "User", future + timedelta(days=2), future)
    # Past date
    past = today - timedelta(days=1)
    with pytest.raises(InvalidDateError):
        system.book_room(101, "User", past, past + timedelta(days=2))
    # Unavailable (overlap)
    check_in = today + timedelta(days=10)
    check_out = check_in + timedelta(days=4)
    system.book_room(101, "First", check_in, check_out)
    # Overlap start
    with pytest.raises(RoomUnavailableError):
        system.book_room(101, "Overlap1", check_in - timedelta(days=1), check_in + timedelta(days=1))
    # Overlap end
    with pytest.raises(RoomUnavailableError):
        system.book_room(101, "Overlap2", check_out - timedelta(days=1), check_out + timedelta(days=1))
    # Fully inside existing reservation
    with pytest.raises(RoomUnavailableError):
        system.book_room(101, "Overlap3", check_in + timedelta(days=1), check_out - timedelta(days=1))


@pytest.mark.parametrize(
    "days_until_checkin, expected_refund_factor",
    [
        (8, 1.0),   # >7 days => full refund
        (7, 0.5),   # exactly 7 days => 50%
        (5, 0.5),   # between 2 and 7 => 50%
        (2, 0.5),   # exactly 2 days => 50%
        (1, 0.0),   # <2 days => 0%
        (0, 0.0),   # same day => 0%
    ],
)
def test_cancel_reservation_refund_policy(system, days_until_checkin, expected_refund_factor):
    today = datetime.date.today()
    check_in = today + timedelta(days=days_until_checkin)
    check_out = check_in + timedelta(days=2)
    res_id = system.book_room(101, "Guest", check_in, check_out)
    reservation = system.reservations[res_id]
    expected_refund = round(reservation.total_price * expected_refund_factor, 2)
    refund = system.cancel_reservation(res_id)
    assert refund == expected_refund


def test_cancel_reservation_not_found(system):
    with pytest.raises(ReservationNotFoundError):
        system.cancel_reservation("NON-EXISTENT")


def test_get_room_occupancy(system):
    today = datetime.date.today()
    # No reservations yet
    assert system.get_room_occupancy(today) == []
    # Create two reservations on different rooms
    system.add_room(102, "double", 150.0)
    res1 = system.book_room(101, "A", today + timedelta(days=1), today + timedelta(days=4))
    res2 = system.book_room(102, "B", today + timedelta(days=2), today + timedelta(days=5))
    # Date where only room 101 is occupied
    occ_day1 = system.get_room_occupancy(today + timedelta(days=1))
    assert occ_day1 == [101]
    # Date where both rooms are occupied
    occ_day2 = system.get_room_occupancy(today + timedelta(days=2))
    assert occ_day2 == [101, 102]
    # Date after first reservation ends but second still active
    occ_day3 = system.get_room_occupancy(today + timedelta(days=4))
    assert occ_day3 == [102]
    # Date after all reservations
    occ_day4 = system.get_room_occupancy(today + timedelta(days=6))
    assert occ_day4 == []