import pytest
import datetime
from dataclasses import replace
from data.input_code.d05_hotel import (
    HotelReservationSystem,
    RoomNotFoundError,
    RoomUnavailableError,
    InvalidDateError,
    ReservationNotFoundError,
    Reservation,
)


@pytest.fixture
def hotel():
    return HotelReservationSystem()


def test_add_room_invalid_price_raises(hotel):
    with pytest.raises(ValueError):
        hotel.add_room(room_number=101, room_type="Single", price_per_night=0)
    with pytest.raises(ValueError):
        hotel.add_room(room_number=102, room_type="Double", price_per_night=-50)


def test_book_room_room_not_found(hotel):
    today = datetime.date.today()
    with pytest.raises(RoomNotFoundError):
        hotel.book_room(
            room_number=999,
            user_name="Alice",
            check_in=today + datetime.timedelta(days=1),
            check_out=today + datetime.timedelta(days=3),
        )


def test_book_room_invalid_dates_checkin_ge_checkout(hotel):
    hotel.add_room(101, "Single", 100.0)
    today = datetime.date.today()
    # check_in == check_out
    with pytest.raises(InvalidDateError):
        hotel.book_room(101, "Bob", today + datetime.timedelta(days=5), today + datetime.timedelta(days=5))
    # check_in > check_out
    with pytest.raises(InvalidDateError):
        hotel.book_room(101, "Bob", today + datetime.timedelta(days=6), today + datetime.timedelta(days=5))


def test_book_room_past_checkin_raises(hotel):
    hotel.add_room(101, "Single", 100.0)
    past = datetime.date.today() - datetime.timedelta(days=1)
    future = datetime.date.today() + datetime.timedelta(days=2)
    with pytest.raises(InvalidDateError):
        hotel.book_room(101, "Carol", past, future)


def test_book_room_success_and_price_calculation(hotel):
    hotel.add_room(101, "Single", 120.5)
    today = datetime.date.today()
    check_in = today + datetime.timedelta(days=2)
    check_out = check_in + datetime.timedelta(days=4)  # 4 nights
    res_id = hotel.book_room(101, "Dave", check_in, check_out)

    # Verify reservation stored correctly
    assert res_id in hotel.reservations
    reservation = hotel.reservations[res_id]
    assert reservation.room_number == 101
    assert reservation.user_name == "Dave"
    assert reservation.check_in == check_in
    assert reservation.check_out == check_out
    expected_total = round(4 * 120.5, 2)
    assert reservation.total_price == expected_total




def test_cancel_reservation_not_found_raises(hotel):
    with pytest.raises(ReservationNotFoundError):
        hotel.cancel_reservation("NON-EXISTENT")


@pytest.mark.parametrize(
    "days_until_checkin, expected_refund_factor",
    [
        (10, 1.0),   # >7 days -> full refund
        (7, 0.5),    # exactly 7 days -> 50%
        (5, 0.5),    # between 2 and 7 -> 50%
        (2, 0.5),    # exactly 2 days -> 50%
        (1, 0.0),    # <2 days -> 0%
        (0, 0.0),    # same day -> 0%
    ],
)
def test_cancel_reservation_refund_policy(hotel, days_until_checkin, expected_refund_factor):
    hotel.add_room(202, "Deluxe", 200.0)
    today = datetime.date.today()
    check_in = today + datetime.timedelta(days=days_until_checkin)
    check_out = check_in + datetime.timedelta(days=3)
    res_id = hotel.book_room(202, "Kate", check_in, check_out)

    reservation = hotel.reservations[res_id]
    expected_refund = round(reservation.total_price * expected_refund_factor, 2)

    refund = hotel.cancel_reservation(res_id)
    assert refund == expected_refund
    # Ensure reservation is removed
    assert res_id not in hotel.reservations


def test_get_room_occupancy(hotel):
    hotel.add_room(301, "Suite", 300.0)
    hotel.add_room(302, "Suite", 300.0)
    today = datetime.date.today()
    # Reservation for room 301 covering today+1 to today+4
    res1 = hotel.book_room(
        301,
        "Leo",
        today + datetime.timedelta(days=1),
        today + datetime.timedelta(days=4),
    )
    # Reservation for room 302 covering today+3 to today+6
    res2 = hotel.book_room(
        302,
        "Mia",
        today + datetime.timedelta(days=3),
        today + datetime.timedelta(days=6),
    )

    # Date before any reservation
    assert hotel.get_room_occupancy(today) == []

    # Date where only room 301 is occupied
    date_one = today + datetime.timedelta(days=2)
    assert hotel.get_room_occupancy(date_one) == [301]

    # Date where both rooms are occupied
    date_two = today + datetime.timedelta(days=3)
    assert hotel.get_room_occupancy(date_two) == [301, 302]

    # Date after room 301 checkout but before room 302 checkout
    date_three = today + datetime.timedelta(days=5)
    assert hotel.get_room_occupancy(date_three) == [302]

    # Clean up by cancelling
    hotel.cancel_reservation(res1)
    hotel.cancel_reservation(res2)
    assert hotel.get_room_occupancy(date_two) == []