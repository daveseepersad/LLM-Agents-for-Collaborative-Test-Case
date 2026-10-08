import pytest
import datetime
from data.input_code.d05_hotel import *

# ----------------------------------------------------------------------
# Fixtures
# ----------------------------------------------------------------------
@pytest.fixture(autouse=True)
def fixed_today(monkeypatch):
    """Patch datetime.date.today() to a fixed point for deterministic tests."""
    class FixedDate(datetime.date):
        @classmethod
        def today(cls):
            return datetime.date(2024, 1, 1)

    monkeypatch.setattr(datetime, "date", FixedDate)


@pytest.fixture
def system():
    """Provide a fresh HotelReservationSystem instance for each test."""
    return HotelReservationSystem()


# ----------------------------------------------------------------------
# add_room tests
# ----------------------------------------------------------------------
@pytest.mark.parametrize(
    "room_number, room_type, price, expect_exception",
    [
        (1, "single", 100.0, None),          # T1_OK_add_room
        (1, "single", -100.0, ValueError),  # T2_ERR_add_room
    ],
)
def test_add_room(system, room_number, room_type, price, expect_exception):
    if expect_exception:
        with pytest.raises(expect_exception):
            system.add_room(room_number, room_type, price)
    else:
        system.add_room(room_number, room_type, price)
        assert room_number in system.rooms
        assert system.rooms[room_number]["type"] == room_type
        assert system.rooms[room_number]["price_per_night"] == price


# ----------------------------------------------------------------------
# book_room tests
# ----------------------------------------------------------------------
def test_book_room_success(system):
    # T3_OK_book_room
    system.add_room(1, "single", 100.0)
    check_in = datetime.date(2024, 9, 20)
    check_out = datetime.date(2024, 9, 25)
    res_id = system.book_room(1, "John Doe", check_in, check_out)
    assert res_id == "RES-0001"


def test_book_room_room_not_found(system):
    # T4_ERR_book_room_room_not_found
    check_in = datetime.date(2024, 9, 20)
    check_out = datetime.date(2024, 9, 25)
    with pytest.raises(RoomNotFoundError):
        system.book_room(2, "John Doe", check_in, check_out)


def test_book_room_invalid_dates(system):
    # T5_ERR_book_room_invalid_dates
    system.add_room(1, "single", 100.0)
    check_in = datetime.date(2024, 9, 25)
    check_out = datetime.date(2024, 9, 20)
    with pytest.raises(InvalidDateError):
        system.book_room(1, "John Doe", check_in, check_out)


def test_book_room_past_dates(system):
    # T6_ERR_book_room_past_dates
    system.add_room(1, "single", 100.0)
    check_in = datetime.date(2022, 9, 20)
    check_out = datetime.date(2022, 9, 25)
    with pytest.raises(InvalidDateError):
        system.book_room(1, "John Doe", check_in, check_out)


def test_book_room_unavailable(system):
    # T7_ERR_book_room_room_unavailable
    system.add_room(1, "single", 100.0)
    check_in = datetime.date(2024, 9, 20)
    check_out = datetime.date(2024, 9, 25)
    # First reservation succeeds
    first_res = system.book_room(1, "John Doe", check_in, check_out)
    assert first_res == "RES-0001"
    # Second overlapping reservation should fail
    with pytest.raises(RoomUnavailableError):
        system.book_room(1, "Jane Smith", check_in, check_out)


# ----------------------------------------------------------------------
# cancel_reservation tests
# ----------------------------------------------------------------------
def test_cancel_reservation_success(system):
    # T8_OK_cancel_reservation
    system.add_room(1, "single", 100.0)
    check_in = datetime.date(2024, 9, 20)
    check_out = datetime.date(2024, 9, 25)
    res_id = system.book_room(1, "John Doe", check_in, check_out)
    refund = system.cancel_reservation(res_id)
    # 5 nights * 100 = 500.0, and >7 days before check‑in => full refund
    assert refund == 500.0


def test_cancel_reservation_not_found(system):
    # T9_ERR_cancel_reservation_not_found
    with pytest.raises(ReservationNotFoundError):
        system.cancel_reservation("RES-0002")


# ----------------------------------------------------------------------
# get_room_occupancy tests
# ----------------------------------------------------------------------
def test_get_room_occupancy(system):
    # T10_OK_get_room_occupancy
    system.add_room(1, "single", 100.0)
    check_in = datetime.date(2024, 9, 20)
    check_out = datetime.date(2024, 9, 25)
    system.book_room(1, "John Doe", check_in, check_out)
    occupancy = system.get_room_occupancy(datetime.date(2024, 9, 22))
    assert occupancy == [1]


# ----------------------------------------------------------------------
# _is_room_available tests
# ----------------------------------------------------------------------
def test_is_room_available_true(system):
    # T11_OK_is_room_available
    system.add_room(1, "single", 100.0)
    check_in = datetime.date(2024, 9, 20)
    check_out = datetime.date(2024, 9, 25)
    available = system._is_room_available(1, check_in, check_out)
    assert available is True

# ----------------------------------------------------------------------
# Edge case tests
# ----------------------------------------------------------------------


def test_book_room_edge_7_days_before(system):
    # T_MISSING_EDGE_book_room: booking exactly 7 days after today
    system.add_room(1, "single", 100.0)
    check_in = datetime.date(2024, 1, 8)
    check_out = datetime.date(2024, 1, 15)
    res_id = system.book_room(1, "John Doe", check_in, check_out)
    assert res_id == "RES-0001"


def test_cancel_reservation_edge_less_than_2_days(system, monkeypatch):
    # T_MISSING_EDGE_cancel_reservation: cancelling less than 2 days before check‑in
    # Adjust today to 2024‑01‑02 so that check‑in (2024‑01‑03) is 1 day away
    class FixedDate(datetime.date):
        @classmethod
        def today(cls):
            return datetime.date(2024, 1, 2)

    monkeypatch.setattr(datetime, "date", FixedDate)

    system.add_room(1, "single", 100.0)
    # Booking from 2024‑01‑03 to 2024‑01‑10
    system.book_room(1, "John Doe", datetime.date(2024, 1, 3), datetime.date(2024, 1, 10))
    refund = system.cancel_reservation("RES-0001")
    assert refund == 0.0


def test_get_room_occupancy_current_date(system):
    # T_MISSING_EDGE_get_room_occupancy: occupancy on the current (patched) date
    occupancy = system.get_room_occupancy(datetime.date(2024, 1, 1))
    assert occupancy == []


def test_book_room_edge_overlap_raises(system):
    # T_MISSING_EDGE_book_room_overlap: attempting to book overlapping dates should fail
    system.add_room(1, "single", 100.0)
    # Existing reservation: 2024‑01‑05 to 2024‑01‑12
    system.book_room(1, "Jane Doe", datetime.date(2024, 1, 5), datetime.date(2024, 1, 12))
    # Overlapping reservation attempt
    with pytest.raises(RoomUnavailableError):
        system.book_room(1, "John Doe", datetime.date(2024, 1, 10), datetime.date(2024, 1, 15))


def test_cancel_reservation_partial_refund(system):
    # T_MISSING_EDGE_cancel_reservation_partial_refund: 2‑7 days before check‑in => 50% refund
    system.add_room(1, "single", 100.0)
    # Booking from 2024‑01‑05 to 2024‑01‑10 (5 nights, total 500)
    system.book_room(1, "John Doe", datetime.date(2024, 1, 5), datetime.date(2024, 1, 10))
    refund = system.cancel_reservation("RES-0001")
    assert refund == 250.0


def test_get_room_occupancy_multiple_rooms(system):
    # T_MISSING_EDGE_get_room_occupancy_multiple_rooms: occupancy on a date with two rooms booked
    system.add_room(1, "single", 100.0)
    system.add_room(2, "double", 200.0)
    # Room 1: 2024‑01‑05 to 2024‑01‑15
    system.book_room(1, "John Doe", datetime.date(2024, 1, 5), datetime.date(2024, 1, 15))
    # Room 2: 2024‑01‑08 to 2024‑01‑12
    system.book_room(2, "Jane Doe", datetime.date(2024, 1, 8), datetime.date(2024, 1, 12))
    occupancy = system.get_room_occupancy(datetime.date(2024, 1, 10))
    assert occupancy == [1, 2]