import pytest
from data.input_code.d05_hotel import *
from datetime import date, timedelta

@pytest.fixture
def hotel_system():
    return HotelReservationSystem()

@pytest.mark.parametrize('room_number, room_type, price_per_night, expected', [
    (101, 'single', 100.0, None),
    (102, 'double', 0.0, 'ValueError')
])
def test_add_room(hotel_system, room_number, room_type, price_per_night, expected):
    if expected == 'ValueError':
        with pytest.raises(ValueError):
            hotel_system.add_room(room_number, room_type, price_per_night)
    else:
        hotel_system.add_room(room_number, room_type, price_per_night)
        assert room_number in hotel_system.rooms

def test_book_room(hotel_system):
    # Setup rooms
    hotel_system.add_room(101, 'single', 100.0)
    hotel_system.add_room(201, 'double', 200.0)
    hotel_system.add_room(301, 'suite', 200.0)

    # Pre-book to create an occupancy scenario
    today = date.today()
    pre_start = today + timedelta(days=10)
    pre_end = pre_start + timedelta(days=4)
    hotel_system.book_room(201, 'Existing', pre_start, pre_end)

    cases = [
        (999, 'Alice', today + timedelta(days=1), today + timedelta(days=2), 'RoomNotFoundError'),
        (101, 'Bob', today + timedelta(days=3), today + timedelta(days=3), 'InvalidDateError'),  # equal dates
        (101, 'Carol', today - timedelta(days=1), today, 'InvalidDateError'),  # past dates
        (201, 'Dave', pre_start + timedelta(days=1), pre_start + timedelta(days=5), 'RoomUnavailableError'),  # overlaps pre-book
        (301, 'Eve', today + timedelta(days=20), today + timedelta(days=23), 'RES-0002')
    ]
    for room_number, user_name, check_in, check_out, expected in cases:
        if expected in ['RoomNotFoundError', 'InvalidDateError', 'RoomUnavailableError']:
            with pytest.raises(eval(expected)):
                hotel_system.book_room(room_number, user_name, check_in, check_out)
        else:
            result = hotel_system.book_room(room_number, user_name, check_in, check_out)
            assert result == expected

def test_is_room_available(hotel_system):
    hotel_system.add_room(301, 'suite', 200.0)
    hotel_system.add_room(401, 'single', 100.0)

    today = date.today()
    start = today + timedelta(days=10)
    end = start + timedelta(days=4)

    # Occupy room 301
    hotel_system.book_room(301, 'Existing', start, end)

    # Case: for 401 with non-overlapping window -> should be available
    assert hotel_system._is_room_available(401, start - timedelta(days=1), start) is True
    # Case: overlapping with existing reservation for 301 -> not available
    assert hotel_system._is_room_available(301, start + timedelta(days=1), end + timedelta(days=1)) is False

def test_cancel_reservation(hotel_system):
    hotel_system.add_room(1000, 'single', 400.0)
    hotel_system.add_room(1001, 'double', 300.0)
    hotel_system.add_room(1002, 'suite', 500.0)

    today = date.today()
    r1 = hotel_system.book_room(1000, 'User1', today + timedelta(days=10), today + timedelta(days=13))
    r2 = hotel_system.book_room(1001, 'User2', today + timedelta(days=5), today + timedelta(days=7))
    r3 = hotel_system.book_room(1002, 'User3', today + timedelta(days=1), today + timedelta(days=3))

    refund1 = hotel_system.cancel_reservation(r1)
    assert refund1 == 1200.0  # 3 nights * 400 = 1200, >7 days ahead => full refund

    refund2 = hotel_system.cancel_reservation(r2)
    assert refund2 == 300.0  # 2 nights * 300 = 600, 5 days ahead => 50% refund

    refund3 = hotel_system.cancel_reservation(r3)
    assert refund3 == 0.0  # 2 nights * 500 = 1000, 1 day ahead => 0% refund

    with pytest.raises(ReservationNotFoundError):
        hotel_system.cancel_reservation('NON-EXISTENT')

def test_get_room_occupancy(hotel_system):
    hotel_system.add_room(101, 'single', 100.0)
    hotel_system.add_room(301, 'suite', 200.0)

    today = date.today()
    start = today + timedelta(days=5)
    end = start + timedelta(days=10)

    hotel_system.book_room(101, 'User1', start, end)
    hotel_system.book_room(301, 'User2', start, end)

    mid_date = start + timedelta(days=5)
    result = hotel_system.get_room_occupancy(mid_date)
    assert result == [101, 301]

    before_date = start - timedelta(days=1)
    result_before = hotel_system.get_room_occupancy(before_date)
    assert result_before == []