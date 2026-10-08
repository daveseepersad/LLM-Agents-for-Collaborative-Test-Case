import pytest
from data.input_code.d05_hotel import HotelReservationSystem, RoomNotFoundError, RoomUnavailableError, InvalidDateError, ReservationNotFoundError
from datetime import date, timedelta

@pytest.fixture
def hotel_system():
    return HotelReservationSystem()

def test_add_room_valid_price(hotel_system):
    hotel_system.add_room(1, "single", 100.0)
    assert 1 in hotel_system.rooms

def test_add_room_invalid_price(hotel_system):
    with pytest.raises(ValueError):
        hotel_system.add_room(1, "single", 0.0)

def test_book_room_valid_dates(hotel_system):
    hotel_system.add_room(1, "single", 100.0)
    reservation_id = hotel_system.book_room(1, "John Doe", date.today() + timedelta(days=1), date.today() + timedelta(days=5))
    assert reservation_id in hotel_system.reservations

def test_book_room_non_existent_room(hotel_system):
    with pytest.raises(RoomNotFoundError):
        hotel_system.book_room(1, "John Doe", date.today() + timedelta(days=1), date.today() + timedelta(days=5))

def test_book_room_invalid_dates(hotel_system):
    hotel_system.add_room(1, "single", 100.0)
    with pytest.raises(InvalidDateError):
        hotel_system.book_room(1, "John Doe", date.today() + timedelta(days=5), date.today() + timedelta(days=1))

def test_book_room_occupied_room(hotel_system):
    hotel_system.add_room(1, "single", 100.0)
    hotel_system.book_room(1, "John Doe", date.today() + timedelta(days=1), date.today() + timedelta(days=5))
    with pytest.raises(RoomUnavailableError):
        hotel_system.book_room(1, "John Doe", date.today() + timedelta(days=1), date.today() + timedelta(days=5))

def test_book_room_in_the_past(hotel_system):
    hotel_system.add_room(1, "single", 100.0)
    with pytest.raises(InvalidDateError):
        hotel_system.book_room(1, "John Doe", date.today() - timedelta(days=1), date.today() + timedelta(days=5))

@pytest.mark.parametrize("days_until_checkin, expected_refund", [
    (10, 400.0),
    (5, 200.0),
    (1, 0.0)
])
def test_cancel_reservation(hotel_system, days_until_checkin, expected_refund):
    hotel_system.add_room(1, "single", 100.0)
    reservation_id = hotel_system.book_room(1, "John Doe", date.today() + timedelta(days=days_until_checkin), date.today() + timedelta(days=days_until_checkin + 4))
    refund = hotel_system.cancel_reservation(reservation_id)
    assert refund == expected_refund

def test_cancel_non_existent_reservation(hotel_system):
    with pytest.raises(ReservationNotFoundError):
        hotel_system.cancel_reservation("RES-0001")

def test_get_room_occupancy(hotel_system):
    hotel_system.add_room(1, "single", 100.0)
    hotel_system.book_room(1, "John Doe", date.today(), date.today() + timedelta(days=5))
    occupied_rooms = hotel_system.get_room_occupancy(date.today())
    assert occupied_rooms == [1]

def test_get_room_occupancy_no_reservations(hotel_system):
    occupied_rooms = hotel_system.get_room_occupancy(date.today())
    assert occupied_rooms == []