import pytest
from data.input_code.d05_hotel import *
import datetime

@pytest.mark.parametrize('room_number, room_type, price_per_night, expected_exception', [
    (101, 'single', 100.0, None),
    (102, 'double', 0, ValueError)
])
def test_add_room(room_number, room_type, price_per_night, expected_exception):
    system = HotelReservationSystem()
    if expected_exception:
        with pytest.raises(expected_exception):
            system.add_room(room_number, room_type, price_per_night)
    else:
        system.add_room(room_number, room_type, price_per_night)
        assert room_number in system.rooms

@pytest.mark.parametrize('initial_rooms, initial_reservations, room_number, user_name, check_in, check_out, expected', [
    ([{'room_number': 201, 'room_type': 'suite', 'price_per_night': 150.0}], [], 201, 'Alice', datetime.date(2026, 10, 8), datetime.date(2026, 10, 10), 'RES-0001'),
    ([], [], 999, 'Bob', datetime.date(2026, 10, 8), datetime.date(2026, 10, 9), RoomNotFoundError),
    ([{'room_number': 101, 'room_type': 'single', 'price_per_night': 100.0}], [], 101, 'Cara', datetime.date(2026, 10, 11), datetime.date(2026, 10, 10), InvalidDateError),
    ([{'room_number': 301, 'room_type': 'standard', 'price_per_night': 100.0}], [{'reservation_id': 'RES-0001', 'room_number': 301, 'user_name': 'Existing', 'check_in': datetime.date(2026, 10, 8), 'check_out': datetime.date(2026, 10, 11), 'total_price': 300.0}], 301, 'New', datetime.date(2026, 10, 9), datetime.date(2026, 10, 12), RoomUnavailableError),
    ([{'room_number': 401, 'room_type': 'standard', 'price_per_night': 100.0}], [], 401, 'Drew', datetime.date(2023, 10, 6), datetime.date(2023, 10, 8), InvalidDateError)
])
def test_book_room(initial_rooms, initial_reservations, room_number, user_name, check_in, check_out, expected):
    system = HotelReservationSystem()
    for room in initial_rooms:
        system.add_room(room['room_number'], room['room_type'], room['price_per_night'])
    for reservation in initial_reservations:
        system.reservations[reservation['reservation_id']] = Reservation(**reservation)
    if isinstance(expected, type) and issubclass(expected, Exception):
        with pytest.raises(expected):
            system.book_room(room_number, user_name, check_in, check_out)
    else:
        assert system.book_room(room_number, user_name, check_in, check_out) == expected

@pytest.mark.parametrize('initial_rooms, initial_reservations, reservation_id, expected', [
    ([{'room_number': 302, 'room_type': 'standard', 'price_per_night': 100.0}], [{'reservation_id': 'RES-0001', 'room_number': 302, 'user_name': 'Eve', 'check_in': datetime.date.today() + datetime.timedelta(days=10), 'check_out': datetime.date.today() + datetime.timedelta(days=12), 'total_price': 200.0}], 'RES-0001', 200.0),
    ([{'room_number': 303, 'room_type': 'standard', 'price_per_night': 120.0}], [{'reservation_id': 'RES-0002', 'room_number': 303, 'user_name': 'Frank', 'check_in': datetime.date.today() + datetime.timedelta(days=5), 'check_out': datetime.date.today() + datetime.timedelta(days=7), 'total_price': 240.0}], 'RES-0002', 120.0),
    ([{'room_number': 304, 'room_type': 'standard', 'price_per_night': 100.0}], [{'reservation_id': 'RES-0003', 'room_number': 304, 'user_name': 'Grace', 'check_in': datetime.date.today() + datetime.timedelta(days=1), 'check_out': datetime.date.today() + datetime.timedelta(days=3), 'total_price': 200.0}], 'RES-0003', 0.0),
    ([{'room_number': 305, 'room_type': 'standard', 'price_per_night': 100.0}], [], 'RES-UNKNOWN', ReservationNotFoundError)
])
def test_cancel_reservation(initial_rooms, initial_reservations, reservation_id, expected):
    system = HotelReservationSystem()
    for room in initial_rooms:
        system.add_room(room['room_number'], room['room_type'], room['price_per_night'])
    for reservation in initial_reservations:
        system.reservations[reservation['reservation_id']] = Reservation(**reservation)
    if isinstance(expected, type) and issubclass(expected, Exception):
        with pytest.raises(expected):
            system.cancel_reservation(reservation_id)
    else:
        assert system.cancel_reservation(reservation_id) == expected

@pytest.mark.parametrize('initial_rooms, initial_reservations, date, expected', [
    ([{'room_number': 301, 'room_type': 'standard', 'price_per_night': 100.0}, {'room_number': 302, 'room_type': 'standard', 'price_per_night': 100.0}], [{'reservation_id': 'RES-0001', 'room_number': 301, 'user_name': 'Alice', 'check_in': datetime.date(2026, 10, 8), 'check_out': datetime.date(2026, 10, 12), 'total_price': 400.0}, {'reservation_id': 'RES-0002', 'room_number': 302, 'user_name': 'Bob', 'check_in': datetime.date(2026, 10, 9), 'check_out': datetime.date(2026, 10, 13), 'total_price': 400.0}], datetime.date(2026, 10, 10), [301, 302]),
    ([{'room_number': 401, 'room_type': 'standard', 'price_per_night': 100.0}], [], datetime.date(2026, 10, 20), [])
])
def test_get_room_occupancy(initial_rooms, initial_reservations, date, expected):
    system = HotelReservationSystem()
    for room in initial_rooms:
        system.add_room(room['room_number'], room['room_type'], room['price_per_night'])
    for reservation in initial_reservations:
        system.reservations[reservation['reservation_id']] = Reservation(**reservation)
    assert system.get_room_occupancy(date) == expected