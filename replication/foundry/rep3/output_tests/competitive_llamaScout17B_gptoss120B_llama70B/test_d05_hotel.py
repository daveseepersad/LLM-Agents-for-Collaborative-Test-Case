import pytest
import datetime
from data.input_code.d05_hotel import *

@pytest.fixture
def empty_system():
    """Provides a fresh HotelReservationSystem instance."""
    return HotelReservationSystem()

@pytest.fixture
def system_with_room(empty_system):
    """System with a valid room (101) added."""
    empty_system.add_room(room_number=101, room_type="Single", price_per_night=100.0)
    return empty_system

@pytest.fixture
def system_with_booking(system_with_room):
    """System with one successful booking for room 101 (today+1 to today+3)."""
    check_in = datetime.date.today() + datetime.timedelta(days=1)
    check_out = datetime.date.today() + datetime.timedelta(days=3)
    res_id = system_with_room.book_room(
        room_number=101,
        user_name="John",
        check_in=check_in,
        check_out=check_out,
    )
    return system_with_room, res_id, check_in, check_out

def test_init():
    """T1_INIT – Initialize empty system."""
    HotelReservationSystem()  # should not raise

@pytest.mark.parametrize(
    "room_number, room_type, price, expected",
    [
        (101, "Single", 100.0, None),  # T2_ADD_ROOM_VALID
    ],
)
def test_add_room_valid(system_with_room, room_number, room_type, price, expected):
    # room already added in fixture; just verify presence
    assert room_number in system_with_room.rooms
    assert system_with_room.rooms[room_number]["type"] == room_type
    assert system_with_room.rooms[room_number]["price_per_night"] == price

@pytest.mark.parametrize(
    "room_number, room_type, price, exc",
    [
        (102, "Double", -50.0, ValueError),  # T3_ADD_ROOM_INVALID_PRICE
    ],
)
def test_add_room_invalid_price(empty_system, room_number, room_type, price, exc):
    with pytest.raises(exc):
        empty_system.add_room(room_number=room_number, room_type=room_type, price_per_night=price)

def test_book_room_nonexistent(empty_system):
    """T4_BOOK_ROOM_NONEXISTENT – Attempt to book a room that hasn't been added."""
    check_in = datetime.date.today() + datetime.timedelta(days=1)
    check_out = datetime.date.today() + datetime.timedelta(days=3)
    with pytest.raises(RoomNotFoundError):
        empty_system.book_room(
            room_number=103,
            user_name="John",
            check_in=check_in,
            check_out=check_out,
        )

def test_book_room_invalid_dates(system_with_room):
    """T5_BOOK_ROOM_INVALID_DATES – Check-out before check-in."""
    check_in = datetime.date.today() + datetime.timedelta(days=3)
    check_out = datetime.date.today() + datetime.timedelta(days=1)
    with pytest.raises(InvalidDateError):
        system_with_room.book_room(
            room_number=101,
            user_name="John",
            check_in=check_in,
            check_out=check_out,
        )

def test_book_room_past(system_with_room):
    """T6_BOOK_ROOM_PAST – Booking dates in the past."""
    check_in = datetime.date.today() - datetime.timedelta(days=1)
    check_out = datetime.date.today() + datetime.timedelta(days=1)
    with pytest.raises(InvalidDateError):
        system_with_room.book_room(
            room_number=101,
            user_name="John",
            check_in=check_in,
            check_out=check_out,
        )

def test_book_room_success(system_with_room):
    """T7_BOOK_ROOM_SUCCESS – Successful booking returns correct reservation ID."""
    check_in = datetime.date.today() + datetime.timedelta(days=1)
    check_out = datetime.date.today() + datetime.timedelta(days=3)
    res_id = system_with_room.book_room(
        room_number=101,
        user_name="John",
        check_in=check_in,
        check_out=check_out,
    )
    assert res_id == "RES-0001"
    # Verify reservation stored correctly
    reservation = system_with_room.reservations[res_id]
    assert reservation.room_number == 101
    assert reservation.user_name == "John"
    assert reservation.check_in == check_in
    assert reservation.check_out == check_out
    assert reservation.total_price == 200.0  # 2 nights * $100

def test_book_room_unavailable(system_with_booking):
    """T8_BOOK_ROOM_UNAVAILABLE – Overlapping reservation should raise error."""
    system, _, _, _ = system_with_booking
    overlapping_check_in = datetime.date.today() + datetime.timedelta(days=2)
    overlapping_check_out = datetime.date.today() + datetime.timedelta(days=4)
    with pytest.raises(RoomUnavailableError):
        system.book_room(
            room_number=101,
            user_name="Jane",
            check_in=overlapping_check_in,
            check_out=overlapping_check_out,
        )

def test_cancel_nonexistent(empty_system):
    """T9_CANCEL_NONEXISTENT – Cancel a reservation that does not exist."""
    with pytest.raises(ReservationNotFoundError):
        empty_system.cancel_reservation("RES-9999")

def test_cancel_full_refund():
    """T10_CANCEL_FULL_REFUND – Cancel >7 days before check-in yields full refund."""
    system = HotelReservationSystem()
    system.add_room(room_number=101, room_type="Single", price_per_night=100.0)
    check_in = datetime.date.today() + datetime.timedelta(days=10)
    check_out = datetime.date.today() + datetime.timedelta(days=12)
    res_id = system.book_room(
        room_number=101,
        user_name="Alice",
        check_in=check_in,
        check_out=check_out,
    )
    refund = system.cancel_reservation(res_id)
    assert refund == 200.0  # 2 nights * $100, full refund

def test_get_occupancy(system_with_booking):
    """T11_GET_OCCUPANCY – Verify occupied rooms on a specific date."""
    system, _, _, _ = system_with_booking
    target_date = datetime.date.today() + datetime.timedelta(days=2)
    occupied = system.get_room_occupancy(target_date)
    assert occupied == [101]

import pytest
import datetime
from data.input_code.d05_hotel import *

def test_cancel_partial_refund(system_with_room):
    """T_MISSING_PARTIAL_REFUND – Cancellation 2-7 days before check-in yields 50% refund."""
    # Book a reservation 5 days from today (within 2-7 day window)
    check_in = datetime.date.today() + datetime.timedelta(days=5)
    check_out = datetime.date.today() + datetime.timedelta(days=7)
    res_id = system_with_room.book_room(
        room_number=101,
        user_name="Bob",
        check_in=check_in,
        check_out=check_out,
    )
    refund = system_with_room.cancel_reservation(res_id)
    # Total price = 2 nights * $100 = $200, 50% refund = $100
    assert refund == 100.0

def test_cancel_no_refund(system_with_room):
    """T_MISSING_NO_REFUND – Cancellation less than 2 days before check-in yields no refund."""
    # Book a reservation 1 day from today (less than 2 days)
    check_in = datetime.date.today() + datetime.timedelta(days=1)
    check_out = datetime.date.today() + datetime.timedelta(days=3)
    res_id = system_with_room.book_room(
        room_number=101,
        user_name="Carol",
        check_in=check_in,
        check_out=check_out,
    )
    refund = system_with_room.cancel_reservation(res_id)
    assert refund == 0.0

def test_is_room_available_edge():
    """T_MISSING_ROOM_AVAILABILITY_EDGE – Room should be available on another reservation's check-out date."""
    system = HotelReservationSystem()
    system.add_room(room_number=101, room_type="Single", price_per_night=100.0)
    # Existing reservation ends on 2024-01-01
    existing_res = Reservation(
        reservation_id="RES-0001",
        room_number=101,
        user_name="Existing",
        check_in=datetime.date(2023, 12, 30),
        check_out=datetime.date(2024, 1, 1),
        total_price=200.0,
    )
    system.reservations[existing_res.reservation_id] = existing_res
    # Check availability starting exactly at previous check-out
    available = system._is_room_available(
        room_number=101,
        check_in=datetime.date(2024, 1, 1),
        check_out=datetime.date(2024, 1, 2),
    )
    assert available is True

def test_get_room_occupancy_empty(empty_system):
    """T_MISSING_GET_OCCUPANCY_EMPTY – Occupancy list should be empty when no reservations exist."""
    occupancy = empty_system.get_room_occupancy(datetime.date.today())
    assert occupancy == []

def test_add_room_overwrite(system_with_room):
    """T_MISSING_BOOK_ROOM_OVERWRITE – Adding a room with an existing number overwrites its data."""
    system_with_room.add_room(room_number=101, room_type="Single", price_per_night=150.0)
    assert system_with_room.rooms[101]["price_per_night"] == 150.0

def test_book_room_adjacent_dates(system_with_booking):
    """T_MISSING_BOOK_ROOM_ADJACENT_DATES – Booking allowed when check-in equals another reservation's check-out."""
    system, _, _, _ = system_with_booking
    # Existing reservation occupies days today+1 to today+3 (check_out = today+3)
    new_check_in = datetime.date.today() + datetime.timedelta(days=3)
    new_check_out = datetime.date.today() + datetime.timedelta(days=5)
    res_id = system.book_room(
        room_number=101,
        user_name="Jane",
        check_in=new_check_in,
        check_out=new_check_out,
    )
    assert res_id == "RES-0002"