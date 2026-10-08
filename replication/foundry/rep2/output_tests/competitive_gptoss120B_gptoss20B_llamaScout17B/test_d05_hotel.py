import pytest
from data.input_code.d05_hotel import *
import datetime

def test_hotel_reservation_system_plan():
    hrs = HotelReservationSystem()
    today = datetime.date.today()

    # T1: add_room with non-positive price should raise ValueError
    with pytest.raises(ValueError):
        hrs.add_room(101, "Single", 0)

    # Add valid room for subsequent tests
    hrs.add_room(101, "Single", 100)

    # T2: booking a non-existent room should raise RoomNotFoundError
    with pytest.raises(RoomNotFoundError):
        hrs.book_room(999, "Alice", today + datetime.timedelta(days=10), today + datetime.timedelta(days=12))

    # T3: check_in >= check_out should raise InvalidDateError
    with pytest.raises(InvalidDateError):
        hrs.book_room(101, "Bob", today + datetime.timedelta(days=60), today + datetime.timedelta(days=60))

    # T4: check_in in the past should raise InvalidDateError
    with pytest.raises(InvalidDateError):
        hrs.book_room(101, "Carol",
                      today - datetime.timedelta(days=365),
                      today - datetime.timedelta(days=363))

    # T5: successful booking returns first reservation ID
    res1 = hrs.book_room(101, "Dave", today + datetime.timedelta(days=30), today + datetime.timedelta(days=32))
    assert res1 == "RES-0001"
    total1 = hrs.reservations[res1].total_price
    assert total1 == 200.0

    # T6: overlapping reservation should raise RoomUnavailableError
    with pytest.raises(RoomUnavailableError):
        hrs.book_room(101, "Eve", today + datetime.timedelta(days=31), today + datetime.timedelta(days=33))

    # T7: unknown reservation cancellation should raise ReservationNotFoundError
    with pytest.raises(ReservationNotFoundError):
        hrs.cancel_reservation("NON-EXISTENT")

    # T8: >7 days before check-in returns full refund
    res2 = hrs.book_room(101, "Grace", today + datetime.timedelta(days=40), today + datetime.timedelta(days=42))
    assert res2 == "RES-0002"
    refund2 = hrs.cancel_reservation(res2)
    assert refund2 == 200.0

    # T9: 2-7 days before check-in returns 50% refund
    res3 = hrs.book_room(101, "Heidi", today + datetime.timedelta(days=6), today + datetime.timedelta(days=8))
    assert res3 == "RES-0003"
    refund3 = hrs.cancel_reservation(res3)
    assert refund3 == 100.0

    # T10: <2 days before check-in returns 0 refund
    res4 = hrs.book_room(101, "Ivan", today + datetime.timedelta(days=1), today + datetime.timedelta(days=3))
    assert res4 == "RES-0004"
    refund4 = hrs.cancel_reservation(res4)
    assert refund4 == 0.0

    # T11: date within an active reservation returns occupied room list
    occupancy = hrs.get_room_occupancy(today + datetime.timedelta(days=31))
    assert occupancy == [101]

    # T12: date with no reservations returns empty list
    occupancy_empty = hrs.get_room_occupancy(today + datetime.timedelta(days=100))
    assert occupancy_empty == []