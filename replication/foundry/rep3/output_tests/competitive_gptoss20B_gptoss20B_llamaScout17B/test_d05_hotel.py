import pytest
import datetime
from data.input_code.d05_hotel import *

def test_hotel_reservation_plan():
    # Initialize system
    h = HotelReservationSystem()

    # T1_ADD_ROOM_OK
    h.add_room(101, "Standard", 100.0)
    assert 101 in h.rooms
    assert h.rooms[101]['type'] == "Standard"
    assert h.rooms[101]['price_per_night'] == 100.0

    # T2_ADD_ROOM_NEG_PRICE
    with pytest.raises(ValueError):
        h.add_room(102, "Deluxe", 0.0)

    # T3_BOOK_ROOM_SUCCESS
    ci = datetime.date(2026, 10, 10)
    co = datetime.date(2026, 10, 12)
    res1 = h.book_room(101, "Alice", ci, co)
    assert res1 == "RES-0001"

    # T4_BOOK_ROOM_NOT_FOUND
    with pytest.raises(RoomNotFoundError):
        h.book_room(999, "Bob", datetime.date(2026, 10, 15), datetime.date(2026, 10, 17))

    # T5_BOOK_ROOM_INVALID_DATES_ORDER
    with pytest.raises(InvalidDateError):
        h.book_room(101, "Carol", datetime.date(2026, 10, 12), datetime.date(2026, 10, 12))

    # T6_BOOK_ROOM_PAST_DATE
    past_in = datetime.date.today() - datetime.timedelta(days=1)
    past_out = past_in + datetime.timedelta(days=2)
    with pytest.raises(InvalidDateError):
        h.book_room(101, "Dan", past_in, past_out)

    # T7_BOOK_ROOM_UNAVAILABLE_OVERLAP
    with pytest.raises(RoomUnavailableError):
        h.book_room(101, "Eve", datetime.date(2026, 10, 11), datetime.date(2026, 10, 13))

    # T8_CANCEL_RESERVATION_NOT_FOUND
    with pytest.raises(ReservationNotFoundError):
        h.cancel_reservation("RES-9999")

    # T9_CANCEL_RESERVATION_FULL_REFUND
    # Create RES-0002 for future to test refund (>7 days before check-in)
    res2 = h.book_room(101, "Frank", datetime.date(2026, 11, 1), datetime.date(2026, 11, 3))
    assert res2 == "RES-0002"
    refund_full = h.cancel_reservation("RES-0002")
    assert refund_full == 200.0

    # T3a/T11 precursor: Create RES-0003 to satisfy occupancy test on 2026-10-21
    res3 = h.book_room(101, "Grace", datetime.date(2026, 10, 21), datetime.date(2026, 10, 22))
    assert res3 == "RES-0003"

    # T10_CANCEL_RESERVATION_HALF_REFUND
    refund_half = h.cancel_reservation("RES-0001")
    assert refund_half == 100.0

    # T11_GET_ROOM_OCCUPANCY
    occ_date = datetime.date(2026, 10, 21)
    occupancy = h.get_room_occupancy(occ_date)
    assert occupancy == [101]

    # T12_ADD_ROOM_OVERWRITE
    h.add_room(101, "Standard-Updated", 150.0)
    assert h.rooms[101]['type'] == "Standard-Updated"
    assert h.rooms[101]['price_per_night'] == 150.0

def test_MISSING_TOTAL_PRICE_ONE_NIGHT():
    h = HotelReservationSystem()
    h.add_room(201, "Standard", 120.0)
    ci = datetime.date(2026, 12, 1)
    co = datetime.date(2026, 12, 2)
    res_id = h.book_room(201, "Test", ci, co)
    assert res_id == "RES-0001"
    assert h.reservations[res_id].total_price == 120.0

def test_MISSING_PRIVATE_IS_AVAIL_NON_OVERLAP():
    h = HotelReservationSystem()
    h.add_room(201, "Standard", 100.0)
    # Create an existing reservation that ends on 2026-12-03
    h.book_room(201, "Alice", datetime.date(2026, 12, 1), datetime.date(2026, 12, 3))
    # New booking starting exactly as previous checkout should be allowed (non-overlapping)
    assert h._is_room_available(201, datetime.date(2026, 12, 3), datetime.date(2026, 12, 5)) is True

def test_MISSING_OCCUPANCY_TWO_ROOMS():
    h = HotelReservationSystem()
    h.add_room(301, "Standard", 100.0)
    h.add_room(302, "Standard", 100.0)
    h.book_room(301, "Alice", datetime.date(2026, 12, 6), datetime.date(2026, 12, 8))
    h.book_room(302, "Bob", datetime.date(2026, 12, 6), datetime.date(2026, 12, 9))
    occ = h.get_room_occupancy(datetime.date(2026, 12, 6))
    assert occ == [301, 302]

def test_MISSING_CANCEL_NO_REFUND_TODAY():
    h = HotelReservationSystem()
    h.add_room(501, "Standard", 100.0)
    ci = datetime.date.today()
    co = ci + datetime.timedelta(days=1)
    res = Reservation("TEST-001", 501, "UnitTest", ci, co, 100.0)
    h.reservations["TEST-001"] = res
    assert h.cancel_reservation("TEST-001") == 0.0

def test_MISSING_CANCEL_NO_REFUND_REPEAT():
    h = HotelReservationSystem()
    h.add_room(502, "Standard", 120.0)
    ci = datetime.date.today()
    co = ci + datetime.timedelta(days=1)
    res = Reservation("TEST-001", 502, "UnitTest", ci, co, 120.0)
    h.reservations["TEST-001"] = res
    refund1 = h.cancel_reservation("TEST-001")
    assert refund1 == 0.0
    with pytest.raises(ReservationNotFoundError):
        h.cancel_reservation("TEST-001")