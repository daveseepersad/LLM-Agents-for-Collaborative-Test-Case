import pytest
from data.input_code.d05_hotel import *

@pytest.fixture
def system():
    return HotelReservationSystem()

def _future_date(days):
    return datetime.date.today() + datetime.timedelta(days=days)

def _past_date(days):
    return datetime.date.today() - datetime.timedelta(days=days)

@pytest.mark.parametrize(
    "room_number, room_type, price, expect_exception",
    [
        (1, "single", 100.0, None),          # valid
        (2, "double", 0.0, ValueError),     # invalid price
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

def test_book_room_success(system):
    system.add_room(1, "single", 100.0)
    check_in = _future_date(10)
    check_out = _future_date(15)
    res_id = system.book_room(1, "John Doe", check_in, check_out)
    assert res_id == "RES-0001"
    assert res_id in system.reservations

def test_book_room_errors(system):
    # room not found
    with pytest.raises(RoomNotFoundError):
        system.book_room(99, "John Doe", _future_date(1), _future_date(2))

    system.add_room(1, "single", 100.0)

    # invalid date order
    with pytest.raises(InvalidDateError):
        system.book_room(1, "John Doe", _future_date(5), _future_date(3))

    # past dates
    with pytest.raises(InvalidDateError):
        system.book_room(1, "John Doe", _past_date(5), _past_date(3))

    # room unavailable (double booking)
    check_in = _future_date(20)
    check_out = _future_date(25)
    system.book_room(1, "John Doe", check_in, check_out)  # first reservation
    with pytest.raises(RoomUnavailableError):
        system.book_room(1, "Jane Roe", check_in, check_out)

def test_cancel_reservation_success(system):
    system.add_room(1, "single", 100.0)
    check_in = _future_date(15)   # >7 days from today
    check_out = _future_date(20)
    res_id = system.book_room(1, "John Doe", check_in, check_out)
    refund = system.cancel_reservation(res_id)
    assert refund == 500.0  # 5 nights * 100.0

def test_cancel_reservation_not_found(system):
    with pytest.raises(ReservationNotFoundError):
        system.cancel_reservation("RES-9999")

def test_get_room_occupancy(system):
    system.add_room(1, "single", 100.0)
    check_in = _future_date(30)
    check_out = _future_date(35)
    system.book_room(1, "John Doe", check_in, check_out)
    occupancy_date = _future_date(32)
    occupied = system.get_room_occupancy(occupancy_date)
    assert occupied == [1]

def test_is_room_available_true(system):
    system.add_room(1, "single", 100.0)
    check_in = _future_date(40)
    check_out = _future_date(45)
    assert system._is_room_available(1, check_in, check_out) is True

import datetime
import pytest

@pytest.mark.parametrize(
    "days_until_checkin, nights, price_per_night, expected_refund",
    [
        (5, 5, 100.0, 250.0),   # 5 days ahead → 50% refund
        (1, 1, 100.0, 0.0),     # 1 day ahead → 0% refund
    ],
)
def test_cancel_reservation_refund(system, days_until_checkin, nights, price_per_night, expected_refund):
    # Setup room
    system.add_room(1, "single", price_per_night)
    # Create reservation with specified lead time and length
    check_in = datetime.date.today() + datetime.timedelta(days=days_until_checkin)
    check_out = check_in + datetime.timedelta(days=nights)
    res_id = system.book_room(1, "John Doe", check_in, check_out)
    # Cancel and verify refund
    refund = system.cancel_reservation(res_id)
    assert refund == expected_refund


def test_get_room_occupancy_multiple(system):
    # Add rooms
    system.add_room(1, "single", 100.0)
    system.add_room(2, "double", 150.0)

    # Manually insert overlapping reservations for a past date (bypassing validation)
    occ_date = datetime.date(2024, 9, 16)
    res1 = Reservation(
        reservation_id="RES-0001",
        room_number=1,
        user_name="Alice",
        check_in=occ_date - datetime.timedelta(days=1),   # 2024-09-15
        check_out=occ_date + datetime.timedelta(days=1),  # 2024-09-17
        total_price=200.0,
    )
    res2 = Reservation(
        reservation_id="RES-0002",
        room_number=2,
        user_name="Bob",
        check_in=occ_date - datetime.timedelta(days=2),   # 2024-09-14
        check_out=occ_date + datetime.timedelta(days=2),  # 2024-09-18
        total_price=300.0,
    )
    system.reservations[res1.reservation_id] = res1
    system.reservations[res2.reservation_id] = res2

    occupied = system.get_room_occupancy(occ_date)
    assert occupied == [1, 2]


def test_book_room_edge_case_single_night(system):
    system.add_room(1, "single", 100.0)
    check_in = _future_date(1)
    check_out = _future_date(2)  # exactly one night
    res_id = system.book_room(1, "John Doe", check_in, check_out)
    assert res_id == "RES-0001"
    assert res_id in system.reservations
    reservation = system.reservations[res_id]
    assert reservation.total_price == 100.0  # 1 night * 100.0


def test_is_room_available_false(system):
    system.add_room(1, "single", 100.0)
    # Book an initial reservation
    first_check_in = _future_date(10)
    first_check_out = _future_date(12)
    system.book_room(1, "John Doe", first_check_in, first_check_out)

    # Overlapping request should be unavailable
    overlapping_check_in = _future_date(11)
    overlapping_check_out = _future_date(13)
    assert system._is_room_available(1, overlapping_check_in, overlapping_check_out) is False