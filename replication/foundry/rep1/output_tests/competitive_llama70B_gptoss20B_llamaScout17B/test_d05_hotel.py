import pytest
from data.input_code.d05_hotel import *
from datetime import date, timedelta

@pytest.fixture
def hotel_reservation_system():
    return HotelReservationSystem()

def test_add_room_success(hotel_reservation_system):
    hotel_reservation_system.add_room(1, 'single', 100.0)
    assert 1 in hotel_reservation_system.rooms

def test_add_room_error(hotel_reservation_system):
    with pytest.raises(ValueError):
        hotel_reservation_system.add_room(1, 'single', -100.0)

def test_book_room_success(hotel_reservation_system):
    hotel_reservation_system.add_room(1, 'single', 100.0)
    check_in = date.today() + timedelta(days=5)
    check_out = check_in + timedelta(days=2)
    res_id = hotel_reservation_system.book_room(1, 'John Doe', check_in, check_out)
    assert res_id == 'RES-0001'

def test_book_room_error(hotel_reservation_system):
    hotel_reservation_system.add_room(1, 'single', 100.0)
    # Case 1: room not found
    with pytest.raises(RoomNotFoundError):
        hotel_reservation_system.book_room(2, 'John Doe', date.today() + timedelta(days=1), date.today() + timedelta(days=3))
    # Case 2: invalid date order
    with pytest.raises(InvalidDateError):
        hotel_reservation_system.book_room(1, 'John Doe', date.today() + timedelta(days=5), date.today() + timedelta(days=4))
    # Case 3: booking in the past
    with pytest.raises(InvalidDateError):
        hotel_reservation_system.book_room(1, 'John Doe', date.today() - timedelta(days=1), date.today() + timedelta(days=1))

def test_book_room_unavailable(hotel_reservation_system):
    hotel_reservation_system.add_room(1, 'single', 100.0)
    in1 = date.today() + timedelta(days=3)
    out1 = in1 + timedelta(days=4)
    hotel_reservation_system.book_room(1, 'John Doe', in1, out1)
    with pytest.raises(RoomUnavailableError):
        hotel_reservation_system.book_room(1, 'Jane Doe', in1 + timedelta(days=1), in1 + timedelta(days=2))

def test_cancel_reservation_success(hotel_reservation_system):
    hotel_reservation_system.add_room(1, 'single', 100.0)
    in1 = date.today() + timedelta(days=10)
    out1 = in1 + timedelta(days=5)
    reservation_id = hotel_reservation_system.book_room(1, 'John Doe', in1, out1)
    amount = hotel_reservation_system.cancel_reservation(reservation_id)
    assert isinstance(amount, float)

def test_cancel_reservation_error(hotel_reservation_system):
    with pytest.raises(ReservationNotFoundError):
        hotel_reservation_system.cancel_reservation('RES-0001')

def test_get_room_occupancy(hotel_reservation_system):
    hotel_reservation_system.add_room(1, 'single', 100.0)
    in1 = date.today() + timedelta(days=2)
    out1 = in1 + timedelta(days=3)
    hotel_reservation_system.book_room(1, 'John Doe', in1, out1)
    occupancy = hotel_reservation_system.get_room_occupancy(in1 + timedelta(days=1))
    assert occupancy == [1]

def test_is_room_available(hotel_reservation_system):
    hotel_reservation_system.add_room(1, 'single', 100.0)
    in1 = date.today() + timedelta(days=5)
    out1 = in1 + timedelta(days=4)
    hotel_reservation_system.book_room(1, 'John Doe', in1, out1)
    # Overlapping period should be unavailable
    assert hotel_reservation_system._is_room_available(1, in1, out1) == False
    # A non-overlapping period should be available
    assert hotel_reservation_system._is_room_available(1, in1 + timedelta(days=5), in1 + timedelta(days=9)) == True

def test_T_MISSING_EDGE_BOOKING(hotel_reservation_system, monkeypatch):
    import datetime
    class FixedDate(datetime.date):
        @classmethod
        def today(cls):
            return cls(2024, 9, 8)
    monkeypatch.setattr(datetime, 'date', FixedDate, raising=True)

    hotel_reservation_system.add_room(1, 'single', 142.85714285714286)
    check_in = FixedDate(2024, 9, 16)
    check_out = FixedDate(2024, 9, 23)
    res_id = hotel_reservation_system.book_room(1, 'John Doe', check_in, check_out)
    assert res_id == 'RES-0001'


def test_T_MISSING_EDGE_CANCEL_7DAYS(hotel_reservation_system, monkeypatch):
    import datetime
    class FixedDate(datetime.date):
        @classmethod
        def today(cls):
            return cls(2024, 9, 8)
    monkeypatch.setattr(datetime, 'date', FixedDate, raising=True)

    hotel_reservation_system.add_room(1, 'single', 142.85714285714286)
    check_in = FixedDate(2024, 9, 16)
    check_out = FixedDate(2024, 9, 23)
    res_id = hotel_reservation_system.book_room(1, 'John Doe', check_in, check_out)
    amount = hotel_reservation_system.cancel_reservation(res_id)
    assert amount == 1000.0


def test_T_MISSING_EDGE_CANCEL_2DAYS(hotel_reservation_system, monkeypatch):
    import datetime
    class FixedDate2(datetime.date):
        @classmethod
        def today(cls):
            return cls(2024, 9, 14)
    monkeypatch.setattr(datetime, 'date', FixedDate2, raising=True)

    hotel_reservation_system.add_room(1, 'single', 142.85714285714286)
    check_in = FixedDate2(2024, 9, 16)
    check_out = FixedDate2(2024, 9, 23)
    res_id = hotel_reservation_system.book_room(1, 'John Doe', check_in, check_out)
    amount = hotel_reservation_system.cancel_reservation(res_id)
    assert amount == 500.0


def test_T_MISSING_EDGE_GET_OCCUPANCY_CHECKIN(hotel_reservation_system, monkeypatch):
    import datetime
    class FixedDate(datetime.date):
        @classmethod
        def today(cls):
            return cls(2024, 9, 8)
    monkeypatch.setattr(datetime, 'date', FixedDate, raising=True)

    hotel_reservation_system.add_room(1, 'single', 100.0)
    in_date = FixedDate(2024, 9, 16)
    out_date = FixedDate(2024, 9, 23)
    hotel_reservation_system.book_room(1, 'John Doe', in_date, out_date)
    occupancy = hotel_reservation_system.get_room_occupancy(FixedDate(2024, 9, 16))
    assert occupancy == [1]


def test_T_MISSING_EDGE_GET_OCCUPANCY_CHECKOUT(hotel_reservation_system, monkeypatch):
    import datetime
    class FixedDate(datetime.date):
        @classmethod
        def today(cls):
            return cls(2024, 9, 8)
    monkeypatch.setattr(datetime, 'date', FixedDate, raising=True)

    hotel_reservation_system.add_room(1, 'single', 100.0)
    in_date = FixedDate(2024, 9, 16)
    out_date = FixedDate(2024, 9, 23)
    hotel_reservation_system.book_room(1, 'John Doe', in_date, out_date)
    occupancy = hotel_reservation_system.get_room_occupancy(FixedDate(2024, 9, 22))
    assert occupancy == [1]


def test_T_MISSING_EDGE_GET_OCCUPANCY_AFTER_CHECKOUT(hotel_reservation_system, monkeypatch):
    import datetime
    class FixedDate(datetime.date):
        @classmethod
        def today(cls):
            return cls(2024, 9, 8)
    monkeypatch.setattr(datetime, 'date', FixedDate, raising=True)

    hotel_reservation_system.add_room(1, 'single', 100.0)
    in_date = FixedDate(2024, 9, 16)
    out_date = FixedDate(2024, 9, 23)
    hotel_reservation_system.book_room(1, 'John Doe', in_date, out_date)
    occupancy = hotel_reservation_system.get_room_occupancy(FixedDate(2024, 9, 23))
    assert occupancy == []

def test_T_MISSING_EDGE_CANCEL_LESS_THAN_2_DAYS(hotel_reservation_system, monkeypatch):
    import datetime
    class FixedDate(datetime.date):
        @classmethod
        def today(cls):
            return cls(2024, 9, 15)
    monkeypatch.setattr(datetime, 'date', FixedDate, raising=True)

    hotel_reservation_system.add_room(1, 'single', 100.0)
    check_in = FixedDate(2024, 9, 16)
    check_out = FixedDate(2024, 9, 23)
    res_id = hotel_reservation_system.book_room(1, 'John Doe', check_in, check_out)
    amount = hotel_reservation_system.cancel_reservation(res_id)
    assert amount == 0.0


def test_T_MISSING_EDGE_BOOKING_ON_CHECKIN_DATE(hotel_reservation_system, monkeypatch):
    import datetime
    class FixedDate(datetime.date):
        @classmethod
        def today(cls):
            return cls(2024, 9, 16)
    monkeypatch.setattr(datetime, 'date', FixedDate, raising=True)

    hotel_reservation_system.add_room(1, 'single', 100.0)
    check_in = FixedDate(2024, 9, 16)
    check_out = FixedDate(2024, 9, 17)
    res_id = hotel_reservation_system.book_room(1, 'John Doe', check_in, check_out)
    assert res_id == 'RES-0001'


def test_T_MISSING_EDGE_BOOKING_ON_CHECKOUT_DATE(hotel_reservation_system, monkeypatch):
    import datetime
    class FixedDate(datetime.date):
        @classmethod
        def today(cls):
            return cls(2024, 9, 15)
    monkeypatch.setattr(datetime, 'date', FixedDate, raising=True)

    hotel_reservation_system.add_room(1, 'single', 100.0)
    with pytest.raises(InvalidDateError):
        hotel_reservation_system.book_room(1, 'John Doe', FixedDate(2024, 9, 16), FixedDate(2024, 9, 16))


def test_T_MISSING_EDGE_GET_OCCUPANCY_BEFORE_CHECKIN(hotel_reservation_system, monkeypatch):
    import datetime
    class FixedDate(datetime.date):
        @classmethod
        def today(cls):
            return cls(2024, 9, 15)
    monkeypatch.setattr(datetime, 'date', FixedDate, raising=True)

    hotel_reservation_system.add_room(1, 'single', 100.0)
    in_date = FixedDate(2024, 9, 16)
    out_date = FixedDate(2024, 9, 23)
    hotel_reservation_system.book_room(1, 'John Doe', in_date, out_date)
    occupancy = hotel_reservation_system.get_room_occupancy(FixedDate(2024, 9, 15))
    assert occupancy == []


def test_T_MISSING_EDGE_GET_OCCUPANCY_AFTER_CHECKOUT(hotel_reservation_system, monkeypatch):
    import datetime
    class FixedDate(datetime.date):
        @classmethod
        def today(cls):
            return cls(2024, 9, 15)
    monkeypatch.setattr(datetime, 'date', FixedDate, raising=True)

    hotel_reservation_system.add_room(1, 'single', 100.0)
    in_date = FixedDate(2024, 9, 16)
    out_date = FixedDate(2024, 9, 23)
    hotel_reservation_system.book_room(1, 'John Doe', in_date, out_date)
    occupancy = hotel_reservation_system.get_room_occupancy(FixedDate(2024, 9, 24))
    assert occupancy == []