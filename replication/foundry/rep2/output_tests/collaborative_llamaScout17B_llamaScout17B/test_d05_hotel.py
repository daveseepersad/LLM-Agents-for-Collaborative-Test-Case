import pytest
from data.input_code.d05_hotel import *
import datetime

@pytest.fixture
def hotel_system():
    return HotelReservationSystem()

def test_init(hotel_system):
    assert hotel_system.rooms == {}
    assert hotel_system.reservations == {}

@pytest.mark.parametrize('price_per_night, expected', [
    (0.0, 'ValueError'),
    (-50.0, 'ValueError')
])
def test_add_room_invalid_price(hotel_system, price_per_night, expected):
    if expected == 'ValueError':
        with pytest.raises(ValueError):
            hotel_system.add_room(102, "Double", price_per_night)
    else:
        hotel_system.add_room(102, "Double", price_per_night)
        assert hotel_system.rooms[102]['price_per_night'] == price_per_night

def test_add_room_valid(hotel_system):
    hotel_system.add_room(101, "Single", 100.0)
    assert hotel_system.rooms[101]['price_per_night'] == 100.0

def test_book_room_nonexistent(hotel_system):
    with pytest.raises(RoomNotFoundError):
        hotel_system.book_room(999, "John", datetime.date.today() + datetime.timedelta(days=1), datetime.date.today() + datetime.timedelta(days=3))

@pytest.mark.parametrize('check_in, check_out, expected', [
    (datetime.date.today() + datetime.timedelta(days=3), datetime.date.today() + datetime.timedelta(days=1), 'InvalidDateError'),
    (datetime.date.today() - datetime.timedelta(days=1), datetime.date.today() + datetime.timedelta(days=1), 'InvalidDateError')
])
def test_book_room_invalid_dates(hotel_system, check_in, check_out, expected):
    hotel_system.add_room(101, "Single", 100.0)
    if expected == 'InvalidDateError':
        with pytest.raises(InvalidDateError):
            hotel_system.book_room(101, "John", check_in, check_out)

def test_book_room_success(hotel_system):
    hotel_system.add_room(101, "Single", 100.0)
    res_id = hotel_system.book_room(101, "John", datetime.date.today() + datetime.timedelta(days=1), datetime.date.today() + datetime.timedelta(days=3))
    assert res_id == "RES-0001"

def test_book_room_unavailable(hotel_system):
    hotel_system.add_room(101, "Single", 100.0)
    hotel_system.book_room(101, "John", datetime.date.today() + datetime.timedelta(days=1), datetime.date.today() + datetime.timedelta(days=3))
    with pytest.raises(RoomUnavailableError):
        hotel_system.book_room(101, "Jane", datetime.date.today() + datetime.timedelta(days=1), datetime.date.today() + datetime.timedelta(days=3))

def test_cancel_nonexistent(hotel_system):
    with pytest.raises(ReservationNotFoundError):
        hotel_system.cancel_reservation("RES-9999")

def test_get_occupancy(hotel_system):
    hotel_system.add_room(101, "Single", 100.0)
    hotel_system.book_room(101, "John", datetime.date.today() + datetime.timedelta(days=1), datetime.date.today() + datetime.timedelta(days=3))
    assert hotel_system.get_room_occupancy(datetime.date.today() + datetime.timedelta(days=2)) == [101]

# Additional tests for T11, T13, T14 are needed with proper setup

import pytest
from data.input_code.d05_hotel import *
import datetime

@pytest.fixture
def hotel_system():
    return HotelReservationSystem()

def test_cancel_full_refund(hotel_system):
    hotel_system.add_room(101, "Single", 100.0)
    check_in = datetime.date.today() + datetime.timedelta(days=8)
    hotel_system.book_room(101, "John", check_in, check_in + datetime.timedelta(days=2))
    assert hotel_system.cancel_reservation("RES-0001") == 200.0

def test_cancel_partial_refund(hotel_system):
    hotel_system.add_room(101, "Single", 100.0)
    check_in = datetime.date.today() + datetime.timedelta(days=5)
    hotel_system.book_room(101, "John", check_in, check_in + datetime.timedelta(days=2))
    assert hotel_system.cancel_reservation("RES-0001") == 100.0

def test_cancel_no_refund(hotel_system):
    hotel_system.add_room(101, "Single", 100.0)
    check_in = datetime.date.today() + datetime.timedelta(days=1)
    hotel_system.book_room(101, "John", check_in, check_in + datetime.timedelta(days=2))
    assert hotel_system.cancel_reservation("RES-0001") == 0.0

def test_get_occupancy_multiple_rooms(hotel_system):
    hotel_system.add_room(101, "Single", 100.0)
    hotel_system.add_room(102, "Double", 200.0)
    check_in = datetime.date.today() + datetime.timedelta(days=1)
    hotel_system.book_room(101, "John", check_in, check_in + datetime.timedelta(days=3))
    hotel_system.book_room(102, "Jane", check_in, check_in + datetime.timedelta(days=3))
    assert hotel_system.get_room_occupancy(check_in + datetime.timedelta(days=2)) == [101, 102]

def test_get_occupancy_no_rooms(hotel_system):
    assert hotel_system.get_room_occupancy(datetime.date.today() + datetime.timedelta(days=2)) == []

def test_book_room_overlap(hotel_system):
    hotel_system.add_room(101, "Single", 100.0)
    hotel_system.book_room(101, "John", datetime.date.today() + datetime.timedelta(days=1), datetime.date.today() + datetime.timedelta(days=3))
    with pytest.raises(RoomUnavailableError):
        hotel_system.book_room(101, "Jane", datetime.date.today() + datetime.timedelta(days=2), datetime.date.today() + datetime.timedelta(days=4))

def test_add_room_overwrite(hotel_system):
    hotel_system.add_room(101, "Single", 100.0)
    hotel_system.add_room(101, "Double", 150.0)
    assert hotel_system.rooms[101]['price_per_night'] == 150.0
    assert hotel_system.rooms[101]['type'] == "Double"