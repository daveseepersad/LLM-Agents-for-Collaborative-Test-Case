import pytest
from data.input_code.d05_hotel import *

# Fixed "today" for deterministic date calculations
FIXED_TODAY = datetime.date(2026, 10, 1)

@pytest.fixture(autouse=True)
def patch_today(monkeypatch):
    """Patch datetime.date.today() to return a constant date."""
    class FixedDate(datetime.date):
        @classmethod
        def today(cls):
            return FIXED_TODAY
    monkeypatch.setattr(datetime, "date", FixedDate)
    yield
    # No teardown needed; monkeypatch will restore original attribute


@pytest.fixture
def system():
    """Provide a fresh HotelReservationSystem for each test."""
    return HotelReservationSystem()


@pytest.mark.parametrize(
    "room_number, room_type, price, expected_rooms",
    [
        (101, "Deluxe", 150.0, {101: {"type": "Deluxe", "price_per_night": 150.0}}),
    ],
)
def test_add_room_valid(system, room_number, room_type, price, expected_rooms):
    # Should not raise
    system.add_room(room_number, room_type, price)
    assert system.rooms == expected_rooms


@pytest.mark.parametrize(
    "room_number, room_type, price, exc",
    [
        (102, "Standard", 0.0, ValueError),
        (103, "Standard", -10.0, ValueError),
    ],
)
def test_add_room_invalid_price(system, room_number, room_type, price, exc):
    with pytest.raises(exc):
        system.add_room(room_number, room_type, price)


def test_book_room_success(system):
    # Arrange
    system.add_room(201, "Suite", 100.0)
    check_in = FIXED_TODAY + datetime.timedelta(days=5)   # 2026-10-06
    check_out = check_in + datetime.timedelta(days=3)    # 2026-10-09
    # Act
    res_id = system.book_room(201, "Alice", check_in, check_out)
    # Assert
    assert res_id == "RES-0001"
    reservation = system.reservations[res_id]
    assert reservation.room_number == 201
    assert reservation.user_name == "Alice"
    assert reservation.total_price == 300.0  # 3 nights * 100


def test_book_room_not_found(system):
    with pytest.raises(RoomNotFoundError):
        system.book_room(999, "Bob", FIXED_TODAY + datetime.timedelta(days=1),
                         FIXED_TODAY + datetime.timedelta(days=2))


def test_book_room_invalid_dates(system):
    system.add_room(301, "Standard", 80.0)
    check_in = FIXED_TODAY + datetime.timedelta(days=10)
    check_out = FIXED_TODAY + datetime.timedelta(days=5)  # earlier than check_in
    with pytest.raises(InvalidDateError):
        system.book_room(301, "Carol", check_in, check_out)


def test_book_room_past_date(system):
    system.add_room(302, "Standard", 80.0)
    past_check_in = FIXED_TODAY - datetime.timedelta(days=1)
    past_check_out = FIXED_TODAY + datetime.timedelta(days=1)
    with pytest.raises(InvalidDateError):
        system.book_room(302, "Dan", past_check_in, past_check_out)


def test_cancel_reservation_not_found(system):
    with pytest.raises(ReservationNotFoundError):
        system.cancel_reservation("RES-9999")


def _make_reservation(system, room_number, price, days_until_checkin, nights):
    """Helper to create a reservation with a specific check‑in offset."""
    system.add_room(room_number, "Test", price)
    check_in = FIXED_TODAY + datetime.timedelta(days=days_until_checkin)
    check_out = check_in + datetime.timedelta(days=nights)
    res_id = system.book_room(room_number, "Tester", check_in, check_out)
    return res_id, system.reservations[res_id].total_price


def test_cancel_reservation_full_refund(system):
    # Reservation >7 days away from check‑in
    res_id, total = _make_reservation(system, 401, 150.0, days_until_checkin=10, nights=2)
    refund = system.cancel_reservation(res_id)
    assert refund == total  # 100% refund


def test_cancel_reservation_half_refund(system):
    # Reservation 5 days away (2‑7 days window)
    res_id, total = _make_reservation(system, 402, 200.0, days_until_checkin=5, nights=2)
    refund = system.cancel_reservation(res_id)
    assert refund == round(total * 0.5, 2)  # 50% refund


def test_cancel_reservation_zero_refund(system):
    # Reservation 1 day away (<2 days)
    res_id, total = _make_reservation(system, 403, 120.0, days_until_checkin=1, nights=2)
    refund = system.cancel_reservation(res_id)
    assert refund == 0.0


def test_get_room_occupancy_empty(system):
    # No rooms added / no reservations
    date = FIXED_TODAY + datetime.timedelta(days=3)
    assert system.get_room_occupancy(date) == []


def test_get_room_occupancy_with_reservations(system):
    # Setup two rooms and overlapping reservations
    system.add_room(501, "Deluxe", 100.0)
    system.add_room(502, "Deluxe", 100.0)

    # Reservation for room 501: 2026-10-05 to 2026-10-08
    system.book_room(
        501,
        "Eve",
        FIXED_TODAY + datetime.timedelta(days=4),
        FIXED_TODAY + datetime.timedelta(days=7),
    )
    # Reservation for room 502: 2026-10-06 to 2026-10-09
    system.book_room(
        502,
        "Frank",
        FIXED_TODAY + datetime.timedelta(days=5),
        FIXED_TODAY + datetime.timedelta(days=8),
    )

    # Query a date where both rooms are occupied
    query_date = FIXED_TODAY + datetime.timedelta(days=5)  # 2026-10-06
    assert system.get_room_occupancy(query_date) == [501, 502]

    # Query a date where only room 501 is occupied
    query_date = FIXED_TODAY + datetime.timedelta(days=4)  # 2026-10-05
    assert system.get_room_occupancy(query_date) == [501]

    # Query a date with no occupancy
    query_date = FIXED_TODAY + datetime.timedelta(days=9)  # 2026-10-10
    assert system.get_room_occupancy(query_date) == []

def test_book_room_overlap_raises(system):
    # Setup initial reservation that occupies 2026-10-01 to 2026-10-04
    system.add_room(605, "Standard", 100.0)
    initial_check_in = datetime.date.fromisoformat("2026-10-01")
    initial_check_out = datetime.date.fromisoformat("2026-10-04")
    system.book_room(605, "Initial", initial_check_in, initial_check_out)

    # Attempt overlapping booking 2026-10-03 to 2026-10-06
    overlap_check_in = datetime.date.fromisoformat("2026-10-03")
    overlap_check_out = datetime.date.fromisoformat("2026-10-06")
    with pytest.raises(RoomUnavailableError):
        system.book_room(605, "Alice", overlap_check_in, overlap_check_out)


def test_get_room_occupancy_boundary_excludes_checkout(system):
    # Setup room and reservation
    system.add_room(606, "Standard", 100.0)
    check_in = datetime.date.fromisoformat("2026-10-04")
    check_out = datetime.date.fromisoformat("2026-10-07")
    system.book_room(606, "Carol", check_in, check_out)

    # Query on the checkout date; should be empty
    query_date = datetime.date.fromisoformat("2026-10-07")
    assert system.get_room_occupancy(query_date) == []