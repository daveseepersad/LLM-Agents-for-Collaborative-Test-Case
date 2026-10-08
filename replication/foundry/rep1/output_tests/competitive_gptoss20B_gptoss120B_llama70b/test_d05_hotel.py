import pytest
from data.input_code.d05_hotel import *
from datetime import date, timedelta

@pytest.fixture
def hotel_system():
    return HotelReservationSystem()

def test_add_room_valid(hotel_system):
    hotel_system.add_room(101, "Standard", 100.0)
    assert 101 in hotel_system.rooms

def test_add_room_invalid_price(hotel_system):
    with pytest.raises(ValueError):
        hotel_system.add_room(102, "Standard", 0)

def test_book_room_success(hotel_system):
    hotel_system.add_room(101, "Standard", 100.0)
    reservation_id = hotel_system.book_room(
        101,
        "Alice",
        date.today() + timedelta(days=1),
        date.today() + timedelta(days=2)
    )
    assert reservation_id in hotel_system.reservations

def test_book_room_not_found(hotel_system):
    with pytest.raises(RoomNotFoundError):
        hotel_system.book_room(
            999,
            "Bob",
            date.today() + timedelta(days=1),
            date.today() + timedelta(days=2)
        )

def test_book_room_invalid_dates(hotel_system):
    hotel_system.add_room(101, "Standard", 100.0)
    with pytest.raises(InvalidDateError):
        hotel_system.book_room(
            101,
            "Carol",
            date.today() + timedelta(days=2),
            date.today() + timedelta(days=2)
        )

def test_book_room_past_date(hotel_system):
    hotel_system.add_room(101, "Standard", 100.0)
    with pytest.raises(InvalidDateError):
        hotel_system.book_room(
            101,
            "Dave",
            date.today() - timedelta(days=1),
            date.today()
        )

def test_book_room_unavailable(hotel_system):
    hotel_system.add_room(101, "Standard", 100.0)
    hotel_system.book_room(
        101,
        "Alice",
        date.today() + timedelta(days=1),
        date.today() + timedelta(days=2)
    )
    with pytest.raises(RoomUnavailableError):
        hotel_system.book_room(
            101,
            "Eve",
            date.today() + timedelta(days=1),
            date.today() + timedelta(days=3)
        )

def test_cancel_full_refund(hotel_system):
    hotel_system.add_room(101, "Standard", 100.0)
    reservation_id = hotel_system.book_room(
        101,
        "Alice",
        date.today() + timedelta(days=10),
        date.today() + timedelta(days=11)
    )
    refund = hotel_system.cancel_reservation(reservation_id)
    assert refund == 100.0

def test_cancel_half_refund(hotel_system):
    hotel_system.add_room(101, "Standard", 100.0)
    reservation_id = hotel_system.book_room(
        101,
        "Alice",
        date.today() + timedelta(days=3),
        date.today() + timedelta(days=4)
    )
    refund = hotel_system.cancel_reservation(reservation_id)
    assert refund == 50.0

def test_cancel_no_refund(hotel_system):
    hotel_system.add_room(101, "Standard", 100.0)
    reservation_id = hotel_system.book_room(
        101,
        "Alice",
        date.today() + timedelta(days=1),
        date.today() + timedelta(days=2)
    )
    refund = hotel_system.cancel_reservation(reservation_id)
    assert refund == 0.0

def test_cancel_not_found(hotel_system):
    with pytest.raises(ReservationNotFoundError):
        hotel_system.cancel_reservation("RES-9999")

def test_occupancy_multiple(hotel_system):
    hotel_system.add_room(101, "Standard", 100.0)
    hotel_system.add_room(102, "Standard", 100.0)
    hotel_system.book_room(
        101,
        "Alice",
        date.today(),
        date.today() + timedelta(days=1)
    )
    hotel_system.book_room(
        102,
        "Bob",
        date.today(),
        date.today() + timedelta(days=1)
    )
    occupied_rooms = hotel_system.get_room_occupancy(date.today())
    assert occupied_rooms == [101, 102]

def test_occupancy_boundary_checkin(hotel_system):
    hotel_system.add_room(101, "Standard", 100.0)
    hotel_system.book_room(
        101,
        "Alice",
        date.today(),
        date.today() + timedelta(days=1)
    )
    occupied_rooms = hotel_system.get_room_occupancy(date.today())
    assert occupied_rooms == [101]

def test_occupancy_boundary_checkout(hotel_system):
    hotel_system.add_room(101, "Standard", 100.0)
    hotel_system.add_room(102, "Standard", 100.0)
    # Reservation that ends on the target date (checkout today+1) – should NOT be occupied.
    hotel_system.book_room(
        101,
        "Alice",
        date.today(),
        date.today() + timedelta(days=1)
    )
    # Reservation that starts on the target date – should be occupied.
    hotel_system.book_room(
        102,
        "Bob",
        date.today() + timedelta(days=1),
        date.today() + timedelta(days=2)
    )
    occupied_rooms = hotel_system.get_room_occupancy(date.today() + timedelta(days=1))
    assert occupied_rooms == [102]