import pytest
from data.input_code.d05_hotel import *
import importlib

def test_module_importable():
    mod = importlib.import_module("data.input_code.d05_hotel")
    assert mod is not None

def test_module_public_api_not_empty():
    mod = importlib.import_module("data.input_code.d05_hotel")
    public = [name for name in dir(mod) if not name.startswith("_")]
    assert len(public) > 0

import pytest
from data.input_code.d05_hotel import *
import datetime

def test_add_room_positive():
    system = HotelReservationSystem()
    system.add_room(101, "Deluxe", 120.0)
    assert 101 in system.rooms
    assert system.rooms[101]['type'] == "Deluxe"
    assert system.rooms[101]['price_per_night'] == 120.0

def test_add_room_invalid_price():
    system = HotelReservationSystem()
    with pytest.raises(ValueError):
        system.add_room(102, "Standard", 0.0)

def test_book_room_success():
    system = HotelReservationSystem()
    system.add_room(101, "Deluxe", 120.0)
    check_in = datetime.date(2026, 10, 20)
    check_out = datetime.date(2026, 10, 22)
    res_id = system.book_room(101, "Alice", check_in, check_out)
    assert res_id == "RES-0001"
    assert res_id in system.reservations
    res = system.reservations[res_id]
    assert res.room_number == 101
    assert res.user_name == "Alice"
    assert res.check_in == check_in
    assert res.check_out == check_out

def test_book_room_not_found():
    system = HotelReservationSystem()
    with pytest.raises(RoomNotFoundError):
        system.book_room(999, "Bob", datetime.date(2026, 10, 20), datetime.date(2026, 10, 22))

def test_book_room_invalid_dates_order():
    system = HotelReservationSystem()
    system.add_room(101, "Deluxe", 100.0)
    with pytest.raises(InvalidDateError):
        system.book_room(101, "Carol", datetime.date(2026, 10, 10), datetime.date(2026, 10, 10))

def test_book_room_past_date():
    system = HotelReservationSystem()
    system.add_room(101, "Deluxe", 100.0)
    with pytest.raises(InvalidDateError):
        system.book_room(101, "Dave", datetime.date(2020, 1, 1), datetime.date(2020, 1, 3))

def test_book_room_unavailable():
    system = HotelReservationSystem()
    system.add_room(101, "Deluxe", 100.0)
    # First booking
    first_check_in = datetime.date(2026, 10, 21)
    first_check_out = datetime.date(2026, 10, 23)
    system.book_room(101, "Eve", first_check_in, first_check_out)
    # Attempt overlapping booking
    with pytest.raises(RoomUnavailableError):
        system.book_room(101, "Frank", datetime.date(2026, 10, 22), datetime.date(2026, 10, 24))

def test_cancel_refund_full():
    system = HotelReservationSystem()
    system.add_room(101, "Standard", 100.0)
    check_in = datetime.date(2026, 10, 20)
    check_out = datetime.date(2026, 10, 22)
    res_id = system.book_room(101, "Alice", check_in, check_out)
    refund = system.cancel_reservation(res_id)
    assert refund == 200.0  # 2 nights * 100

def test_cancel_refund_half():
    system = HotelReservationSystem()
    system.add_room(101, "Standard", 100.0)
    today = datetime.date.today()
    check_in = today + datetime.timedelta(days=7)  # 7 days from today
    check_out = check_in + datetime.timedelta(days=2)
    res_id = system.book_room(101, "Bob", check_in, check_out)
    refund = system.cancel_reservation(res_id)
    assert refund == 100.0  # 50% of 2 nights * 100

def test_cancel_refund_none():
    system = HotelReservationSystem()
    system.add_room(101, "Deluxe", 100.0)
    today = datetime.date.today()
    check_in = today + datetime.timedelta(days=1)  # 1 day from today
    check_out = check_in + datetime.timedelta(days=2)
    res_id = system.book_room(101, "Carol", check_in, check_out)
    refund = system.cancel_reservation(res_id)
    assert refund == 0.0

def test_cancel_not_found():
    system = HotelReservationSystem()
    with pytest.raises(ReservationNotFoundError):
        system.cancel_reservation("RES-9999")

def test_get_occupancy():
    system = HotelReservationSystem()
    system.add_room(101, "Deluxe", 100.0)
    check_in = datetime.date(2026, 10, 21)
    check_out = datetime.date(2026, 10, 22)
    system.book_room(101, "Alice", check_in, check_out)
    occupancy = system.get_room_occupancy(datetime.date(2026, 10, 21))
    assert occupancy == [101]