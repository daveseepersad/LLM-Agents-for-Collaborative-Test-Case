import pytest
from data.input_code.d05_hotel import *
from datetime import date

@pytest.fixture(scope="module")
def system():
    # Shared system instance for all tests in this module
    h = HotelReservationSystem()
    # Pre-create rooms used in tests
    h.add_room(101, "Deluxe", 99.99)
    h.add_room(102, "Standard", 99.99)
    return h

def test_T1_ADD_ROOM_SUCCESS(system):
    # Add an existing room again to confirm overwrite behavior and presence
    system.add_room(101, "Deluxe", 99.99)
    assert 101 in system.rooms
    assert system.rooms[101]['price_per_night'] == 99.99

def test_T2_ADD_ROOM_INVALID_PRICE(system):
    with pytest.raises(ValueError):
        system.add_room(102, "Standard", 0)

def test_T3_BOOK_ROOM_SUCCESS(system):
    res = system.book_room(101, "Alice", date(2026, 10, 17), date(2026, 10, 20))
    assert res == "RES-0001"

def test_T4_BOOK_ROOM_UNAVAILABLE(system):
    with pytest.raises(RoomUnavailableError):
        system.book_room(101, "Bob", date(2026, 10, 18), date(2026, 10, 19))

def test_T5_BOOK_ROOM_INVALID_DATES_SAME(system):
    with pytest.raises(InvalidDateError):
        system.book_room(101, "Carol", date(2026, 10, 25), date(2026, 10, 25))

def test_T6_BOOK_ROOM_INVALID_DATES_PAST(system):
    with pytest.raises(InvalidDateError):
        system.book_room(101, "Dave", date(2026, 10, 5), date(2026, 10, 6))

def test_T7_BOOK_ROOM_ROOM_NOT_FOUND(system):
    with pytest.raises(RoomNotFoundError):
        system.book_room(999, "Eve", date(2026, 10, 20), date(2026, 10, 22))

def test_T8_BOOK_ROOM_EDGE_AVAILABLE(system):
    res = system.book_room(101, "Frank", date(2026, 10, 20), date(2026, 10, 22))
    assert res == "RES-0002"

def test_T9_CANCEL_RESERVATION_FULL(system):
    # Create a reservation far in the future to test 100% refund
    res_id = system.book_room(101, "Grace", date(2026, 10, 25), date(2026, 10, 27))
    assert res_id == "RES-0003"
    refund = system.cancel_reservation("RES-0003")
    assert refund == 199.98

def test_T10_CANCEL_RESERVATION_HALF(system):
    # Create a reservation with 2 nights to test 50% refund
    res_id = system.book_room(101, "Heidi", date(2026, 10, 12), date(2026, 10, 14))
    assert res_id == "RES-0004"
    refund = system.cancel_reservation("RES-0004")
    assert refund == 99.99

def test_T11_CANCEL_RESERVATION_NONE(system):
    # Create a reservation with check-in date and test refund policy (depends on current date)
    res_id = system.book_room(101, "Ivan", date(2026, 10, 8), date(2026, 10, 10))
    assert res_id == "RES-0005"
    refund = system.cancel_reservation("RES-0005")
    days_until_checkin = (date(2026, 10, 8) - date.today()).days
    if days_until_checkin > 7:
        expected = 199.98
    elif 2 <= days_until_checkin <= 7:
        expected = 99.99
    else:
        expected = 0.0
    assert refund == expected

def test_T12_CANCEL_RESERVATION_NOT_FOUND(system):
    with pytest.raises(ReservationNotFoundError):
        system.cancel_reservation("RES-9999")

def test_T13_GET_OCCUPANCY_SINGLE(system):
    occ = system.get_room_occupancy(date(2026, 10, 18))
    assert occ == [101]

def test_T14_GET_OCCUPANCY_EMPTY(system):
    occ = system.get_room_occupancy(date(2026, 10, 7))
    assert occ == []

def test_T15_GET_OCCUPANCY_MULTIPLE(system):
    occ = system.get_room_occupancy(date(2026, 10, 18))
    assert occ == [101]

def test_T_MISSING_EDGE_CHECKOUT_EQUALS_CHECKIN(system):
    res = system.book_room(101, "EdgeCaseUser", date(2026, 10, 15), date(2026, 10, 17))
    assert res == "RES-0006"

def test_T_MISSING_TODAY_BOOKING(system):
    from datetime import date, timedelta
    check_in = date.today()
    check_out = date.today() + timedelta(days=1)
    res = system.book_room(101, "TodayUser", check_in, check_out)
    assert res == "RES-0007"

def test_T_MISSING_OCCUPANCY_CHECKOUT_EDGE(system):
    occ = system.get_room_occupancy(date(2026, 10, 20))
    assert occ == [101]

def test_T_MISSING_OCCUPANCY_MULTIPLE(system):
    res_102 = system.book_room(102, "OccupyUser", date(2026, 10, 18), date(2026, 10, 19))
    assert res_102 == "RES-0008"
    occ = system.get_room_occupancy(date(2026, 10, 18))
    assert occ == [101, 102]

def test_T_MISSING_ADJACENT_BEFORE(system):
    res = system.book_room(101, "AdjBefore", date(2026, 10, 14), date(2026, 10, 15))
    assert res == "RES-0009"

def test_T_MISSING_OCCUPANCY_CHECKOUT_NOT_OCCUPIED(system):
    occ = system.get_room_occupancy(date(2026, 10, 31))
    assert occ == []

@pytest.mark.parametrize("days_before_checkin, expected_refund", [
    (8, 99.99),  # Full refund
    (5, 49.99),  # Half refund
    (1, 0.0),    # No refund
])
def test_T_MISSING_REFUND_SCENARIOS(system, days_before_checkin, expected_refund):
    check_in = date.today() + datetime.timedelta(days=days_before_checkin)
    check_out = check_in + datetime.timedelta(days=1)
    res_id = system.book_room(102, "RefundTest", check_in, check_out)
    refund = system.cancel_reservation(res_id)
    assert refund == expected_refund

def test_T_MISSING_ADD_ROOM_OVERWRITE_PRICE(system):
    system.add_room(101, "Deluxe", 120.0)
    assert system.rooms[101]['price_per_night'] == 120.0