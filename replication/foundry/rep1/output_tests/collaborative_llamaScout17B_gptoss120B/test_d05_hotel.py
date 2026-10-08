import pytest
import datetime
from data.input_code.d05_hotel import *

@pytest.fixture
def system():
    """Provides a fresh HotelReservationSystem for each test."""
    return HotelReservationSystem()

def test_init(system):
    assert system.rooms == {}
    assert system.reservations == {}
    assert system._reservation_counter == 0

def test_add_room_valid(system):
    system.add_room(room_number=101, room_type="Single", price_per_night=100.0)
    assert 101 in system.rooms
    assert system.rooms[101]["type"] == "Single"
    assert system.rooms[101]["price_per_night"] == 100.0

@pytest.mark.parametrize(
    "price,exc",
    [
        (-10.0, ValueError),
        (0.0, ValueError),
    ],
)
def test_add_room_invalid_price(system, price, exc):
    with pytest.raises(exc):
        system.add_room(room_number=102, room_type="Double", price_per_night=price)

def test_book_room_nonexistent(system):
    with pytest.raises(RoomNotFoundError):
        system.book_room(
            room_number=999,
            user_name="John",
            check_in=datetime.date.today() + datetime.timedelta(days=1),
            check_out=datetime.date.today() + datetime.timedelta(days=3),
        )

def test_book_room_invalid_dates(system):
    system.add_room(101, "Single", 100.0)
    with pytest.raises(InvalidDateError):
        system.book_room(
            room_number=101,
            user_name="John",
            check_in=datetime.date.today() + datetime.timedelta(days=3),
            check_out=datetime.date.today() + datetime.timedelta(days=1),
        )

def test_book_room_past(system):
    system.add_room(101, "Single", 100.0)
    with pytest.raises(InvalidDateError):
        system.book_room(
            room_number=101,
            user_name="John",
            check_in=datetime.date.today() - datetime.timedelta(days=1),
            check_out=datetime.date.today() + datetime.timedelta(days=1),
        )

def test_book_room_success(system):
    system.add_room(101, "Single", 100.0)
    check_in = datetime.date.today() + datetime.timedelta(days=1)
    check_out = datetime.date.today() + datetime.timedelta(days=3)
    res_id = system.book_room(101, "John", check_in, check_out)
    assert isinstance(res_id, str)
    assert res_id.startswith("RES-")
    reservation = system.reservations[res_id]
    assert reservation.room_number == 101
    assert reservation.user_name == "John"
    assert reservation.check_in == check_in
    assert reservation.check_out == check_out
    expected_price = round((check_out - check_in).days * 100.0, 2)
    assert reservation.total_price == expected_price

def test_book_room_unavailable(system):
    system.add_room(101, "Single", 100.0)
    ci = datetime.date.today() + datetime.timedelta(days=1)
    co = datetime.date.today() + datetime.timedelta(days=3)
    # first booking succeeds
    system.book_room(101, "John", ci, co)
    # second booking overlapping same dates should fail
    with pytest.raises(RoomUnavailableError):
        system.book_room(101, "Jane", ci, co)

def test_cancel_nonexistent(system):
    with pytest.raises(ReservationNotFoundError):
        system.cancel_reservation("RES-0001")

def _make_reservation(system, check_in_offset, check_out_offset, user_name="User"):
    """Helper to add a room and create a reservation with given offsets."""
    system.add_room(101, "Single", 100.0)
    check_in = datetime.date.today() + datetime.timedelta(days=check_in_offset)
    check_out = datetime.date.today() + datetime.timedelta(days=check_out_offset)
    return system.book_room(101, user_name, check_in, check_out), check_in, check_out

def test_cancel_valid_full_refund(system):
    # reservation >7 days away → full refund
    res_id, check_in, _ = _make_reservation(system, 10, 12)
    reservation = system.reservations[res_id]
    refund = system.cancel_reservation(res_id)
    assert refund == reservation.total_price

def test_get_room_occupancy(system):
    system.add_room(101, "Single", 100.0)
    ci = datetime.date.today() + datetime.timedelta(days=1)
    co = datetime.date.today() + datetime.timedelta(days=4)
    res_id = system.book_room(101, "John", ci, co)
    # date within the reservation period
    target_date = datetime.date.today() + datetime.timedelta(days=2)
    occupied = system.get_room_occupancy(target_date)
    assert occupied == [101]
    # date after checkout should be empty
    after_date = datetime.date.today() + datetime.timedelta(days=5)
    assert system.get_room_occupancy(after_date) == []

@pytest.mark.parametrize(
    "check_in_offset,expected_refund_factor",
    [
        (10, 1.0),   # >7 days → 100%
        (5, 0.5),    # 2‑7 days → 50%
        (1, 0.0),    # <2 days → 0%
    ],
)
def test_cancel_refund_policy(system, check_in_offset, expected_refund_factor):
    # create reservation with 2‑night stay
    res_id, check_in, check_out = _make_reservation(
        system,
        check_in_offset,
        check_in_offset + 2,
        user_name=f"User{check_in_offset}"
    )
    reservation = system.reservations[res_id]
    expected_refund = round(reservation.total_price * expected_refund_factor, 2)
    refund = system.cancel_reservation(res_id)
    assert refund == expected_refund