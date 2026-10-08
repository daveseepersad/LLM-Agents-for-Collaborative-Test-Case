import pytest
import datetime
from data.input_code.d05_hotel import *

# T1_INIT
def test_T1_INIT():
    h = HotelReservationSystem()
    assert h.rooms == {}
    assert h.reservations == {}
    assert h._reservation_counter == 0

# T2_ADD_ROOM_VALID
def test_T2_ADD_ROOM_VALID():
    h = HotelReservationSystem()
    h.add_room(101, "Single", 100.0)
    assert 101 in h.rooms
    assert h.rooms[101] == {'type': 'Single', 'price_per_night': 100.0}

# T3_ADD_ROOM_INVALID_PRICE
def test_T3_ADD_ROOM_INVALID_PRICE():
    h = HotelReservationSystem()
    with pytest.raises(ValueError):
        h.add_room(102, "Double", -50.0)

# T4_BOOK_ROOM_NONEXISTENT
def test_T4_BOOK_ROOM_NONEXISTENT():
    h = HotelReservationSystem()
    with pytest.raises(RoomNotFoundError):
        h.book_room(103, "John", datetime.date.today() + datetime.timedelta(days=1),
                    datetime.date.today() + datetime.timedelta(days=3))

# T5_BOOK_ROOM_INVALID_DATES
def test_T5_BOOK_ROOM_INVALID_DATES():
    h = HotelReservationSystem()
    h.add_room(101, "Single", 100.0)
    with pytest.raises(InvalidDateError):
        h.book_room(101, "John", datetime.date.today() + datetime.timedelta(days=3),
                    datetime.date.today() + datetime.timedelta(days=1))

# T6_BOOK_ROOM_PAST
def test_T6_BOOK_ROOM_PAST():
    h = HotelReservationSystem()
    h.add_room(101, "Single", 100.0)
    with pytest.raises(InvalidDateError):
        h.book_room(101, "John", datetime.date.today() - datetime.timedelta(days=1),
                    datetime.date.today() + datetime.timedelta(days=1))

# T7_BOOK_ROOM_SUCCESS
def test_T7_BOOK_ROOM_SUCCESS():
    h = HotelReservationSystem()
    h.add_room(101, "Single", 100.0)
    res_id = h.book_room(101, "John", datetime.date.today() + datetime.timedelta(days=1),
                         datetime.date.today() + datetime.timedelta(days=3))
    assert res_id == "RES-0001"
    assert res_id in h.reservations
    assert h.reservations[res_id].total_price == 200.0

# T8_BOOK_ROOM_UNAVAILABLE
def test_T8_BOOK_ROOM_UNAVAILABLE():
    h = HotelReservationSystem()
    h.add_room(101, "Single", 100.0)
    h.book_room(101, "John", datetime.date.today() + datetime.timedelta(days=1),
                datetime.date.today() + datetime.timedelta(days=3))
    with pytest.raises(RoomUnavailableError):
        h.book_room(101, "Jane", datetime.date.today() + datetime.timedelta(days=1),
                    datetime.date.today() + datetime.timedelta(days=3))

# T9_CANCEL_NONEXISTENT
def test_T9_CANCEL_NONEXISTENT():
    h = HotelReservationSystem()
    with pytest.raises(ReservationNotFoundError):
        h.cancel_reservation("RES-9999")

# T10_CANCEL_FULL_REFUND
def test_T10_CANCEL_FULL_REFUND():
    h = HotelReservationSystem()
    h.add_room(101, "Single", 100.0)
    res_id = h.book_room(101, "John", datetime.date.today() + datetime.timedelta(days=8),
                         datetime.date.today() + datetime.timedelta(days=10))
    refund = h.cancel_reservation(res_id)
    # Days until check-in = 8 -> full refund
    assert refund == 200.0

# T11_GET_OCCUPANCY
def test_T11_GET_OCCUPANCY():
    h = HotelReservationSystem()
    h.add_room(101, "Single", 100.0)
    res_id = h.book_room(101, "John", datetime.date.today() + datetime.timedelta(days=2),
                         datetime.date.today() + datetime.timedelta(days=4))
    occupancy = h.get_room_occupancy(datetime.date.today() + datetime.timedelta(days=2))
    assert 101 in occupancy
    assert occupancy == [101]

# T12_CANCEL_PARTIAL_REFUND
def test_T12_CANCEL_PARTIAL_REFUND():
    h = HotelReservationSystem()
    h.add_room(101, "Single", 100.0)
    res_id = h.book_room(101, "John", datetime.date.today() + datetime.timedelta(days=3),
                         datetime.date.today() + datetime.timedelta(days=5))
    refund = h.cancel_reservation(res_id)
    # 2 nights, 3-7 days before check-in would yield 50% refund
    assert refund == 100.0

# T13_BOOK_ANOTHER_ROOM
def test_T13_BOOK_ANOTHER_ROOM():
    h = HotelReservationSystem()
    h.add_room(102, "Double", 100.0)
    res_id = h.book_room(102, "Jane", datetime.date.today() + datetime.timedelta(days=5),
                         datetime.date.today() + datetime.timedelta(days=7))
    assert res_id == "RES-0001"

# T14_CANCEL_PARTIAL_REFUND
def test_T14_CANCEL_PARTIAL_REFUND():
    h = HotelReservationSystem()
    h.add_room(102, "Double", 100.0)
    res_id = h.book_room(102, "Jane", datetime.date.today() + datetime.timedelta(days=5),
                         datetime.date.today() + datetime.timedelta(days=7))
    refund = h.cancel_reservation(res_id)
    assert refund == 100.0

# T15_BOOK_FOR_NO_REFUND
def test_T15_BOOK_FOR_NO_REFUND():
    h = HotelReservationSystem()
    with pytest.raises(RoomNotFoundError):
        h.book_room(103, "Jim", datetime.date.today() + datetime.timedelta(days=1),
                    datetime.date.today() + datetime.timedelta(days=3))

# T16_ADD_ROOM_FOR_T15
def test_T16_ADD_ROOM_FOR_T15():
    h = HotelReservationSystem()
    h.add_room(103, "Suite", 200.0)
    assert 103 in h.rooms
    assert h.rooms[103] == {'type': 'Suite', 'price_per_night': 200.0}

# T17_BOOK_FOR_NO_REFUND
def test_T17_BOOK_FOR_NO_REFUND():
    h = HotelReservationSystem()
    h.add_room(103, "Suite", 200.0)
    res_id = h.book_room(103, "Jim", datetime.date.today() + datetime.timedelta(days=1),
                         datetime.date.today() + datetime.timedelta(days=3))
    assert res_id == "RES-0001"

# T18_CANCEL_NO_REFUND
def test_T18_CANCEL_NO_REFUND():
    h = HotelReservationSystem()
    h.add_room(103, "Suite", 200.0)
    res_id = h.book_room(103, "Jim", datetime.date.today() + datetime.timedelta(days=1),
                         datetime.date.today() + datetime.timedelta(days=3))
    refund = h.cancel_reservation(res_id)
    # Cancellation within <2 days yields no refund
    assert refund == 0.0