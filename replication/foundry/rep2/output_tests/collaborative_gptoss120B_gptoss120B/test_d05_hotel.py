import pytest
import datetime
from data.input_code.d05_hotel import *

# Helper to monkeypatch datetime.date.today()
@pytest.fixture(autouse=True)
def fixed_today(monkeypatch):
    fixed = datetime.date(2023, 1, 1)
    class MockDate(datetime.date):
        @classmethod
        def today(cls):
            return fixed
    monkeypatch.setattr(datetime, "date", MockDate)

@pytest.fixture
def system():
    """Fresh HotelReservationSystem for each test."""
    return HotelReservationSystem()

# ---------- add_room ----------
@pytest.mark.parametrize(
    "room_number, room_type, price, expect_exception",
    [
        (101, "Deluxe", 150.0, None),          # T1_ADD_ROOM_OK
        (102, "Standard", 0.0, ValueError),   # T2_ADD_ROOM_INVALID_PRICE
    ],
)
def test_add_room(system, room_number, room_type, price, expect_exception):
    if expect_exception:
        with pytest.raises(expect_exception):
            system.add_room(room_number, room_type, price)
    else:
        system.add_room(room_number, room_type, price)
        assert system.rooms[room_number]["price_per_night"] == price

# ---------- book_room ----------
def test_book_room_not_found(system):
    with pytest.raises(RoomNotFoundError):
        system.book_room(
            room_number=999,
            user_name="Alice",
            check_in=datetime.date(2023, 6, 10),
            check_out=datetime.date(2023, 6, 12),
        )

def test_book_room_invalid_date_order(system):
    system.add_room(101, "Deluxe", 150.0)
    with pytest.raises(InvalidDateError):
        system.book_room(
            room_number=101,
            user_name="Bob",
            check_in=datetime.date(2023, 7, 15),
            check_out=datetime.date(2023, 7, 10),
        )

def test_book_room_past_date(system):
    system.add_room(101, "Deluxe", 150.0)
    # today is fixed to 2023-01-01, so 2022-12-01 is in the past
    with pytest.raises(InvalidDateError):
        system.book_room(
            room_number=101,
            user_name="Carol",
            check_in=datetime.date(2022, 12, 1),
            check_out=datetime.date(2022, 12, 5),
        )

def test_book_room_success_and_unavailable(system):
    system.add_room(101, "Deluxe", 150.0)

    # T6_BOOK_ROOM_SUCCESS
    res_id = system.book_room(
        room_number=101,
        user_name="Dave",
        check_in=datetime.date(2023, 6, 1),
        check_out=datetime.date(2023, 6, 4),
    )
    assert res_id == "RES-0001"
    reservation = system.reservations[res_id]
    assert reservation.total_price == 450.0  # 3 nights * 150

    # T7_BOOK_ROOM_UNAVAILABLE (overlap with previous reservation)
    with pytest.raises(RoomUnavailableError):
        system.book_room(
            room_number=101,
            user_name="Eve",
            check_in=datetime.date(2023, 6, 2),
            check_out=datetime.date(2023, 6, 5),
        )

# ---------- cancel_reservation ----------
@pytest.fixture
def system_with_reservations():
    """System pre‑populated with three reservations for cancellation tests."""
    sys = HotelReservationSystem()
    sys.add_room(101, "Deluxe", 150.0)

    # Helper to create a reservation with given check‑in offset (days from today)
    def make_res(days_until_checkin, nights, expected_id):
        check_in = datetime.date.today() + datetime.timedelta(days=days_until_checkin)
        check_out = check_in + datetime.timedelta(days=nights)
        res_id = sys.book_room(
            room_number=101,
            user_name=f"User-{expected_id}",
            check_in=check_in,
            check_out=check_out,
        )
        assert res_id == expected_id
        return res_id

    # RES-0001: 15 days from today, 3 nights -> total 450, full refund
    make_res(days_until_checkin=15, nights=3, expected_id="RES-0001")
    # RES-0002: 5 days from today, 3 nights -> total 450, 50% refund
    make_res(days_until_checkin=5, nights=3, expected_id="RES-0002")
    # RES-0003: 1 day from today, 2 nights -> total 300, no refund
    make_res(days_until_checkin=1, nights=2, expected_id="RES-0003")
    return sys

def test_cancel_reservation_full_refund(system_with_reservations):
    refund = system_with_reservations.cancel_reservation("RES-0001")
    assert refund == 450.0

def test_cancel_reservation_half_refund(system_with_reservations):
    refund = system_with_reservations.cancel_reservation("RES-0002")
    assert refund == 225.0

def test_cancel_reservation_no_refund(system_with_reservations):
    refund = system_with_reservations.cancel_reservation("RES-0003")
    assert refund == 0.0

def test_cancel_reservation_not_found(system):
    with pytest.raises(ReservationNotFoundError):
        system.cancel_reservation("NONEXISTENT")

# ---------- get_room_occupancy ----------
def test_get_occupancy_occupied(system):
    system.add_room(101, "Deluxe", 150.0)
    system.book_room(
        room_number=101,
        user_name="Dave",
        check_in=datetime.date(2023, 6, 1),
        check_out=datetime.date(2023, 6, 4),
    )
    occupied = system.get_room_occupancy(datetime.date(2023, 6, 2))
    assert occupied == [101]

def test_get_occupancy_empty(system):
    system.add_room(101, "Deluxe", 150.0)
    # No bookings
    empty = system.get_room_occupancy(datetime.date(2023, 7, 1))
    assert empty == []