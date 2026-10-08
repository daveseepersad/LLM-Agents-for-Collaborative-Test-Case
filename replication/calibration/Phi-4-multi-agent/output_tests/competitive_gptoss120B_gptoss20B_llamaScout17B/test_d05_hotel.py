import pytest
import datetime
from data.input_code.d05_hotel import *

@pytest.fixture
def hotel(monkeypatch):
    fixed_today = datetime.date(2023, 1, 1)

    class FixedDate(datetime.date):
        @classmethod
        def today(cls):
            return fixed_today

    # Patch the date class used in the code to control today()
    monkeypatch.setattr(datetime, 'date', FixedDate, raising=False)
    return HotelReservationSystem()

def test_T1_add_room_ok(hotel):
    res = hotel.add_room(101, "Deluxe", 150.0)
    assert res is None
    assert 101 in hotel.rooms
    assert hotel.rooms[101] == {"type": "Deluxe", "price_per_night": 150.0}

def test_T2_add_room_invalid_price(hotel):
    with pytest.raises(ValueError):
        hotel.add_room(102, "Standard", 0.0)

def test_T3_book_room_success(hotel):
    hotel.add_room(101, "Deluxe", 150.0)
    res_id = hotel.book_room(101, "Alice", datetime.date(2023, 1, 10), datetime.date(2023, 1, 12))
    assert res_id == "RES-0001"

def test_T4_book_room_not_found(hotel):
    with pytest.raises(RoomNotFoundError):
        hotel.book_room(999, "Bob", datetime.date(2023, 1, 10), datetime.date(2023, 1, 12))

def test_T5_book_room_invalid_dates(hotel):
    hotel.add_room(103, "Suite", 200.0)
    with pytest.raises(InvalidDateError):
        hotel.book_room(103, "Carl", datetime.date(2023, 1, 15), datetime.date(2023, 1, 15))

def test_T6_book_room_past_date(hotel):
    hotel.add_room(104, "Standard", 100.0)
    with pytest.raises(InvalidDateError):
        hotel.book_room(104, "Dave", datetime.date(2022, 12, 30), datetime.date(2023, 1, 2))

def test_T7_book_room_unavailable(hotel):
    hotel.add_room(105, "Deluxe", 150.0)
    hotel.book_room(105, "Eve", datetime.date(2023, 1, 10), datetime.date(2023, 1, 15))
    with pytest.raises(RoomUnavailableError):
        hotel.book_room(105, "Frank", datetime.date(2023, 1, 12), datetime.date(2023, 1, 14))

def test_T8_cancel_not_found(hotel):
    with pytest.raises(ReservationNotFoundError):
        hotel.cancel_reservation("RES-9999")

def test_T9_cancel_refund_full(hotel):
    hotel.add_room(106, "Suite", 250.0)
    hotel.book_room(106, "Grace", datetime.date(2023, 1, 20), datetime.date(2023, 1, 22))
    refund = hotel.cancel_reservation("RES-0001")
    assert refund == 500.0

def test_T10_cancel_refund_half(hotel):
    hotel.add_room(107, "Standard", 120.0)
    hotel.book_room(107, "Heidi", datetime.date(2023, 1, 6), datetime.date(2023, 1, 8))
    refund = hotel.cancel_reservation("RES-0001")
    assert refund == 120.0

def test_T11_cancel_refund_none(hotel):
    hotel.add_room(108, "Standard", 80.0)
    hotel.book_room(108, "Ivan", datetime.date(2023, 1, 2), datetime.date(2023, 1, 4))
    refund = hotel.cancel_reservation("RES-0001")
    assert refund == 0.0

def test_T12_get_occupancy_nonempty(hotel):
    hotel.add_room(109, "Deluxe", 180.0)
    hotel.book_room(109, "Judy", datetime.date(2023, 1, 10), datetime.date(2023, 1, 12))
    occ = hotel.get_room_occupancy(datetime.date(2023, 1, 11))
    assert occ == [109]

def test_T13_get_occupancy_empty(hotel):
    hotel.add_room(110, "Standard", 90.0)
    occ = hotel.get_room_occupancy(datetime.date(2023, 1, 5))
    assert occ == []