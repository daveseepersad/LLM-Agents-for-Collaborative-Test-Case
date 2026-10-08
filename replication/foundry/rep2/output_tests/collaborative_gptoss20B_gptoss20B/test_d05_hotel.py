import pytest
import datetime
from data.input_code.d05_hotel import *

def test_T1_add_room_ok():
    system = HotelReservationSystem()
    system.add_room(101, "Deluxe", 150.0)
    # Validate no exception and internal state updated
    assert system.rooms[101]['type'] == "Deluxe"
    assert system.rooms[101]['price_per_night'] == 150.0

def test_T2_add_room_neg_price():
    system = HotelReservationSystem()
    with pytest.raises(ValueError):
        system.add_room(102, "Standard", 0.0)

def test_T3_book_ok():
    system = HotelReservationSystem()
    system.add_room(201, "Deluxe", 150.0)
    check_in = datetime.date.fromisoformat("2099-12-01")
    check_out = datetime.date.fromisoformat("2099-12-03")
    res_id = system.book_room(201, "alice", check_in, check_out)
    assert res_id == "RES-0001"

def test_T4_book_room_not_found():
    system = HotelReservationSystem()
    check_in = datetime.date.fromisoformat("2099-12-01")
    check_out = datetime.date.fromisoformat("2099-12-02")
    with pytest.raises(RoomNotFoundError):
        system.book_room(999, "bob", check_in, check_out)

def test_T5_book_invalid_dates():
    system = HotelReservationSystem()
    system.add_room(202, "Standard", 100.0)
    check_in = datetime.date.fromisoformat("2099-12-05")
    check_out = datetime.date.fromisoformat("2099-12-04")
    with pytest.raises(InvalidDateError):
        system.book_room(202, "carol", check_in, check_out)

def test_T6_book_past_date():
    system = HotelReservationSystem()
    system.add_room(203, "Standard", 100.0)
    check_in = datetime.date.fromisoformat("1900-01-01")
    check_out = datetime.date.fromisoformat("1900-01-02")
    with pytest.raises(InvalidDateError):
        system.book_room(203, "dave", check_in, check_out)

def test_T7_cancel_non_existent_reservation():
    system = HotelReservationSystem()
    with pytest.raises(ReservationNotFoundError):
        system.cancel_reservation("RES-9999")

def test_T8_get_occupancy_empty():
    system = HotelReservationSystem()
    date = datetime.date.fromisoformat("2099-12-15")
    occupancy = system.get_room_occupancy(date)
    assert occupancy == []

import pytest
import datetime
from data.input_code.d05_hotel import *

def test_T_MISSING_NEG_PRICE_ADD_ROOM():
    system = HotelReservationSystem()
    with pytest.raises(ValueError):
        system.add_room(204, "Suite", -10.0)

def test_T_MISSING_EQUAL_DATES_BOOKING():
    system = HotelReservationSystem()
    system.add_room(202, "Standard", 100.0)
    check_in = datetime.date.fromisoformat("2099-12-05")
    check_out = datetime.date.fromisoformat("2099-12-05")
    with pytest.raises(InvalidDateError):
        system.book_room(202, "carol", check_in, check_out)

import pytest
import datetime
from data.input_code.d05_hotel import *

def test_T_OVERLAP_BOOKING():
    system = HotelReservationSystem()
    system.add_room(301, "Standard", 100.0)
    first_in = datetime.date.fromisoformat("2099-12-01")
    first_out = datetime.date.fromisoformat("2099-12-03")
    system.book_room(301, "alice", first_in, first_out)
    second_in = datetime.date.fromisoformat("2099-12-02")
    second_out = datetime.date.fromisoformat("2099-12-04")
    with pytest.raises(RoomUnavailableError):
        system.book_room(301, "bob", second_in, second_out)

def test_T_CANCEL_FULL_REFUND():
    system = HotelReservationSystem()
    system.add_room(402, "Deluxe", 120.0)
    check_in = datetime.date.fromisoformat("2099-12-10")
    check_out = datetime.date.fromisoformat("2099-12-12")
    res_id = system.book_room(402, "carol", check_in, check_out)
    assert res_id == "RES-0001"
    refund = system.cancel_reservation(res_id)
    assert refund == 240.0

def test_T_OCCUPANCY_WITH_RESERVATION():
    system = HotelReservationSystem()
    system.add_room(405, "Standard", 120.0)
    check_in = datetime.date.fromisoformat("2099-12-04")
    check_out = datetime.date.fromisoformat("2099-12-06")
    system.book_room(405, "dave", check_in, check_out)
    date_to_check = datetime.date.fromisoformat("2099-12-05")
    occupancy = system.get_room_occupancy(date_to_check)
    assert occupancy == [405]

import pytest
from data.input_code.d05_hotel import *
import datetime

def test_T9_BOUNDARY_NON_OVERLAP_BOOKING():
    system = HotelReservationSystem()
    system.add_room(301, "Standard", 100.0)
    check_in = datetime.date.fromisoformat("2099-12-03")
    check_out = datetime.date.fromisoformat("2099-12-04")
    res_id = system.book_room(301, "alice", check_in, check_out)
    assert res_id == "RES-0001"

def test_T10_OVERWRITE_ROOM():
    system = HotelReservationSystem()
    system.add_room(501, "Standard", 100.0)
    # Overwrite with a new price
    system.add_room(501, "Standard", 150.0)
    assert system.rooms[501]['price_per_night'] == 150.0

def test_T11_CANCEL_HALF_REFUND():
    system = HotelReservationSystem()
    system.add_room(502, "Deluxe", 100.0)
    today = datetime.date.today()
    check_in = today + datetime.timedelta(days=5)
    check_out = today + datetime.timedelta(days=6)
    res_id = system.book_room(502, "erin", check_in, check_out)
    assert res_id == "RES-0001"
    refund = system.cancel_reservation(res_id)
    assert refund == 50.0

def test_T12_CANCEL_NO_REFUND():
    system = HotelReservationSystem()
    system.add_room(503, "Standard", 80.0)
    today = datetime.date.today()
    check_in1 = today + datetime.timedelta(days=5)
    check_out1 = today + datetime.timedelta(days=7)
    res1 = system.book_room(503, "fran", check_in1, check_out1)
    assert res1 == "RES-0001"
    check_in2 = today + datetime.timedelta(days=1)
    check_out2 = today + datetime.timedelta(days=2)
    res2 = system.book_room(503, "gabe", check_in2, check_out2)
    assert res2 == "RES-0002"
    refund = system.cancel_reservation(res2)
    assert refund == 0.0