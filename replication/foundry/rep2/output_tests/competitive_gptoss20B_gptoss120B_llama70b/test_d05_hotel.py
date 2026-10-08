import pytest
import datetime
from data.input_code.d05_hotel import *

@pytest.fixture
def system():
    """Provides a fresh HotelReservationSystem for each test."""
    return HotelReservationSystem()

@pytest.mark.parametrize(
    "room_number, room_type, price, expect_exception",
    [
        (101, "Deluxe", 150.0, None),          # valid
        (102, "Standard", 0.0, ValueError),   # invalid price
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


def test_book_room_not_found(system):
    with pytest.raises(RoomNotFoundError):
        system.book_room(
            room_number=999,
            user_name="Alice",
            check_in=datetime.date(2100, 1, 1),
            check_out=datetime.date(2100, 1, 2),
        )


def test_book_room_invalid_dates(system):
    # need a valid room first
    system.add_room(101, "Deluxe", 150.0)
    # check_in after check_out triggers InvalidDateError
    with pytest.raises(InvalidDateError):
        system.book_room(
            room_number=101,
            user_name="Alice",
            check_in=datetime.date(2100, 1, 2),
            check_out=datetime.date(2100, 1, 1),
        )


def test_book_room_past_date(system):
    system.add_room(101, "Deluxe", 150.0)
    with pytest.raises(InvalidDateError):
        system.book_room(
            room_number=101,
            user_name="Bob",
            check_in=datetime.date(1999, 12, 31),
            check_out=datetime.date(2000, 1, 1),
        )


def test_book_room_success(system):
    system.add_room(101, "Deluxe", 150.0)
    res_id = system.book_room(
        room_number=101,
        user_name="Alice",
        check_in=datetime.date(2100, 1, 1),
        check_out=datetime.date(2100, 1, 2),
    )
    assert res_id == "RES-0001"
    # verify reservation stored correctly
    reservation = system.reservations[res_id]
    assert reservation.total_price == 150.0
    assert reservation.room_number == 101


def test_book_room_overlap(system):
    system.add_room(101, "Deluxe", 150.0)
    # first reservation
    system.book_room(
        room_number=101,
        user_name="Alice",
        check_in=datetime.date(2100, 1, 1),
        check_out=datetime.date(2100, 1, 2),
    )
    # overlapping reservation attempt
    with pytest.raises(RoomUnavailableError):
        system.book_room(
            room_number=101,
            user_name="Charlie",
            check_in=datetime.date(2100, 1, 1),
            check_out=datetime.date(2100, 1, 3),
        )


def test_cancel_reservation_not_found(system):
    with pytest.raises(ReservationNotFoundError):
        system.cancel_reservation("RES-9999")


def test_get_room_occupancy(system):
    system.add_room(101, "Deluxe", 150.0)
    system.book_room(
        room_number=101,
        user_name="Alice",
        check_in=datetime.date(2100, 1, 1),
        check_out=datetime.date(2100, 1, 2),
    )
    occupied = system.get_room_occupancy(datetime.date(2100, 1, 1))
    assert occupied == [101]


def test_cancel_reservation_success(system):
    system.add_room(101, "Deluxe", 150.0)
    res_id = system.book_room(
        room_number=101,
        user_name="Alice",
        check_in=datetime.date(2100, 1, 1),
        check_out=datetime.date(2100, 1, 2),
    )
    refund = system.cancel_reservation(res_id)
    assert refund == 150.0

def test_book_room_same_day_invalid(system):
    """Booking with check-in and check-out on the same day should raise InvalidDateError."""
    system.add_room(101, "Deluxe", 150.0)
    with pytest.raises(InvalidDateError):
        system.book_room(
            room_number=101,
            user_name="Alice",
            check_in=datetime.date(2100, 1, 1),
            check_out=datetime.date(2100, 1, 1),
        )


def test_get_room_occupancy_empty(system):
    """Getting occupancy for a date with no reservations should return an empty list."""
    occupied = system.get_room_occupancy(datetime.date(2100, 1, 1))
    assert occupied == []


def test_add_room_negative_price(system):
    """Adding a room with a non‑positive price should raise ValueError."""
    with pytest.raises(ValueError):
        system.add_room(room_number=202, room_type="Deluxe", price_per_night=-5)


def test_cancel_reservation_not_found_duplicate(system):
    """Cancelling a non‑existent reservation should raise ReservationNotFoundError."""
    with pytest.raises(ReservationNotFoundError):
        system.cancel_reservation("RES-9999")

import datetime
import pytest

def test_add_room_overwrite(system):
    # First addition
    system.add_room(room_number=101, room_type="Deluxe", price_per_night=150.0)
    # Overwrite with new data
    system.add_room(room_number=101, room_type="Suite", price_per_night=200.0)
    # Expected final state
    expected = {"room_number": 101, "type": "Suite", "price_per_night": 200.0}
    assert 101 in system.rooms
    assert system.rooms[101]["type"] == expected["type"]
    assert system.rooms[101]["price_per_night"] == expected["price_per_night"]


def test_book_room_boundary_no_overlap(system):
    # Prepare room
    system.add_room(room_number=101, room_type="Deluxe", price_per_night=150.0)
    # First reservation
    res1 = system.book_room(
        room_number=101,
        user_name="Alice",
        check_in=datetime.date.fromisoformat("2100-01-01"),
        check_out=datetime.date.fromisoformat("2100-01-02"),
    )
    # Second reservation that starts exactly when the first ends
    res2 = system.book_room(
        room_number=101,
        user_name="Bob",
        check_in=datetime.date.fromisoformat("2100-01-02"),
        check_out=datetime.date.fromisoformat("2100-01-03"),
    )
    assert [res1, res2] == ["RES-0001", "RES-0002"]

import datetime
import pytest

def test_get_room_occupancy_multiple(system):
    # Setup rooms
    system.add_room(101, "Deluxe", 150.0)
    system.add_room(102, "Standard", 180.0)
    # Create reservations that overlap on the same date
    system.book_room(
        room_number=101,
        user_name="Alice",
        check_in=datetime.date(2100, 1, 1),
        check_out=datetime.date(2100, 1, 2),
    )
    system.book_room(
        room_number=102,
        user_name="Bob",
        check_in=datetime.date(2100, 1, 1),
        check_out=datetime.date(2100, 1, 2),
    )
    # Verify both rooms are reported as occupied on the target date
    occupied = system.get_room_occupancy(datetime.date(2100, 1, 1))
    assert occupied == [101, 102]


@pytest.mark.parametrize(
    "check_in_offset, check_out_offset, expected_refund",
    [
        (7, 8, 75.0),   # 7 days until check‑in → 50% refund
        (1, 2, 0.0),    # 1 day until check‑in → 0% refund
    ],
)
def test_cancel_reservation_refund_boundary(system, check_in_offset, check_out_offset, expected_refund):
    # Add a room
    system.add_room(101, "Deluxe", 150.0)
    today = datetime.date.today()
    check_in = today + datetime.timedelta(days=check_in_offset)
    check_out = today + datetime.timedelta(days=check_out_offset)

    # Book the reservation
    reservation_id = system.book_room(
        room_number=101,
        user_name="TestUser",
        check_in=check_in,
        check_out=check_out,
    )

    # Cancel and verify refund amount
    refund = system.cancel_reservation(reservation_id)
    assert refund == expected_refund