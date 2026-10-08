import pytest
import datetime
from data.input_code.d05_hotel import *

# Fixed "today" for deterministic tests
FIXED_TODAY = datetime.date(2026, 10, 7)


@pytest.fixture(autouse=True)
def freeze_today(monkeypatch):
    """Patch datetime.date.today() to return a constant date."""
    class FixedDate(datetime.date):
        @classmethod
        def today(cls):
            return FIXED_TODAY

    monkeypatch.setattr(datetime, "date", FixedDate)


@pytest.fixture
def system():
    """Provide a fresh HotelReservationSystem for each test."""
    return HotelReservationSystem()


# ----------------------------------------------------------------------
# add_room tests
# ----------------------------------------------------------------------
@pytest.mark.parametrize(
    "room_number, room_type, price, expect_exception",
    [
        (101, "Standard", 150.0, None),          # TC1_ADD_ROOM_VALID
        (102, "Deluxe", 0, ValueError),          # TC2_ADD_ROOM_INVALID_PRICE_ZERO
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


# ----------------------------------------------------------------------
# book_room error handling
# ----------------------------------------------------------------------
@pytest.mark.parametrize(
    "setup_rooms, room_number, check_in, check_out, expected_exc",
    [
        # TC3_BOOK_ROOM_NOT_FOUND
        ([], 999, datetime.date(2026, 10, 9), datetime.date(2026, 10, 12), RoomNotFoundError),
        # TC4_BOOK_ROOM_INVALID_DATES (same day)
        ([(201, "Standard", 120.0)], 201,
         datetime.date(2026, 10, 12), datetime.date(2026, 10, 12), InvalidDateError),
        # TC5_BOOK_ROOM_PAST_CHECKIN (check-in before today)
        ([(202, "Standard", 120.0)], 202,
         datetime.date(2026, 10, 6), datetime.date(2026, 10, 8), InvalidDateError),
        # TC6_BOOK_ROOM_UNAVAILABLE (overlap with existing reservation)
        ([(301, "Standard", 200.0)], 301,
         datetime.date(2026, 10, 9), datetime.date(2026, 10, 12), RoomUnavailableError),
    ],
)
def test_book_room_errors(system, setup_rooms, room_number, check_in, check_out, expected_exc):
    # Prepare rooms
    for rn, rt, price in setup_rooms:
        system.add_room(rn, rt, price)

    # For TC6 we need a pre‑existing reservation that creates the conflict
    if expected_exc is RoomUnavailableError:
        # book the same room for overlapping dates first
        system.book_room(
            room_number,
            "ExistingUser",
            datetime.date(2026, 10, 8),
            datetime.date(2026, 10, 11),
        )

    with pytest.raises(expected_exc):
        system.book_room(room_number, "Tester", check_in, check_out)


# ----------------------------------------------------------------------
# successful booking (used for later cancellation & occupancy tests)
# ----------------------------------------------------------------------
def test_successful_booking_and_reservation_ids(system):
    system.add_room(101, "Standard", 150.0)
    res_id = system.book_room(
        101,
        "Alice",
        datetime.date(2026, 10, 9),
        datetime.date(2026, 10, 12),
    )
    assert res_id.startswith("RES-")
    assert res_id in system.reservations
    reservation = system.reservations[res_id]
    assert reservation.total_price == 3 * 150.0  # 3 nights


# ----------------------------------------------------------------------
# cancel_reservation tests (refund policy)
# ----------------------------------------------------------------------
@pytest.fixture
def populated_system(system):
    """Create a system with three reservations covering the three refund scenarios."""
    system.add_room(401, "Standard", 100.0)

    # >7 days before check‑in (full refund)
    res_full = system.book_room(
        401,
        "UserFull",
        FIXED_TODAY + datetime.timedelta(days=10),
        FIXED_TODAY + datetime.timedelta(days=13),
    )
    # 3 days before check‑in (50% refund)
    res_half = system.book_room(
        401,
        "UserHalf",
        FIXED_TODAY + datetime.timedelta(days=4),
        FIXED_TODAY + datetime.timedelta(days=6),
    )
    # 1 day before check‑in (no refund)
    res_none = system.book_room(
        401,
        "UserNone",
        FIXED_TODAY + datetime.timedelta(days=1),
        FIXED_TODAY + datetime.timedelta(days=3),
    )
    return system, {
        "full": (res_full, system.reservations[res_full].total_price),
        "half": (res_half, round(system.reservations[res_half].total_price * 0.5, 2)),
        "none": (res_none, 0.0),
    }


@pytest.mark.parametrize(
    "scenario, expected_refund",
    [
        ("full", None),   # placeholder, will be replaced inside test
        ("half", None),
        ("none", None),
    ],
)
def test_cancel_reservation_refund(populated_system, scenario, expected_refund):
    system, refs = populated_system
    res_id, expected_amount = refs[scenario]
    refund = system.cancel_reservation(res_id)
    assert refund == expected_amount


def test_cancel_reservation_not_found(system):
    with pytest.raises(ReservationNotFoundError):
        system.cancel_reservation("RES-9999")  # TC7_CANCEL_RESERVATION_NOT_FOUND


# ----------------------------------------------------------------------
# get_room_occupancy tests
# ----------------------------------------------------------------------
@pytest.fixture
def occupancy_system(system):
    """System with a known reservation for occupancy checks."""
    system.add_room(101, "Standard", 150.0)
    system.add_room(102, "Deluxe", 200.0)

    # Reservation occupying room 101 on 2026‑10‑09
    system.book_room(
        101,
        "Bob",
        datetime.date(2026, 10, 9),
        datetime.date(2026, 10, 12),
    )
    return system


@pytest.mark.parametrize(
    "query_date, expected_rooms",
    [
        (datetime.date(2026, 10, 9), [101]),  # TC11_GET_ROOM_OCCUPANCY_SINGLE
        (datetime.date(2026, 10, 7), []),    # TC12_GET_ROOM_OCCUPANCY_EMPTY
    ],
)
def test_get_room_occupancy(occupancy_system, query_date, expected_rooms):
    assert occupancy_system.get_room_occupancy(query_date) == expected_rooms