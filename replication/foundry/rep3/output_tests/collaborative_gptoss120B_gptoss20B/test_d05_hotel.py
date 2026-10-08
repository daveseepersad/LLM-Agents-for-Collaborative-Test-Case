import pytest
import datetime
from data.input_code.d05_hotel import *

# Fixture to fix the current date for all tests
@pytest.fixture(autouse=True)
def fixed_today(monkeypatch):
    """Patch datetime.date.today() to return a constant date for deterministic tests."""
    class FixedDate(datetime.date):
        @classmethod
        def today(cls):
            return datetime.date(2026, 10, 7)

    monkeypatch.setattr(datetime, "date", FixedDate)


@pytest.fixture
def empty_system():
    """Provides a fresh HotelReservationSystem with no rooms or reservations."""
    return HotelReservationSystem()


@pytest.fixture
def system_with_one_reservation(empty_system):
    """System with a single reservation for room 101 from 2026-10-08 to 2026-10-10."""
    empty_system.add_room(101, "Single", 100.0)
    empty_system.book_room(
        101,
        "UserOne",
        datetime.date(2026, 10, 8),
        datetime.date(2026, 10, 10)
    )
    return empty_system


@pytest.fixture
def system_with_two_reservations(empty_system):
    """
    System with two reservations for room 101:
    - RES-0001: 2026-12-01 to 2026-12-10
    - RES-0002: 2026-12-20 to 2026-12-30 (used for overlap tests)
    """
    empty_system.add_room(101, "Single", 100.0)
    empty_system.book_room(
        101,
        "UserA",
        datetime.date(2026, 12, 1),
        datetime.date(2026, 12, 10)
    )
    empty_system.book_room(
        101,
        "UserB",
        datetime.date(2026, 12, 20),
        datetime.date(2026, 12, 30)
    )
    return empty_system


def _expected_refund(reservation: Reservation) -> float:
    """Helper to compute expected refund using the same policy as the system."""
    days_until_checkin = (reservation.check_in - datetime.date.today()).days
    if days_until_checkin > 7:
        return reservation.total_price
    elif 2 <= days_until_checkin <= 7:
        return round(reservation.total_price * 0.5, 2)
    else:
        return 0.0


def test_add_room_ok(empty_system):
    empty_system.add_room(101, "Single", 100.0)
    assert 101 in empty_system.rooms
    assert empty_system.rooms[101]["type"] == "Single"
    assert empty_system.rooms[101]["price_per_night"] == 100.0


def test_add_room_invalid_price(empty_system):
    with pytest.raises(ValueError):
        empty_system.add_room(102, "Double", 0)


def test_book_room_success(empty_system):
    empty_system.add_room(101, "Single", 100.0)
    expected_id = f"RES-{empty_system._reservation_counter + 1:04d}"
    res_id = empty_system.book_room(
        101,
        "Alice",
        datetime.date(2026, 10, 8),
        datetime.date(2026, 10, 10)
    )
    assert res_id == expected_id


def test_book_room_room_not_found(empty_system):
    with pytest.raises(RoomNotFoundError):
        empty_system.book_room(
            999,
            "Bob",
            datetime.date(2026, 10, 12),
            datetime.date(2026, 10, 14)
        )


def test_book_room_invalid_dates(empty_system):
    empty_system.add_room(101, "Single", 100.0)
    with pytest.raises(InvalidDateError):
        empty_system.book_room(
            101,
            "Carol",
            datetime.date(2026, 10, 12),
            datetime.date(2026, 10, 12)
        )


def test_book_room_past_date(empty_system):
    empty_system.add_room(101, "Single", 100.0)
    with pytest.raises(InvalidDateError):
        empty_system.book_room(
            101,
            "Dave",
            datetime.date(2020, 1, 1),
            datetime.date(2026, 1, 2)
        )


def test_book_room_unavailable(system_with_two_reservations):
    # Overlap with RES-0002 (2026-12-20 to 2026-12-30)
    with pytest.raises(RoomUnavailableError):
        system_with_two_reservations.book_room(
            101,
            "Eve",
            datetime.date(2026, 12, 25),
            datetime.date(2026, 12, 28)
        )


def test_cancel_reservation_refund_full(system_with_two_reservations):
    # Compute expected refund from the reservation before cancelling
    reservation = system_with_two_reservations.reservations["RES-0002"]
    expected_refund = _expected_refund(reservation)
    refund = system_with_two_reservations.cancel_reservation("RES-0002")
    assert refund == expected_refund


def test_cancel_reservation_not_found(empty_system):
    with pytest.raises(ReservationNotFoundError):
        empty_system.cancel_reservation("RES-9999")


def test_get_room_occupancy_some_date(system_with_one_reservation):
    occupied = system_with_one_reservation.get_room_occupancy(datetime.date(2026, 10, 9))
    assert occupied == [101]


def test_get_room_occupancy_empty(system_with_one_reservation):
    occupied = system_with_one_reservation.get_room_occupancy(datetime.date(2026, 12, 1))
    assert occupied == []


def test_book_room_boundary_no_overlap(system_with_one_reservation):
    # Existing reservation: 2026-10-08 to 2026-10-10
    expected_id = f"RES-{system_with_one_reservation._reservation_counter + 1:04d}"
    res_id = system_with_one_reservation.book_room(
        101,
        "BoundaryTester",
        datetime.date(2026, 10, 10),
        datetime.date(2026, 10, 12)
    )
    assert res_id == expected_id


def test_cancel_reservation_mid_refund(empty_system):
    # Setup room
    empty_system.add_room(201, "Standard", 100.0)
    # Book reservation (RES-0001)
    empty_system.book_room(
        201,
        "TesterMid",
        datetime.date(2026, 10, 10),
        datetime.date(2026, 10, 12)
    )
    # Retrieve the reservation object to compute expected refund
    reservation = empty_system.reservations["RES-0001"]
    expected_refund = _expected_refund(reservation)
    refund = empty_system.cancel_reservation("RES-0001")
    assert refund == expected_refund


def test_cancel_reservation_zero_refund(empty_system):
    # Setup room
    empty_system.add_room(202, "Standard", 150.0)
    # Book reservation (RES-0001)
    empty_system.book_room(
        202,
        "TesterZero",
        datetime.date(2026, 10, 8),
        datetime.date(2026, 10, 10)
    )
    # Retrieve the reservation object to compute expected refund
    reservation = empty_system.reservations["RES-0001"]
    expected_refund = _expected_refund(reservation)
    refund = empty_system.cancel_reservation("RES-0001")
    assert refund == expected_refund


def test_get_room_occupancy_multiple_rooms_sorted(empty_system):
    # Setup rooms
    empty_system.add_room(101, "Single", 100.0)
    empty_system.add_room(102, "Single", 100.0)
    # Create reservations
    empty_system.book_room(
        101,
        "UserA",
        datetime.date(2026, 10, 8),
        datetime.date(2026, 10, 10)
    )
    empty_system.book_room(
        102,
        "UserB",
        datetime.date(2026, 10, 9),
        datetime.date(2026, 10, 11)
    )
    # Check occupancy on 2026-10-09
    occupied = empty_system.get_room_occupancy(datetime.date(2026, 10, 9))
    assert occupied == [101, 102]