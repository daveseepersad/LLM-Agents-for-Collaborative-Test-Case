import pytest
import datetime
from data.input_code.d05_hotel import *

@pytest.fixture
def system():
    return HotelReservationSystem()

@pytest.fixture
def system_with_room(system):
    system.add_room(101, "Single", 100.0)
    return system

@pytest.fixture
def system_with_booking(system_with_room):
    check_in = datetime.date.today() + datetime.timedelta(days=1)
    check_out = datetime.date.today() + datetime.timedelta(days=3)
    res_id = system_with_room.book_room(101, "John", check_in, check_out)
    return system_with_room, res_id, check_in, check_out

# ---------- add_room ----------
@pytest.mark.parametrize(
    "room_number, room_type, price, expect_exception",
    [
        (101, "Single", 100.0, None),          # valid
        (102, "Double", 0.0, ValueError),      # invalid price
    ],
)
def test_add_room(room_number, room_type, price, expect_exception, system):
    if expect_exception:
        with pytest.raises(expect_exception):
            system.add_room(room_number, room_type, price)
    else:
        system.add_room(room_number, room_type, price)
        assert room_number in system.rooms
        assert system.rooms[room_number]["price_per_night"] == price

# ---------- book_room ----------
def test_book_room_not_found(system):
    with pytest.raises(RoomNotFoundError):
        system.book_room(
            103,
            "John",
            datetime.date.today() + datetime.timedelta(days=1),
            datetime.date.today() + datetime.timedelta(days=3),
        )

def test_book_room_invalid_dates(system_with_room):
    with pytest.raises(InvalidDateError):
        system_with_room.book_room(
            101,
            "John",
            datetime.date.today() + datetime.timedelta(days=3),
            datetime.date.today() + datetime.timedelta(days=1),
        )

def test_book_room_past_dates(system_with_room):
    with pytest.raises(InvalidDateError):
        system_with_room.book_room(
            101,
            "John",
            datetime.date.today() - datetime.timedelta(days=1),
            datetime.date.today() + datetime.timedelta(days=1),
        )

def test_book_room_success(system_with_room):
    check_in = datetime.date.today() + datetime.timedelta(days=1)
    check_out = datetime.date.today() + datetime.timedelta(days=3)
    res_id = system_with_room.book_room(101, "John", check_in, check_out)
    assert res_id == "RES-0001"
    # verify reservation stored correctly
    reservation = system_with_room.reservations[res_id]
    assert reservation.room_number == 101
    assert reservation.user_name == "John"
    assert reservation.check_in == check_in
    assert reservation.check_out == check_out

def test_book_room_unavailable(system_with_booking):
    system, _, _, _ = system_with_booking
    # overlapping dates
    with pytest.raises(RoomUnavailableError):
        system.book_room(
            101,
            "Jane",
            datetime.date.today() + datetime.timedelta(days=2),
            datetime.date.today() + datetime.timedelta(days=4),
        )

# ---------- cancel_reservation ----------
def test_cancel_reservation_not_found(system):
    with pytest.raises(ReservationNotFoundError):
        system.cancel_reservation("RES-9999")

def test_cancel_reservation_full_refund(system_with_room):
    # create a reservation with check‑in > 7 days away
    check_in = datetime.date.today() + datetime.timedelta(days=10)
    check_out = datetime.date.today() + datetime.timedelta(days=12)
    res_id = system_with_room.book_room(101, "John", check_in, check_out)
    reservation = system_with_room.reservations[res_id]
    refund = system_with_room.cancel_reservation(res_id)
    assert refund == reservation.total_price

def test_cancel_reservation_partial_refund(system):
    # Setup: add room and create a reservation with check‑in 5 days from today
    system.add_room(101, "Single", 50.0)
    check_in = datetime.date.today() + datetime.timedelta(days=5)
    check_out = check_in + datetime.timedelta(days=2)  # 2 nights
    res_id = system.book_room(101, "John", check_in, check_out)
    reservation = system.reservations[res_id]
    # Cancel and expect 50% refund (total_price = 100.0 → refund = 50.0)
    refund = system.cancel_reservation(res_id)
    assert refund == 50.0
    # Ensure reservation is removed
    assert res_id not in system.reservations

def test_cancel_reservation_no_refund(system):
    # Setup: add room and create a reservation with check‑in 1 day from today
    system.add_room(101, "Single", 50.0)
    check_in = datetime.date.today() + datetime.timedelta(days=1)
    check_out = check_in + datetime.timedelta(days=2)  # 2 nights
    res_id = system.book_room(101, "John", check_in, check_out)
    # Cancel and expect no refund
    refund = system.cancel_reservation(res_id)
    assert refund == 0.0
    # Ensure reservation is removed
    assert res_id not in system.reservations

# ---------- get_room_occupancy ----------
def test_get_room_occupancy_occupied(system_with_booking):
    system, _, check_in, check_out = system_with_booking
    target_date = check_in + datetime.timedelta(days=1)  # within the booking range
    occupancy = system.get_room_occupancy(target_date)
    assert occupancy == [101]

def test_get_room_occupancy_empty(system_with_room):
    target_date = datetime.date.today()
    occupancy = system_with_room.get_room_occupancy(target_date)
    assert occupancy == []

def test_get_room_occupancy_boundaries(system):
    # No reservations exist; any date should return empty list
    target_date = datetime.date(2024, 1, 1)
    occupancy = system.get_room_occupancy(target_date)
    assert occupancy == []

def test_add_room_overwrite_price(system):
    # First addition
    system.add_room(101, "Single", 100.0)
    # Overwrite with new price
    system.add_room(101, "Single", 150.0)
    assert system.rooms[101]["price_per_night"] == 150.0

def test_is_room_available_edge_cases(system):
    # Add room and a reservation that ends exactly at the new check‑in date
    system.add_room(101, "Single", 100.0)
    today = datetime.date.today()
    # Existing reservation: today+1 to today+5
    system.book_room(
        101,
        "Alice",
        today + datetime.timedelta(days=1),
        today + datetime.timedelta(days=5),
    )
    # New request: today+5 to today+7 (touches previous checkout, should be available)
    available = system._is_room_available(
        101,
        today + datetime.timedelta(days=5),
        today + datetime.timedelta(days=7),
    )
    assert available is True