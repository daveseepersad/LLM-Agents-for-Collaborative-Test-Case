import pytest
import datetime
from data.input_code.d05_hotel import *

@pytest.fixture
def fresh_system():
    """Provides a fresh HotelReservationSystem instance for each test."""
    return HotelReservationSystem()

# ---------- add_room ----------
@pytest.mark.parametrize(
    "room_number, room_type, price, expected_exception",
    [
        (101, "Single", 100.0, None),          # valid
        (102, "Double", -50.0, ValueError),   # invalid price
    ],
)
def test_add_room(fresh_system, room_number, room_type, price, expected_exception):
    if expected_exception:
        with pytest.raises(expected_exception):
            fresh_system.add_room(room_number, room_type, price)
    else:
        fresh_system.add_room(room_number, room_type, price)
        assert fresh_system.rooms[room_number]["type"] == room_type
        assert fresh_system.rooms[room_number]["price_per_night"] == price

# ---------- book_room ----------
def test_book_room_success(fresh_system):
    fresh_system.add_room(101, "Single", 100.0)
    check_in = datetime.date.today() + datetime.timedelta(days=1)
    check_out = datetime.date.today() + datetime.timedelta(days=3)
    res_id = fresh_system.book_room(101, "John Doe", check_in, check_out)
    assert res_id == "RES-0001"
    # verify reservation stored correctly
    reservation = fresh_system.reservations[res_id]
    assert reservation.room_number == 101
    assert reservation.user_name == "John Doe"
    assert reservation.check_in == check_in
    assert reservation.check_out == check_out
    assert reservation.total_price == 200.0  # 2 nights * 100.0

@pytest.mark.parametrize(
    "room_number, check_in_offset, check_out_offset, expected_exception",
    [
        (103, 1, 3, RoomNotFoundError),          # room does not exist
        (101, 3, 1, InvalidDateError),          # checkout before checkin
        (101, -1, 3, InvalidDateError),         # check‑in in the past
    ],
)
def test_book_room_errors(fresh_system, room_number, check_in_offset, check_out_offset, expected_exception):
    # ensure room 101 exists for the date‑related cases
    if room_number == 101:
        fresh_system.add_room(101, "Single", 100.0)
    check_in = datetime.date.today() + datetime.timedelta(days=check_in_offset)
    check_out = datetime.date.today() + datetime.timedelta(days=check_out_offset)
    with pytest.raises(expected_exception):
        fresh_system.book_room(room_number, "John Doe", check_in, check_out)

def test_book_room_unavailable(fresh_system):
    fresh_system.add_room(101, "Single", 100.0)
    ci = datetime.date.today() + datetime.timedelta(days=1)
    co = datetime.date.today() + datetime.timedelta(days=3)
    # first booking succeeds
    first_res = fresh_system.book_room(101, "John Doe", ci, co)
    assert first_res == "RES-0001"
    # second booking for overlapping dates should fail
    with pytest.raises(RoomUnavailableError):
        fresh_system.book_room(101, "Jane Doe", ci, co)

# ---------- cancel_reservation ----------
def test_cancel_reservation_full_refund(fresh_system):
    fresh_system.add_room(101, "Single", 100.0)
    check_in = datetime.date.today() + datetime.timedelta(days=10)
    check_out = datetime.date.today() + datetime.timedelta(days=12)
    res_id = fresh_system.book_room(101, "John Doe", check_in, check_out)
    refund = fresh_system.cancel_reservation(res_id)
    assert refund == 200.0  # 2 nights * 100.0, full refund (>7 days)

def test_cancel_reservation_partial_refund(fresh_system):
    fresh_system.add_room(101, "Single", 100.0)
    check_in = datetime.date.today() + datetime.timedelta(days=6)
    check_out = datetime.date.today() + datetime.timedelta(days=8)
    res_id = fresh_system.book_room(101, "John Doe", check_in, check_out)
    refund = fresh_system.cancel_reservation(res_id)
    assert refund == 100.0  # 2 nights * 100.0 * 0.5 (2‑7 days)

def test_cancel_reservation_no_refund(fresh_system):
    fresh_system.add_room(101, "Single", 100.0)
    check_in = datetime.date.today() + datetime.timedelta(days=1)
    check_out = datetime.date.today() + datetime.timedelta(days=3)
    res_id = fresh_system.book_room(101, "John Doe", check_in, check_out)
    refund = fresh_system.cancel_reservation(res_id)
    assert refund == 0.0  # <2 days until check‑in

def test_cancel_reservation_not_found(fresh_system):
    with pytest.raises(ReservationNotFoundError):
        fresh_system.cancel_reservation("RES-9999")

# ---------- get_room_occupancy ----------
def test_get_room_occupancy_occupied(fresh_system):
    fresh_system.add_room(101, "Single", 100.0)
    ci = datetime.date.today() + datetime.timedelta(days=1)
    co = datetime.date.today() + datetime.timedelta(days=3)
    fresh_system.book_room(101, "John Doe", ci, co)
    query_date = datetime.date.today() + datetime.timedelta(days=2)
    occupied = fresh_system.get_room_occupancy(query_date)
    assert occupied == [101]

def test_get_room_occupancy_empty(fresh_system):
    query_date = datetime.date.today()
    occupied = fresh_system.get_room_occupancy(query_date)
    assert occupied == []