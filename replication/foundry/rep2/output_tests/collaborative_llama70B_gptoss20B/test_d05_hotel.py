import pytest
import datetime as dt
from data.input_code.d05_hotel import *

# Test T1_OK_add_room and T2_ERR_add_room (grouped parametrically)
@pytest.mark.parametrize('room_number, room_type, price_per_night, expected_exception', [
    (1, 'single', 100.0, None),
    (1, 'single', 0.0, ValueError),
])
def test_T1_T2_add_room(room_number, room_type, price_per_night, expected_exception):
    system = HotelReservationSystem()
    if expected_exception:
        with pytest.raises(expected_exception):
            system.add_room(room_number, room_type, price_per_night)
    else:
        system.add_room(room_number, room_type, price_per_night)
        assert room_number in system.rooms
        assert system.rooms[room_number]['price_per_night'] == price_per_night


# Test T3_OK_book_room
def test_T3_OK_book_room(monkeypatch):
    class FixedDate(dt.date):
        @classmethod
        def today(cls):
            return dt.date(2024, 1, 1)
    monkeypatch.setattr(dt, 'date', FixedDate, raising=True)

    system = HotelReservationSystem()
    system.add_room(1, 'single', 100.0)
    check_in = dt.date(2024, 9, 20)
    check_out = dt.date(2024, 9, 25)
    res_id = system.book_room(1, 'John Doe', check_in, check_out)
    assert res_id == 'RES-0001'


# Test T4_ERR_book_room_room_not_found
def test_T4_ERR_book_room_room_not_found(monkeypatch):
    class FixedDate(dt.date):
        @classmethod
        def today(cls):
            return dt.date(2024, 1, 1)
    monkeypatch.setattr(dt, 'date', FixedDate, raising=True)

    system = HotelReservationSystem()
    check_in = dt.date(2024, 9, 20)
    check_out = dt.date(2024, 9, 25)
    with pytest.raises(RoomNotFoundError):
        system.book_room(2, 'John Doe', check_in, check_out)


# Test T5_ERR_book_room_invalid_dates
def test_T5_ERR_book_room_invalid_dates():
    system = HotelReservationSystem()
    system.add_room(1, 'single', 100.0)
    check_in = dt.date(2024, 9, 25)
    check_out = dt.date(2024, 9, 20)
    with pytest.raises(InvalidDateError):
        system.book_room(1, 'John Doe', check_in, check_out)


# Test T6_ERR_book_room_past_dates
def test_T6_ERR_book_room_past_dates(monkeypatch):
    class FixedDate(dt.date):
        @classmethod
        def today(cls):
            return dt.date(2024, 1, 1)
    monkeypatch.setattr(dt, 'date', FixedDate, raising=True)

    system = HotelReservationSystem()
    system.add_room(1, 'single', 100.0)
    check_in = dt.date(2022, 9, 20)
    check_out = dt.date(2022, 9, 25)
    with pytest.raises(InvalidDateError):
        system.book_room(1, 'John Doe', check_in, check_out)


# Test T7_ERR_book_room_room_unavailable
def test_T7_ERR_book_room_room_unavailable(monkeypatch):
    class FixedDate(dt.date):
        @classmethod
        def today(cls):
            return dt.date(2024, 1, 1)
    monkeypatch.setattr(dt, 'date', FixedDate, raising=True)

    system = HotelReservationSystem()
    system.add_room(1, 'single', 100.0)
    ci = dt.date(2024, 9, 20)
    co = dt.date(2024, 9, 25)
    system.book_room(1, 'John Doe', ci, co)
    with pytest.raises(RoomUnavailableError):
        system.book_room(1, 'Another User', ci, co)


# Test T8_OK_cancel_reservation
def test_T8_OK_cancel_reservation(monkeypatch):
    class FixedDate(dt.date):
        @classmethod
        def today(cls):
            return dt.date(2024, 1, 1)
    monkeypatch.setattr(dt, 'date', FixedDate, raising=True)

    system = HotelReservationSystem()
    system.add_room(1, 'single', 100.0)
    ci = dt.date(2024, 9, 20)
    co = dt.date(2024, 9, 25)
    res_id = system.book_room(1, 'John Doe', ci, co)
    refund = system.cancel_reservation(res_id)
    assert refund == 500.0


# Test T9_ERR_cancel_reservation_not_found
def test_T9_ERR_cancel_reservation_not_found():
    system = HotelReservationSystem()
    with pytest.raises(ReservationNotFoundError):
        system.cancel_reservation('RES-0002')


# Test T10_OK_get_room_occupancy
def test_T10_OK_get_room_occupancy(monkeypatch):
    class FixedDate(dt.date):
        @classmethod
        def today(cls):
            return dt.date(2024, 1, 1)
    monkeypatch.setattr(dt, 'date', FixedDate, raising=True)

    system = HotelReservationSystem()
    system.add_room(1, 'single', 100.0)
    ci = dt.date(2024, 9, 20)
    co = dt.date(2024, 9, 25)
    system.book_room(1, 'John Doe', ci, co)
    date_to_check = dt.date(2024, 9, 22)
    occupancy = system.get_room_occupancy(date_to_check)
    assert occupancy == [1]


# Test T11_OK_get_room_occupancy_no_occupancy
def test_T11_OK_get_room_occupancy_no_occupancy():
    system = HotelReservationSystem()
    system.add_room(1, 'single', 100.0)
    date_to_check = dt.date(2024, 9, 1)
    occupancy = system.get_room_occupancy(date_to_check)
    assert occupancy == []

import pytest
import datetime as dt
from data.input_code.d05_hotel import *

# New tests appended as per JSON plan

def test_T_MISSING_EDGE_BOOK_ROOM_CHECKIN_TODAY(monkeypatch):
    class FixedDate(dt.date):
        @classmethod
        def today(cls):
            return dt.date(2024, 1, 1)
    monkeypatch.setattr(dt, 'date', FixedDate, raising=True)

    system = HotelReservationSystem()
    system.add_room(1, 'single', 100.0)
    check_in = dt.date.today()
    check_out = dt.date.today() + dt.timedelta(days=5)
    res_id = system.book_room(1, 'John Doe', check_in, check_out)
    assert res_id == 'RES-0001'


def test_T_MISSING_EDGE_CANCEL_RESERVATION_CHECKIN_TODAY(monkeypatch):
    class FixedDate(dt.date):
        @classmethod
        def today(cls):
            return dt.date(2024, 1, 1)
    monkeypatch.setattr(dt, 'date', FixedDate, raising=True)

    system = HotelReservationSystem()
    system.add_room(1, 'single', 100.0)
    check_in = dt.date.today()
    check_out = dt.date.today() + dt.timedelta(days=5)
    res_id = system.book_room(1, 'John Doe', check_in, check_out)
    refund = system.cancel_reservation(res_id)
    assert refund == 0.0


def test_T_MISSING_EDGE_CANCEL_RESERVATION_CHECKIN_TOMORROW(monkeypatch):
    class FixedDate(dt.date):
        @classmethod
        def today(cls):
            return dt.date(2024, 1, 1)
    monkeypatch.setattr(dt, 'date', FixedDate, raising=True)

    system = HotelReservationSystem()
    system.add_room(1, 'single', 200.0)
    check_in = dt.date.today() + dt.timedelta(days=3)
    check_out = check_in + dt.timedelta(days=5)
    res_id = system.book_room(1, 'John Doe', check_in, check_out)
    refund = system.cancel_reservation(res_id)
    # 50% refund expected for 2-7 days until check-in
    assert refund == 500.0


def test_T_MISSING_EDGE_CANCEL_RESERVATION_CHECKIN_IN_2_DAYS(monkeypatch):
    class FixedDate(dt.date):
        @classmethod
        def today(cls):
            return dt.date(2024, 1, 1)
    monkeypatch.setattr(dt, 'date', FixedDate, raising=True)

    system = HotelReservationSystem()
    system.add_room(1, 'single', 100.0)
    check_in = dt.date.today() + dt.timedelta(days=2)
    check_out = check_in + dt.timedelta(days=5)
    res_id = system.book_room(1, 'John Doe', check_in, check_out)
    refund = system.cancel_reservation(res_id)
    # 50% refund for 2-7 days
    assert refund == 250.0


def test_T_MISSING_EDGE_GET_ROOM_OCCUPANCY_CHECKIN_DATE(monkeypatch):
    class FixedDate(dt.date):
        @classmethod
        def today(cls):
            return dt.date(2024, 1, 1)
    monkeypatch.setattr(dt, 'date', FixedDate, raising=True)

    system = HotelReservationSystem()
    system.add_room(1, 'single', 100.0)
    date_to_check = dt.date.today() + dt.timedelta(days=5)
    occupancy = system.get_room_occupancy(date_to_check)
    assert occupancy == []


def test_T_MISSING_EDGE_GET_ROOM_OCCUPANCY_CHECKOUT_DATE(monkeypatch):
    class FixedDate(dt.date):
        @classmethod
        def today(cls):
            return dt.date(2024, 1, 1)
    monkeypatch.setattr(dt, 'date', FixedDate, raising=True)

    system = HotelReservationSystem()
    system.add_room(1, 'single', 100.0)
    date_to_check = dt.date.today() + dt.timedelta(days=10)
    occupancy = system.get_room_occupancy(date_to_check)
    assert occupancy == []