import datetime
import pytest
from data.input_code.d05_hotel import (
    HotelReservationSystem,
    RoomNotFoundError,
    RoomUnavailableError,
    InvalidDateError,
    ReservationNotFoundError,
)


@pytest.fixture
def fixed_today(monkeypatch):
    """Patch datetime.date.today() to return a constant date."""
    fixed = datetime.date(2023, 1, 1)
    class FixedDate(datetime.date):
        @classmethod
        def today(cls):
            return fixed
    monkeypatch.setattr(datetime, "date", FixedDate)
    return fixed


def test_add_room_and_overwrite(fixed_today):
    hrs = HotelReservationSystem()
    # Normal addition
    hrs.add_room(101, "single", 100.0)
    assert hrs.rooms[101]["price_per_night"] == 100.0
    # Overwrite with new price
    hrs.add_room(101, "single", 150.0)
    assert hrs.rooms[101]["price_per_night"] == 150.0
    # Invalid price raises
    with pytest.raises(ValueError):
        hrs.add_room(102, "double", 0)


def test_book_room_success_and_price_calculation(fixed_today):
    hrs = HotelReservationSystem()
    hrs.add_room(201, "double", 80.0)
    check_in = fixed_today + datetime.timedelta(days=5)
    check_out = check_in + datetime.timedelta(days=3)  # 3 nights
    res_id = hrs.book_room(201, "Alice", check_in, check_out)
    assert res_id.startswith("RES-")
    reservation = hrs.reservations[res_id]
    assert reservation.total_price == round(3 * 80.0, 2)
    # Ensure reservation stored correctly
    assert reservation.user_name == "Alice"
    assert reservation.room_number == 201


def test_book_room_errors(fixed_today):
    hrs = HotelReservationSystem()
    hrs.add_room(301, "suite", 200.0)

    # Non‑existent room
    with pytest.raises(RoomNotFoundError):
        hrs.book_room(999, "Bob", fixed_today + datetime.timedelta(days=1), fixed_today + datetime.timedelta(days=2))

    # Invalid date range (check_in >= check_out)
    with pytest.raises(InvalidDateError):
        hrs.book_room(301, "Bob", fixed_today + datetime.timedelta(days=2), fixed_today + datetime.timedelta(days=2))

    # Booking in the past
    past = fixed_today - datetime.timedelta(days=1)
    future = fixed_today + datetime.timedelta(days=1)
    with pytest.raises(InvalidDateError):
        hrs.book_room(301, "Bob", past, future)

    # Room unavailable due to overlap
    check_in = fixed_today + datetime.timedelta(days=10)
    check_out = check_in + datetime.timedelta(days=5)
    res_id = hrs.book_room(301, "Bob", check_in, check_out)
    # Overlapping request
    with pytest.raises(RoomUnavailableError):
        hrs.book_room(301, "Carol", check_in + datetime.timedelta(days=2), check_out + datetime.timedelta(days=2))


def test_cancel_reservation_refund_policy(fixed_today):
    hrs = HotelReservationSystem()
    hrs.add_room(401, "deluxe", 120.0)

    # Helper to create reservation with specific check‑in offset
    def make_res(days_until_checkin):
        check_in = fixed_today + datetime.timedelta(days=days_until_checkin)
        check_out = check_in + datetime.timedelta(days=2)
        res_id = hrs.book_room(401, "Dave", check_in, check_out)
        return res_id, hrs.reservations[res_id].total_price

    # >7 days: full refund
    res_id, price = make_res(10)
    refund = hrs.cancel_reservation(res_id)
    assert refund == price

    # 2‑7 days: 50% refund (test middle value)
    res_id, price = make_res(5)
    refund = hrs.cancel_reservation(res_id)
    assert refund == round(price * 0.5, 2)

    # <2 days: no refund
    res_id, price = make_res(1)
    refund = hrs.cancel_reservation(res_id)
    assert refund == 0.0

    # Cancel non‑existent reservation
    with pytest.raises(ReservationNotFoundError):
        hrs.cancel_reservation("NON_EXISTENT")


def test_get_room_occupancy_and_overlap_logic(fixed_today):
    hrs = HotelReservationSystem()
    hrs.add_room(501, "standard", 70.0)
    hrs.add_room(502, "standard", 70.0)

    # Reservation 1 occupies 501 from day 3 to day 6
    check_in1 = fixed_today + datetime.timedelta(days=3)
    check_out1 = check_in1 + datetime.timedelta(days=3)
    hrs.book_room(501, "Eve", check_in1, check_out1)

    # Reservation 2 occupies 502 from day 5 to day 8
    check_in2 = fixed_today + datetime.timedelta(days=5)
    check_out2 = check_in2 + datetime.timedelta(days=3)
    hrs.book_room(502, "Frank", check_in2, check_out2)

    # Day 4: only room 501 occupied
    occupied_day4 = hrs.get_room_occupancy(fixed_today + datetime.timedelta(days=4))
    assert occupied_day4 == [501]

    # Day 5: both rooms occupied (overlap day)
    occupied_day5 = hrs.get_room_occupancy(fixed_today + datetime.timedelta(days=5))
    assert occupied_day5 == [501, 502]

    # Day 8: no rooms occupied (checkout is exclusive)
    occupied_day8 = hrs.get_room_occupancy(fixed_today + datetime.timedelta(days=8))
    assert occupied_day8 == []


def test_is_room_available_private_method_directly(fixed_today):
    hrs = HotelReservationSystem()
    hrs.add_room(601, "single", 50.0)

    # No reservations yet -> available
    assert hrs._is_room_available(601, fixed_today + datetime.timedelta(days=1), fixed_today + datetime.timedelta(days=2))

    # Create a reservation
    check_in = fixed_today + datetime.timedelta(days=10)
    check_out = check_in + datetime.timedelta(days=4)
    res_id = hrs.book_room(601, "Grace", check_in, check_out)

    # Overlap cases
    # Starts before existing and ends inside
    assert not hrs._is_room_available(601, check_in - datetime.timedelta(days=1), check_in + datetime.timedelta(days=1))
    # Fully inside existing
    assert not hrs._is_room_available(601, check_in + datetime.timedelta(days=1), check_out - datetime.timedelta(days=1))
    # Starts inside and ends after
    assert not hrs._is_room_available(601, check_out - datetime.timedelta(days=1), check_out + datetime.timedelta(days=2))
    # Completely before existing
    assert hrs._is_room_available(601, check_in - datetime.timedelta(days=5), check_in - datetime.timedelta(days=1))
    # Completely after existing
    assert hrs._is_room_available(601, check_out + datetime.timedelta(days=1), check_out + datetime.timedelta(days=3))