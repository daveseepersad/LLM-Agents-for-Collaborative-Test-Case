import pytest
from data.input_code.d05_hotel import HotelReservationSystem, RoomNotFoundError, RoomUnavailableError, InvalidDateError, ReservationNotFoundError
from datetime import date, timedelta

@pytest.fixture
def hotel_system():
    return HotelReservationSystem()

def test_add_room_normal_path(hotel_system):
    hotel_system.add_room(101, "Deluxe", 150.0)
    assert 101 in hotel_system.rooms

def test_add_room_non_positive_price(hotel_system):
    with pytest.raises(ValueError):
        hotel_system.add_room(102, "Standard", 0.0)

def test_book_room_success(hotel_system):
    hotel_system.add_room(101, "Deluxe", 150.0)
    res_id = hotel_system.book_room(101, "Alice", date.today() + timedelta(days=10), date.today() + timedelta(days=15))
    assert res_id == "RES-0001"

def test_book_room_room_not_found(hotel_system):
    with pytest.raises(RoomNotFoundError):
        hotel_system.book_room(999, "Bob", date.today() + timedelta(days=10), date.today() + timedelta(days=15))

def test_book_room_invalid_date(hotel_system):
    hotel_system.add_room(101, "Deluxe", 150.0)
    with pytest.raises(InvalidDateError):
        hotel_system.book_room(101, "Carol", date.today() + timedelta(days=10), date.today() + timedelta(days=10))

def test_book_room_past_date(hotel_system):
    hotel_system.add_room(101, "Deluxe", 150.0)
    with pytest.raises(InvalidDateError):
        hotel_system.book_room(101, "Dave", date.today() - timedelta(days=10), date.today() + timedelta(days=5))

def test_book_room_room_unavailable(hotel_system):
    hotel_system.add_room(101, "Deluxe", 150.0)
    hotel_system.book_room(101, "Alice", date.today() + timedelta(days=10), date.today() + timedelta(days=15))
    with pytest.raises(RoomUnavailableError):
        hotel_system.book_room(101, "Eve", date.today() + timedelta(days=12), date.today() + timedelta(days=14))

def test_cancel_reservation_non_existent(hotel_system):
    with pytest.raises(ReservationNotFoundError):
        hotel_system.cancel_reservation("NONEXISTENT")

def test_cancel_reservation_full_refund(hotel_system):
    hotel_system.add_room(202, "Suite", 150.0)
    res_id = hotel_system.book_room(202, "Frank", date.today() + timedelta(days=20), date.today() + timedelta(days=25))
    refund = hotel_system.cancel_reservation(res_id)
    assert refund == 150.0 * 5

def test_cancel_reservation_half_refund(hotel_system):
    hotel_system.add_room(303, "Deluxe", 150.0)
    res_id = hotel_system.book_room(303, "Grace", date.today() + timedelta(days=5), date.today() + timedelta(days=8))
    refund = hotel_system.cancel_reservation(res_id)
    assert refund == 150.0 * 3 * 0.5

def test_cancel_reservation_no_refund(hotel_system):
    hotel_system.add_room(404, "Standard", 100.0)
    res_id = hotel_system.book_room(404, "Heidi", date.today() + timedelta(days=1), date.today() + timedelta(days=3))
    refund = hotel_system.cancel_reservation(res_id)
    assert refund == 0.0

def test_get_room_occupancy_occupied(hotel_system):
    hotel_system.add_room(101, "Deluxe", 150.0)
    hotel_system.book_room(101, "Ivan", date.today() + timedelta(days=10), date.today() + timedelta(days=15))
    occupied_rooms = hotel_system.get_room_occupancy(date.today() + timedelta(days=12))
    assert occupied_rooms == [101]

def test_get_room_occupancy_not_occupied(hotel_system):
    hotel_system.add_room(101, "Deluxe", 150.0)
    occupied_rooms = hotel_system.get_room_occupancy(date.today() + timedelta(days=10))
    assert occupied_rooms == []