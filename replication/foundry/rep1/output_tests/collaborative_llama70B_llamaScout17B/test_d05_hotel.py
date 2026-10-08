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
        hotel_system.add_room(1, 'single', -100.0)

@pytest.mark.parametrize('room_number, user_name, check_in, check_out, expected', [
    (1, 'John Doe', date.today() + timedelta(days=1), date.today() + timedelta(days=6), 'RES-0001')
])
def test_book_room_success(hotel_system, room_number, user_name, check_in, check_out, expected):
    hotel_system.add_room(room_number, 'single', 100.0)
    assert hotel_system.book_room(room_number, user_name, check_in, check_out) == expected

@pytest.mark.parametrize('room_number, user_name, check_in, check_out, expected_exception', [
    (2, 'John Doe', date.today() + timedelta(days=1), date.today() + timedelta(days=6), RoomNotFoundError),
    (1, 'John Doe', date.today() + timedelta(days=6), date.today() + timedelta(days=1), InvalidDateError),
    (1, 'Jane Doe', date.today() + timedelta(days=1), date.today() + timedelta(days=6), RoomUnavailableError)
])
def test_book_room_error(hotel_system, room_number, user_name, check_in, check_out, expected_exception):
    hotel_system.add_room(1, 'single', 100.0)
    hotel_system.book_room(1, 'John Doe', date.today() + timedelta(days=1), date.today() + timedelta(days=6))
    with pytest.raises(expected_exception):
        hotel_system.book_room(room_number, user_name, check_in, check_out)

@pytest.mark.parametrize('reservation_id, expected', [
    ('RES-0001', 500.0)
])
def test_cancel_reservation_success(hotel_system, reservation_id, expected):
    hotel_system.add_room(1, 'single', 100.0)
    res_id = hotel_system.book_room(1, 'John Doe', date.today() + timedelta(days=10), date.today() + timedelta(days=15))
    assert hotel_system.cancel_reservation(res_id) == expected

def test_cancel_reservation_error(hotel_system):
    with pytest.raises(ReservationNotFoundError):
        hotel_system.cancel_reservation('RES-0002')

def test_get_room_occupancy(hotel_system):
    hotel_system.add_room(1, 'single', 100.0)
    hotel_system.book_room(1, 'John Doe', date.today() + timedelta(days=1), date.today() + timedelta(days=6))
    assert hotel_system.get_room_occupancy(date.today() + timedelta(days=3)) == [1]

@pytest.mark.parametrize('room_number, check_in, check_out, expected', [
    (1, date.today() + timedelta(days=1), date.today() + timedelta(days=6), True),
    (1, date.today() + timedelta(days=1), date.today() + timedelta(days=6), False)
])
def test_is_room_available(hotel_system, room_number, check_in, check_out, expected):
    hotel_system.add_room(1, 'single', 100.0)
    if not expected:
        hotel_system.book_room(1, 'John Doe', check_in, check_out)
    assert hotel_system._is_room_available(room_number, check_in, check_out) == expected

@pytest.mark.parametrize('room_number, user_name, check_in, check_out, expected_exception', [
    (1, 'John Doe', date(2022, 1, 1), date(2022, 1, 6), InvalidDateError)
])
def test_book_room_checkin_past(hotel_system, room_number, user_name, check_in, check_out, expected_exception):
    hotel_system.add_room(room_number, 'single', 100.0)
    with pytest.raises(expected_exception):
        hotel_system.book_room(room_number, user_name, check_in, check_out)

@pytest.mark.parametrize('room_number, user_name, check_in, check_out, expected_exception', [
    (1, 'John Doe', date(2024, 9, 20), date(2024, 9, 19), InvalidDateError)
])
def test_book_room_checkout_before_checkin(hotel_system, room_number, user_name, check_in, check_out, expected_exception):
    hotel_system.add_room(room_number, 'single', 100.0)
    with pytest.raises(expected_exception):
        hotel_system.book_room(room_number, user_name, check_in, check_out)

@pytest.mark.parametrize('check_in, check_out, expected', [
    (date.today() + timedelta(days=5), date.today() + timedelta(days=10), 250.0)
])
def test_cancel_reservation_50_percent_refund(hotel_system, check_in, check_out, expected):
    hotel_system.add_room(1, 'single', 100.0)
    res_id = hotel_system.book_room(1, 'John Doe', check_in, check_out)
    assert hotel_system.cancel_reservation(res_id) == expected

@pytest.mark.parametrize('check_in, check_out, expected', [
    (date.today() + timedelta(days=1), date.today() + timedelta(days=2), 0.0)
])
def test_cancel_reservation_0_percent_refund(hotel_system, check_in, check_out, expected):
    hotel_system.add_room(1, 'single', 100.0)
    res_id = hotel_system.book_room(1, 'John Doe', check_in, check_out)
    assert hotel_system.cancel_reservation(res_id) == expected

def test_get_room_occupancy_no_reservations(hotel_system):
    assert hotel_system.get_room_occupancy(date(2024, 9, 20)) == []

def test_get_room_occupancy_multiple_reservations(hotel_system):
    hotel_system.add_room(1, 'single', 100.0)
    hotel_system.add_room(2, 'double', 200.0)
    future_date = date.today() + timedelta(days=10)
    hotel_system.book_room(1, 'John Doe', future_date, future_date + timedelta(days=3))
    hotel_system.book_room(2, 'Jane Doe', future_date, future_date + timedelta(days=3))
    assert hotel_system.get_room_occupancy(future_date + timedelta(days=1)) == [1, 2]

@pytest.mark.parametrize('room_number, room_type, price_per_night, expected_exception', [
    (1, 'single', 0.0, ValueError)
])
def test_add_room_price_zero(hotel_system, room_number, room_type, price_per_night, expected_exception):
    with pytest.raises(expected_exception):
        hotel_system.add_room(room_number, room_type, price_per_night)