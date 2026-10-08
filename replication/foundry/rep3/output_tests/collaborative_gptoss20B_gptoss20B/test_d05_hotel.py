import pytest
import datetime
from data.input_code.d05_hotel import *

@pytest.mark.parametrize('room_number, check_in_str, check_out_str, expected', [
    (101, "2099-01-04", "2099-01-07", True),
    (102, "2099-01-04", "2099-01-06", True),
])
def test_is_room_available_overlap_and_boundary(room_number, check_in_str, check_out_str, expected):
    system = HotelReservationSystem()
    # Ensure rooms exist for the availability check
    system.add_room(101, "Standard", 100.0)
    system.add_room(102, "Standard", 100.0)

    check_in = datetime.date.fromisoformat(check_in_str)
    check_out = datetime.date.fromisoformat(check_out_str)

    result = system._is_room_available(room_number, check_in, check_out)
    assert result == expected

import pytest
import datetime
from data.input_code.d05_hotel import *

def test_T_NEW_ADDROOM_INVALID_PRICE():
    system = HotelReservationSystem()
    with pytest.raises(ValueError):
        system.add_room(201, "Deluxe", -10.0)

def test_T_NEW_BOOK_ROOM_NOT_EXIST():
    system = HotelReservationSystem()
    with pytest.raises(RoomNotFoundError):
        system.book_room(999, "Alice", datetime.date.fromisoformat("2099-01-04"), datetime.date.fromisoformat("2099-01-05"))

def test_T_NEW_BOOK_ROOM_INVALID_DATES():
    system = HotelReservationSystem()
    system.add_room(101, "Standard", 100.0)
    with pytest.raises(InvalidDateError):
        system.book_room(101, "Bob", datetime.date.fromisoformat("2099-01-10"), datetime.date.fromisoformat("2099-01-10"))

def test_T_NEW_CANCEL_NONEXIST_RESERVATION():
    system = HotelReservationSystem()
    with pytest.raises(ReservationNotFoundError):
        system.cancel_reservation("RES-9999")

def test_T_NEW_GET_OCCUPANCY_EMPTY():
    system = HotelReservationSystem()
    date = datetime.date.fromisoformat("2099-01-01")
    result = system.get_room_occupancy(date)
    assert result == []

import pytest
import datetime
from data.input_code.d05_hotel import *

@pytest.mark.parametrize('room_number, user_name, check_in_str, check_out_str, expected', [
    (101, "Alice", "2099-01-04", "2099-01-07", "RES-0001"),
    (101, "Bob", "2000-01-01", "2000-01-02", "InvalidDateError"),
])
def test_T_NEW_BOOK_BOOKING(room_number, user_name, check_in_str, check_out_str, expected):
    system = HotelReservationSystem()
    system.add_room(room_number, "Standard", 100.0)

    check_in = datetime.date.fromisoformat(check_in_str)
    check_out = datetime.date.fromisoformat(check_out_str)

    if isinstance(expected, str) and expected.endswith("Error"):
        exc_class = globals().get(expected)
        with pytest.raises(exc_class):
            system.book_room(room_number, user_name, check_in, check_out)
    else:
        res_id = system.book_room(room_number, user_name, check_in, check_out)
        assert res_id == expected

def test_T_NEW_BOOK_OVERLAP_UNAVAILABLE():
    system = HotelReservationSystem()
    system.add_room(101, "Standard", 100.0)

    res_id = system.book_room(101, "Carol", datetime.date(2099, 1, 4), datetime.date(2099, 1, 8))
    assert res_id == "RES-0001"

    with pytest.raises(RoomUnavailableError):
        system.book_room(101, "Dave", datetime.date(2099, 1, 4), datetime.date(2099, 1, 8))

def test_T_NEW_OCCUPANCY_DATE():
    system = HotelReservationSystem()
    system.add_room(101, "Standard", 100.0)

    system.book_room(101, "Alice", datetime.date(2099, 1, 4), datetime.date(2099, 1, 7))

    date_to_check = datetime.date(2099, 1, 5)
    occupancy = system.get_room_occupancy(date_to_check)
    assert occupancy == [101]

def test_T_NEW_CANCEL_NONEXIST_RESERVATION_2():
    system = HotelReservationSystem()
    with pytest.raises(ReservationNotFoundError):
        system.cancel_reservation("RES-9999")

import pytest
import datetime
from data.input_code.d05_hotel import *

def test_T_NEW_CANCEL_REFUND_FULL_PATH():
    system = HotelReservationSystem()
    check_in = datetime.date.today() + datetime.timedelta(days=8)
    res = Reservation(
        reservation_id="RES-1000",
        room_number=101,
        user_name="Alice",
        check_in=check_in,
        check_out=check_in + datetime.timedelta(days=2),
        total_price=200.0
    )
    system.reservations[res.reservation_id] = res
    refund = system.cancel_reservation(res.reservation_id)
    assert refund == 200.0

def test_T_NEW_CANCEL_REFUND_HALF_PATH():
    system = HotelReservationSystem()
    check_in = datetime.date.today() + datetime.timedelta(days=5)
    res = Reservation(
        reservation_id="RES-1001",
        room_number=101,
        user_name="Bob",
        check_in=check_in,
        check_out=check_in + datetime.timedelta(days=2),
        total_price=150.0
    )
    system.reservations[res.reservation_id] = res
    refund = system.cancel_reservation(res.reservation_id)
    assert refund == 75.0

def test_T_NEW_CANCEL_REFUND_NONE_PATH():
    system = HotelReservationSystem()
    check_in = datetime.date.today() + datetime.timedelta(days=1)
    res = Reservation(
        reservation_id="RES-1002",
        room_number=101,
        user_name="Charlie",
        check_in=check_in,
        check_out=check_in + datetime.timedelta(days=1),
        total_price=75.0
    )
    system.reservations[res.reservation_id] = res
    refund = system.cancel_reservation(res.reservation_id)
    assert refund == 0.0