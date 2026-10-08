import pytest
from data.input_code.d05_hotel import HotelReservationSystem, RoomNotFoundError, RoomUnavailableError, InvalidDateError, ReservationNotFoundError
from datetime import date, timedelta

@pytest.fixture
def hotel_system():
    return HotelReservationSystem()

def test_add_room_success(hotel_system):
    hotel_system.add_room(1, "single", 100.0)
    assert 1 in hotel_system.rooms

def test_add_room_error(hotel_system):
    with pytest.raises(ValueError):
        hotel_system.add_room(1, "single", 0.0)

def test_book_room_success(hotel_system):
    hotel_system.add_room(1, "single", 100.0)
    today = date.today()
    res_id = hotel_system.book_room(1, "John", today + timedelta(days=1), today + timedelta(days=6))
    assert res_id in hotel_system.reservations

def test_book_room_room_not_found(hotel_system):
    with pytest.raises(RoomNotFoundError):
        hotel_system.book_room(1, "John", date.today() + timedelta(days=1), date.today() + timedelta(days=6))

def test_book_room_invalid_dates(hotel_system):
    hotel_system.add_room(1, "single", 100.0)
    with pytest.raises(InvalidDateError):
        hotel_system.book_room(1, "John", date.today() + timedelta(days=6), date.today() + timedelta(days=1))

def test_book_room_past_dates(hotel_system):
    hotel_system.add_room(1, "single", 100.0)
    with pytest.raises(InvalidDateError):
        hotel_system.book_room(1, "John", date.today() - timedelta(days=1), date.today() + timedelta(days=6))

def test_book_room_room_unavailable(hotel_system):
    hotel_system.add_room(1, "single", 100.0)
    hotel_system.book_room(1, "John", date.today() + timedelta(days=1), date.today() + timedelta(days=6))
    with pytest.raises(RoomUnavailableError):
        hotel_system.book_room(1, "John", date.today() + timedelta(days=1), date.today() + timedelta(days=6))

def test_cancel_reservation_success(hotel_system):
    hotel_system.add_room(1, "single", 100.0)
    res_id = hotel_system.book_room(1, "John", date.today() + timedelta(days=8), date.today() + timedelta(days=13))
    refund = hotel_system.cancel_reservation(res_id)
    assert refund > 0

def test_cancel_reservation_not_found(hotel_system):
    with pytest.raises(ReservationNotFoundError):
        hotel_system.cancel_reservation("RES-0001")

def test_cancel_reservation_partial_refund(hotel_system):
    hotel_system.add_room(1, "single", 100.0)
    res_id = hotel_system.book_room(1, "John", date.today() + timedelta(days=3), date.today() + timedelta(days=8))
    refund = hotel_system.cancel_reservation(res_id)
    assert refund > 0

def test_cancel_reservation_no_refund(hotel_system):
    hotel_system.add_room(1, "single", 100.0)
    res_id = hotel_system.book_room(1, "John", date.today() + timedelta(days=1), date.today() + timedelta(days=6))
    refund = hotel_system.cancel_reservation(res_id)
    assert refund == 0.0

def test_get_room_occupancy_success(hotel_system):
    hotel_system.add_room(1, "single", 100.0)
    hotel_system.book_room(1, "John", date.today() + timedelta(days=1), date.today() + timedelta(days=6))
    occupied_rooms = hotel_system.get_room_occupancy(date.today() + timedelta(days=3))
    assert 1 in occupied_rooms

def test_is_room_available_success(hotel_system):
    hotel_system.add_room(1, "single", 100.0)
    assert hotel_system._is_room_available(1, date.today() + timedelta(days=1), date.today() + timedelta(days=6))

def test_is_room_available_failure(hotel_system):
    hotel_system.add_room(1, "single", 100.0)
    hotel_system.book_room(1, "John", date.today() + timedelta(days=1), date.today() + timedelta(days=6))
    assert not hotel_system._is_room_available(1, date.today() + timedelta(days=1), date.today() + timedelta(days=6))