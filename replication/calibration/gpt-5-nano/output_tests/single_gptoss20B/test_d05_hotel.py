import pytest
import datetime
from data.input_code.d05_hotel import (
    HotelReservationSystem,
    RoomNotFoundError,
    RoomUnavailableError,
    InvalidDateError,
    ReservationNotFoundError
)

def test_add_room_and_price_validation():
    system = HotelReservationSystem()
    system.add_room(101, "Deluxe", 150.0)
    assert 101 in system.rooms
    assert system.rooms[101]['price_per_night'] == 150.0

    with pytest.raises(ValueError):
        system.add_room(102, "Standard", 0)

def test_book_room_success_and_occupancy():
    system = HotelReservationSystem()
    system.add_room(101, "Deluxe", 100.0)
    today = datetime.date.today()
    check_in = today + datetime.timedelta(days=1)
    check_out = today + datetime.timedelta(days=3)

    res_id = system.book_room(101, "Alice", check_in, check_out)
    assert res_id == "RES-0001"
    assert res_id in system.reservations

    res = system.reservations[res_id]
    assert res.room_number == 101
    assert res.user_name == "Alice"
    assert res.check_in == check_in
    assert res.check_out == check_out
    assert res.total_price == round((check_out - check_in).days * system.rooms[101]['price_per_night'], 2)

    occupancy_date = today + datetime.timedelta(days=2)
    occupied = system.get_room_occupancy(occupancy_date)
    assert 101 in occupied

def test_book_room_missing_room_raises():
    system = HotelReservationSystem()
    with pytest.raises(RoomNotFoundError):
        today = datetime.date.today()
        system.book_room(999, "Bob", today + datetime.timedelta(days=1), today + datetime.timedelta(days=2))

def test_book_room_invalid_dates():
    system = HotelReservationSystem()
    system.add_room(201, "Suite", 200.0)
    today = datetime.date.today()

    # check_out before check_in
    with pytest.raises(InvalidDateError):
        system.book_room(201, "Chris", today + datetime.timedelta(days=2), today + datetime.timedelta(days=1))

    # check_in in the past
    with pytest.raises(InvalidDateError):
        system.book_room(201, "Chris", today - datetime.timedelta(days=1), today + datetime.timedelta(days=1))

def test_room_unavailability_on_overlap():
    system = HotelReservationSystem()
    system.add_room(301, "Standard", 120.0)
    today = datetime.date.today()
    check_in_1 = today + datetime.timedelta(days=2)
    check_out_1 = today + datetime.timedelta(days=5)
    system.book_room(301, "Dana", check_in_1, check_out_1)

    # Overlapping reservation should fail
    with pytest.raises(RoomUnavailableError):
        system.book_room(301, "Eli", today + datetime.timedelta(days=3), today + datetime.timedelta(days=6))

def test_cancel_reservation_full_partial_none_refunds():
    # Full refund (>7 days)
    system_full = HotelReservationSystem()
    system_full.add_room(401, "Deluxe", 100.0)
    today = datetime.date.today()
    check_in = today + datetime.timedelta(days=10)
    check_out = today + datetime.timedelta(days=12)
    res_id_full = system_full.book_room(401, "Frank", check_in, check_out)
    total_full = system_full.reservations[res_id_full].total_price
    refunded_full = system_full.cancel_reservation(res_id_full)
    assert refunded_full == total_full
    assert res_id_full not in system_full.reservations

    # 2-7 days => 50% refund
    system_half = HotelReservationSystem()
    system_half.add_room(402, "Standard", 80.0)
    check_in_half = today + datetime.timedelta(days=5)
    check_out_half = today + datetime.timedelta(days=7)
    res_id_half = system_half.book_room(402, "Grace", check_in_half, check_out_half)
    total_half = system_half.reservations[res_id_half].total_price
    refunded_half = system_half.cancel_reservation(res_id_half)
    assert refunded_half == round(total_half * 0.5, 2)
    assert res_id_half not in system_half.reservations

    # <2 days => 0% refund
    system_none = HotelReservationSystem()
    system_none.add_room(501, "Economy", 60.0)
    check_in_none = today + datetime.timedelta(days=1)
    check_out_none = today + datetime.timedelta(days=2)
    res_id_none = system_none.book_room(501, "Hank", check_in_none, check_out_none)
    total_none = system_none.reservations[res_id_none].total_price
    refunded_none = system_none.cancel_reservation(res_id_none)
    assert refunded_none == 0.0
    assert res_id_none not in system_none.reservations

def test_cancel_reservation_non_existent_raises():
    system = HotelReservationSystem()
    with pytest.raises(ReservationNotFoundError):
        system.cancel_reservation("RES-9999")

def test_get_room_occupancy_boundaries():
    system = HotelReservationSystem()
    system.add_room(601, "Deluxe", 150.0)
    system.add_room(602, "Deluxe", 150.0)
    today = datetime.date.today()

    r1_in = today + datetime.timedelta(days=1)
    r1_out = today + datetime.timedelta(days=3)

    r2_in = today + datetime.timedelta(days=2)
    r2_out = today + datetime.timedelta(days=4)

    id1 = system.book_room(601, "Ian", r1_in, r1_out)
    id2 = system.book_room(602, "Jen", r2_in, r2_out)

    mid_date = today + datetime.timedelta(days=2)
    occupancy_mid = system.get_room_occupancy(mid_date)
    assert 601 in occupancy_mid and 602 in occupancy_mid

    # Boundary: date equal to r1_out should not include 601 (since check_out is exclusive)
    boundary_date = r1_out
    occupancy_boundary = system.get_room_occupancy(boundary_date)
    assert 601 not in occupancy_boundary
    assert 602 in occupancy_boundary