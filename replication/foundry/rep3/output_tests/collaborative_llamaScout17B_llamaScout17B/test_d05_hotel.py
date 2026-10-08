import pytest
from data.input_code.d05_hotel import *
import datetime

@pytest.fixture
def hotel_system():
    return HotelReservationSystem()

def test_add_room_valid(hotel_system):
    hotel_system.add_room(101, "Single", 100.0)
    assert 101 in hotel_system.rooms

def test_add_room_invalid_price(hotel_system):
    with pytest.raises(ValueError):
        hotel_system.add_room(102, "Double", 0.0)

@pytest.mark.parametrize('room_number, user_name, check_in, check_out, expected', [
    (103, "John", datetime.date.today() + datetime.timedelta(days=1), datetime.date.today() + datetime.timedelta(days=3), 'RoomNotFoundError'),
    (101, "John", datetime.date.today() + datetime.timedelta(days=3), datetime.date.today() + datetime.timedelta(days=1), 'InvalidDateError'),
    (101, "John", datetime.date.today() - datetime.timedelta(days=1), datetime.date.today() + datetime.timedelta(days=1), 'InvalidDateError'),
])
def test_book_room_error(hotel_system, room_number, user_name, check_in, check_out, expected):
    hotel_system.add_room(101, "Single", 100.0)
    with pytest.raises(eval(expected)):
        hotel_system.book_room(room_number, user_name, check_in, check_out)

def test_book_room_success(hotel_system):
    hotel_system.add_room(101, "Single", 100.0)
    res_id = hotel_system.book_room(101, "John", datetime.date.today() + datetime.timedelta(days=1), datetime.date.today() + datetime.timedelta(days=3))
    assert res_id.startswith('RES-')

def test_book_room_unavailable(hotel_system):
    hotel_system.add_room(101, "Single", 100.0)
    hotel_system.book_room(101, "John", datetime.date.today() + datetime.timedelta(days=1), datetime.date.today() + datetime.timedelta(days=3))
    with pytest.raises(RoomUnavailableError):
        hotel_system.book_room(101, "Jane", datetime.date.today() + datetime.timedelta(days=2), datetime.date.today() + datetime.timedelta(days=4))

def test_cancel_reservation_not_found(hotel_system):
    with pytest.raises(ReservationNotFoundError):
        hotel_system.cancel_reservation("RES-9999")

def test_get_room_occupancy(hotel_system):
    hotel_system.add_room(101, "Single", 100.0)
    hotel_system.book_room(101, "John", datetime.date.today() + datetime.timedelta(days=1), datetime.date.today() + datetime.timedelta(days=3))
    assert hotel_system.get_room_occupancy(datetime.date.today() + datetime.timedelta(days=2)) == [101]

@pytest.mark.parametrize('days_before_checkin, expected_refund_ratio', [
    (10, 1.0),  # > 7 days
    (5, 0.5),   # 2-7 days
    (1, 0.0),   # < 2 days
])
def test_cancel_reservation_refund(hotel_system, days_before_checkin, expected_refund_ratio, monkeypatch):
    hotel_system.add_room(101, "Single", 100.0)
    check_in_date = datetime.date.today() + datetime.timedelta(days=days_before_checkin)
    res_id = hotel_system.book_room(101, "John", check_in_date, check_in_date + datetime.timedelta(days=2))
    assert res_id == "RES-0001"
    class MockDate(datetime.date):
        @classmethod
        def today(cls):
            return check_in_date - datetime.timedelta(days=days_before_checkin)
    monkeypatch.setattr(datetime, 'date', MockDate)
    refund = hotel_system.cancel_reservation(res_id)
    assert refund == round(200.0 * expected_refund_ratio, 2)