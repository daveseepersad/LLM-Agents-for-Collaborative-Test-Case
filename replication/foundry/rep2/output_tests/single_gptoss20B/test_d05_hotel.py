import pytest
import datetime

from data.input_code.d05_hotel import (
    HotelReservationSystem,
    RoomNotFoundError,
    RoomUnavailableError,
    InvalidDateError,
    ReservationNotFoundError,
)

def test_add_room_negative_price_raises_value_error():
    h = HotelReservationSystem()
    with pytest.raises(ValueError):
        h.add_room(101, "Deluxe", -50)

def test_book_room_success_calculates_price_and_returns_id():
    h = HotelReservationSystem()
    h.add_room(101, "Deluxe", 100.0)
    today = datetime.date.today()
    check_in = today + datetime.timedelta(days=2)
    check_out = check_in + datetime.timedelta(days=3)  # 3 nights
    res_id = h.book_room(101, "Alice", check_in, check_out)
    assert res_id == "RES-0001"
    res = h.reservations[res_id]
    assert res.room_number == 101
    assert res.user_name == "Alice"
    assert res.check_in == check_in
    assert res.check_out == check_out
    assert res.total_price == 300.0

def test_book_room_room_not_found_raises():
    h = HotelReservationSystem()
    with pytest.raises(RoomNotFoundError):
        h.book_room(
            999,
            "Bob",
            datetime.date.today() + datetime.timedelta(days=1),
            datetime.date.today() + datetime.timedelta(days=2),
        )

def test_book_room_invalid_dates_raises_invaliddate():
    h = HotelReservationSystem()
    h.add_room(101, "Deluxe", 100)
    today = datetime.date.today()
    check_in = today + datetime.timedelta(days=2)
    check_out = check_in  # same day, invalid
    with pytest.raises(InvalidDateError):
        h.book_room(101, "Bob", check_in, check_out)

def test_book_room_in_past_raises_invaliddate():
    h = HotelReservationSystem()
    h.add_room(101, "Deluxe", 100)
    past = datetime.date.today() - datetime.timedelta(days=1)
    future = datetime.date.today() + datetime.timedelta(days=2)
    with pytest.raises(InvalidDateError):
        h.book_room(101, "Bob", past, future)

def test_book_room_unavailable_due_to_overlap():
    h = HotelReservationSystem()
    h.add_room(101, "Deluxe", 100)
    today = datetime.date.today()
    check_in = today + datetime.timedelta(days=2)
    check_out = check_in + datetime.timedelta(days=3)  # 3 nights
    h.book_room(101, "Alice", check_in, check_out)

    # Overlapping range
    with pytest.raises(RoomUnavailableError):
        h.book_room(
            101,
            "Charlie",
            check_in + datetime.timedelta(days=1),
            check_out + datetime.timedelta(days=1),
        )

def test_cancel_reservation_full_refund():
    h = HotelReservationSystem()
    h.add_room(101, "Deluxe", 100)
    today = datetime.date.today()
    check_in = today + datetime.timedelta(days=10)
    check_out = check_in + datetime.timedelta(days=2)  # 2 nights
    res_id = h.book_room(101, "Ana", check_in, check_out)
    refund = h.cancel_reservation(res_id)
    assert refund == 200.0  # >7 days => 100% refund

def test_cancel_reservation_half_refund():
    h = HotelReservationSystem()
    h.add_room(101, "Deluxe", 100)
    today = datetime.date.today()
    check_in = today + datetime.timedelta(days=5)
    check_out = check_in + datetime.timedelta(days=2)  # 2 nights
    res_id = h.book_room(101, "Ben", check_in, check_out)
    refund = h.cancel_reservation(res_id)
    assert refund == 100.0  # 2-7 days => 50% refund

def test_cancel_reservation_no_refund():
    h = HotelReservationSystem()
    h.add_room(101, "Deluxe", 100)
    today = datetime.date.today()
    check_in = today + datetime.timedelta(days=1)
    check_out = check_in + datetime.timedelta(days=2)  # 2 nights
    res_id = h.book_room(101, "Cara", check_in, check_out)
    refund = h.cancel_reservation(res_id)
    assert refund == 0.0  # <2 days => 0% refund

def test_cancel_reservation_nonexistent_raises():
    h = HotelReservationSystem()
    with pytest.raises(ReservationNotFoundError):
        h.cancel_reservation("RES-9999")

def test_get_room_occupancy_returns_sorted_occupied_rooms():
    h = HotelReservationSystem()
    h.add_room(101, "Deluxe", 100)
    h.add_room(102, "Suite", 150)

    today = datetime.date.today()
    # Reservation occupying room 101 from day 2 to 4
    r1_in = today + datetime.timedelta(days=2)
    r1_out = r1_in + datetime.timedelta(days=2)
    h.book_room(101, "Alice", r1_in, r1_out)

    # Reservation occupying room 102 from day 3 to 5
    r2_in = today + datetime.timedelta(days=3)
    r2_out = r2_in + datetime.timedelta(days=2)
    h.book_room(102, "Bob", r2_in, r2_out)

    # Check occupancy on day 3: both 101 and 102 should be occupied
    date_to_check = today + datetime.timedelta(days=3)
    occupancy = h.get_room_occupancy(date=date_to_check)
    assert occupancy == [101, 102]