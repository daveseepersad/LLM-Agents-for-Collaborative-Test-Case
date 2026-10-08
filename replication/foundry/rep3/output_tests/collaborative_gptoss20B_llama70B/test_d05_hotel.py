import pytest
from data.input_code.d05_hotel import HotelReservationSystem, RoomNotFoundError, RoomUnavailableError, InvalidDateError, ReservationNotFoundError
from datetime import date, timedelta

@pytest.fixture
def hotel_system():
    return HotelReservationSystem()

def test_add_room(hotel_system):
    hotel_system.add_room(101, "Deluxe", 100.0)
    assert 101 in hotel_system.rooms

def test_add_room_invalid_price(hotel_system):
    with pytest.raises(ValueError):
        hotel_system.add_room(101, "Deluxe", -100.0)

def test_book_room_success(hotel_system):
    hotel_system.add_room(101, "Deluxe", 100.0)
    res_id = hotel_system.book_room(101, "Alice", date.today() + timedelta(days=1), date.today() + timedelta(days=3))
    assert res_id in hotel_system.reservations

def test_book_room_room_not_found(hotel_system):
    with pytest.raises(RoomNotFoundError):
        hotel_system.book_room(101, "Alice", date.today() + timedelta(days=1), date.today() + timedelta(days=3))

def test_book_room_invalid_dates(hotel_system):
    hotel_system.add_room(101, "Deluxe", 100.0)
    with pytest.raises(InvalidDateError):
        hotel_system.book_room(101, "Alice", date.today() + timedelta(days=3), date.today() + timedelta(days=1))

def test_book_room_room_unavailable(hotel_system):
    hotel_system.add_room(101, "Deluxe", 100.0)
    hotel_system.book_room(101, "Alice", date.today() + timedelta(days=1), date.today() + timedelta(days=3))
    with pytest.raises(RoomUnavailableError):
        hotel_system.book_room(101, "Bob", date.today() + timedelta(days=2), date.today() + timedelta(days=4))

def test_cancel_reservation_success(hotel_system):
    hotel_system.add_room(101, "Deluxe", 100.0)
    res_id = hotel_system.book_room(101, "Alice", date.today() + timedelta(days=10), date.today() + timedelta(days=12))
    refund = hotel_system.cancel_reservation(res_id)
    assert res_id not in hotel_system.reservations

def test_cancel_reservation_not_found(hotel_system):
    with pytest.raises(ReservationNotFoundError):
        hotel_system.cancel_reservation("RES-0001")

def test_get_room_occupancy(hotel_system):
    hotel_system.add_room(101, "Deluxe", 100.0)
    hotel_system.add_room(102, "Standard", 80.0)
    hotel_system.book_room(101, "Alice", date.today(), date.today() + timedelta(days=2))
    hotel_system.book_room(102, "Bob", date.today(), date.today() + timedelta(days=2))
    occupied_rooms = hotel_system.get_room_occupancy(date.today())
    assert occupied_rooms == [101, 102]

def test_get_room_occupancy_after_cancel(hotel_system):
    hotel_system.add_room(101, "Deluxe", 100.0)
    hotel_system.add_room(102, "Standard", 80.0)
    res_id1 = hotel_system.book_room(101, "Alice", date.today(), date.today() + timedelta(days=2))
    res_id2 = hotel_system.book_room(102, "Bob", date.today(), date.today() + timedelta(days=2))
    hotel_system.cancel_reservation(res_id1)
    occupied_rooms = hotel_system.get_room_occupancy(date.today())
    assert occupied_rooms == [102]