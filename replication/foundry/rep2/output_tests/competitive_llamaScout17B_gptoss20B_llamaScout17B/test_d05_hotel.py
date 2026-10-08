import pytest
from data.input_code.d05_hotel import *
import datetime

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
        hotel_system.book_room(999, 'John', datetime.date.today() + datetime.timedelta(days=1), datetime.date.today() + datetime.timedelta(days=3))

@pytest.mark.parametrize('room_number, user_name, check_in, check_out, expected', [
    (101, 'John', datetime.date.today() + datetime.timedelta(days=3), datetime.date.today() + datetime.timedelta(days=1), 'InvalidDateError'),
    (101, 'John', datetime.date.today() - datetime.timedelta(days=1), datetime.date.today() + datetime.timedelta(days=1), 'InvalidDateError'),
    (101, 'John', datetime.date.today() + datetime.timedelta(days=1), datetime.date.today() + datetime.timedelta(days=3), 'RES-0001')
])
def test_book_room(hotel_system, room_number, user_name, check_in, check_out, expected):
    hotel_system.add_room(room_number, 'Single', 100.0)
    if expected.startswith('RES-'):
        res_id = hotel_system.book_room(room_number, user_name, check_in, check_out)
        assert res_id == expected
    else:
        with pytest.raises(eval(expected)):
            hotel_system.book_room(room_number, user_name, check_in, check_out)

def test_book_room_unavailable(hotel_system):
    hotel_system.add_room(101, 'Single', 100.0)
    hotel_system.book_room(101, 'John', datetime.date.today() + datetime.timedelta(days=1), datetime.date.today() + datetime.timedelta(days=3))
    with pytest.raises(RoomUnavailableError):
        hotel_system.book_room(101, 'Jane', datetime.date.today() + datetime.timedelta(days=2), datetime.date.today() + datetime.timedelta(days=4))

def test_cancel_non_existent(hotel_system):
    with pytest.raises(ReservationNotFoundError):
        hotel_system.cancel_reservation('RES-9999')

def test_get_occupancy(hotel_system):
    hotel_system.add_room(101, 'Single', 100.0)
    hotel_system.book_room(101, 'John', datetime.date.today() + datetime.timedelta(days=1), datetime.date.today() + datetime.timedelta(days=3))
    assert hotel_system.get_room_occupancy(datetime.date.today() + datetime.timedelta(days=2)) == [101]

def test_cancel_reservation_full_refund(hotel_system):
    hotel_system.add_room(101, 'Single', 100.0)
    res_id = hotel_system.book_room(101, 'John', datetime.date.today() + datetime.timedelta(days=10), datetime.date.today() + datetime.timedelta(days=13))
    assert hotel_system.cancel_reservation(res_id) == 300.0  # 3 nights * 100 = 300

def test_cancel_reservation_mid_refund(hotel_system):
    hotel_system.add_room(101, 'Single', 100.0)
    res_id = hotel_system.book_room(101, 'John', datetime.date.today() + datetime.timedelta(days=6), datetime.date.today() + datetime.timedelta(days=9))
    assert hotel_system.cancel_reservation(res_id) == 150.0  # 50% refund for 2-7 days before check-in

def test_cancel_reservation_no_refund(hotel_system):
    hotel_system.add_room(101, 'Single', 100.0)
    res_id = hotel_system.book_room(101, 'John', datetime.date.today() + datetime.timedelta(days=1), datetime.date.today() + datetime.timedelta(days=4))
    assert hotel_system.cancel_reservation(res_id) == 0.0  # < 2 days before check-in