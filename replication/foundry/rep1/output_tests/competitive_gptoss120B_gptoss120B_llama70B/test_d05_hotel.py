import pytest
from data.input_code.d05_hotel import *
import datetime

# ----------------------------------------------------------------------
# Fixture to freeze "today" to a deterministic date for all tests
# ----------------------------------------------------------------------
@pytest.fixture(autouse=True)
def fixed_today(monkeypatch):
    fixed = datetime.date(2099, 1, 1)

    class FixedDate(datetime.date):
        @classmethod
        def today(cls):
            return fixed

    # replace datetime.date with our FixedDate subclass
    monkeypatch.setattr(datetime, "date", FixedDate)


# ----------------------------------------------------------------------
# Fixture providing a fresh HotelReservationSystem instance per test
# ----------------------------------------------------------------------
@pytest.fixture
def hotel():
    return HotelReservationSystem()


# ----------------------------------------------------------------------
# Add room tests
# ----------------------------------------------------------------------
@pytest.mark.parametrize(
    "room_number, room_type, price, expect_error",
    [
        (101, "single", 120.0, None),          # T1_AddRoom_Success
        (102, "double", 0.0, ValueError),     # T2_AddRoom_InvalidPrice
    ],
)
def test_add_room(hotel, room_number, room_type, price, expect_error):
    if expect_error:
        with pytest.raises(expect_error):
            hotel.add_room(room_number, room_type, price)
    else:
        hotel.add_room(room_number, room_type, price)
        assert room_number in hotel.rooms
        assert hotel.rooms[room_number]["price_per_night"] == price


# ----------------------------------------------------------------------
# Book room error scenarios
# ----------------------------------------------------------------------
def test_book_room_room_not_found(hotel):
    # T3_BookRoom_RoomNotFound
    with pytest.raises(RoomNotFoundError):
        hotel.book_room(
            room_number=999,
            user_name="Alice",
            check_in=datetime.date(2099, 1, 10),
            check_out=datetime.date(2099, 1, 15),
        )


def test_book_room_invalid_date_order(hotel):
    # T4_BookRoom_InvalidDate_Order
    hotel.add_room(101, "single", 120.0)
    with pytest.raises(InvalidDateError):
        hotel.book_room(
            room_number=101,
            user_name="Bob",
            check_in=datetime.date(2099, 1, 10),
            check_out=datetime.date(2099, 1, 5),
        )


def test_book_room_invalid_date_past(hotel):
    # T5_BookRoom_InvalidDate_Past
    hotel.add_room(101, "single", 120.0)
    with pytest.raises(InvalidDateError):
        hotel.book_room(
            room_number=101,
            user_name="Carol",
            check_in=datetime.date(2000, 1, 1),
            check_out=datetime.date(2000, 1, 5),
        )


def test_book_room_unavailable(hotel):
    # T6_BookRoom_Unavailable
    hotel.add_room(101, "single", 120.0)
    # first reservation occupies the period
    hotel.book_room(
        room_number=101,
        user_name="First",
        check_in=datetime.date(2099, 2, 1),
        check_out=datetime.date(2099, 2, 5),
    )
    # overlapping reservation should fail
    with pytest.raises(RoomUnavailableError):
        hotel.book_room(
            room_number=101,
            user_name="Dave",
            check_in=datetime.date(2099, 2, 3),
            check_out=datetime.date(2099, 2, 7),
        )


def test_book_room_success(hotel):
    # T7_BookRoom_Success
    hotel.add_room(101, "single", 120.0)
    res_id = hotel.book_room(
        room_number=101,
        user_name="Eve",
        check_in=datetime.date(2099, 3, 1),
        check_out=datetime.date(2099, 3, 4),
    )
    assert res_id == "RES-0001"
    reservation = hotel.reservations[res_id]
    assert reservation.total_price == 360.0  # 3 nights * 120.0


# ----------------------------------------------------------------------
# Cancel reservation tests
# ----------------------------------------------------------------------
def test_cancel_reservation_not_found(hotel):
    # T8_CancelReservation_NotFound
    with pytest.raises(ReservationNotFoundError):
        hotel.cancel_reservation("NONEXISTENT")


def test_cancel_reservation_full_refund(hotel):
    # T9_CancelReservation_FullRefund
    hotel.add_room(101, "single", 120.0)
    # check‑in > today + 7 days (today is 2099‑01‑01)
    res_id = hotel.book_room(
        room_number=101,
        user_name="User1",
        check_in=datetime.date(2099, 1, 10),
        check_out=datetime.date(2099, 1, 12),
    )
    reservation = hotel.reservations[res_id]
    refund = hotel.cancel_reservation(res_id)
    assert refund == reservation.total_price


def test_cancel_reservation_half_refund(hotel):
    # T10_CancelReservation_HalfRefund
    hotel.add_room(101, "single", 120.0)
    # check‑in 3 days from today (within 2‑7 day window)
    res_id = hotel.book_room(
        room_number=101,
        user_name="User2",
        check_in=datetime.date(2099, 1, 4),
        check_out=datetime.date(2099, 1, 6),
    )
    reservation = hotel.reservations[res_id]
    refund = hotel.cancel_reservation(res_id)
    assert refund == round(reservation.total_price * 0.5, 2)


def test_cancel_reservation_no_refund(hotel):
    # T11_CancelReservation_NoRefund
    hotel.add_room(101, "single", 120.0)
    # check‑in 1 day from today (less than 2 days)
    res_id = hotel.book_room(
        room_number=101,
        user_name="User3",
        check_in=datetime.date(2099, 1, 2),
        check_out=datetime.date(2099, 1, 4),
    )
    refund = hotel.cancel_reservation(res_id)
    assert refund == 0.0


# ----------------------------------------------------------------------
# Occupancy test
# ----------------------------------------------------------------------
def test_get_room_occupancy_mixed(hotel):
    # T12_GetRoomOccupancy_Mixed
    # add three rooms
    hotel.add_room(101, "single", 120.0)
    hotel.add_room(102, "double", 150.0)
    hotel.add_room(103, "suite", 200.0)

    # reservations:
    # 101: 2099-04-01 to 2099-04-05
    hotel.book_room(
        room_number=101,
        user_name="A",
        check_in=datetime.date(2099, 4, 1),
        check_out=datetime.date(2099, 4, 5),
    )
    # 103: 2099-04-02 to 2099-04-04
    hotel.book_room(
        room_number=103,
        user_name="B",
        check_in=datetime.date(2099, 4, 2),
        check_out=datetime.date(2099, 4, 4),
    )
    # query occupancy for 2099-04-03
    occupied = hotel.get_room_occupancy(datetime.date(2099, 4, 3))
    assert occupied == [101, 103]