import pytest
from data.input_code.d05_hotel import *
from datetime import date, timedelta

@pytest.mark.parametrize('room_number, room_type, price_per_night, expected', [
    (101, 'Deluxe', 150.0, None),
    (102, 'Standard', 0.0, 'ValueError')
])
def test_add_room(room_number, room_type, price_per_night, expected):
    hotel = HotelReservationSystem()
    if expected == 'ValueError':
        with pytest.raises(ValueError):
            hotel.add_room(room_number, room_type, price_per_night)
    else:
        hotel.add_room(room_number, room_type, price_per_night)
        assert room_number in hotel.rooms

@pytest.mark.parametrize('prepopulate_rooms, prepopulate_reservations, room_number, user_name, check_in, check_out, expected', [
    ({}, {}, 999, 'Alice', date.today() + timedelta(days=3), date.today() + timedelta(days=6), 'RoomNotFoundError'),
    ({101: {'type': 'Deluxe', 'price_per_night': 150.0}}, {}, 101, 'Bob', date.today() + timedelta(days=6), date.today() + timedelta(days=3), 'InvalidDateError'),
    ({101: {'type': 'Deluxe', 'price_per_night': 150.0}}, {}, 101, 'Carol', date.today() - timedelta(days=1), date.today() + timedelta(days=2), 'InvalidDateError'),
    ({101: {'type': 'Deluxe', 'price_per_night': 150.0}}, {'RES-0001': Reservation('RES-0001', 101, 'Dave', date.today() + timedelta(days=3), date.today() + timedelta(days=6), 450.0)}, 101, 'Eve', date.today() + timedelta(days=3), date.today() + timedelta(days=6), 'RoomUnavailableError'),
    ({101: {'type': 'Deluxe', 'price_per_night': 150.0}}, {}, 101, 'Frank', date.today() + timedelta(days=3), date.today() + timedelta(days=6), 'RES-0001')
])
def test_book_room(prepopulate_rooms, prepopulate_reservations, room_number, user_name, check_in, check_out, expected):
    hotel = HotelReservationSystem()
    hotel.rooms = prepopulate_rooms
    hotel.reservations = prepopulate_reservations
    if expected == 'RoomNotFoundError':
        with pytest.raises(RoomNotFoundError):
            hotel.book_room(room_number, user_name, check_in, check_out)
    elif expected == 'InvalidDateError':
        with pytest.raises(InvalidDateError):
            hotel.book_room(room_number, user_name, check_in, check_out)
    elif expected == 'RoomUnavailableError':
        with pytest.raises(RoomUnavailableError):
            hotel.book_room(room_number, user_name, check_in, check_out)
    else:
        res_id = hotel.book_room(room_number, user_name, check_in, check_out)
        assert res_id == expected

@pytest.mark.parametrize('prepopulate_reservations, reservation_id, expected', [
    ({}, 'RES-9999', 'ReservationNotFoundError'),
    ({'RES-0001': Reservation('RES-0001', 101, 'Grace', date.today() + timedelta(days=10), date.today() + timedelta(days=13), 300.0)}, 'RES-0001', 300.0),
    ({'RES-0002': Reservation('RES-0002', 102, 'Heidi', date.today() + timedelta(days=5), date.today() + timedelta(days=8), 300.0)}, 'RES-0002', 150.0),
    ({'RES-0003': Reservation('RES-0003', 103, 'Ivan', date.today() + timedelta(days=1), date.today() + timedelta(days=3), 300.0)}, 'RES-0003', 0.0)
])
def test_cancel_reservation(prepopulate_reservations, reservation_id, expected):
    hotel = HotelReservationSystem()
    hotel.reservations = prepopulate_reservations
    if expected == 'ReservationNotFoundError':
        with pytest.raises(ReservationNotFoundError):
            hotel.cancel_reservation(reservation_id)
    else:
        refund = hotel.cancel_reservation(reservation_id)
        assert refund == expected

@pytest.mark.parametrize('prepopulate_reservations, date, expected', [
    ({'RES-0004': Reservation('RES-0004', 101, 'Judy', date(2023, 1, 10), date(2023, 1, 13), 450.0),
      'RES-0005': Reservation('RES-0005', 102, 'Ken', date(2023, 1, 12), date(2023, 1, 15), 300.0)}, date(2023, 1, 12), [101, 102]),
    ({'RES-0006': Reservation('RES-0006', 101, 'Liam', date(2023, 1, 10), date(2023, 1, 13), 450.0)}, date(2023, 1, 14), [])
])
def test_get_room_occupancy(prepopulate_reservations, date, expected):
    hotel = HotelReservationSystem()
    hotel.reservations = prepopulate_reservations
    occupied_rooms = hotel.get_room_occupancy(date)
    assert occupied_rooms == expected