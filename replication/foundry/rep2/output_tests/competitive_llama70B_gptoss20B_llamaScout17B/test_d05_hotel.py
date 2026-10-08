import pytest
import datetime
from data.input_code.d05_hotel import *

@pytest.fixture
def hotel():
    return HotelReservationSystem()

def test_T1_OK_add_room(hotel):
    hotel.add_room(1, 'single', 100.0)
    assert 1 in hotel.rooms
    assert hotel.rooms[1]['price_per_night'] == 100.0
    assert hotel.rooms[1]['type'] == 'single'

def test_T2_ERR_add_room_negative_price(hotel):
    with pytest.raises(ValueError):
        hotel.add_room(1, 'single', -50.0)

def test_T3_OK_book_room_creates_reservation(hotel):
    hotel.add_room(1, 'single', 100.0)
    check_in = datetime.date.today() + datetime.timedelta(days=30)
    check_out = check_in + datetime.timedelta(days=5)
    res_id = hotel.book_room(1, 'John Doe', check_in, check_out)
    assert res_id == 'RES-0001'
    assert res_id in hotel.reservations
    assert hotel.reservations[res_id].room_number == 1

def test_T4_ERR_book_room_nonexistent_room(hotel):
    check_in = datetime.date.today() + datetime.timedelta(days=10)
    check_out = check_in + datetime.timedelta(days=5)
    with pytest.raises(RoomNotFoundError):
        hotel.book_room(2, 'John Doe', check_in, check_out)

def test_T5_ERR_invalid_dates(hotel):
    hotel.add_room(1, 'single', 100.0)
    check_in = datetime.date.today() + datetime.timedelta(days=10)
    check_out = check_in - datetime.timedelta(days=1)
    with pytest.raises(InvalidDateError):
        hotel.book_room(1, 'John Doe', check_in, check_out)

def test_T6_ERR_book_in_past(hotel):
    hotel.add_room(1, 'single', 100.0)
    check_in = datetime.date.today() - datetime.timedelta(days=1)
    check_out = datetime.date.today() + datetime.timedelta(days=1)
    with pytest.raises(InvalidDateError):
        hotel.book_room(1, 'John Doe', check_in, check_out)

def test_T7_OK_cancel_reservation_full_refund(hotel):
    hotel.add_room(1, 'single', 100.0)
    check_in = datetime.date.today() + datetime.timedelta(days=30)
    check_out = check_in + datetime.timedelta(days=5)
    res_id = hotel.book_room(1, 'John Doe', check_in, check_out)
    total = hotel.reservations[res_id].total_price
    refund = hotel.cancel_reservation(res_id)
    assert refund == total

def test_T8_ERR_cancel_reservation_not_found(hotel):
    with pytest.raises(ReservationNotFoundError):
        hotel.cancel_reservation('RES-9999')

def test_T9_OK_get_room_occupancy(hotel):
    hotel.add_room(1, 'single', 100.0)
    check_in = datetime.date.today() + datetime.timedelta(days=20)
    check_out = check_in + datetime.timedelta(days=3)
    res_id = hotel.book_room(1, 'Alice', check_in, check_out)
    date_to_check = check_in + datetime.timedelta(days=1)
    occupancy = hotel.get_room_occupancy(date_to_check)
    assert 1 in occupancy

def test_T10_OK_is_room_available(hotel):
    hotel.add_room(1, 'single', 100.0)
    check_in = datetime.date.today() + datetime.timedelta(days=40)
    check_out = check_in + datetime.timedelta(days=5)
    hotel.book_room(1, 'Bob', check_in, check_out)
    # Non-overlapping range
    new_check_in = check_in + datetime.timedelta(days=6)
    new_check_out = new_check_in + datetime.timedelta(days=4)
    available = hotel._is_room_available(1, new_check_in, new_check_out)
    assert available is True

def test_T11_ERR_book_room_unavailable(hotel):
    hotel.add_room(1, 'single', 100.0)
    check_in = datetime.date.today() + datetime.timedelta(days=10)
    check_out = check_in + datetime.timedelta(days=5)
    hotel.book_room(1, 'Carol', check_in, check_out)
    # Overlapping range
    overlap_in = check_in + datetime.timedelta(days=2)
    overlap_out = overlap_in + datetime.timedelta(days=4)
    with pytest.raises(RoomUnavailableError):
        hotel.book_room(1, 'Dave', overlap_in, overlap_out)

def test_T_MISSING_EDGE_CANCEL_7DAYS(hotel):
    hotel.add_room(1, 'single', 100.0)
    check_in = datetime.date.today() + datetime.timedelta(days=7)
    check_out = check_in + datetime.timedelta(days=1)
    res_id = hotel.book_room(1, 'John Doe', check_in, check_out)
    total = hotel.reservations[res_id].total_price
    refund = hotel.cancel_reservation(res_id)
    assert refund == total * 0.5

def test_T_MISSING_EDGE_CANCEL_2DAYS(hotel):
    hotel.add_room(1, 'single', 100.0)
    check_in = datetime.date.today() + datetime.timedelta(days=2)
    check_out = check_in + datetime.timedelta(days=1)
    res_id = hotel.book_room(1, 'John Doe', check_in, check_out)
    total = hotel.reservations[res_id].total_price
    refund = hotel.cancel_reservation(res_id)
    assert refund == total * 0.5

def test_T_MISSING_GET_ROOM_OCCUPANCY_NO_RESERVATIONS(hotel):
    occupancy = hotel.get_room_occupancy(datetime.date.today())
    assert occupancy == []

def test_T_MISSING_GET_ROOM_OCCUPANCY_MULTIPLE_RESERVATIONS(hotel):
    hotel.add_room(1, 'single', 100.0)
    hotel.add_room(2, 'double', 200.0)
    check_in1 = datetime.date.today() + datetime.timedelta(days=10)
    check_out1 = check_in1 + datetime.timedelta(days=3)
    hotel.book_room(1, 'Alice', check_in1, check_out1)
    check_in2 = datetime.date.today() + datetime.timedelta(days=10)
    check_out2 = check_in2 + datetime.timedelta(days=3)
    hotel.book_room(2, 'Bob', check_in2, check_out2)
    date_to_check = check_in1
    occupancy = hotel.get_room_occupancy(date_to_check)
    assert occupancy == [1, 2]

@pytest.mark.parametrize("check_in, check_out, expected", [
    (datetime.date.today(), datetime.date.today() + datetime.timedelta(days=1), 'RES-0001'),
    (datetime.date.today() - datetime.timedelta(days=1), datetime.date.today(), 'InvalidDateError')
])
def test_T_MISSING_BOOK_ROOM_SAME_DAY(hotel, check_in, check_out, expected):
    hotel.add_room(1, 'single', 100.0)
    if isinstance(expected, str) and expected.startswith('RES-'):
        res_id = hotel.book_room(1, 'John Doe', check_in, check_out)
        assert res_id == expected
    else:
        with pytest.raises(globals()[expected]):
            hotel.book_room(1, 'John Doe', check_in, check_out)

def test_T_MISSING_EDGE_CANCEL_LESS_2DAYS(hotel):
    hotel.add_room(1, 'single', 100.0)
    check_in = datetime.date.today() + datetime.timedelta(days=1)
    check_out = check_in + datetime.timedelta(days=1)
    res_id = hotel.book_room(1, 'John Doe', check_in, check_out)
    refund = hotel.cancel_reservation(res_id)
    assert refund == 0.0

def test_T_MISSING_EDGE_BOOK_ROOM_SAME_CHECKIN_CHECKOUT(hotel):
    hotel.add_room(1, 'single', 100.0)
    check_in = datetime.date.today()
    check_out = datetime.date.today()
    with pytest.raises(InvalidDateError):
        hotel.book_room(1, 'John Doe', check_in, check_out)

def test_T_MISSING_EDGE_GET_ROOM_OCCUPANCY_CHECKIN_DATE(hotel):
    date_to_check = datetime.date(2100, 1, 1)
    occupancy = hotel.get_room_occupancy(date_to_check)
    assert occupancy == []

def test_T_MISSING_EDGE_GET_ROOM_OCCUPANCY_CHECKOUT_DATE(hotel):
    date_to_check = datetime.date(2100, 1, 2)
    occupancy = hotel.get_room_occupancy(date_to_check)
    assert occupancy == []

def test_T_MISSING_EDGE_IS_ROOM_AVAILABLE_OVERLAPPING_RESERVATIONS(hotel):
    hotel.add_room(1, 'single', 100.0)
    today = datetime.date.today()
    existing_check_in = today + datetime.timedelta(days=5)
    existing_check_out = existing_check_in + datetime.timedelta(days=5)
    hotel.book_room(1, 'Alice', existing_check_in, existing_check_out)
    probe_check_in = today + datetime.timedelta(days=7)
    probe_check_out = probe_check_in + datetime.timedelta(days=3)
    available = hotel._is_room_available(1, probe_check_in, probe_check_out)
    assert available is False