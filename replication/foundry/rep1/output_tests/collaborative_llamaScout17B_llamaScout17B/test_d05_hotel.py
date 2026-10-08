import pytest
from data.input_code.d05_hotel import *
import datetime
from unittest.mock import patch
from freezegun import freeze_time

@pytest.fixture
def hotel_system():
    return HotelReservationSystem()

def test_init(hotel_system):
    assert hotel_system.rooms == {}
    assert hotel_system.reservations == {}

@pytest.mark.parametrize('room_number, room_type, price_per_night, expected', [
    (101, 'Single', 100.0, None),
    (102, 'Double', -50.0, 'ValueError')
])
def test_add_room(hotel_system, room_number, room_type, price_per_night, expected):
    if expected is None:
        hotel_system.add_room(room_number, room_type, price_per_night)
        assert hotel_system.rooms[room_number] == {'type': room_type, 'price_per_night': price_per_night}
    else:
        with pytest.raises(eval(expected)):
            hotel_system.add_room(room_number, room_type, price_per_night)

def test_book_room_non_existent(hotel_system):
    with pytest.raises(RoomNotFoundError):
        hotel_system.book_room(103, 'John', datetime.date.today() + datetime.timedelta(days=1), datetime.date.today() + datetime.timedelta(days=3))

@pytest.mark.parametrize('room_number, user_name, check_in, check_out, expected', [
    (101, 'John', datetime.date.today() + datetime.timedelta(days=3), datetime.date.today() + datetime.timedelta(days=1), 'InvalidDateError'),
    (101, 'John', datetime.date.today() - datetime.timedelta(days=1), datetime.date.today() + datetime.timedelta(days=1), 'InvalidDateError'),
    (101, 'John', datetime.date.today() + datetime.timedelta(days=1), datetime.date.today() + datetime.timedelta(days=3), 'RES-0001')
])
def test_book_room(hotel_system, room_number, user_name, check_in, check_out, expected):
    hotel_system.add_room(room_number, 'Single', 100.0)
    if isinstance(expected, str) and expected.startswith('RES-'):
        res_id = hotel_system.book_room(room_number, user_name, check_in, check_out)
        assert res_id == expected
    else:
        with pytest.raises(eval(expected)):
            hotel_system.book_room(room_number, user_name, check_in, check_out)

def test_book_room_unavailable(hotel_system):
    hotel_system.add_room(101, 'Single', 100.0)
    hotel_system.book_room(101, 'John', datetime.date.today() + datetime.timedelta(days=1), datetime.date.today() + datetime.timedelta(days=3))
    with pytest.raises(RoomUnavailableError):
        hotel_system.book_room(101, 'Jane', datetime.date.today() + datetime.timedelta(days=1), datetime.date.today() + datetime.timedelta(days=3))

def test_cancel_non_existent(hotel_system):
    with pytest.raises(ReservationNotFoundError):
        hotel_system.cancel_reservation('RES-9999')

def test_get_occupancy(hotel_system):
    hotel_system.add_room(101, 'Single', 100.0)
    hotel_system.book_room(101, 'John', datetime.date.today() + datetime.timedelta(days=1), datetime.date.today() + datetime.timedelta(days=3))
    assert hotel_system.get_room_occupancy(datetime.date.today() + datetime.timedelta(days=2)) == [101]

@pytest.mark.parametrize('days_until_checkin, expected_refund_ratio', [
    (10, 1.0),  # > 7 days
    (5, 0.5),   # 2-7 days
    (1, 0.0)    # < 2 days
])
@freeze_time("2023-01-01")
def test_cancel_reservation(hotel_system, days_until_checkin, expected_refund_ratio):
    hotel_system.add_room(101, 'Single', 100.0)
    check_in_date = datetime.date.today() + datetime.timedelta(days=days_until_checkin)
    check_out_date = check_in_date + datetime.timedelta(days=2)
    res_id = hotel_system.book_room(101, 'John', check_in_date, check_out_date)
    refund_amount = hotel_system.cancel_reservation(res_id)
    expected_refund = round(2 * 100.0 * expected_refund_ratio, 2)
    assert refund_amount == expected_refund