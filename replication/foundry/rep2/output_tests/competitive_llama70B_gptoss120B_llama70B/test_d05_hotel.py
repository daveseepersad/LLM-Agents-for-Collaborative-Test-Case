import pytest
import datetime
from data.input_code.d05_hotel import *

@pytest.fixture
def empty_system():
    """Provides a fresh HotelReservationSystem with no rooms."""
    return HotelReservationSystem()

@pytest.fixture
def system_with_room():
    """Provides a system with a single room (room 1) added."""
    sys = HotelReservationSystem()
    sys.add_room(1, "single", 100.0)
    return sys


# ---------- add_room ----------
@pytest.mark.parametrize(
    "room_number, room_type, price, expected_exception",
    [
        (1, "single", 100.0, None),          # valid addition
        (2, "double", 0.0, ValueError),      # invalid price
    ],
)
def test_add_room(empty_system, room_number, room_type, price, expected_exception):
    if expected_exception:
        with pytest.raises(expected_exception):
            empty_system.add_room(room_number, room_type, price)
    else:
        empty_system.add_room(room_number, room_type, price)
        assert empty_system.rooms[room_number]["price_per_night"] == price


# ---------- book_room ----------
def test_book_room_success(system_with_room):
    check_in = datetime.date.today() + datetime.timedelta(days=10)
    check_out = check_in + datetime.timedelta(days=5)   # 5 nights
    res_id = system_with_room.book_room(
        room_number=1,
        user_name="John Doe",
        check_in=check_in,
        check_out=check_out,
    )
    assert res_id == "RES-0001"
    # verify reservation stored correctly
    reservation = system_with_room.reservations[res_id]
    assert reservation.total_price == 500.0  # 5 nights * 100.0


@pytest.mark.parametrize(
    "room_number, check_in_offset, check_out_offset, expected_exception",
    [
        (2, 10, 15, RoomNotFoundError),          # room does not exist
        (1, 10, 5, InvalidDateError),           # checkout before checkin
        (1, -10, -5, InvalidDateError),         # dates in the past
    ],
)
def test_book_room_errors(system_with_room, room_number, check_in_offset, check_out_offset, expected_exception):
    today = datetime.date.today()
    check_in = today + datetime.timedelta(days=check_in_offset)
    check_out = today + datetime.timedelta(days=check_out_offset)
    with pytest.raises(expected_exception):
        system_with_room.book_room(
            room_number=room_number,
            user_name="John Doe",
            check_in=check_in,
            check_out=check_out,
        )


# ---------- cancel_reservation ----------
def test_cancel_reservation_full_refund(system_with_room):
    # create a reservation far enough in the future (>7 days)
    check_in = datetime.date.today() + datetime.timedelta(days=20)
    check_out = check_in + datetime.timedelta(days=5)
    res_id = system_with_room.book_room(1, "John Doe", check_in, check_out)

    refund = system_with_room.cancel_reservation(res_id)
    assert refund == 500.0  # 5 nights * 100.0, full refund (>7 days)


def test_cancel_reservation_not_found(system_with_room):
    with pytest.raises(ReservationNotFoundError):
        system_with_room.cancel_reservation("RES-9999")


# ---------- get_room_occupancy ----------
def test_get_room_occupancy(system_with_room):
    check_in = datetime.date.today() + datetime.timedelta(days=10)
    check_out = check_in + datetime.timedelta(days=5)
    system_with_room.book_room(1, "John Doe", check_in, check_out)

    # pick a date inside the reservation period
    target_date = check_in + datetime.timedelta(days=2)
    occupied = system_with_room.get_room_occupancy(target_date)
    assert occupied == [1]


# ---------- _is_room_available ----------
def test_is_room_available_true(system_with_room):
    check_in = datetime.date.today() + datetime.timedelta(days=30)
    check_out = check_in + datetime.timedelta(days=5)
    available = system_with_room._is_room_available(1, check_in, check_out)
    assert available is True


def test_is_room_available_false(system_with_room):
    # first reservation
    first_check_in = datetime.date.today() + datetime.timedelta(days=30)
    first_check_out = first_check_in + datetime.timedelta(days=5)
    system_with_room.book_room(1, "John Doe", first_check_in, first_check_out)

    # overlapping request
    overlapping_check_in = first_check_in + datetime.timedelta(days=2)
    overlapping_check_out = overlapping_check_in + datetime.timedelta(days=3)
    available = system_with_room._is_room_available(1, overlapping_check_in, overlapping_check_out)
    assert available is False

# ---------- cancel_reservation ----------
@pytest.mark.parametrize(
    "check_in_offset, check_out_offset, expected_refund",
    [
        (10, 15, 500.0),  # >7 days before check-in, full refund
        (1, 6, 0.0),      # < 2 days before check-in, no refund
    ],
)
def test_cancel_reservation_partial_refund(system_with_room, check_in_offset, check_out_offset, expected_refund):
    today = datetime.date.today()
    check_in = today + datetime.timedelta(days=check_in_offset)
    check_out = today + datetime.timedelta(days=check_out_offset)
    res_id = system_with_room.book_room(1, "John Doe", check_in, check_out)

    refund = system_with_room.cancel_reservation(res_id)
    assert refund == expected_refund


# ---------- book_room ----------
def test_book_room_unavailable(system_with_room):
    # first reservation
    first_check_in = datetime.date.today() + datetime.timedelta(days=10)
    first_check_out = first_check_in + datetime.timedelta(days=5)
    system_with_room.book_room(1, "John Doe", first_check_in, first_check_out)

    # overlapping request
    overlapping_check_in = first_check_in + datetime.timedelta(days=2)
    overlapping_check_out = overlapping_check_in + datetime.timedelta(days=3)
    with pytest.raises(RoomUnavailableError):
        system_with_room.book_room(1, "Jane Doe", overlapping_check_in, overlapping_check_out)


# ---------- get_room_occupancy ----------
def test_get_room_occupancy_multiple_rooms(system_with_room):
    system_with_room.add_room(2, "double", 150.0)

    check_in1 = datetime.date.today() + datetime.timedelta(days=10)
    check_out1 = check_in1 + datetime.timedelta(days=5)
    system_with_room.book_room(1, "John Doe", check_in1, check_out1)

    check_in2 = datetime.date.today() + datetime.timedelta(days=10)
    check_out2 = check_in2 + datetime.timedelta(days=5)
    system_with_room.book_room(2, "Jane Doe", check_in2, check_out2)

    # pick a date inside both reservation periods
    target_date = check_in1 + datetime.timedelta(days=2)
    occupied = system_with_room.get_room_occupancy(target_date)
    assert occupied == [1, 2]


def test_get_room_occupancy_no_occupancy(system_with_room):
    # pick a date before any reservations
    target_date = datetime.date.today() - datetime.timedelta(days=1)
    occupied = system_with_room.get_room_occupancy(target_date)
    assert occupied == []


# ---------- _is_room_available ----------
def test_is_room_available_edge_cases(system_with_room):
    check_in = datetime.date.today() + datetime.timedelta(days=10)
    check_out = check_in
    available = system_with_room._is_room_available(1, check_in, check_out)
    assert available is True

@pytest.mark.parametrize(
    "check_in_offset, check_out_offset, expected_refund",
    [
        (5, 10, 250.0),  # 2-7 days before check-in, 50% refund
    ],
)
def test_cancel_reservation_mid_refund(system_with_room, check_in_offset, check_out_offset, expected_refund):
    today = datetime.date.today()
    check_in = today + datetime.timedelta(days=check_in_offset)
    check_out = today + datetime.timedelta(days=check_out_offset)
    res_id = system_with_room.book_room(1, "John Doe", check_in, check_out)
    refund = system_with_room.cancel_reservation(res_id)
    assert refund == expected_refund


def test_book_room_same_day_success(system_with_room):
    """Booking a room for today should succeed (no past date restriction)."""
    check_in = datetime.date.today()
    check_out = check_in + datetime.timedelta(days=1)
    res_id = system_with_room.book_room(1, "John Doe", check_in, check_out)
    assert res_id == "RES-0001"
    reservation = system_with_room.reservations[res_id]
    assert reservation.total_price == 100.0
    # Verify occupancy for today includes the room
    occupied_today = system_with_room.get_room_occupancy(check_in)
    assert occupied_today == [1]


def test_get_room_occupancy_tomorrow(system_with_room):
    target_date = datetime.date.today() + datetime.timedelta(days=1)
    occupied = system_with_room.get_room_occupancy(target_date)
    assert occupied == []


def test_is_room_available_tomorrow(system_with_room):
    check_in = datetime.date.today() + datetime.timedelta(days=1)
    check_out = check_in + datetime.timedelta(days=1)
    available = system_with_room._is_room_available(1, check_in, check_out)
    assert available is True