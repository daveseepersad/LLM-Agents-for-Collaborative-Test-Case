import pytest
from data.input_code.d05_hotel import HotelReservationSystem, RoomNotFoundError, RoomUnavailableError, InvalidDateError, ReservationNotFoundError
from datetime import date, timedelta

@pytest.fixture
def hotel_system():
    return HotelReservationSystem()

def test_add_room_negative_price(hotel_system):
    with pytest.raises(ValueError):
        hotel_system.add_room(101, "Standard", -50)

def test_add_room_valid(hotel_system):
    hotel_system.add_room(101, "Standard", 100.0)
    assert hotel_system.rooms[101]['type'] == "Standard"
    assert hotel_system.rooms[101]['price_per_night'] == 100.0

def test_book_room_success(hotel_system):
    hotel_system.add_room(101, "Standard", 100.0)
    check_in = date(2026, 10, 20)
    check_out = date(2026, 10, 23)
    res_id = hotel_system.book_room(101, "Alice", check_in, check_out)
    assert res_id == "RES-0001"

def test_book_room_unavailable(hotel_system):
    hotel_system.add_room(101, "Standard", 100.0)
    check_in = date(2026, 10, 20)
    check_out = date(2026, 10, 23)
    hotel_system.book_room(101, "Alice", check_in, check_out)
    check_in = date(2026, 10, 21)
    check_out = date(2026, 10, 24)
    with pytest.raises(RoomUnavailableError):
        hotel_system.book_room(101, "Bob", check_in, check_out)

def test_cancel_reservation_success(hotel_system):
    hotel_system.add_room(101, "Standard", 100.0)
    check_in = date(2026, 10, 20)
    check_out = date(2026, 10, 23)
    res_id = hotel_system.book_room(101, "Alice", check_in, check_out)
    refund = hotel_system.cancel_reservation(res_id)
    assert refund == 300.0

def test_get_room_occupancy_date(hotel_system):
    hotel_system.add_room(101, "Standard", 100.0)
    check_in = date(2026, 10, 20)
    check_out = date(2026, 10, 23)
    hotel_system.book_room(101, "Alice", check_in, check_out)
    occupied_rooms = hotel_system.get_room_occupancy(date(2026, 10, 21))
    assert occupied_rooms == [101]

def test_cancel_reservation_not_found(hotel_system):
    with pytest.raises(ReservationNotFoundError):
        hotel_system.cancel_reservation("RES-9999")

def test_book_room_invalid_dates_equal(hotel_system):
    hotel_system.add_room(101, "Standard", 100.0)
    check_in = date(2026, 10, 25)
    check_out = date(2026, 10, 25)
    with pytest.raises(InvalidDateError):
        hotel_system.book_room(101, "Carol", check_in, check_out)

def test_book_room_past_date(hotel_system):
    hotel_system.add_room(101, "Standard", 100.0)
    check_in = date(2020, 1, 1)
    check_out = date(2020, 1, 4)
    with pytest.raises(InvalidDateError):
        hotel_system.book_room(101, "Dave", check_in, check_out)

def test_get_room_occupancy_empty(hotel_system):
    occupied_rooms = hotel_system.get_room_occupancy(date(2026, 11, 1))
    assert occupied_rooms == []

def test_book_room_non_existent_room(hotel_system):
    with pytest.raises(RoomNotFoundError):
        hotel_system.book_room(999, "Test", date(2026, 11, 10), date(2026, 11, 12))

def test_add_room_zero_price(hotel_system):
    with pytest.raises(ValueError):
        hotel_system.add_room(102, "Standard", 0)

def test_book_room_today(hotel_system):
    hotel_system.add_room(101, "Standard", 100.0)
    check_in = date.today()
    check_out = check_in + timedelta(days=1)
    res_id = hotel_system.book_room(101, "Zoe", check_in, check_out)
    assert res_id == "RES-0001"

def test_cancel_reservation_50_percent_refund(hotel_system):
    hotel_system.add_room(101, "Standard", 100.0)
    check_in = date.today() + timedelta(days=3)
    check_out = check_in + timedelta(days=3)
    res_id = hotel_system.book_room(101, "Alice", check_in, check_out)
    refund = hotel_system.cancel_reservation(res_id)
    assert refund == 150.0

def test_cancel_reservation_0_percent_refund(hotel_system):
    hotel_system.add_room(101, "Standard", 100.0)
    check_in = date.today() + timedelta(days=1)
    check_out = check_in + timedelta(days=3)
    res_id = hotel_system.book_room(101, "Bob", check_in, check_out)
    refund = hotel_system.cancel_reservation(res_id)
    assert refund == 0.0