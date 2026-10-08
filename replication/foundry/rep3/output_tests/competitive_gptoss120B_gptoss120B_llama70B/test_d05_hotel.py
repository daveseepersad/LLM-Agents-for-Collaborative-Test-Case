import pytest
from datetime import date, timedelta
from data.input_code.d05_hotel import (
    HotelReservationSystem,
    RoomNotFoundError,
    RoomUnavailableError,
    InvalidDateError,
    ReservationNotFoundError,
)

@pytest.fixture
def hotel_system():
    return HotelReservationSystem()

def test_add_room_valid(hotel_system):
    hotel_system.add_room(101, "single", 100.0)
    assert 101 in hotel_system.rooms

def test_add_room_invalid_price(hotel_system):
    with pytest.raises(ValueError):
        hotel_system.add_room(103, "suite", 0.0)

def test_book_room_success(hotel_system):
    hotel_system.add_room(101, "single", 100.0)
    res_id = hotel_system.book_room(
        101,
        "Alice",
        date.today() + timedelta(days=10),
        date.today() + timedelta(days=12),
    )
    assert res_id in hotel_system.reservations

def test_book_room_not_found(hotel_system):
    with pytest.raises(RoomNotFoundError):
        hotel_system.book_room(
            999,
            "Bob",
            date.today() + timedelta(days=10),
            date.today() + timedelta(days=12),
        )

def test_book_room_invalid_dates_equal(hotel_system):
    hotel_system.add_room(101, "single", 100.0)
    today = date.today()
    with pytest.raises(InvalidDateError):
        hotel_system.book_room(101, "Carol", today + timedelta(days=5), today + timedelta(days=5))

def test_book_room_past_date(hotel_system):
    hotel_system.add_room(101, "single", 100.0)
    past_day = date.today() - timedelta(days=1)
    future_day = date.today() + timedelta(days=1)
    with pytest.raises(InvalidDateError):
        hotel_system.book_room(101, "Dave", past_day, future_day)

def test_book_room_unavailable(hotel_system):
    hotel_system.add_room(101, "single", 100.0)
    hotel_system.book_room(
        101,
        "Alice",
        date.today() + timedelta(days=10),
        date.today() + timedelta(days=12),
    )
    with pytest.raises(RoomUnavailableError):
        hotel_system.book_room(
            101,
            "Eve",
            date.today() + timedelta(days=11),
            date.today() + timedelta(days=13),
        )

def test_book_room_full_refund(hotel_system):
    hotel_system.add_room(102, "double", 200.0)
    check_in = date.today() + timedelta(days=10)
    check_out = check_in + timedelta(days=2)
    res_id = hotel_system.book_room(102, "Frank", check_in, check_out)
    assert res_id in hotel_system.reservations

def test_cancel_reservation_full_refund(hotel_system):
    hotel_system.add_room(102, "double", 200.0)
    check_in = date.today() + timedelta(days=10)
    check_out = check_in + timedelta(days=2)
    res_id = hotel_system.book_room(102, "Frank", check_in, check_out)
    refund = hotel_system.cancel_reservation(res_id)
    # 2 nights × $200 = $400, full refund because >7 days before check‑in
    assert refund == 400.0

def test_book_room_half_refund(hotel_system):
    hotel_system.add_room(102, "double", 200.0)
    check_in = date.today() + timedelta(days=3)
    check_out = check_in + timedelta(days=2)
    res_id = hotel_system.book_room(102, "Grace", check_in, check_out)
    assert res_id in hotel_system.reservations

def test_cancel_reservation_half_refund(hotel_system):
    hotel_system.add_room(102, "double", 200.0)
    check_in = date.today() + timedelta(days=3)
    check_out = check_in + timedelta(days=2)
    res_id = hotel_system.book_room(102, "Grace", check_in, check_out)
    refund = hotel_system.cancel_reservation(res_id)
    # 2 nights × $200 = $400, 50 % refund because 2–7 days before check‑in
    assert refund == 200.0

def test_book_room_no_refund(hotel_system):
    hotel_system.add_room(102, "double", 200.0)
    check_in = date.today() + timedelta(days=1)
    check_out = check_in + timedelta(days=1)
    res_id = hotel_system.book_room(102, "Heidi", check_in, check_out)
    assert res_id in hotel_system.reservations

def test_cancel_reservation_no_refund(hotel_system):
    hotel_system.add_room(102, "double", 200.0)
    check_in = date.today() + timedelta(days=1)
    check_out = check_in + timedelta(days=1)
    res_id = hotel_system.book_room(102, "Heidi", check_in, check_out)
    refund = hotel_system.cancel_reservation(res_id)
    # Cancellation less than 2 days before check‑in yields no refund
    assert refund == 0.0

def test_cancel_reservation_not_found(hotel_system):
    with pytest.raises(ReservationNotFoundError):
        hotel_system.cancel_reservation("NONEXISTENT")

def test_get_room_occupancy(hotel_system):
    hotel_system.add_room(101, "single", 100.0)
    check_in = date.today() + timedelta(days=5)
    check_out = check_in + timedelta(days=2)
    hotel_system.book_room(101, "Alice", check_in, check_out)
    occupied_rooms = hotel_system.get_room_occupancy(check_in + timedelta(days=1))
    assert occupied_rooms == [101]