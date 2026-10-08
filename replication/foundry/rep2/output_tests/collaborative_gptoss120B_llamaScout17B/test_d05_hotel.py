import pytest
from datetime import date, timedelta
from data.input_code.d05_hotel import *

def parse_date(date_str):
    if date_str == "__TODAY_PLUS_1__":
        return date.today() + timedelta(days=1)
    elif date_str == "__TODAY_PLUS_2__":
        return date.today() + timedelta(days=2)
    elif date_str == "__TODAY_PLUS_3__":
        return date.today() + timedelta(days=3)
    elif date_str == "__TODAY_PLUS_4__":
        return date.today() + timedelta(days=4)
    elif date_str == "__TODAY_PLUS_5__":
        return date.today() + timedelta(days=5)
    elif date_str == "__TODAY_PLUS_6__":
        return date.today() + timedelta(days=6)
    elif date_str == "__TODAY_PLUS_10__":
        return date.today() + timedelta(days=10)
    elif date_str == "__TODAY_PLUS_12__":
        return date.today() + timedelta(days=12)
    elif date_str == "__TODAY_PLUS_20__":
        return date.today() + timedelta(days=20)
    elif date_str == "__TODAY_MINUS_1__":
        return date.today() - timedelta(days=1)
    else:
        return date.fromisoformat(date_str)

@pytest.fixture
def hotel_system():
    return HotelReservationSystem()

@pytest.mark.parametrize('room_number, room_type, price_per_night, expected', [
    (101, 'single', 100.0, None),
    (102, 'double', 0.0, 'ValueError')
])
def test_add_room(hotel_system, room_number, room_type, price_per_night, expected):
    if expected == 'ValueError':
        with pytest.raises(ValueError):
            hotel_system.add_room(room_number, room_type, price_per_night)
    else:
        hotel_system.add_room(room_number, room_type, price_per_night)
        assert room_number in hotel_system.rooms

@pytest.mark.parametrize('room_number, user_name, check_in, check_out, expected', [
    (101, 'Alice', '__TODAY_PLUS_1__', '__TODAY_PLUS_4__', 'RES-0001'),
    (999, 'Bob', '__TODAY_PLUS_1__', '__TODAY_PLUS_3__', 'RoomNotFoundError'),
    (101, 'Carol', '__TODAY_PLUS_5__', '__TODAY_PLUS_5__', 'InvalidDateError'),
    (101, 'Dave', '__TODAY_MINUS_1__', '__TODAY_PLUS_1__', 'InvalidDateError'),
    (101, 'Eve', '__TODAY_PLUS_2__', '__TODAY_PLUS_5__', 'RoomUnavailableError'),
    (102, 'Frank', '__TODAY_PLUS_10__', '__TODAY_PLUS_12__', 'RES-0002'),
    (102, 'Grace', '__TODAY_PLUS_5__', '__TODAY_PLUS_6__', 'RES-0003'),
    (101, 'Heidi', '__TODAY_PLUS_1__', '__TODAY_PLUS_2__', 'RoomUnavailableError')
])
def test_book_room(hotel_system, room_number, user_name, check_in, check_out, expected):
    hotel_system.add_room(101, 'single', 100.0)
    hotel_system.add_room(102, 'double', 150.0)
    
    check_in_date = parse_date(check_in)
    check_out_date = parse_date(check_out)
    
    if expected == 'RoomNotFoundError':
        with pytest.raises(RoomNotFoundError):
            hotel_system.book_room(room_number, user_name, check_in_date, check_out_date)
    elif expected == 'InvalidDateError':
        with pytest.raises(InvalidDateError):
            hotel_system.book_room(room_number, user_name, check_in_date, check_out_date)
    elif expected == 'RoomUnavailableError':
        hotel_system.book_room(101, 'Alice', parse_date('__TODAY_PLUS_1__'), parse_date('__TODAY_PLUS_4__'))
        with pytest.raises(RoomUnavailableError):
            hotel_system.book_room(room_number, user_name, check_in_date, check_out_date)
    else:
        res_id = hotel_system.book_room(room_number, user_name, check_in_date, check_out_date)
        assert res_id.startswith('RES-')  # Check if reservation ID is in correct format

@pytest.mark.parametrize('reservation_id, expected_refund', [
    ('RES-0001', 0.0),
    ('RES-0002', 300.0),
    ('RES-0003', 75.0),
    ('NON_EXISTENT', 'ReservationNotFoundError')
])
def test_cancel_reservation(hotel_system, reservation_id, expected_refund):
    hotel_system.add_room(101, 'single', 100.0)
    hotel_system.add_room(102, 'double', 150.0)
    hotel_system.book_room(101, 'Alice', parse_date('__TODAY_PLUS_1__'), parse_date('__TODAY_PLUS_4__'))
    hotel_system.book_room(102, 'Frank', parse_date('__TODAY_PLUS_10__'), parse_date('__TODAY_PLUS_12__'))
    hotel_system.book_room(102, 'Grace', parse_date('__TODAY_PLUS_5__'), parse_date('__TODAY_PLUS_6__'))
    
    if expected_refund == 'ReservationNotFoundError':
        with pytest.raises(ReservationNotFoundError):
            hotel_system.cancel_reservation(reservation_id)
    else:
        refund = hotel_system.cancel_reservation(reservation_id)
        assert refund == expected_refund

@pytest.mark.parametrize('date_str, expected', [
    ('__TODAY_PLUS_2__', [101]),
    ('__TODAY_PLUS_20__', [])
])
def test_get_room_occupancy(hotel_system, date_str, expected):
    hotel_system.add_room(101, 'single', 100.0)
    hotel_system.book_room(101, 'Alice', parse_date('__TODAY_PLUS_1__'), parse_date('__TODAY_PLUS_4__'))
    
    date_obj = parse_date(date_str)
    occupied_rooms = hotel_system.get_room_occupancy(date_obj)
    assert occupied_rooms == expected