import pytest
import datetime
from data.input_code.d05_hotel import *

@pytest.fixture
def system():
    """Provides a fresh HotelReservationSystem for each test."""
    return HotelReservationSystem()


@pytest.mark.parametrize(
    "room_number, room_type, price, expected_rooms",
    [
        (101, "Deluxe", 150.0, {101: {"type": "Deluxe", "price_per_night": 150.0}}),
    ],
)
def test_add_room_valid(system, room_number, room_type, price, expected_rooms):
    # Act
    system.add_room(room_number, room_type, price)

    # Assert
    assert system.rooms == expected_rooms


@pytest.mark.parametrize(
    "room_number, room_type, price, exc",
    [
        (102, "Standard", 0, ValueError),
        (103, "Suite", -50, ValueError),
    ],
)
def test_add_room_invalid_price(system, room_number, room_type, price, exc):
    with pytest.raises(exc):
        system.add_room(room_number, room_type, price)


def test_book_room_nonexistent_room(system):
    check_in = datetime.date(2030, 1, 15)
    check_out = datetime.date(2030, 1, 17)
    with pytest.raises(RoomNotFoundError):
        system.book_room(999, "Alice", check_in, check_out)


def test_cancel_reservation_not_found(system):
    with pytest.raises(ReservationNotFoundError):
        system.cancel_reservation("RES-9999")


def test_get_room_occupancy_no_reservations(system):
    date = datetime.date(2030, 1, 10)
    assert system.get_room_occupancy(date) == []

import pytest
import datetime
from data.input_code.d05_hotel import *

def test_book_room_success(system):
    # Arrange: add the room first
    system.add_room(201, "Deluxe", 120.0)
    check_in = datetime.date.fromisoformat("2030-01-10")
    check_out = datetime.date.fromisoformat("2030-01-13")
    # Act
    reservation_id = system.book_room(201, "Alice", check_in, check_out)
    # Assert
    assert reservation_id == "RES-0001"
    # Verify reservation details (price calculation)
    reservation = system.reservations[reservation_id]
    assert reservation.total_price == round(3 * 120.0, 2)  # 3 nights


@pytest.mark.parametrize(
    "room_number, user_name, check_in_str, check_out_str, exc",
    [
        (202, "Bob", "2030-02-10", "2030-02-10", InvalidDateError),   # same day
        (203, "Carol", "2000-01-01", "2000-01-02", InvalidDateError), # past dates
    ],
)
def test_book_room_invalid_dates(system, room_number, user_name, check_in_str, check_out_str, exc):
    # Arrange: ensure the room exists
    system.add_room(room_number, "Standard", 80.0)
    check_in = datetime.date.fromisoformat(check_in_str)
    check_out = datetime.date.fromisoformat(check_out_str)
    # Act & Assert
    with pytest.raises(exc):
        system.book_room(room_number, user_name, check_in, check_out)

import pytest
import datetime
from data.input_code.d05_hotel import *

def test_book_room_unavailable_overlap(system):
    # Arrange: add room and create an existing reservation
    system.add_room(301, "Standard", 100.0)
    system.book_room(
        301,
        "Bob",
        datetime.date(2030, 1, 14),
        datetime.date(2030, 1, 16)
    )
    # Act & Assert: overlapping booking should raise RoomUnavailableError
    with pytest.raises(RoomUnavailableError):
        system.book_room(
            301,
            "Alice",
            datetime.date(2030, 1, 15),
            datetime.date(2030, 1, 17)
        )

import pytest
import datetime
from data.input_code.d05_hotel import *

@pytest.mark.parametrize(
    "reservation_id, days_until_checkin, total_price, expected",
    [
        ("RES-TEST-FULL", 10, 200.0, 200.0),   # >7 days → full refund
        ("RES-TEST-HALF", 5, 200.0, 100.0),   # 2‑7 days → 50% refund
        ("RES-TEST-NONE", 1, 200.0, 0.0),     # <2 days → no refund
    ],
    ids=[
        "T_CANCEL_REFUND_FULL_INJECT",
        "T_CANCEL_REFUND_HALF_INJECT",
        "T_CANCEL_REFUND_NONE_INJECT",
    ],
)
def test_cancel_reservation_refund_injected(system, reservation_id, days_until_checkin, total_price, expected):
    today = datetime.date.today()
    check_in = today + datetime.timedelta(days=days_until_checkin)
    check_out = check_in + datetime.timedelta(days=2)

    # Inject a reservation directly into the system
    system.reservations[reservation_id] = Reservation(
        reservation_id=reservation_id,
        room_number=101,
        user_name="Tester",
        check_in=check_in,
        check_out=check_out,
        total_price=total_price,
    )

    # Act
    refund = system.cancel_reservation(reservation_id)

    # Assert
    assert refund == expected

import pytest
import datetime
from data.input_code.d05_hotel import *

def test_add_room_overwrite(system):
    # First addition
    system.add_room(101, "Deluxe", 150.0)
    # Overwrite with new price
    system.add_room(101, "Deluxe", 180.0)
    assert system.rooms[101]["price_per_night"] == 180.0


def test_adjacent_bookings_allowed(system):
    # Arrange: add the room
    system.add_room(301, "Standard", 100.0)

    # First reservation
    res1 = system.book_room(
        301,
        "Bob",
        datetime.date.fromisoformat("2030-01-14"),
        datetime.date.fromisoformat("2030-01-16"),
    )
    # Second reservation (adjacent)
    res2 = system.book_room(
        301,
        "Alice",
        datetime.date.fromisoformat("2030-01-16"),
        datetime.date.fromisoformat("2030-01-18"),
    )
    assert [res1, res2] == ["RES-0001", "RES-0002"]


def test_get_room_occupancy_single(system):
    # Seed a reservation directly
    system.reservations["RES-TEST-1"] = Reservation(
        reservation_id="RES-TEST-1",
        room_number=401,
        user_name="Tester",
        check_in=datetime.date.fromisoformat("2030-01-10"),
        check_out=datetime.date.fromisoformat("2030-01-12"),
        total_price=200.0,
    )
    # Query occupancy on a date within the reservation range
    occupancy = system.get_room_occupancy(datetime.date.fromisoformat("2030-01-11"))
    assert occupancy == [401]


def test_book_room_invalid_reverse_dates(system):
    # Ensure the room exists
    system.add_room(501, "Suite", 150.0)
    check_in = datetime.date.fromisoformat("2030-02-10")
    check_out = datetime.date.fromisoformat("2030-02-09")
    with pytest.raises(InvalidDateError):
        system.book_room(501, "X", check_in, check_out)