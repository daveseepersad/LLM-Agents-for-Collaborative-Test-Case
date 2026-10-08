import pytest
import datetime
from data.input_code.d05_hotel import *

@pytest.fixture
def system(monkeypatch):
    """Create a HotelReservationSystem with a fixed today date."""
    fixed_today = datetime.date(2024, 9, 10)

    # Patch datetime.date.today() to return the fixed date
    class FixedDate(datetime.date):
        @classmethod
        def today(cls):
            return fixed_today

    monkeypatch.setattr(datetime, "date", FixedDate)
    return HotelReservationSystem()


# ---------- add_room ----------
@pytest.mark.parametrize(
    "room_number, room_type, price, expect_exception",
    [
        (1, "single", 100.0, None),          # valid
        (1, "single", -100.0, ValueError),  # negative price
        (1, "single", 0.0, ValueError),     # zero price
    ],
)
def test_add_room(system, room_number, room_type, price, expect_exception):
    if expect_exception:
        with pytest.raises(expect_exception):
            system.add_room(room_number, room_type, price)
    else:
        system.add_room(room_number, room_type, price)
        assert room_number in system.rooms
        assert system.rooms[room_number]["price_per_night"] == price


# ---------- book_room ----------
def test_book_room_success(system):
    system.add_room(1, "single", 100.0)
    res_id = system.book_room(
        1,
        "John Doe",
        datetime.date(2024, 9, 20),
        datetime.date(2024, 9, 25),
    )
    assert res_id == "RES-0001"
    assert res_id in system.reservations


def test_book_room_not_found(system):
    with pytest.raises(RoomNotFoundError):
        system.book_room(
            2,
            "John Doe",
            datetime.date(2024, 9, 20),
            datetime.date(2024, 9, 25),
        )


def test_book_room_invalid_dates(system):
    system.add_room(1, "single", 100.0)
    with pytest.raises(InvalidDateError):
        system.book_room(
            1,
            "John Doe",
            datetime.date(2024, 9, 25),
            datetime.date(2024, 9, 20),
        )


def test_book_room_unavailable(system):
    system.add_room(1, "single", 100.0)
    # first reservation occupies the range
    system.book_room(
        1,
        "John Doe",
        datetime.date(2024, 9, 20),
        datetime.date(2024, 9, 25),
    )
    # overlapping reservation should fail
    with pytest.raises(RoomUnavailableError):
        system.book_room(
            1,
            "Jane Smith",
            datetime.date(2024, 9, 22),
            datetime.date(2024, 9, 27),
        )


def test_book_room_none_user_name(system):
    system.add_room(1, "single", 100.0)
    res_id = system.book_room(
        1,
        None,
        datetime.date(2024, 9, 20),
        datetime.date(2024, 9, 25),
    )
    assert res_id == "RES-0001"
    assert system.reservations[res_id].user_name is None


def test_book_room_same_day_dates_invalid(system):
    """Check that booking with check_in == check_out raises InvalidDateError."""
    system.add_room(1, "single", 100.0)
    with pytest.raises(InvalidDateError):
        system.book_room(
            1,
            "John Doe",
            datetime.date(2024, 9, 20),
            datetime.date(2024, 9, 20),
        )


# ---------- cancel_reservation ----------
def test_cancel_reservation_full_refund(system):
    """Reservation >7 days from today → 100% refund."""
    system.add_room(1, "single", 100.0)
    res_id = system.book_room(
        1,
        "John Doe",
        datetime.date(2024, 9, 20),  # 10 days ahead of fixed today (2024‑09‑10)
        datetime.date(2024, 9, 25),
    )
    refund = system.cancel_reservation(res_id)
    assert refund == 500.0  # 5 nights × $100


def test_cancel_reservation_half_refund(system):
    """Reservation 3 days from today → 50% refund."""
    system.add_room(1, "single", 100.0)
    res_id = system.book_room(
        1,
        "John Doe",
        datetime.date(2024, 9, 13),  # 3 days ahead
        datetime.date(2024, 9, 15),
    )
    refund = system.cancel_reservation(res_id)
    assert refund == 100.0  # 2 nights × $100 × 0.5


def test_cancel_reservation_no_refund(system):
    """Reservation 1 day from today → 0% refund."""
    system.add_room(1, "single", 100.0)
    res_id = system.book_room(
        1,
        "John Doe",
        datetime.date(2024, 9, 11),  # 1 day ahead
        datetime.date(2024, 9, 12),
    )
    refund = system.cancel_reservation(res_id)
    assert refund == 0.0


def test_cancel_reservation_not_found(system):
    with pytest.raises(ReservationNotFoundError):
        system.cancel_reservation("RES-9999")


# ---------- get_room_occupancy ----------
def test_get_room_occupancy(system):
    system.add_room(1, "single", 100.0)
    system.book_room(
        1,
        "John Doe",
        datetime.date(2024, 9, 20),
        datetime.date(2024, 9, 25),
    )
    occupied = system.get_room_occupancy(datetime.date(2024, 9, 22))
    assert occupied == [1]

import pytest
import datetime
from data.input_code.d05_hotel import *

def test_book_room_past_date(system):
    """Booking a room with a past check-in date should raise InvalidDateError."""
    system.add_room(1, "single", 100.0)
    with pytest.raises(InvalidDateError):
        system.book_room(
            1,
            "John Doe",
            datetime.date(2024, 9, 5),   # past date relative to fixed today (2024-09-10)
            datetime.date(2024, 9, 10),
        )

def test_cancel_reservation_zero_refund_boundary(system):
    """Cancel a reservation that is 1 day away from check‑in should yield a 0.0 refund."""
    system.add_room(1, "single", 100.0)
    # Reservation check‑in is tomorrow (2024‑09‑11), i.e., 1 day from fixed today
    res_id = system.book_room(
        1,
        "John Doe",
        datetime.date(2024, 9, 11),
        datetime.date(2024, 9, 13),
    )
    refund = system.cancel_reservation(res_id)
    assert refund == 0.0

def test_get_room_occupancy_no_occupancy_on_date(system):
    """When no rooms are booked, occupancy for any date should be an empty list."""
    occupied = system.get_room_occupancy(datetime.date(2024, 9, 20))
    assert occupied == []

@pytest.mark.parametrize(
    "check_in, check_out",
    [
        (datetime.date(2024, 9, 20), datetime.date(2024, 9, 20)),  # same day
    ],
)
def test_book_room_same_checkin_checkout_date(system, check_in, check_out):
    """Booking a room where check‑in equals check‑out should raise InvalidDateError."""
    system.add_room(1, "single", 100.0)
    with pytest.raises(InvalidDateError):
        system.book_room(1, "John Doe", check_in, check_out)