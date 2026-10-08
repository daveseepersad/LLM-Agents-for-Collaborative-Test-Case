import pytest
from data.input_code.d05_hotel import *
import datetime

def test_T1_ADD_ROOM_NEG_PRICE():
    h = HotelReservationSystem()
    with pytest.raises(ValueError):
        h.add_room(101, "Standard", -50.0)

def test_T2_BOOK_ROOM_NONEXISTENT():
    h = HotelReservationSystem()
    check_in = datetime.date(2100, 1, 1)
    check_out = datetime.date(2100, 1, 2)
    with pytest.raises(RoomNotFoundError):
        h.book_room(999, "Alice", check_in, check_out)

def test_T3_BOOK_ROOM_PAST_DATE():
    h = HotelReservationSystem()
    h.add_room(101, "Standard", 100.0)
    check_in = datetime.date(2000, 1, 1)
    check_out = datetime.date(2000, 1, 2)
    with pytest.raises(InvalidDateError):
        h.book_room(101, "Bob", check_in, check_out)

def test_T4_BOOK_ROOM_SUCCESS_ONE_NIGHT():
    h = HotelReservationSystem()
    h.add_room(101, "Standard", 200.0)
    check_in = datetime.date(2100, 1, 1)
    check_out = datetime.date(2100, 1, 2)
    res_id = h.book_room(101, "Carol", check_in, check_out)
    assert res_id == "RES-0001"
    assert h.reservations[res_id].total_price == 200.0

def test_T5_BOOK_ROOM_OVERLAP():
    h = HotelReservationSystem()
    h.add_room(101, "Standard", 200.0)
    check_in1 = datetime.date(2100, 1, 1)
    check_out1 = datetime.date(2100, 1, 2)
    h.book_room(101, "Carol", check_in1, check_out1)
    check_in2 = datetime.date(2100, 1, 1)
    check_out2 = datetime.date(2100, 1, 3)
    with pytest.raises(RoomUnavailableError):
        h.book_room(101, "Dave", check_in2, check_out2)

def test_T6_CANCEL_RESERVATION_NOT_FOUND():
    h = HotelReservationSystem()
    with pytest.raises(ReservationNotFoundError):
        h.cancel_reservation("RES-9999")

def test_T7_CANCEL_RESERVATION_REFUND_MORE_THAN_7():
    h = HotelReservationSystem()
    h.add_room(101, "Standard", 200.0)
    check_in = datetime.date(2100, 1, 1)
    check_out = datetime.date(2100, 1, 3)  # 2 nights
    res_id = h.book_room(101, "Eve", check_in, check_out)
    refund = h.cancel_reservation(res_id)
    assert refund == 400.0

def test_T8_GET_ROOM_OCCUPANCY_EMPTY():
    h = HotelReservationSystem()
    h.add_room(101, "Standard", 100.0)
    date_to_check = datetime.date(2100, 1, 5)
    occupancy = h.get_room_occupancy(date_to_check)
    assert occupancy == []

def test_T_MISSING_BOUNDARY_AVAILABILITY_NO_OVERLAP():
    h = HotelReservationSystem()
    h.add_room(101, "Standard", 150.0)
    # Existing reservation ends exactly when the new one would start
    existing_check_in = datetime.date(2100, 1, 1)
    existing_check_out = datetime.date(2100, 1, 2)
    h.book_room(101, "Alice", existing_check_in, existing_check_out)
    # Boundary: new booking starts on the existing checkout date, should be available
    assert h._is_room_available(101, datetime.date(2100, 1, 2), datetime.date(2100, 1, 3)) is True

def test_T_MISSING_OCCUPANCY_AFTER_PRESET():
    h = HotelReservationSystem()
    h.add_room(101, "Standard", 100.0)
    # Create a reservation that occupies the room on 2100-01-02
    h.book_room(101, "Bob", datetime.date(2100, 1, 1), datetime.date(2100, 1, 3))
    occupancy = h.get_room_occupancy(datetime.date(2100, 1, 2))
    assert occupancy == [101]

def test_T9_ADD_ROOM_ZERO_PRICE():
    h = HotelReservationSystem()
    with pytest.raises(ValueError):
        h.add_room(102, "Standard", 0.0)

def test_T10_BOOK_ROOM_INVALID_DATE_ORDER():
    h = HotelReservationSystem()
    h.add_room(101, "Standard", 100.0)
    check_in = datetime.date(2100, 1, 4)
    check_out = datetime.date(2100, 1, 1)
    with pytest.raises(InvalidDateError):
        h.book_room(101, "Tester", check_in, check_out)

def test_T11_BOOK_ROOM_TWO_NIGHTS():
    h = HotelReservationSystem()
    h.add_room(101, "Standard", 100.0)
    check_in = datetime.date(2100, 1, 1)
    check_out = datetime.date(2100, 1, 3)
    res_id = h.book_room(101, "Alice", check_in, check_out)
    assert res_id == "RES-0001"

def test_T12_CANCEL_RESERVATION_50_PERCENT():
    h = HotelReservationSystem()
    h.add_room(201, "Standard", 100.0)
    check_in = datetime.date.today() + datetime.timedelta(days=5)
    check_out = check_in + datetime.timedelta(days=2)
    res_id = h.book_room(201, "Zoe", check_in, check_out)
    refund = h.cancel_reservation(res_id)
    assert refund == 100.0

def test_T13_CANCEL_RESERVATION_0_PERCENT():
    h = HotelReservationSystem()
    h.add_room(202, "Standard", 150.0)
    check_in = datetime.date.today() + datetime.timedelta(days=1)
    check_out = check_in + datetime.timedelta(days=2)
    res_id = h.book_room(202, "Mia", check_in, check_out)
    refund = h.cancel_reservation(res_id)
    assert refund == 0.0

def test_T14_OCCUPANCY_MULTIPLE_ROOMS_SORTED():
    h = HotelReservationSystem()
    h.add_room(301, "Standard", 120.0)
    h.add_room(302, "Standard", 120.0)
    base = datetime.date.today() + datetime.timedelta(days=10)
    r1_check_in = base
    r1_check_out = base + datetime.timedelta(days=3)
    r2_check_in = base + datetime.timedelta(days=1)
    r2_check_out = base + datetime.timedelta(days=4)
    h.book_room(301, "Alice", r1_check_in, r1_check_out)
    h.book_room(302, "Bob", r2_check_in, r2_check_out)
    query_date = base + datetime.timedelta(days=1)
    occupancy = h.get_room_occupancy(query_date)
    assert occupancy == [301, 302]