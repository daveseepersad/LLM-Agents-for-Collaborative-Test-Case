import pytest
import datetime
from data.input_code.d05_hotel import *

def test_T1_OK_add_room():
    system = HotelReservationSystem()
    system.add_room(1, 'single', 100.0)

def test_T2_ERR_add_room():
    system = HotelReservationSystem()
    with pytest.raises(ValueError):
        system.add_room(1, 'single', 0.0)

def test_T3_OK_book_room():
    system = HotelReservationSystem()
    system.add_room(1, 'single', 100.0)
    today = datetime.date.today()
    check_in = today + datetime.timedelta(days=60)
    check_out = today + datetime.timedelta(days=65)
    res_id = system.book_room(1, "John Doe", check_in, check_out)
    assert res_id == "RES-0001"

def test_T4_ERR_book_room_room_not_found():
    system = HotelReservationSystem()
    system.add_room(1, 'single', 100.0)
    today = datetime.date.today()
    check_in = today + datetime.timedelta(days=60)
    check_out = today + datetime.timedelta(days=62)
    with pytest.raises(RoomNotFoundError):
        system.book_room(2, "John Doe", check_in, check_out)

def test_T5_ERR_book_room_invalid_dates():
    system = HotelReservationSystem()
    system.add_room(1, 'single', 100.0)
    today = datetime.date.today()
    check_in = today + datetime.timedelta(days=30)
    check_out = today + datetime.timedelta(days=25)
    with pytest.raises(InvalidDateError):
        system.book_room(1, "John Doe", check_in, check_out)

def test_T6_ERR_book_room_room_unavailable():
    system = HotelReservationSystem()
    system.add_room(1, 'single', 100.0)
    today = datetime.date.today()
    check_in1 = today + datetime.timedelta(days=10)
    check_out1 = today + datetime.timedelta(days=13)
    system.book_room(1, "Alice", check_in1, check_out1)
    check_in2 = today + datetime.timedelta(days=12)
    check_out2 = today + datetime.timedelta(days=15)
    with pytest.raises(RoomUnavailableError):
        system.book_room(1, "John Doe", check_in2, check_out2)

def test_T7_OK_cancel_reservation():
    system = HotelReservationSystem()
    system.add_room(1, 'single', 100.0)
    today = datetime.date.today()
    check_in = today + datetime.timedelta(days=8)
    check_out = today + datetime.timedelta(days=13)
    res_id = system.book_room(1, "John Doe", check_in, check_out)
    refund = system.cancel_reservation(res_id)
    nights = (check_out - check_in).days
    expected_total = nights * 100.0
    assert res_id == "RES-0001"
    assert refund == expected_total

def test_T8_ERR_cancel_reservation_not_found():
    system = HotelReservationSystem()
    with pytest.raises(ReservationNotFoundError):
        system.cancel_reservation("RES-9999")

def test_T9_OK_get_room_occupancy():
    system = HotelReservationSystem()
    system.add_room(1, 'single', 100.0)
    today = datetime.date.today()
    check_in = today + datetime.timedelta(days=10)
    check_out = today + datetime.timedelta(days=12)
    system.book_room(1, "John Doe", check_in, check_out)
    target_date = check_in + datetime.timedelta(days=1)
    occupancy = system.get_room_occupancy(target_date)
    assert occupancy == [1]

def test_T10_OK_is_room_available():
    system = HotelReservationSystem()
    system.add_room(1, 'single', 100.0)
    assert system._is_room_available(1, datetime.date.today() + datetime.timedelta(days=30),
                                   datetime.date.today() + datetime.timedelta(days=32)) is True

import pytest
import datetime
from data.input_code.d05_hotel import *

def test_T_MISSING_EDGE_BOOK_PAST():
    system = HotelReservationSystem()
    system.add_room(1, 'single', 100.0)
    past_check_in = datetime.date(2022, 1, 1)
    past_check_out = datetime.date(2022, 1, 5)
    with pytest.raises(InvalidDateError):
        system.book_room(1, "John Doe", past_check_in, past_check_out)

def test_T_MISSING_EDGE_CANCEL_REFUND_50():
    system = HotelReservationSystem()
    system.add_room(1, 'single', 100.0)
    today = datetime.date.today()
    check_in = today + datetime.timedelta(days=5)
    check_out = check_in + datetime.timedelta(days=2)
    res_id = system.book_room(1, "John Doe", check_in, check_out)
    refund = system.cancel_reservation(res_id)
    nights = (check_out - check_in).days
    total_price = round(nights * 100.0, 2)
    expected = round(total_price * 0.5, 2)
    assert refund == expected

def test_T_MISSING_EDGE_CANCEL_REFUND_0():
    system = HotelReservationSystem()
    system.add_room(1, 'single', 100.0)
    today = datetime.date.today()
    check_in = today + datetime.timedelta(days=1)
    check_out = check_in + datetime.timedelta(days=2)
    res_id = system.book_room(1, "John Doe", check_in, check_out)
    refund = system.cancel_reservation(res_id)
    assert refund == 0.0

def test_T_MISSING_EDGE_GET_ROOM_OCCUPANCY_NO_BOOKINGS():
    system = HotelReservationSystem()
    date = datetime.datetime.strptime("2024-09-16", "%Y-%m-%d").date()
    occupancy = system.get_room_occupancy(date)
    assert occupancy == []

def test_T_MISSING_EDGE_GET_ROOM_OCCUPANCY_MULTIPLE_BOOKINGS():
    system = HotelReservationSystem()
    system.add_room(1, 'single', 100.0)
    system.add_room(2, 'double', 150.0)
    base = datetime.date.today() + datetime.timedelta(days=10)
    check_in = base - datetime.timedelta(days=1)
    check_out = base + datetime.timedelta(days=1)
    system.book_room(1, "Alice", check_in, check_out)
    system.book_room(2, "Bob", check_in, check_out)
    target_date = base
    occupancy = system.get_room_occupancy(target_date)
    assert occupancy == [1, 2]

def test_T_MISSING_EDGE_BOOK_ROOM_CHECKIN_SAME_DAY():
    system = HotelReservationSystem()
    system.add_room(1, 'single', 100.0)
    today = datetime.date.today()
    check_in = today + datetime.timedelta(days=2)
    check_out = check_in  # same day as check-in
    with pytest.raises(InvalidDateError):
        system.book_room(1, "John Doe", check_in, check_out)