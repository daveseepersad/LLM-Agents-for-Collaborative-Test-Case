import pytest
import datetime
from unittest.mock import patch
from data.input_code.d05_hotel import *

# ----------------------------------------------------------------------
# Fixture to freeze datetime.date.today() to a known reference date
# ----------------------------------------------------------------------
@pytest.fixture(autouse=True)
def freeze_today():
    fixed_today = datetime.date(2023, 1, 10)

    class FixedDate(datetime.date):
        @classmethod
        def today(cls):
            return fixed_today

    with patch('datetime.date', FixedDate):
        yield


# ----------------------------------------------------------------------
# Add room tests
# ----------------------------------------------------------------------
@pytest.mark.parametrize(
    "room_number, room_type, price, expect_exception",
    [
        (101, "Deluxe", 150.0, None),          # TC01_AddRoom_Success
        (102, "Standard", 0.0, ValueError),   # TC02_AddRoom_InvalidPrice
    ],
)
def test_add_room(room_number, room_type, price, expect_exception):
    system = HotelReservationSystem()
    if expect_exception:
        with pytest.raises(expect_exception):
            system.add_room(room_number, room_type, price)
    else:
        system.add_room(room_number, room_type, price)
        assert room_number in system.rooms
        assert system.rooms[room_number]["type"] == room_type
        assert system.rooms[room_number]["price_per_night"] == price


# ----------------------------------------------------------------------
# Book room tests
# ----------------------------------------------------------------------
def test_book_room_success():
    system = HotelReservationSystem()
    system.add_room(101, "Deluxe", 150.0)
    res_id = system.book_room(
        room_number=101,
        user_name="Alice",
        check_in=datetime.date(2023, 1, 20),
        check_out=datetime.date(2023, 1, 25),
    )
    assert res_id == "RES-0001"


@pytest.mark.parametrize(
    "room_number, user_name, check_in, check_out, expected_exc",
    [
        (999, "Bob", datetime.date(2023, 1, 20), datetime.date(2023, 1, 22), RoomNotFoundError),   # TC04
        (101, "Carol", datetime.date(2023, 1, 20), datetime.date(2023, 1, 20), InvalidDateError), # TC05
        (101, "Dave", datetime.date(2022, 12, 30), datetime.date(2023, 1, 2), InvalidDateError),   # TC06
    ],
)
def test_book_room_errors(room_number, user_name, check_in, check_out, expected_exc):
    system = HotelReservationSystem()
    system.add_room(101, "Deluxe", 150.0)
    with pytest.raises(expected_exc):
        system.book_room(room_number, user_name, check_in, check_out)


def test_book_room_unavailable():
    system = HotelReservationSystem()
    system.add_room(101, "Deluxe", 150.0)
    # Existing reservation (TC03)
    system.book_room(
        room_number=101,
        user_name="Alice",
        check_in=datetime.date(2023, 1, 20),
        check_out=datetime.date(2023, 1, 25),
    )
    # Overlapping request (TC07)
    with pytest.raises(RoomUnavailableError):
        system.book_room(
            room_number=101,
            user_name="Eve",
            check_in=datetime.date(2023, 1, 24),
            check_out=datetime.date(2023, 1, 28),
        )


# ----------------------------------------------------------------------
# Cancel reservation tests
# ----------------------------------------------------------------------
def _make_reservation(system, res_id, room_number, check_in, check_out, price_per_night, nights):
    """Helper to inject a reservation with a known ID."""
    total_price = round(price_per_night * nights, 2)
    reservation = Reservation(
        reservation_id=res_id,
        room_number=room_number,
        user_name="Tester",
        check_in=check_in,
        check_out=check_out,
        total_price=total_price,
    )
    system.reservations[res_id] = reservation
    return total_price


def test_cancel_reservation_not_found():
    system = HotelReservationSystem()
    with pytest.raises(ReservationNotFoundError):
        system.cancel_reservation("NONEXIST")  # TC08


def test_cancel_reservation_full_refund():
    system = HotelReservationSystem()
    system.add_room(200, "Suite", 100.0)
    total = _make_reservation(
        system,
        res_id="RES-1000",
        room_number=200,
        check_in=datetime.date(2023, 1, 20),   # 10 days from frozen today
        check_out=datetime.date(2023, 1, 25),
        price_per_night=100.0,
        nights=5,
    )
    refund = system.cancel_reservation("RES-1000")
    assert refund == total  # TC09


def test_cancel_reservation_half_refund():
    system = HotelReservationSystem()
    system.add_room(201, "Suite", 100.0)
    total = _make_reservation(
        system,
        res_id="RES-1001",
        room_number=201,
        check_in=datetime.date(2023, 1, 15),   # 5 days from today
        check_out=datetime.date(2023, 1, 18),
        price_per_night=100.0,
        nights=3,
    )
    refund = system.cancel_reservation("RES-1001")
    assert refund == round(total * 0.5, 2)  # TC10


def test_cancel_reservation_no_refund():
    system = HotelReservationSystem()
    system.add_room(202, "Suite", 100.0)
    total = _make_reservation(
        system,
        res_id="RES-1002",
        room_number=202,
        check_in=datetime.date(2023, 1, 11),   # 1 day from today
        check_out=datetime.date(2023, 1, 13),
        price_per_night=100.0,
        nights=2,
    )
    refund = system.cancel_reservation("RES-1002")
    assert refund == 0.0  # TC11


# ----------------------------------------------------------------------
# Occupancy tests
# ----------------------------------------------------------------------
def test_get_room_occupancy_empty():
    system = HotelReservationSystem()
    system.add_room(101, "Deluxe", 150.0)
    # No reservations made
    occupied = system.get_room_occupancy(datetime.date(2023, 1, 20))
    assert occupied == []  # TC12


def test_get_room_occupancy_occupied():
    system = HotelReservationSystem()
    system.add_room(101, "Deluxe", 150.0)
    # Create a reservation covering 2023-01-20 to 2023-01-25
    system.book_room(
        room_number=101,
        user_name="Alice",
        check_in=datetime.date(2023, 1, 20),
        check_out=datetime.date(2023, 1, 25),
    )
    occupied = system.get_room_occupancy(datetime.date(2023, 1, 22))
    assert occupied == [101]  # TC13