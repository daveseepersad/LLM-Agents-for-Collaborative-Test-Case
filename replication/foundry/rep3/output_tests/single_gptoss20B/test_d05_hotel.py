import pytest
import datetime

from data.input_code.d05_hotel import (
    HotelReservationSystem,
    RoomNotFoundError,
    RoomUnavailableError,
    InvalidDateError,
    ReservationNotFoundError,
)

def test_add_room_valid_and_invalid_price():
    system = HotelReservationSystem()
    system.add_room(101, "Standard", 120.0)
    assert 101 in system.rooms
    assert system.rooms[101]["type"] == "Standard"
    assert system.rooms[101]["price_per_night"] == 120.0

    with pytest.raises(ValueError):
        system.add_room(102, "Deluxe", -50.0)

def test_book_room_success_and_price_and_id():
    system = HotelReservationSystem()
    system.add_room(101, "Standard", 150.0)

    today = datetime.date.today()
    check_in = today + datetime.timedelta(days=1)
    check_out = today + datetime.timedelta(days=3)  # 2 nights

    res_id = system.book_room(101, "Alice", check_in, check_out)

    assert isinstance(res_id, str)
    assert res_id.startswith("RES-")
    assert res_id in system.reservations

    reservation = system.reservations[res_id]
    assert reservation.room_number == 101
    assert reservation.user_name == "Alice"
    assert reservation.check_in == check_in
    assert reservation.check_out == check_out
    assert reservation.total_price == 2 * 150.0

def test_book_room_room_not_found():
    system = HotelReservationSystem()
    today = datetime.date.today()
    check_in = today + datetime.timedelta(days=1)
    check_out = today + datetime.timedelta(days=2)

    with pytest.raises(RoomNotFoundError):
        system.book_room(999, "Bob", check_in, check_out)

def test_book_room_invalid_dates():
    system = HotelReservationSystem()
    system.add_room(201, "Standard", 100.0)

    today = datetime.date.today()
    check_in = today + datetime.timedelta(days=3)
    check_out = check_in  # same day -> invalid

    with pytest.raises(InvalidDateError):
        system.book_room(201, "Carol", check_in, check_out)

def test_book_room_in_past():
    system = HotelReservationSystem()
    system.add_room(202, "Standard", 100.0)

    today = datetime.date.today()
    check_in = today - datetime.timedelta(days=1)
    check_out = today + datetime.timedelta(days=1)

    with pytest.raises(InvalidDateError):
        system.book_room(202, "Dave", check_in, check_out)

def test_book_room_unavailable_due_to_overlap():
    system = HotelReservationSystem()
    system.add_room(301, "Standard", 100.0)

    today = datetime.date.today()
    first_in = today + datetime.timedelta(days=1)
    first_out = today + datetime.timedelta(days=3)

    system.book_room(301, "Eve", first_in, first_out)

    # Overlapping period
    second_in = today + datetime.timedelta(days=2)
    second_out = today + datetime.timedelta(days=4)

    with pytest.raises(RoomUnavailableError):
        system.book_room(301, "Frank", second_in, second_out)

def test_cancel_reservation_various_refunds():
    today = datetime.date.today()

    # > 7 days before check-in: 100% refund
    sys_full = HotelReservationSystem()
    sys_full.add_room(401, "Standard", 100.0)
    ci_full = today + datetime.timedelta(days=10)
    co_full = ci_full + datetime.timedelta(days=2)
    rid_full = sys_full.book_room(401, "Grace", ci_full, co_full)
    refund_full = sys_full.cancel_reservation(rid_full)
    reservation_full = sys_full.reservations.get(rid_full, None)
    assert reservation_full is None or isinstance(refund_full, float)
    # Since reservation is removed, ensure refund equals total_price observed before removal
    assert refund_full == 2 * 100.0

    # 2-7 days before check-in: 50% refund
    sys_half = HotelReservationSystem()
    sys_half.add_room(402, "Standard", 100.0)
    ci_half = today + datetime.timedelta(days=5)
    co_half = ci_half + datetime.timedelta(days=2)
    rid_half = sys_half.book_room(402, "Heidi", ci_half, co_half)
    refund_half = sys_half.cancel_reservation(rid_half)
    assert refund_half == round(2 * 100.0 * 0.5, 2)

    # < 2 days before check-in: 0% refund
    sys_none = HotelReservationSystem()
    sys_none.add_room(403, "Standard", 100.0)
    ci_none = today + datetime.timedelta(days=1)
    co_none = ci_none + datetime.timedelta(days=2)
    rid_none = sys_none.book_room(403, "Ivan", ci_none, co_none)
    refund_none = sys_none.cancel_reservation(rid_none)
    assert refund_none == 0.0

def test_cancel_reservation_not_found():
    system = HotelReservationSystem()
    with pytest.raises(ReservationNotFoundError):
        system.cancel_reservation("RES-9999")

def test_get_room_occupancy():
    system = HotelReservationSystem()
    system.add_room(501, "Standard", 120.0)
    system.add_room(502, "Standard", 120.0)

    today = datetime.date.today()
    # Room 501 is occupied from +2 to +5
    in1 = today + datetime.timedelta(days=2)
    out1 = today + datetime.timedelta(days=5)
    system.book_room(501, "Jack", in1, out1)

    # Room 502 is occupied from +3 to +6
    in2 = today + datetime.timedelta(days=3)
    out2 = today + datetime.timedelta(days=6)
    system.book_room(502, "Karl", in2, out2)

    # Date with both rooms occupied
    date_both = today + datetime.timedelta(days=3)
    occupancy_both = system.get_room_occupancy(date_both)
    assert occupancy_both == [501, 502]

    # Date where only room 502 is occupied (date = +5 should exclude room 501)
    date_only_502 = today + datetime.timedelta(days=5)
    occupancy_only_502 = system.get_room_occupancy(date_only_502)
    assert occupancy_only_502 == [502]