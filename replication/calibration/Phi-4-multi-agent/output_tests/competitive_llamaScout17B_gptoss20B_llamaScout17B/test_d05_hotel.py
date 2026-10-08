import pytest
from data.input_code.d05_hotel import *
import datetime as dt

def _patch_today(monkeypatch, year, month, day):
    class FixedDate(dt.date):
        @classmethod
        def today(cls):
            return dt.date(year, month, day)
    monkeypatch.setattr(dt, 'date', FixedDate, raising=True)

def test_T1_AddRoom_Valid(monkeypatch):
    _patch_today(monkeypatch, 2023, 11, 1)
    system = HotelReservationSystem()
    system.add_room(101, "Deluxe", 150.0)
    assert 101 in system.rooms
    assert system.rooms[101]['type'] == "Deluxe"
    assert system.rooms[101]['price_per_night'] == 150.0

def test_T2_AddRoom_InvalidPrice(monkeypatch):
    _patch_today(monkeypatch, 2023, 11, 1)
    system = HotelReservationSystem()
    with pytest.raises(ValueError):
        system.add_room(102, "Suite", -50.0)

def test_T3_BookRoom_Valid(monkeypatch):
    _patch_today(monkeypatch, 2023, 11, 1)
    system = HotelReservationSystem()
    system.add_room(101, "Deluxe", 150.0)
    res_id = system.book_room(101, "John Doe", dt.date(2023, 12, 1), dt.date(2023, 12, 5))
    assert res_id == "RES-0001"
    assert res_id in system.reservations
    res = system.reservations[res_id]
    assert res.room_number == 101
    assert res.user_name == "John Doe"
    assert res.check_in == dt.date(2023, 12, 1)
    assert res.check_out == dt.date(2023, 12, 5)
    assert res.total_price == 600.0

def test_T4_BookRoom_RoomNotFound(monkeypatch):
    _patch_today(monkeypatch, 2023, 11, 1)
    system = HotelReservationSystem()
    with pytest.raises(RoomNotFoundError):
        system.book_room(999, "Jane Doe", dt.date(2023, 12, 1), dt.date(2023, 12, 5))

def test_T5_BookRoom_InvalidDates(monkeypatch):
    _patch_today(monkeypatch, 2023, 11, 1)
    system = HotelReservationSystem()
    system.add_room(101, "Deluxe", 150.0)
    with pytest.raises(InvalidDateError):
        system.book_room(101, "Alice", dt.date(2023, 12, 5), dt.date(2023, 12, 1))

def test_T6_BookRoom_PastDate(monkeypatch):
    _patch_today(monkeypatch, 2023, 12, 10)
    system = HotelReservationSystem()
    system.add_room(101, "Deluxe", 150.0)
    with pytest.raises(InvalidDateError):
        system.book_room(101, "Bob", dt.date(2023, 12, 1), dt.date(2023, 12, 3))

def test_T7_BookRoom_RoomUnavailable(monkeypatch):
    _patch_today(monkeypatch, 2023, 11, 1)
    system = HotelReservationSystem()
    system.add_room(101, "Deluxe", 150.0)
    system.book_room(101, "A", dt.date(2023, 12, 2), dt.date(2023, 12, 6))
    with pytest.raises(RoomUnavailableError):
        system.book_room(101, "B", dt.date(2023, 12, 3), dt.date(2023, 12, 4))

def test_T8_CancelReservation_Valid(monkeypatch):
    _patch_today(monkeypatch, 2023, 11, 1)
    system = HotelReservationSystem()
    system.add_room(101, "Deluxe", 150.0)
    res_id = system.book_room(101, "John Doe", dt.date(2023, 12, 1), dt.date(2023, 12, 5))
    assert res_id == "RES-0001"
    refund = system.cancel_reservation(res_id)
    assert refund == 600.0
    assert res_id not in system.reservations

def test_T9_CancelReservation_NotFound(monkeypatch):
    _patch_today(monkeypatch, 2023, 11, 1)
    system = HotelReservationSystem()
    with pytest.raises(ReservationNotFoundError):
        system.cancel_reservation("RES-9999")

def test_T10_CancelReservation_PartialRefund(monkeypatch):
    _patch_today(monkeypatch, 2023, 11, 25)
    system = HotelReservationSystem()
    system.add_room(101, "Deluxe", 150.0)
    res_id = system.book_room(101, "Alice", dt.date(2023, 12, 1), dt.date(2023, 12, 5))
    assert res_id == "RES-0001"
    refund = system.cancel_reservation(res_id)
    assert refund == 300.0
    assert res_id not in system.reservations

def test_T11_CancelReservation_NoRefund(monkeypatch):
    _patch_today(monkeypatch, 2023, 11, 30)
    system = HotelReservationSystem()
    system.add_room(101, "Deluxe", 150.0)
    res_id = system.book_room(101, "Alice", dt.date(2023, 12, 1), dt.date(2023, 12, 5))
    refund = system.cancel_reservation(res_id)
    assert refund == 0.0
    assert res_id not in system.reservations

def test_T12_GetRoomOccupancy_Valid(monkeypatch):
    _patch_today(monkeypatch, 2023, 11, 1)
    system = HotelReservationSystem()
    system.add_room(101, "Deluxe", 150.0)
    system.book_room(101, "X", dt.date(2023, 12, 1), dt.date(2023, 12, 4))
    occupancy = system.get_room_occupancy(dt.date(2023, 12, 3))
    assert occupancy == [101]

def test_T13_GetRoomOccupancy_NoOccupancy(monkeypatch):
    _patch_today(monkeypatch, 2023, 11, 1)
    system = HotelReservationSystem()
    occupancy = system.get_room_occupancy(dt.date(2023, 11, 30))
    assert occupancy == []