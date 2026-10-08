import pytest
from data.input_code.d05_hotel import *
from datetime import date, timedelta

@pytest.fixture
def hotel_system():
    return HotelReservationSystem()

def test_book_room_error_check_in_same_as_today(hotel_system):
    hotel_system.add_room(101, "single", 100.0)
    # Since check-in date is today, it should NOT raise an InvalidDateError
    res_id = hotel_system.book_room(101, "John Doe", date.today(), date.today() + timedelta(days=5))
    assert res_id is not None

def test_book_room_error_check_in_before_today(hotel_system):
    hotel_system.add_room(101, "single", 100.0)
    # Since check-in date is before today, it should raise an InvalidDateError
    with pytest.raises(InvalidDateError):
        hotel_system.book_room(101, "John Doe", date.today() - timedelta(days=1), date.today() + timedelta(days=5))

def test_book_room_error_check_out_before_check_in(hotel_system):
    hotel_system.add_room(101, "single", 100.0)
    # Since check-out date is before check-in date, it should raise an InvalidDateError
    with pytest.raises(InvalidDateError):
        hotel_system.book_room(101, "John Doe", date.today() + timedelta(days=5), date.today())

def test_book_room_success(hotel_system):
    hotel_system.add_room(101, "single", 100.0)
    # Since check-in date is after today and check-out date is after check-in date, it should not raise an error
    res_id = hotel_system.book_room(101, "John Doe", date.today() + timedelta(days=1), date.today() + timedelta(days=5))
    assert res_id is not None

@pytest.mark.parametrize("room_number, user_name, check_in, check_out", [
    (101, "John Doe", date.today() + timedelta(days=1), date.today() + timedelta(days=5))
])
def test_book_room_error_room_not_found(hotel_system, room_number, user_name, check_in, check_out):
    with pytest.raises(RoomNotFoundError):
        hotel_system.book_room(room_number, user_name, check_in, check_out)

@pytest.mark.parametrize("room_number, user_name, check_in, check_out", [
    (101, "John Doe", date.today() + timedelta(days=1), date.today() + timedelta(days=5))
])
def test_book_room_error_room_unavailable(hotel_system, room_number, user_name, check_in, check_out):
    hotel_system.add_room(room_number, "single", 100.0)
    hotel_system.book_room(room_number, "Jane Doe", check_in, check_out)
    with pytest.raises(RoomUnavailableError):
        hotel_system.book_room(room_number, user_name, check_in, check_out)

@pytest.mark.parametrize("room_number, room_type, price_per_night", [
    (101, "single", -100.0)
])
def test_add_room_error_invalid_price(hotel_system, room_number, room_type, price_per_night):
    with pytest.raises(ValueError):
        hotel_system.add_room(room_number, room_type, price_per_night)

def test_cancel_reservation_error_reservation_not_found(hotel_system):
    with pytest.raises(ReservationNotFoundError):
        hotel_system.cancel_reservation("RES-0001")

@pytest.mark.parametrize("days_until_checkin, expected_refund", [
    (10, 500.0),
    (5, 250.0),
    (1, 0.0)
])
def test_cancel_reservation_refund(hotel_system, days_until_checkin, expected_refund):
    hotel_system.add_room(101, "single", 100.0)
    check_in = date.today() + timedelta(days=days_until_checkin)
    check_out = check_in + timedelta(days=5)
    res_id = hotel_system.book_room(101, "John Doe", check_in, check_out)
    refund = hotel_system.cancel_reservation(res_id)
    assert refund == expected_refund

def test_get_room_occupancy(hotel_system):
    hotel_system.add_room(101, "single", 100.0)
    check_in = date.today() + timedelta(days=1)
    check_out = check_in + timedelta(days=5)
    hotel_system.book_room(101, "John Doe", check_in, check_out)
    occupied_rooms = hotel_system.get_room_occupancy(check_in)
    assert occupied_rooms == [101]