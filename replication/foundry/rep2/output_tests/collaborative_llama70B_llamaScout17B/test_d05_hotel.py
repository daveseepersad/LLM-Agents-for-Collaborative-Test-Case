import pytest
from data.input_code.d05_hotel import *
from datetime import date, timedelta

@pytest.fixture
def hotel_system():
    return HotelReservationSystem()

def test_add_room_success(hotel_system):
    hotel_system.add_room(1, 'single', 100.0)
    assert 1 in hotel_system.rooms

def test_add_room_error(hotel_system):
    with pytest.raises(ValueError):
        hotel_system.add_room(1, 'single', 0.0)

@pytest.mark.parametrize('room_number, user_name, check_in, check_out, expected', [
    (1, 'John Doe', date.today() + timedelta(days=10), date.today() + timedelta(days=15), 'RES-0001')
])
def test_book_room_success(hotel_system, room_number, user_name, check_in, check_out, expected):
    hotel_system.add_room(room_number, 'single', 100.0)
    assert hotel_system.book_room(room_number, user_name, check_in, check_out) == expected

@pytest.mark.parametrize('room_number, user_name, check_in, check_out, expected_exception', [
    (2, 'John Doe', date.today() + timedelta(days=10), date.today() + timedelta(days=15), RoomNotFoundError),
    (1, 'John Doe', date.today() + timedelta(days=15), date.today() + timedelta(days=10), InvalidDateError),
    (1, 'John Doe', date(2022, 9, 20), date(2022, 9, 25), InvalidDateError)
])
def test_book_room_error(hotel_system, room_number, user_name, check_in, check_out, expected_exception):
    hotel_system.add_room(1, 'single', 100.0)
    with pytest.raises(expected_exception):
        hotel_system.book_room(room_number, user_name, check_in, check_out)

def test_book_room_unavailable(hotel_system):
    hotel_system.add_room(1, 'single', 100.0)
    hotel_system.book_room(1, 'John Doe', date.today() + timedelta(days=10), date.today() + timedelta(days=15))
    with pytest.raises(RoomUnavailableError):
        hotel_system.book_room(1, 'Jane Doe', date.today() + timedelta(days=10), date.today() + timedelta(days=15))

def test_cancel_reservation_success(hotel_system):
    hotel_system.add_room(1, 'single', 100.0)
    res_id = hotel_system.book_room(1, 'John Doe', date.today() + timedelta(days=10), date.today() + timedelta(days=15))
    assert hotel_system.cancel_reservation(res_id) == 500.0

def test_cancel_reservation_not_found(hotel_system):
    with pytest.raises(ReservationNotFoundError):
        hotel_system.cancel_reservation('RES-0001')

def test_get_room_occupancy(hotel_system):
    hotel_system.add_room(1, 'single', 100.0)
    hotel_system.book_room(1, 'John Doe', date.today() + timedelta(days=10), date.today() + timedelta(days=15))
    assert hotel_system.get_room_occupancy(date.today() + timedelta(days=12)) == [1]

def test_is_room_available(hotel_system):
    hotel_system.add_room(1, 'single', 100.0)
    assert hotel_system._is_room_available(1, date.today() + timedelta(days=10), date.today() + timedelta(days=15)) == True
    hotel_system.book_room(1, 'John Doe', date.today() + timedelta(days=10), date.today() + timedelta(days=15))
    assert hotel_system._is_room_available(1, date.today() + timedelta(days=10), date.today() + timedelta(days=15)) == False

@pytest.mark.parametrize('days_before_checkin, expected_refund', [
    (8, 500.0),
    (5, 250.0),
    (1, 0.0)
])
def test_cancel_reservation_refund_policy(hotel_system, days_before_checkin, expected_refund):
    hotel_system.add_room(1, 'single', 100.0)
    check_in = date.today() + timedelta(days=days_before_checkin)
    check_out = check_in + timedelta(days=5)
    res_id = hotel_system.book_room(1, 'John Doe', check_in, check_out)
    assert hotel_system.cancel_reservation(res_id) == expected_refund

def test_get_room_occupancy_empty(hotel_system):
    assert hotel_system.get_room_occupancy(date(2024, 9, 16)) == []

def test_book_room_overlapping_dates(hotel_system):
    hotel_system.add_room(1, 'single', 100.0)
    hotel_system.book_room(1, 'John Doe', date.today() + timedelta(days=20), date.today() + timedelta(days=25))
    with pytest.raises(RoomUnavailableError):
        hotel_system.book_room(1, 'Jane Doe', date.today() + timedelta(days=22), date.today() + timedelta(days=27))

def test_is_room_available_edge_case(hotel_system):
    hotel_system.add_room(1, 'single', 100.0)
    assert hotel_system._is_room_available(1, date(2024, 9, 20), date(2024, 9, 20)) == True