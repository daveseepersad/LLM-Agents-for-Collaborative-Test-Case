import pytest
from data.input_code.d05_hotel import *
import datetime

@pytest.mark.parametrize('room_number, room_type, price_per_night, expected', [
    (101, 'suite', 0, 'ValueError'),
    (101, 'suite', 200, None)
])
def test_add_room(room_number, room_type, price_per_night, expected):
    hotel = HotelReservationSystem()
    if expected == 'ValueError':
        with pytest.raises(ValueError):
            hotel.add_room(room_number, room_type, price_per_night)
    else:
        hotel.add_room(room_number, room_type, price_per_night)
        assert room_number in hotel.rooms

def test_book_non_existent_room():
    hotel = HotelReservationSystem()
    with pytest.raises(RoomNotFoundError):
        hotel.book_room(999, 'Alice', datetime.date(2026, 10, 8), datetime.date(2026, 10, 9))

def test_cancel_reservation_not_found():
    hotel = HotelReservationSystem()
    with pytest.raises(ReservationNotFoundError):
        hotel.cancel_reservation('RES-9999')

def test_get_room_occupancy_empty_date():
    hotel = HotelReservationSystem()
    assert hotel.get_room_occupancy(datetime.date(2026, 10, 7)) == []

def test_add_room_negative_price():
    hotel = HotelReservationSystem()
    with pytest.raises(ValueError):
        hotel.add_room(303, "deluxe", -10)

def test_book_room_invalid_dates_order():
    hotel = HotelReservationSystem()
    hotel.add_room(400, "standard", 150)
    with pytest.raises(InvalidDateError):
        hotel.book_room(400, "Alice", datetime.date(2026, 10, 10), datetime.date(2026, 10, 10))

def test_book_room_past_date():
    hotel = HotelReservationSystem()
    hotel.add_room(400, "standard", 150)
    today = datetime.date.today()
    past_check_in = today - datetime.timedelta(days=1)
    future_check_out = today + datetime.timedelta(days=1)
    with pytest.raises(InvalidDateError):
        hotel.book_room(400, "Bob", past_check_in, future_check_out)

def test_book_overlapping_dates_raises_room_unavailable():
    hotel = HotelReservationSystem()
    hotel.add_room(101, "suite", 200)
    check_in = datetime.date(2026, 10, 12)
    check_out = datetime.date(2026, 10, 14)
    # Create initial reservation
    hotel.book_room(101, "Alice", check_in, check_out)
    # Attempt overlapping booking should raise
    with pytest.raises(RoomUnavailableError):
        hotel.book_room(101, "Alice", check_in, check_out)

def test_book_price_calculation_three_nights():
    hotel = HotelReservationSystem()
    hotel.add_room(102, "standard", 100)
    check_in = datetime.date(2026, 10, 12)
    check_out = datetime.date(2026, 10, 15)
    res_id = hotel.book_room(102, "Bob", check_in, check_out)
    assert hotel.reservations[res_id].total_price == 300.0

@pytest.mark.parametrize('room_number, user_name, check_in, check_out, expected', [
    (102, "Bob", datetime.date(2026, 10, 12), datetime.date(2026, 10, 13), "RES-0001"),
    (103, "Carol", datetime.date(2026, 10, 12), datetime.date(2026, 10, 14), "RES-0001"),
    (104, "Dan", datetime.date(2026, 10, 7), datetime.date(2026, 10, 8), "RES-0001")
])
def test_new_book_room_cases(room_number, user_name, check_in, check_out, expected):
    hotel = HotelReservationSystem()
    hotel.add_room(room_number, "standard", 100)
    res_id = hotel.book_room(room_number, user_name, check_in, check_out)
    assert res_id == expected

def test_add_room_overwrite_price():
    hotel = HotelReservationSystem()
    # Initial add with a price
    hotel.add_room(501, "standard", 200)
    # Overwrite with new price
    hotel.add_room(501, "standard", 150)
    assert hotel.rooms[501]['price_per_night'] == 150
    assert hotel.rooms[501]['type'] == "standard"

def test_adjacent_bookings_no_overlap():
    hotel = HotelReservationSystem()
    hotel.add_room(603, "standard", 100)
    res1 = hotel.book_room(603, "Alice", datetime.date(2026, 10, 12), datetime.date(2026, 10, 14))
    res2 = hotel.book_room(603, "Bob", datetime.date(2026, 10, 14), datetime.date(2026, 10, 16))
    assert res1 == "RES-0001"
    assert res2 == "RES-0002"

def test_occupancy_single():
    hotel = HotelReservationSystem()
    hotel.add_room(604, "standard", 100)
    hotel.book_room(604, "Alice", datetime.date(2026, 10, 12), datetime.date(2026, 10, 15))
    assert hotel.get_room_occupancy(datetime.date(2026, 10, 13)) == [604]

def test_cancel_refund_full():
    hotel = HotelReservationSystem()
    hotel.add_room(701, "standard", 100)
    check_in = datetime.date.today() + datetime.timedelta(days=8)
    check_out = check_in + datetime.timedelta(days=1)
    res_id = hotel.book_room(701, "Alice", check_in, check_out)
    refund = hotel.cancel_reservation(res_id)
    assert refund == 100.0

def test_cancel_refund_half():
    hotel = HotelReservationSystem()
    hotel.add_room(702, "standard", 100)
    check_in = datetime.date.today() + datetime.timedelta(days=5)
    check_out = check_in + datetime.timedelta(days=1)
    res_id = hotel.book_room(702, "Alice", check_in, check_out)
    refund = hotel.cancel_reservation(res_id)
    assert refund == 50.0

def test_cancel_refund_none():
    hotel = HotelReservationSystem()
    hotel.add_room(703, "standard", 100)
    check_in = datetime.date.today() + datetime.timedelta(days=1)
    check_out = check_in + datetime.timedelta(days=1)
    res_id = hotel.book_room(703, "Alice", check_in, check_out)
    refund = hotel.cancel_reservation(res_id)
    assert refund == 0.0