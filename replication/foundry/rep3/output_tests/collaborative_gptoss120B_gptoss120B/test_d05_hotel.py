import pytest
import datetime
from data.input_code.d05_hotel import *

def _offset(days: int) -> datetime.date:
    """Return a date offset from today by the given number of days."""
    return datetime.date.today() + datetime.timedelta(days=days)

@pytest.fixture
def system():
    """Provide a fresh HotelReservationSystem instance for each test."""
    return HotelReservationSystem()

# ---------- add_room ----------
@pytest.mark.parametrize(
    "room_number, room_type, price, expect_exception",
    [
        (101, "single", 100.0, None),          # normal case
        (102, "double", 0.0, ValueError),     # non‑positive price
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
    system.add_room(101, "single", 100.0)
    res_id = system.book_room(
        101,
        "Alice",
        _offset(1),   # tomorrow
        _offset(4),   # three nights later
    )
    assert res_id == "RES-0001"
    assert res_id in system.reservations

@pytest.mark.parametrize(
    "room_number, user, check_in_offset, check_out_offset, expected_exc",
    [
        (999, "Bob", 1, 4, RoomNotFoundError),                     # room does not exist
        (101, "Carol", 0, 0, InvalidDateError),                   # same day (check_in == check_out)
        (101, "Dave", -1, 2, InvalidDateError),                   # check_in in the past
    ],
)
def test_book_room_errors(system, room_number, user, check_in_offset, check_out_offset, expected_exc):
    # Ensure room 101 exists for relevant cases
    if room_number == 101:
        system.add_room(101, "single", 100.0)

    with pytest.raises(expected_exc):
        system.book_room(
            room_number,
            user,
            _offset(check_in_offset),
            _offset(check_out_offset),
        )

def test_book_room_unavailable(system):
    system.add_room(101, "single", 100.0)
    # First reservation occupies days 1‑4 from today
    system.book_room(
        101,
        "Alice",
        _offset(1),
        _offset(4),
    )
    # Overlapping request should fail
    with pytest.raises(RoomUnavailableError):
        system.book_room(
            101,
            "Eve",
            _offset(2),
            _offset(5),
        )

# ---------- cancel_reservation ----------
@pytest.mark.parametrize(
    "setup_actions, reservation_id, expected_refund",
    [
        # Full refund (>7 days)
        (
            [
                ("add_room", {"room_number": 102, "room_type": "double", "price_per_night": 200.0}),
                ("book_room", {"room_number": 102, "user_name": "Frank",
                               "check_in_offset": 10, "check_out_offset": 12}),
            ],
            "RES-0001",
            400.0,
        ),
        # 50% refund (2‑7 days)
        (
            [
                ("add_room", {"room_number": 103, "room_type": "suite", "price_per_night": 150.0}),
                ("book_room", {"room_number": 103, "user_name": "Grace",
                               "check_in_offset": 5, "check_out_offset": 7}),
            ],
            "RES-0001",
            150.0,
        ),
        # No refund (<2 days)
        (
            [
                ("add_room", {"room_number": 104, "room_type": "single", "price_per_night": 100.0}),
                ("book_room", {"room_number": 104, "user_name": "Heidi",
                               "check_in_offset": 1, "check_out_offset": 2}),
            ],
            "RES-0001",
            0.0,
        ),
    ],
)
def test_cancel_reservation_refunds(system, setup_actions, reservation_id, expected_refund):
    # Execute setup steps
    for method, args in setup_actions:
        if method == "add_room":
            system.add_room(**args)
        elif method == "book_room":
            system.book_room(
                args["room_number"],
                args["user_name"],
                _offset(args["check_in_offset"]),
                _offset(args["check_out_offset"]),
            )
    refund = system.cancel_reservation(reservation_id)
    assert refund == expected_refund

def test_cancel_reservation_not_found(system):
    with pytest.raises(ReservationNotFoundError):
        system.cancel_reservation("RES-9999")

# ---------- get_room_occupancy ----------
@pytest.mark.parametrize(
    "setup_actions, query_offset, expected_rooms",
    [
        # Occupancy on check‑in date (inclusive)
        (
            [
                ("add_room", {"room_number": 101, "room_type": "single", "price_per_night": 100.0}),
                ("book_room", {"room_number": 101, "user_name": "Alice",
                               "check_in_offset": 1, "check_out_offset": 4}),
            ],
            1,
            [101],
        ),
        # Occupancy on check‑out date (exclusive)
        (
            [
                ("add_room", {"room_number": 101, "room_type": "single", "price_per_night": 100.0}),
                ("book_room", {"room_number": 101, "user_name": "Alice",
                               "check_in_offset": 1, "check_out_offset": 4}),
            ],
            4,
            [],
        ),
        # Multiple overlapping reservations, sorted result
        (
            [
                ("add_room", {"room_number": 101, "room_type": "single", "price_per_night": 100.0}),
                ("add_room", {"room_number": 105, "room_type": "double", "price_per_night": 150.0}),
                ("book_room", {"room_number": 101, "user_name": "Alice",
                               "check_in_offset": 1, "check_out_offset": 4}),
                ("book_room", {"room_number": 105, "user_name": "Ivan",
                               "check_in_offset": 3, "check_out_offset": 6}),
            ],
            3,
            [101, 105],
        ),
    ],
)
def test_get_room_occupancy(system, setup_actions, query_offset, expected_rooms):
    for method, args in setup_actions:
        if method == "add_room":
            system.add_room(**args)
        elif method == "book_room":
            system.book_room(
                args["room_number"],
                args["user_name"],
                _offset(args["check_in_offset"]),
                _offset(args["check_out_offset"]),
            )
    result = system.get_room_occupancy(_offset(query_offset))
    assert result == expected_rooms