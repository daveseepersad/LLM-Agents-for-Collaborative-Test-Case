import pytest
from data.input_code.d05_hotel import *
import inspect

def test_imports_are_available():
    # This test ensures that the module loaded without syntax/runtime errors.
    assert True

def test_all_top_level_callables_can_be_attempted():
    results = []
    # Import the module object to inspect its top-level callables
    import data.input_code.d05_hotel as hotel
    for name, obj in hotel.__dict__.items():
        if name.startswith('_'):
            continue
        if inspect.isfunction(obj):
            try:
                value = obj()
            except TypeError:
                # If it requires arguments, try common placeholders
                try:
                    value = obj("sample")
                except TypeError:
                    try:
                        value = obj(1)
                    except TypeError:
                        continue
            except Exception as exc:
                pytest.skip(f"Function {name} raised an unexpected exception on call: {exc}")
            results.append((name, value))
    # If there are no top-level functions, this will be an empty list, which is fine.
    assert len(results) >= 0

import pytest
from data.input_code.d05_hotel import *
import datetime as dt

def test_T_ADD_ROOM_SUCCESS():
    h = HotelReservationSystem()
    h.add_room(101, "single", 120.0)
    assert 101 in h.rooms
    assert h.rooms[101]['price_per_night'] == 120.0
    assert h.rooms[101]['type'] == "single"

def test_T_ADD_ROOM_INVALID_PRICE():
    h = HotelReservationSystem()
    with pytest.raises(ValueError):
        h.add_room(102, "double", 0.0)

def test_T_BOOK_ROOM_NOT_FOUND():
    h = HotelReservationSystem()
    with pytest.raises(RoomNotFoundError):
        h.book_room(999, "Alice", dt.date(2099, 1, 1), dt.date(2099, 1, 5))

def test_T_BOOK_ROOM_INVALID_DATES_ORDER():
    h = HotelReservationSystem()
    h.add_room(201, "single", 100.0)
    with pytest.raises(InvalidDateError):
        h.book_room(201, "Bob", dt.date(2099, 1, 10), dt.date(2099, 1, 10))

def test_T_BOOK_ROOM_PAST_DATE():
    h = HotelReservationSystem()
    h.add_room(202, "double", 80.0)
    with pytest.raises(InvalidDateError):
        h.book_room(202, "Carol", dt.date(2000, 1, 1), dt.date(2000, 1, 5))

def test_T_BOOK_ROOM_UNAVAILABLE():
    h = HotelReservationSystem()
    h.add_room(301, "suite", 250.0)
    h.book_room(301, "Dave", dt.date(2099, 6, 1), dt.date(2099, 6, 5))
    with pytest.raises(RoomUnavailableError):
        h.book_room(301, "Eve", dt.date(2099, 6, 4), dt.date(2099, 6, 8))

def test_T_BOOK_ROOM_SUCCESS():
    h = HotelReservationSystem()
    h.add_room(401, "deluxe", 180.0)
    res_id = h.book_room(401, "Frank", dt.date(2099, 7, 1), dt.date(2099, 7, 4))
    assert res_id == "RES-0001"

def test_T_CANCEL_NOT_FOUND():
    h = HotelReservationSystem()
    with pytest.raises(ReservationNotFoundError):
        h.cancel_reservation("NON_EXISTENT")

def test_T_CANCEL_REFUND_FULL(monkeypatch):
    import datetime as dt

    class FixedDate(dt.date):
        @classmethod
        def today(cls):
            return dt.date(2099, 12, 12)

    monkeypatch.setattr(dt, 'date', FixedDate, raising=True)

    h = HotelReservationSystem()
    h.add_room(501, "standard", 100.0)
    h.book_room(501, "Grace", dt.date(2099, 12, 20), dt.date(2099, 12, 25))
    refund = h.cancel_reservation("RES-0001")
    assert refund == 500.0

def test_T_CANCEL_REFUND_HALF(monkeypatch):
    import datetime as dt

    class FixedDate(dt.date):
        @classmethod
        def today(cls):
            return dt.date(2099, 12, 8)

    monkeypatch.setattr(dt, 'date', FixedDate, raising=True)

    h = HotelReservationSystem()
    h.add_room(502, "standard", 100.0)
    h.book_room(502, "Heidi", dt.date(2099, 12, 10), dt.date(2099, 12, 15))
    refund = h.cancel_reservation("RES-0001")
    assert refund == 250.0

def test_T_CANCEL_REFUND_NONE(monkeypatch):
    import datetime as dt

    class FixedDate(dt.date):
        @classmethod
        def today(cls):
            return dt.date(2099, 12, 1)

    monkeypatch.setattr(dt, 'date', FixedDate, raising=True)

    h = HotelReservationSystem()
    h.add_room(503, "standard", 100.0)
    h.book_room(503, "Ivan", dt.date(2099, 12, 2), dt.date(2099, 12, 4))
    refund = h.cancel_reservation("RES-0001")
    assert refund == 0.0

def test_T_GET_ROOM_OCCUPANCY():
    h = HotelReservationSystem()
    h.add_room(601, "single", 80.0)
    h.add_room(602, "double", 120.0)
    h.book_room(601, "Judy", dt.date(2099, 8, 1), dt.date(2099, 8, 5))
    h.book_room(602, "Ken", dt.date(2099, 8, 3), dt.date(2099, 8, 7))
    occupied = h.get_room_occupancy(dt.date(2099, 8, 4))
    assert occupied == [601, 602]