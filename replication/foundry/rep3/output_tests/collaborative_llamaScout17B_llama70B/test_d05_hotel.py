import pytest
from data.input_code.d05_hotel import *
from datetime import date, timedelta

@pytest.fixture
def hotel_system():
    return HotelReservationSystem()

def test_init(hotel_system):
    assert hotel_system.rooms == {}
    assert hotel_system.reservations == {}
    assert hotel_system._reservation_counter == 0

@pytest.mark.parametrize('room_number, room_type, price_per_night', [
    (101, 'Single', 100.0)
])
def test_add_room_valid(hotel_system, room_number, room_type, price_per_night):
    hotel_system.add_room(room_number, room_type, price_per_night)
    assert hotel_system.rooms[room_number] == {'type': room_type, 'price_per_night': price_per_night}

def test_add_room_invalid_price(hotel_system):
    with pytest.raises(ValueError):
        hotel_system.add_room(102, 'Double', 0.0)

@pytest.mark.parametrize('room_number, user_name, check_in, check_out', [
    (103, 'John', date.today() + timedelta(days=1), date.today() + timedelta(days=3))
])
def test_book_room_nonexistent(hotel_system, room_number, user_name, check_in, check_out):
    with pytest.raises(RoomNotFoundError):
        hotel_system.book_room(room_number, user_name, check_in, check_out)

@pytest.mark.parametrize('room_number, user_name, check_in, check_out', [
    (101, 'John', date.today() + timedelta(days=3), date.today() + timedelta(days=1))
])
def test_book_room_invalid_dates(hotel_system, room_number, user_name, check_in, check_out):
    hotel_system.add_room(room_number, 'Single', 100.0)
    with pytest.raises(InvalidDateError):
        hotel_system.book_room(room_number, user_name, check_in, check_out)

@pytest.mark.parametrize('room_number, user_name, check_in, check_out', [
    (101, 'John', date.today() - timedelta(days=1), date.today() + timedelta(days=1))
])
def test_book_room_past(hotel_system, room_number, user_name, check_in, check_out):
    hotel_system.add_room(room_number, 'Single', 100.0)
    with pytest.raises(InvalidDateError):
        hotel_system.book_room(room_number, user_name, check_in, check_out)

def test_book_room_success(hotel_system):
    hotel_system.add_room(101, 'Single', 100.0)
    res_id = hotel_system.book_room(101, 'John', date.today() + timedelta(days=1), date.today() + timedelta(days=3))
    assert res_id == 'RES-0001'

def test_book_room_unavailable(hotel_system):
    hotel_system.add_room(101, 'Single', 100.0)
    hotel_system.book_room(101, 'John', date.today() + timedelta(days=1), date.today() + timedelta(days=3))
    with pytest.raises(RoomUnavailableError):
        hotel_system.book_room(101, 'Jane', date.today() + timedelta(days=1), date.today() + timedelta(days=3))

def test_cancel_nonexistent(hotel_system):
    with pytest.raises(ReservationNotFoundError):
        hotel_system.cancel_reservation('RES-9999')

def test_cancel_full_refund(hotel_system):
    hotel_system.add_room(101, 'Single', 100.0)
    res_id = hotel_system.book_room(101, 'John', date.today() + timedelta(days=10), date.today() + timedelta(days=12))
    refund = hotel_system.cancel_reservation(res_id)
    assert refund == 200.0

def test_get_occupancy(hotel_system):
    hotel_system.add_room(101, 'Single', 100.0)
    hotel_system.book_room(101, 'John', date.today() + timedelta(days=1), date.today() + timedelta(days=3))
    occupied_rooms = hotel_system.get_room_occupancy(date.today() + timedelta(days=2))
    assert occupied_rooms == [101]

def test_cancel_partial_refund(hotel_system):
    hotel_system.add_room(101, 'Single', 100.0)
    res_id = hotel_system.book_room(101, 'John', date.today() + timedelta(days=5), date.today() + timedelta(days=7))
    refund = hotel_system.cancel_reservation(res_id)
    assert refund == 100.0

def test_cancel_no_refund(hotel_system):
    hotel_system.add_room(101, 'Single', 100.0)
    res_id = hotel_system.book_room(101, 'John', date.today() + timedelta(days=1), date.today() + timedelta(days=3))
    refund = hotel_system.cancel_reservation(res_id)
    assert refund == 0.0