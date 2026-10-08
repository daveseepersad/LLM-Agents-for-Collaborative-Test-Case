import pytest
import datetime
from data.input_code.d05_hotel import *

@pytest.fixture
def system():
    return HotelReservationSystem()

def test_init(system):
    assert system.rooms == {}
    assert system.reservations == {}

@pytest.mark.parametrize(
    "room_number, room_type, price, expect_exception",
    [
        (101, "Single", 100.0, None),          # valid room
        (102, "Double", -50.0, ValueError),   # invalid price
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

@pytest.mark.parametrize(
    "room_number, check_in_offset, check_out_offset, expect_exc",
    [
        (103, 1, 3, RoomNotFoundError),      # non‑existent room
        (101, 3, 1, InvalidDateError),       # checkout before checkin
        (101, -1, 1, InvalidDateError),      # booking in the past
    ],
)
def test_book_room_errors(system, room_number, check_in_offset, check_out_offset, expect_exc):
    # ensure a valid room exists for the relevant cases
    system.add_room(101, "Single", 100.0)

    check_in = datetime.date.today() + datetime.timedelta(days=check_in_offset)
    check_out = datetime.date.today() + datetime.timedelta(days=check_out_offset)

    with pytest.raises(expect_exc):
        system.book_room(room_number, "John", check_in, check_out)

def test_book_room_success_and_unavailable(system):
    system.add_room(101, "Single", 100.0)

    check_in = datetime.date.today() + datetime.timedelta(days=1)
    check_out = datetime.date.today() + datetime.timedelta(days=3)

    res_id = system.book_room(101, "John", check_in, check_out)
    assert res_id == "RES-0001"

    # overlapping reservation should raise RoomUnavailableError
    overlapping_check_in = datetime.date.today() + datetime.timedelta(days=2)
    overlapping_check_out = datetime.date.today() + datetime.timedelta(days=4)

    with pytest.raises(RoomUnavailableError):
        system.book_room(101, "Jane", overlapping_check_in, overlapping_check_out)

def test_get_room_occupancy(system):
    system.add_room(101, "Single", 100.0)

    check_in = datetime.date.today() + datetime.timedelta(days=1)
    check_out = datetime.date.today() + datetime.timedelta(days=3)

    system.book_room(101, "John", check_in, check_out)

    occupancy_date = datetime.date.today() + datetime.timedelta(days=2)
    occupied_rooms = system.get_room_occupancy(occupancy_date)
    assert occupied_rooms == [101]

def test_cancel_nonexistent(system):
    with pytest.raises(ReservationNotFoundError):
        system.cancel_reservation("RES-9999")

@pytest.mark.parametrize(
    "days_until_checkin, expected_refund",
    [
        (8, 200.0),   # >7 days → full refund
        (5, 100.0),   # 2‑7 days → 50% refund
        (1, 0.0),     # <2 days → no refund
    ],
)
def test_cancel_refund(system, days_until_checkin, expected_refund):
    system.add_room(101, "Single", 100.0)

    check_in = datetime.date.today() + datetime.timedelta(days=days_until_checkin)
    check_out = check_in + datetime.timedelta(days=2)  # 2 nights → total 200.0

    res_id = system.book_room(101, "John", check_in, check_out)
    refund = system.cancel_reservation(res_id)
    assert refund == expected_refund