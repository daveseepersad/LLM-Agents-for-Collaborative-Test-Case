import pytest
import datetime
from data.input_code.d05_hotel import (
    HotelReservationSystem, RoomNotFoundError, RoomUnavailableError,
    InvalidDateError, ReservationNotFoundError
)

def test_add_room_and_price_validation():
    hotel = HotelReservationSystem()
    hotel.add_room(101, "Single", 100.0)
    assert hotel.rooms[101]['type'] == "Single"
    assert hotel.rooms[101]['price_per_night'] == 100.0

    with pytest.raises(ValueError):
        hotel.add_room(102, "Double", 0)
    with pytest.raises(ValueError):
        hotel.add_room(103, "Double", -10)

def test_book_room_success_and_room_not_found():
    hotel = HotelReservationSystem()
    hotel.add_room(101, "Single", 100.0)
    today = datetime.date.today()
    check_in = today + datetime.timedelta(days=1)
    check_out = today + datetime.timedelta(days=3)

    res_id = hotel.book_room(101, "Alice", check_in, check_out)
    assert res_id in hotel.reservations
    res = hotel.reservations[res_id]
    assert res.room_number == 101
    assert res.user_name == "Alice"
    assert res.check_in == check_in
    assert res.check_out == check_out
    assert res.total_price == 200.0

    with pytest.raises(RoomNotFoundError):
        hotel.book_room(999, "Bob", check_in, check_out)

def test_book_room_invalid_dates():
    hotel = HotelReservationSystem()
    hotel.add_room(101, "Single", 100.0)
    today = datetime.date.today()
    past_date = today - datetime.timedelta(days=1)
    future_date = today + datetime.timedelta(days=5)

    # check_in >= check_out
    with pytest.raises(InvalidDateError):
        hotel.book_room(101, "Alice", future_date, future_date)
    with pytest.raises(InvalidDateError):
        hotel.book_room(101, "Alice", future_date, future_date - datetime.timedelta(days=1))

    # check_in in the past
    with pytest.raises(InvalidDateError):
        hotel.book_room(101, "Alice", past_date, future_date)

def test_book_room_unavailable():
    hotel = HotelReservationSystem()
    hotel.add_room(101, "Single", 100.0)
    today = datetime.date.today()
    check_in1 = today + datetime.timedelta(days=5)
    check_out1 = today + datetime.timedelta(days=10)
    hotel.book_room(101, "Alice", check_in1, check_out1)

    # Overlapping bookings
    with pytest.raises(RoomUnavailableError):
        hotel.book_room(101, "Bob", check_in1, check_out1)
    with pytest.raises(RoomUnavailableError):
        hotel.book_room(101, "Bob", check_in1 - datetime.timedelta(days=1), check_out1)
    with pytest.raises(RoomUnavailableError):
        hotel.book_room(101, "Bob", check_in1, check_out1 + datetime.timedelta(days=1))
    with pytest.raises(RoomUnavailableError):
        hotel.book_room(101, "Bob", check_in1 + datetime.timedelta(days=1), check_out1 - datetime.timedelta(days=1))

def test_cancel_reservation_refund_policy():
    hotel = HotelReservationSystem()
    hotel.add_room(101, "Single", 100.0)
    today = datetime.date.today()

    # >7 days: full refund
    check_in = today + datetime.timedelta(days=10)
    check_out = check_in + datetime.timedelta(days=2)
    res_id = hotel.book_room(101, "Alice", check_in, check_out)
    refund = hotel.cancel_reservation(res_id)
    assert refund == 200.0

    # 2-7 days: 50% refund
    check_in = today + datetime.timedelta(days=5)
    check_out = check_in + datetime.timedelta(days=2)
    res_id = hotel.book_room(101, "Bob", check_in, check_out)
    refund = hotel.cancel_reservation(res_id)
    assert refund == 100.0  # 50% of 200

    # <2 days: no refund
    check_in = today + datetime.timedelta(days=1)
    check_out = check_in + datetime.timedelta(days=2)
    res_id = hotel.book_room(101, "Carol", check_in, check_out)
    refund = hotel.cancel_reservation(res_id)
    assert refund == 0.0

def test_cancel_reservation_not_found():
    hotel = HotelReservationSystem()
    with pytest.raises(ReservationNotFoundError):
        hotel.cancel_reservation("NONEXISTENT")

def test_get_room_occupancy():
    hotel = HotelReservationSystem()
    hotel.add_room(101, "Single", 100.0)
    hotel.add_room(102, "Double", 150.0)
    today = datetime.date.today()

    # No reservations yet
    assert hotel.get_room_occupancy(today) == []

    # Book room 101 from day 1 to day 3
    check_in1 = today + datetime.timedelta(days=1)
    check_out1 = today + datetime.timedelta(days=3)
    hotel.book_room(101, "Alice", check_in1, check_out1)

    # Book room 102 from day 2 to day 4
    check_in2 = today + datetime.timedelta(days=2)
    check_out2 = today + datetime.timedelta(days=4)
    hotel.book_room(102, "Bob", check_in2, check_out2)

    # Occupancy on day 0: none
    assert hotel.get_room_occupancy(today) == []

    # Occupancy on day 1: room 101
    assert hotel.get_room_occupancy(today + datetime.timedelta(days=1)) == [101]

    # Occupancy on day 2: rooms 101 and 102
    assert hotel.get_room_occupancy(today + datetime.timedelta(days=2)) == [101, 102]

    # Occupancy on day 3: room 102 only (101 checkout day)
    assert hotel.get_room_occupancy(today + datetime.timedelta(days=3)) == [102]

    # Occupancy on day 4: none (102 checkout day)
    assert hotel.get_room_occupancy(today + datetime.timedelta(days=4)) == []