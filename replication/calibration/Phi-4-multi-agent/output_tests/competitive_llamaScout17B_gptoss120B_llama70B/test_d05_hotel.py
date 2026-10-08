import pytest
import datetime
from datetime import timedelta
from data.input_code.d05_hotel import *

@pytest.fixture
def system():
    """Provides a fresh HotelReservationSystem with a default room."""
    hrs = HotelReservationSystem()
    hrs.add_room(room_number=101, room_type="Deluxe", price_per_night=150.0)
    return hrs

def test_add_room_valid():
    hrs = HotelReservationSystem()
    # No exception expected
    hrs.add_room(room_number=202, room_type="Suite", price_per_night=200.0)
    assert hrs.rooms[202]["type"] == "Suite"
    assert hrs.rooms[202]["price_per_night"] == 200.0

@pytest.mark.parametrize(
    "room_number, room_type, price, exc",
    [
        (102, "Suite", -50.0, ValueError),
    ],
)
def test_add_room_invalid_price(room_number, room_type, price, exc):
    hrs = HotelReservationSystem()
    with pytest.raises(exc):
        hrs.add_room(room_number=room_number, room_type=room_type, price_per_night=price)

def test_book_room_valid(system):
    today = datetime.date.today()
    check_in = today + timedelta(days=10)
    check_out = check_in + timedelta(days=4)
    res_id = system.book_room(
        room_number=101,
        user_name="John Doe",
        check_in=check_in,
        check_out=check_out,
    )
    assert res_id == "RES-0001"
    reservation = system.reservations[res_id]
    expected_price = round((check_out - check_in).days * 150.0, 2)
    assert reservation.total_price == expected_price

def test_book_room_nonexistent(system):
    today = datetime.date.today()
    check_in = today + timedelta(days=10)
    check_out = check_in + timedelta(days=4)
    with pytest.raises(RoomNotFoundError):
        system.book_room(
            room_number=999,
            user_name="Jane Doe",
            check_in=check_in,
            check_out=check_out,
        )

def test_book_room_invalid_dates_order(system):
    today = datetime.date.today()
    check_in = today + timedelta(days=10)
    check_out = check_in - timedelta(days=5)  # checkout before checkin
    with pytest.raises(InvalidDateError):
        system.book_room(
            room_number=101,
            user_name="Alice",
            check_in=check_in,
            check_out=check_out,
        )

def test_book_room_past_dates(system):
    today = datetime.date.today()
    check_in = today - timedelta(days=10)
    check_out = today - timedelta(days=5)
    with pytest.raises(InvalidDateError):
        system.book_room(
            room_number=101,
            user_name="Bob",
            check_in=check_in,
            check_out=check_out,
        )

def test_book_room_unavailable(system):
    today = datetime.date.today()
    # First reservation
    check_in1 = today + timedelta(days=10)
    check_out1 = check_in1 + timedelta(days=4)
    system.book_room(
        room_number=101,
        user_name="First Guest",
        check_in=check_in1,
        check_out=check_out1,
    )
    # Overlapping second reservation
    check_in2 = today + timedelta(days=12)
    check_out2 = check_in2 + timedelta(days=3)
    with pytest.raises(RoomUnavailableError):
        system.book_room(
            room_number=101,
            user_name="Charlie",
            check_in=check_in2,
            check_out=check_out2,
        )

def test_cancel_reservation_full_refund(system):
    today = datetime.date.today()
    check_in = today + timedelta(days=20)   # >7 days away
    check_out = check_in + timedelta(days=5)
    res_id = system.book_room(
        room_number=101,
        user_name="Dana",
        check_in=check_in,
        check_out=check_out,
    )
    refund = system.cancel_reservation(reservation_id=res_id)
    # Full refund expected
    expected_price = round((check_out - check_in).days * 150.0, 2)
    assert refund == expected_price

def test_cancel_reservation_not_found(system):
    with pytest.raises(ReservationNotFoundError):
        system.cancel_reservation(reservation_id="RES-9999")

def test_get_room_occupancy_valid(system):
    today = datetime.date.today()
    check_in = today + timedelta(days=10)
    check_out = check_in + timedelta(days=4)
    system.book_room(
        room_number=101,
        user_name="Eve",
        check_in=check_in,
        check_out=check_out,
    )
    occupancy_date = check_in + timedelta(days=2)  # within reservation
    occupied = system.get_room_occupancy(date=occupancy_date)
    assert occupied == [101]

def test_get_room_occupancy_none(system):
    occupancy_date = datetime.date.today() - timedelta(days=1)  # past date, no reservation
    occupied = system.get_room_occupancy(date=occupancy_date)
    assert occupied == []

import pytest
import datetime
from datetime import timedelta

@pytest.mark.parametrize(
    "days_until_checkin, expected_refund",
    [
        (5, 75.0),   # 2-7 days before check-in -> 50% refund
        (1, 0.0),    # less than 2 days before check-in -> no refund
    ],
)
def test_cancel_reservation_refund_variants(system, days_until_checkin, expected_refund):
    today = datetime.date.today()
    check_in = today + timedelta(days=days_until_checkin)
    check_out = check_in + timedelta(days=1)  # one night stay
    res_id = system.book_room(
        room_number=101,
        user_name="Test Guest",
        check_in=check_in,
        check_out=check_out,
    )
    refund = system.cancel_reservation(reservation_id=res_id)
    assert refund == expected_refund


def test_get_room_occupancy_multiple(system):
    # Add a second room
    system.add_room(room_number=202, room_type="Suite", price_per_night=200.0)

    # Manually insert reservations covering 2023-10-12 for both rooms
    res1 = Reservation(
        reservation_id="RES-0001",
        room_number=101,
        user_name="Guest A",
        check_in=datetime.date(2023, 10, 12),
        check_out=datetime.date(2023, 10, 15),
        total_price=0.0,
    )
    res2 = Reservation(
        reservation_id="RES-0002",
        room_number=202,
        user_name="Guest B",
        check_in=datetime.date(2023, 10, 12),
        check_out=datetime.date(2023, 10, 14),
        total_price=0.0,
    )
    system.reservations[res1.reservation_id] = res1
    system.reservations[res2.reservation_id] = res2

    occupied = system.get_room_occupancy(date=datetime.date(2023, 10, 12))
    assert occupied == [101, 202]


def test_get_room_occupancy_overlap(system):
    # Add a second room
    system.add_room(room_number=202, room_type="Suite", price_per_night=200.0)

    # Reservation for room 101 that includes 2023-10-13
    res1 = Reservation(
        reservation_id="RES-0001",
        room_number=101,
        user_name="Guest A",
        check_in=datetime.date(2023, 10, 12),
        check_out=datetime.date(2023, 10, 14),
        total_price=0.0,
    )
    # Reservation for room 202 that ends before 2023-10-13
    res2 = Reservation(
        reservation_id="RES-0002",
        room_number=202,
        user_name="Guest B",
        check_in=datetime.date(2023, 10, 10),
        check_out=datetime.date(2023, 10, 12),
        total_price=0.0,
    )
    system.reservations[res1.reservation_id] = res1
    system.reservations[res2.reservation_id] = res2

    occupied = system.get_room_occupancy(date=datetime.date(2023, 10, 13))
    assert occupied == [101]