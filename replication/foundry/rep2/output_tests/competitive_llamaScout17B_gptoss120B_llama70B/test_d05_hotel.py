import pytest
import datetime
from data.input_code.d05_hotel import *

@pytest.fixture
def fresh_system():
    """Provides a fresh HotelReservationSystem instance for each test."""
    return HotelReservationSystem()

def test_init_empty_system(fresh_system):
    assert fresh_system.rooms == {}
    assert fresh_system.reservations == {}
    assert fresh_system._reservation_counter == 0

def test_add_room_valid(fresh_system):
    fresh_system.add_room(room_number=101, room_type="Single", price_per_night=100.0)
    assert 101 in fresh_system.rooms
    assert fresh_system.rooms[101]["type"] == "Single"
    assert fresh_system.rooms[101]["price_per_night"] == 100.0

@pytest.mark.parametrize(
    "price,expected_exception",
    [
        (-10.0, ValueError),
        (0.0, ValueError),
    ],
)
def test_add_room_invalid_price(fresh_system, price, expected_exception):
    with pytest.raises(expected_exception):
        fresh_system.add_room(room_number=102, room_type="Double", price_per_night=price)

@pytest.mark.parametrize(
    "room_number,user_name,check_in,check_out,expected_exception",
    [
        # Non‑existent room
        (103, "John", datetime.date.today() + datetime.timedelta(days=1),
         datetime.date.today() + datetime.timedelta(days=3), RoomNotFoundError),
        # Invalid date order
        (101, "John", datetime.date.today() + datetime.timedelta(days=3),
         datetime.date.today() + datetime.timedelta(days=1), InvalidDateError),
        # Booking in the past
        (101, "John", datetime.date.today() - datetime.timedelta(days=1),
         datetime.date.today() + datetime.timedelta(days=1), InvalidDateError),
    ],
)
def test_book_room_errors(fresh_system, room_number, user_name, check_in, check_out, expected_exception):
    # Ensure room 101 exists for the cases that need it
    fresh_system.add_room(room_number=101, room_type="Single", price_per_night=100.0)
    with pytest.raises(expected_exception):
        fresh_system.book_room(room_number, user_name, check_in, check_out)

def test_book_room_unavailable(fresh_system):
    # Setup: add room and make an initial reservation
    fresh_system.add_room(room_number=101, room_type="Single", price_per_night=100.0)
    first_check_in = datetime.date.today() + datetime.timedelta(days=1)
    first_check_out = datetime.date.today() + datetime.timedelta(days=3)
    fresh_system.book_room(101, "John", first_check_in, first_check_out)

    # Overlapping reservation should raise RoomUnavailableError
    overlapping_check_in = datetime.date.today() + datetime.timedelta(days=2)
    overlapping_check_out = datetime.date.today() + datetime.timedelta(days=4)
    with pytest.raises(RoomUnavailableError):
        fresh_system.book_room(101, "Jane", overlapping_check_in, overlapping_check_out)

def test_book_room_success(fresh_system):
    fresh_system.add_room(room_number=101, room_type="Single", price_per_night=100.0)
    check_in = datetime.date.today() + datetime.timedelta(days=1)
    check_out = datetime.date.today() + datetime.timedelta(days=3)
    res_id = fresh_system.book_room(101, "John", check_in, check_out)

    assert res_id == "RES-0001"
    reservation = fresh_system.reservations[res_id]
    assert reservation.room_number == 101
    assert reservation.user_name == "John"
    assert reservation.check_in == check_in
    assert reservation.check_out == check_out
    assert reservation.total_price == 200.0  # 2 nights * 100.0

@pytest.mark.parametrize(
    "days_until_checkin,expected_refund_factor",
    [
        (8, 1.0),   # >7 days → full refund
        (5, 0.5),   # 2‑7 days → 50%
        (1, 0.0),   # <2 days → none
    ],
)
def test_cancel_reservation_refund(fresh_system, days_until_checkin, expected_refund_factor):
    fresh_system.add_room(room_number=101, room_type="Single", price_per_night=100.0)

    check_in = datetime.date.today() + datetime.timedelta(days=days_until_checkin)
    check_out = check_in + datetime.timedelta(days=2)
    res_id = fresh_system.book_room(101, "John", check_in, check_out)

    total_price = fresh_system.reservations[res_id].total_price
    refund = fresh_system.cancel_reservation(res_id)

    assert refund == round(total_price * expected_refund_factor, 2)

def test_cancel_reservation_not_found(fresh_system):
    with pytest.raises(ReservationNotFoundError):
        fresh_system.cancel_reservation("RES-9999")

def test_get_room_occupancy(fresh_system):
    fresh_system.add_room(room_number=101, room_type="Single", price_per_night=100.0)
    fresh_system.add_room(room_number=102, room_type="Double", price_per_night=150.0)

    # Book room 101 for days 1‑3
    check_in_101 = datetime.date.today() + datetime.timedelta(days=1)
    check_out_101 = datetime.date.today() + datetime.timedelta(days=3)
    fresh_system.book_room(101, "John", check_in_101, check_out_101)

    # Book room 102 for days 2‑4
    check_in_102 = datetime.date.today() + datetime.timedelta(days=2)
    check_out_102 = datetime.date.today() + datetime.timedelta(days=4)
    fresh_system.book_room(102, "Jane", check_in_102, check_out_102)

    # Occupancy on day 2 (today + 2) should include both rooms
    target_date = datetime.date.today() + datetime.timedelta(days=2)
    occupied = fresh_system.get_room_occupancy(target_date)
    assert occupied == [101, 102]

    # Occupancy on day 1 should include only room 101
    occupied_day1 = fresh_system.get_room_occupancy(datetime.date.today() + datetime.timedelta(days=1))
    assert occupied_day1 == [101]

    # Occupancy on day 4 should be empty (check_out is exclusive)
    occupied_day4 = fresh_system.get_room_occupancy(datetime.date.today() + datetime.timedelta(days=4))
    assert occupied_day4 == []