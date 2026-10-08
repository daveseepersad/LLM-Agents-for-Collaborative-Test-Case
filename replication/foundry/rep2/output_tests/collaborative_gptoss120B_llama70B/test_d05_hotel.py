import pytest
from data.input_code.d05_hotel import HotelReservationSystem, RoomNotFoundError, RoomUnavailableError, InvalidDateError, ReservationNotFoundError
from datetime import date, timedelta

@pytest.mark.parametrize('room_number, room_type, price_per_night', [
    (101, "Deluxe", 150.0)
])
def test_add_room_success(room_number, room_type, price_per_night):
    hotel = HotelReservationSystem()
    hotel.add_room(room_number, room_type, price_per_night)
    assert room_number in hotel.rooms

def test_add_room_negative_price():
    hotel = HotelReservationSystem()
    with pytest.raises(ValueError):
        hotel.add_room(102, "Standard", -50.0)

@pytest.mark.parametrize('room_number, user_name, check_in, check_out', [
    (999, "Alice", date.today() + timedelta(days=1), date.today() + timedelta(days=3))
])
def test_book_room_room_not_found(room_number, user_name, check_in, check_out):
    hotel = HotelReservationSystem()
    with pytest.raises(RoomNotFoundError):
        hotel.book_room(room_number, user_name, check_in, check_out)

@pytest.mark.parametrize('room_number, user_name, check_in, check_out', [
    (101, "Bob", date.today() + timedelta(days=3), date.today() + timedelta(days=1))
])
def test_book_room_invalid_date_check_in_after_check_out(room_number, user_name, check_in, check_out):
    hotel = HotelReservationSystem()
    hotel.add_room(room_number, "Deluxe", 150.0)
    with pytest.raises(InvalidDateError):
        hotel.book_room(room_number, user_name, check_in, check_out)

@pytest.mark.parametrize('room_number, user_name, check_in, check_out', [
    (101, "Carol", date.today() - timedelta(days=1), date.today() + timedelta(days=1))
])
def test_book_room_invalid_date_past_check_in(room_number, user_name, check_in, check_out):
    hotel = HotelReservationSystem()
    hotel.add_room(room_number, "Deluxe", 150.0)
    with pytest.raises(InvalidDateError):
        hotel.book_room(room_number, user_name, check_in, check_out)

def test_book_room_unavailable():
    hotel = HotelReservationSystem()
    hotel.add_room(103, "Suite", 200.0)
    hotel.book_room(103, "Dave", date.today() + timedelta(days=1), date.today() + timedelta(days=3))
    with pytest.raises(RoomUnavailableError):
        hotel.book_room(103, "Eve", date.today() + timedelta(days=2), date.today() + timedelta(days=4))

def test_book_room_success():
    hotel = HotelReservationSystem()
    hotel.add_room(104, "Standard", 100.0)
    assert hotel.book_room(104, "Frank", date.today() + timedelta(days=1), date.today() + timedelta(days=3)) is not None

def test_cancel_reservation_not_found():
    hotel = HotelReservationSystem()
    with pytest.raises(ReservationNotFoundError):
        hotel.cancel_reservation("NONEXISTENT")

def test_cancel_reservation_full_refund():
    hotel = HotelReservationSystem()
    hotel.add_room(105, "Deluxe", 120.0)
    res_id = hotel.book_room(105, "Grace", date.today() + timedelta(days=10), date.today() + timedelta(days=13))
    assert hotel.cancel_reservation(res_id) == 360.0

def test_cancel_reservation_half_refund():
    hotel = HotelReservationSystem()
    hotel.add_room(106, "Standard", 80.0)
    res_id = hotel.book_room(106, "Heidi", date.today() + timedelta(days=3), date.today() + timedelta(days=5))
    assert hotel.cancel_reservation(res_id) == 80.0

def test_cancel_reservation_no_refund():
    hotel = HotelReservationSystem()
    hotel.add_room(107, "Suite", 200.0)
    res_id = hotel.book_room(107, "Ivan", date.today() + timedelta(days=1), date.today() + timedelta(days=3))
    assert hotel.cancel_reservation(res_id) == 0.0

def test_get_room_occupancy_none():
    hotel = HotelReservationSystem()
    hotel.add_room(108, "Standard", 90.0)
    assert hotel.get_room_occupancy(date.today()) == []

def test_get_room_occupancy_some():
    hotel = HotelReservationSystem()
    hotel.add_room(109, "Deluxe", 150.0)
    hotel.book_room(109, "Judy", date.today() + timedelta(days=1), date.today() + timedelta(days=3))
    assert hotel.get_room_occupancy(date.today() + timedelta(days=2)) == [109]