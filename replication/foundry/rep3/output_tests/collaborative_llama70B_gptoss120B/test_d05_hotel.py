import pytest
from datetime import date, timedelta
from data.input_code.d05_hotel import *

@pytest.fixture
def fresh_system():
    """Provides a fresh HotelReservationSystem for each test."""
    return HotelReservationSystem()

def test_add_room_success(fresh_system):
    fresh_system.add_room(room_number=1, room_type="single", price_per_night=100.0)
    assert 1 in fresh_system.rooms
    assert fresh_system.rooms[1]["type"] == "single"
    assert fresh_system.rooms[1]["price_per_night"] == 100.0

def test_add_room_invalid_price(fresh_system):
    with pytest.raises(ValueError):
        fresh_system.add_room(room_number=1, room_type="single", price_per_night=-100.0)

@pytest.mark.parametrize(
    "room_number, user_name, check_in, check_out, expected_id",
    [
        (
            1,
            "John Doe",
            date(2024, 9, 20),   # placeholder, will be adjusted in test
            date(2024, 9, 25),   # placeholder, will be adjusted in test
            "RES-0001",
        )
    ],
)
def test_book_room_success(fresh_system, room_number, user_name, check_in, check_out, expected_id):
    # Ensure dates are in the future relative to today
    if check_in <= date.today():
        check_in = date.today() + timedelta(days=10)
        check_out = check_in + timedelta(days=5)

    fresh_system.add_room(room_number=room_number, room_type="single", price_per_night=100.0)
    res_id = fresh_system.book_room(
        room_number=room_number,
        user_name=user_name,
        check_in=check_in,
        check_out=check_out,
    )
    assert res_id == expected_id
    assert res_id in fresh_system.reservations

@pytest.mark.parametrize(
    "room_number, user_name, check_in, check_out, exc",
    [
        (2, "John Doe", date(2024, 9, 20), date(2024, 9, 25), RoomNotFoundError),
        (1, "John Doe", date(2024, 9, 25), date(2024, 9, 20), InvalidDateError),
        (1, "John Doe", date.today() - timedelta(days=1), date.today() + timedelta(days=4), InvalidDateError),
    ],
)
def test_book_room_errors(fresh_system, room_number, user_name, check_in, check_out, exc):
    if room_number == 1:
        fresh_system.add_room(room_number=1, room_type="single", price_per_night=100.0)
    with pytest.raises(exc):
        fresh_system.book_room(
            room_number=room_number,
            user_name=user_name,
            check_in=check_in,
            check_out=check_out,
        )

def test_cancel_reservation_full_refund(fresh_system):
    fresh_system.add_room(room_number=1, room_type="single", price_per_night=100.0)
    future_check_in = date.today() + timedelta(days=10)
    future_check_out = future_check_in + timedelta(days=5)
    res_id = fresh_system.book_room(
        room_number=1,
        user_name="John Doe",
        check_in=future_check_in,
        check_out=future_check_out,
    )
    refund = fresh_system.cancel_reservation(res_id)
    assert refund == 500.0

def test_cancel_reservation_not_found(fresh_system):
    with pytest.raises(ReservationNotFoundError):
        fresh_system.cancel_reservation("RES-0002")

def test_get_room_occupancy(fresh_system):
    fresh_system.add_room(room_number=1, room_type="single", price_per_night=100.0)
    check_in = date.today() + timedelta(days=20)
    check_out = check_in + timedelta(days=5)
    fresh_system.book_room(
        room_number=1,
        user_name="John Doe",
        check_in=check_in,
        check_out=check_out,
    )
    query_date = check_in + timedelta(days=2)
    occupancy = fresh_system.get_room_occupancy(query_date)
    assert occupancy == [1]

@pytest.mark.parametrize(
    "existing_res, query_check_in, query_check_out, expected",
    [
        (None, date(2024, 9, 20), date(2024, 9, 25), True),
        (
            Reservation(
                reservation_id="RES-0001",
                room_number=1,
                user_name="John Doe",
                check_in=date(2024, 9, 20),
                check_out=date(2024, 9, 25),
                total_price=500.0,
            ),
            date(2024, 9, 22),
            date(2024, 9, 27),
            False,
        ),
    ],
)
def test_is_room_available(fresh_system, existing_res, query_check_in, query_check_out, expected):
    fresh_system.add_room(room_number=1, room_type="single", price_per_night=100.0)

    # Shift dates to the future if they are in the past
    today = date.today()
    if query_check_in <= today:
        offset = (today - query_check_in).days + 10
        query_check_in = query_check_in + timedelta(days=offset)
        query_check_out = query_check_out + timedelta(days=offset)

    if existing_res:
        # Adjust existing reservation dates similarly
        if existing_res.check_in <= today:
            offset = (today - existing_res.check_in).days + 10
            existing_res = Reservation(
                reservation_id=existing_res.reservation_id,
                room_number=existing_res.room_number,
                user_name=existing_res.user_name,
                check_in=existing_res.check_in + timedelta(days=offset),
                check_out=existing_res.check_out + timedelta(days=offset),
                total_price=existing_res.total_price,
            )
        fresh_system.reservations[existing_res.reservation_id] = existing_res

    availability = fresh_system._is_room_available(
        room_number=1,
        check_in=query_check_in,
        check_out=query_check_out,
    )
    assert availability is expected

import pytest
from datetime import date, timedelta
from data.input_code.d05_hotel import *

def test_cancel_reservation_50_percent_refund(fresh_system):
    # Setup: reservation with check-in 5 days from today (2 <= days <= 7)
    fresh_system.add_room(room_number=1, room_type="single", price_per_night=100.0)
    check_in = date.today() + timedelta(days=5)
    check_out = check_in + timedelta(days=3)
    res_id = fresh_system.book_room(
        room_number=1,
        user_name="Alice",
        check_in=check_in,
        check_out=check_out,
    )
    # Cancel and expect 50% refund
    refund = fresh_system.cancel_reservation(res_id)
    expected_total = round((check_out - check_in).days * 100.0, 2)
    assert refund == round(expected_total * 0.5, 2)

def test_cancel_reservation_no_refund(fresh_system):
    # Setup: reservation with check-in 1 day from today (<2 days)
    fresh_system.add_room(room_number=1, room_type="single", price_per_night=100.0)
    check_in = date.today() + timedelta(days=1)
    check_out = check_in + timedelta(days=3)
    res_id = fresh_system.book_room(
        room_number=1,
        user_name="Bob",
        check_in=check_in,
        check_out=check_out,
    )
    # Cancel and expect 0 refund
    refund = fresh_system.cancel_reservation(res_id)
    assert refund == 0.0

def test_book_room_unavailable(fresh_system):
    # Create an existing reservation that occupies the target dates
    fresh_system.add_room(room_number=1, room_type="single", price_per_night=100.0)
    existing_check_in = date.today() + timedelta(days=10)
    existing_check_out = existing_check_in + timedelta(days=5)
    fresh_system.book_room(
        room_number=1,
        user_name="Carol",
        check_in=existing_check_in,
        check_out=existing_check_out,
    )
    # Attempt to book overlapping dates
    overlapping_check_in = existing_check_in + timedelta(days=2)
    overlapping_check_out = overlapping_check_in + timedelta(days=4)
    with pytest.raises(RoomUnavailableError):
        fresh_system.book_room(
            room_number=1,
            user_name="Dave",
            check_in=overlapping_check_in,
            check_out=overlapping_check_out,
        )

def test_get_room_occupancy_no_reservations(fresh_system):
    query_date = date.fromisoformat("2024-09-20")
    # Ensure the date is in the future relative to today
    if query_date <= date.today():
        query_date = date.today() + timedelta(days=30)
    occupancy = fresh_system.get_room_occupancy(query_date)
    assert occupancy == []

def test_get_room_occupancy_multiple_reservations(fresh_system):
    # Add two rooms
    fresh_system.add_room(room_number=1, room_type="single", price_per_night=100.0)
    fresh_system.add_room(room_number=2, room_type="double", price_per_night=150.0)

    # Define a common query date in the future
    query_date = date.today() + timedelta(days=20)

    # Reservation for room 1 covering query_date
    fresh_system.book_room(
        room_number=1,
        user_name="Eve",
        check_in=query_date - timedelta(days=2),
        check_out=query_date + timedelta(days=3),
    )
    # Reservation for room 2 also covering query_date
    fresh_system.book_room(
        room_number=2,
        user_name="Frank",
        check_in=query_date - timedelta(days=1),
        check_out=query_date + timedelta(days=4),
    )

    occupancy = fresh_system.get_room_occupancy(query_date)
    assert occupancy == [1, 2]