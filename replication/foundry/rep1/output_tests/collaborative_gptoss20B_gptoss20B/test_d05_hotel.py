import pytest
import datetime
from data.input_code.d05_hotel import *

def test_T1_BOOK_OK():
    system = HotelReservationSystem()
    system.add_room(room_number=101, room_type="Standard", price_per_night=100)
    check_in = datetime.date.fromisoformat("2026-10-12")
    check_out = datetime.date.fromisoformat("2026-10-14")
    res_id = system.book_room(room_number=101, user_name="Alice", check_in=check_in, check_out=check_out)
    assert res_id == "RES-0001"

def test_T2_BOOK_MISSING_ROOM():
    system = HotelReservationSystem()
    check_in = datetime.date.fromisoformat("2026-10-20")
    check_out = datetime.date.fromisoformat("2026-10-22")
    with pytest.raises(RoomNotFoundError):
        system.book_room(room_number=999, user_name="Bob", check_in=check_in, check_out=check_out)

def test_T3_BOOK_INVALID_DATES():
    system = HotelReservationSystem()
    system.add_room(room_number=101, room_type="Standard", price_per_night=100)
    check_in = datetime.date.fromisoformat("2026-10-12")
    check_out = datetime.date.fromisoformat("2026-10-12")
    with pytest.raises(InvalidDateError):
        system.book_room(room_number=101, user_name="Carol", check_in=check_in, check_out=check_out)

def test_T4_BOOK_PAST_DATE():
    system = HotelReservationSystem()
    system.add_room(room_number=101, room_type="Standard", price_per_night=100)
    check_in = datetime.date.fromisoformat("2026-10-04")
    check_out = datetime.date.fromisoformat("2026-10-06")
    with pytest.raises(InvalidDateError):
        system.book_room(room_number=101, user_name="Dave", check_in=check_in, check_out=check_out)

def test_T5_CANCEL_NOT_FOUND():
    system = HotelReservationSystem()
    with pytest.raises(ReservationNotFoundError):
        system.cancel_reservation("RES-9999")

def test_T6_GET_OCCUPANCY_EMPTY():
    system = HotelReservationSystem()
    date_to_check = datetime.date.fromisoformat("2026-10-07")
    assert system.get_room_occupancy(date_to_check) == []

def test_T7_ADD_ROOM_INVALID_PRICE():
    system = HotelReservationSystem()
    with pytest.raises(ValueError):
        system.add_room(room_number=102, room_type="Standard", price_per_night=-10)

import pytest
import datetime
from data.input_code.d05_hotel import *

def test_T8_CANCEL_REFUND_FULL():
    system = HotelReservationSystem()
    system.add_room(room_number=101, room_type="Standard", price_per_night=100)
    system.add_room(room_number=102, room_type="Standard", price_per_night=60)
    system.add_room(room_number=103, room_type="Standard", price_per_night=150)

    today = datetime.date.today()
    res1_check_in = today + datetime.timedelta(days=8)
    res1_check_out = res1_check_in + datetime.timedelta(days=3)

    res1_id = system.book_room(room_number=101, user_name="Alice", check_in=res1_check_in, check_out=res1_check_out)
    refund = system.cancel_reservation(res1_id)
    assert refund == 300.0

def test_T9_CANCEL_REFUND_HALF():
    system = HotelReservationSystem()
    system.add_room(room_number=101, room_type="Standard", price_per_night=100)
    system.add_room(room_number=102, room_type="Standard", price_per_night=60)
    system.add_room(room_number=103, room_type="Standard", price_per_night=150)

    today = datetime.date.today()
    res1_check_in = today + datetime.timedelta(days=8)
    res1_check_out = res1_check_in + datetime.timedelta(days=3)

    res2_check_in = today + datetime.timedelta(days=4)
    res2_check_out = res2_check_in + datetime.timedelta(days=2)

    res3_check_in = today + datetime.timedelta(days=1)
    res3_check_out = res3_check_in + datetime.timedelta(days=1)

    res1_id = system.book_room(room_number=101, user_name="Alice", check_in=res1_check_in, check_out=res1_check_out)
    res2_id = system.book_room(room_number=102, user_name="Bob", check_in=res2_check_in, check_out=res2_check_out)
    res3_id = system.book_room(room_number=103, user_name="Carol", check_in=res3_check_in, check_out=res3_check_out)

    refund = system.cancel_reservation(res2_id)
    assert refund == 60.0

def test_T10_CANCEL_REFUND_NONE():
    system = HotelReservationSystem()
    system.add_room(room_number=101, room_type="Standard", price_per_night=100)
    system.add_room(room_number=102, room_type="Standard", price_per_night=60)
    system.add_room(room_number=103, room_type="Standard", price_per_night=150)

    today = datetime.date.today()
    res1_check_in = today + datetime.timedelta(days=8)
    res1_check_out = res1_check_in + datetime.timedelta(days=3)

    res2_check_in = today + datetime.timedelta(days=4)
    res2_check_out = res2_check_in + datetime.timedelta(days=2)

    res3_check_in = today + datetime.timedelta(days=1)
    res3_check_out = res3_check_in + datetime.timedelta(days=1)

    res1_id = system.book_room(room_number=101, user_name="Alice", check_in=res1_check_in, check_out=res1_check_out)
    res2_id = system.book_room(room_number=102, user_name="Bob", check_in=res2_check_in, check_out=res2_check_out)
    res3_id = system.book_room(room_number=103, user_name="Carol", check_in=res3_check_in, check_out=res3_check_out)

    refund = system.cancel_reservation(res3_id)
    assert refund == 0.0

import pytest
import datetime
from data.input_code.d05_hotel import *

def test_T11_BOOK_OVERLAP_UNAVAILABLE():
    system = HotelReservationSystem()
    system.add_room(room_number=201, room_type="Standard", price_per_night=100)
    first_check_in = datetime.date.fromisoformat("2026-10-12")
    first_check_out = datetime.date.fromisoformat("2026-10-14")
    system.book_room(room_number=201, user_name="Alice", check_in=first_check_in, check_out=first_check_out)
    with pytest.raises(RoomUnavailableError):
        system.book_room(room_number=201, user_name="Bob",
                         check_in=datetime.date.fromisoformat("2026-10-13"),
                         check_out=datetime.date.fromisoformat("2026-10-15"))

def test_T12_OCCUPANCY_SINGLE():
    system = HotelReservationSystem()
    system.add_room(room_number=301, room_type="Standard", price_per_night=100)
    check_in = datetime.date.fromisoformat("2026-10-12")
    check_out = datetime.date.fromisoformat("2026-10-14")
    system.book_room(room_number=301, user_name="Alice", check_in=check_in, check_out=check_out)
    date_to_check = datetime.date.fromisoformat("2026-10-13")
    assert system.get_room_occupancy(date_to_check) == [301]

def test_T13_OCCUPANCY_BOUNDARY_EXCLUDE_CHECKOUT():
    system = HotelReservationSystem()
    system.add_room(room_number=301, room_type="Standard", price_per_night=100)
    check_in = datetime.date.fromisoformat("2026-10-12")
    check_out = datetime.date.fromisoformat("2026-10-14")
    system.book_room(room_number=301, user_name="Carol", check_in=check_in, check_out=check_out)
    date_to_check = datetime.date.fromisoformat("2026-10-14")
    assert system.get_room_occupancy(date_to_check) == []