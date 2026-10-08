import pytest
from datetime import date, timedelta
from data.input_code.d05_hotel import *

@pytest.fixture
def hotel_system():
    return HotelReservationSystem()

def test_add_room_success(hotel_system):
    hotel_system.add_room(101, 'single', 100.0)
    assert 101 in hotel_system.rooms

def test_add_room_invalid_price(hotel_system):
    with pytest.raises(ValueError):
        hotel_system.add_room(200, 'double', 0.0)

@pytest.mark.parametrize('room_number, user_name, check_in, check_out, expected', [
    (101, 'Alice', date.today() + timedelta(days=1), date.today() + timedelta(days=6), 'RES-0001')
])
def test_book_room_success(hotel_system, room_number, user_name, check_in, check_out, expected):
    hotel_system.add_room(101, 'single', 100.0)
    assert hotel_system.book_room(room_number, user_name, check_in, check_out) == expected

def test_get_room_occupancy(hotel_system):
    hotel_system.add_room(101, 'single', 100.0)
    future_date = date.today() + timedelta(days=10)
    hotel_system.book_room(101, 'Alice', future_date, future_date + timedelta(days=5))
    assert hotel_system.get_room_occupancy(future_date + timedelta(days=2)) == [101]

@pytest.mark.parametrize('room_number, user_name, check_in, check_out, expected', [
    (999, 'Bob', date.today() + timedelta(days=1), date.today() + timedelta(days=3), 'RoomNotFoundError'),
    (101, 'Carol', date.today() + timedelta(days=5), date.today() + timedelta(days=3), 'InvalidDateError'),
    (101, 'Dave', date.today() - timedelta(days=1), date.today() + timedelta(days=2), 'InvalidDateError'),
    (101, 'Eve', date.today() + timedelta(days=2), date.today() + timedelta(days=4), 'RoomUnavailableError')
])
def test_book_room_error(hotel_system, room_number, user_name, check_in, check_out, expected):
    hotel_system.add_room(101, 'single', 100.0)
    hotel_system.book_room(101, 'Alice', date.today() + timedelta(days=1), date.today() + timedelta(days=6))
    with pytest.raises(eval(expected)):
        hotel_system.book_room(room_number, user_name, check_in, check_out)

@pytest.mark.parametrize('reservation_id, expected_refund', [
    ('RES-0001', 500.0),
    ('RES-0002', 0.0),
    ('RES-0003', 0.0)
])
def test_cancel_reservation(hotel_system, reservation_id, expected_refund):
    hotel_system.add_room(101, 'single', 100.0)
    hotel_system.add_room(102, 'double', 200.0)
    hotel_system.add_room(103, 'suite', 300.0)
    res1_id = hotel_system.book_room(101, 'Alice', date.today() + timedelta(days=10), date.today() + timedelta(days=15))
    res2_id = hotel_system.book_room(102, 'Frank', date.today() + timedelta(days=1), date.today() + timedelta(days=4))
    res3_id = hotel_system.book_room(103, 'Grace', date.today() + timedelta(days=1), date.today() + timedelta(days=4))
    
    if reservation_id == 'RES-0001':
        assert hotel_system.cancel_reservation(res1_id) == expected_refund
    elif reservation_id == 'RES-0002':
        assert hotel_system.cancel_reservation(res2_id) == expected_refund
    elif reservation_id == 'RES-0003':
        assert hotel_system.cancel_reservation(res3_id) == expected_refund

def test_cancel_reservation_not_found(hotel_system):
    with pytest.raises(ReservationNotFoundError):
        hotel_system.cancel_reservation('RES-9999')