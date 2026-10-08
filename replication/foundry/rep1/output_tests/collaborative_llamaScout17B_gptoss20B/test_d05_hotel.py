import pytest
from data.input_code.d05_hotel import *
import sys
import inspect

def collect_zero_arg_callables():
    mod = sys.modules.get("data.input_code.d05_hotel")
    results = []
    if mod is None:
        return results

    for name, obj in vars(mod).items():
        # Top-level functions with zero required args
        if inspect.isfunction(obj):
            try:
                sig = inspect.signature(obj)
                required_args = [
                    p for p in sig.parameters.values()
                    if p.default is inspect._empty
                    and p.kind in (p.POSITIONAL_ONLY, p.POSITIONAL_OR_KEYWORD)
                ]
                if len(required_args) == 0:
                    results.append((name, obj))
            except (TypeError, ValueError):
                pass

        # Classes with zero-arg constructors and zero-arg methods
        elif inspect.isclass(obj):
            try:
                cls_sig = inspect.signature(obj)
                ctor_required = [
                    p for p in cls_sig.parameters.values()
                    if p.default is inspect._empty and p.name != 'self'
                ]
                if len(ctor_required) == 0:
                    instance = obj()
                    for m_name in dir(obj):
                        if m_name.startswith("__"):
                            continue
                        attribute = getattr(obj, m_name)
                        if callable(attribute):
                            bound_method = getattr(instance, m_name, None)
                            if bound_method is None or not callable(bound_method):
                                continue
                            try:
                                m_sig = inspect.signature(bound_method)
                                m_required = [
                                    p for p in m_sig.parameters.values()
                                    if p.default is inspect._empty and p.name != 'self'
                                    and p.kind in (p.POSITIONAL_ONLY, p.POSITIONAL_OR_KEYWORD)
                                ]
                                if len(m_required) == 0:
                                    results.append((f"{name}.{m_name}", bound_method))
                            except (TypeError, ValueError):
                                pass
            except (TypeError, ValueError):
                pass

    return results

@pytest.mark.parametrize("label,fn", collect_zero_arg_callables())
def test_zero_arg_callables(label, fn):
    # Ensure calling zero-arg callables does not raise
    fn()

import pytest
from data.input_code.d05_hotel import *
import datetime

def test_room_price_non_positive():
    hr = HotelReservationSystem()
    with pytest.raises(ValueError):
        hr.add_room(1, "test", 0)

def test_book_past_dates():
    hr = HotelReservationSystem()
    hr.add_room(1, "test", 100)
    past_in = datetime.date(2022, 1, 1)
    past_out = datetime.date(2022, 1, 2)
    with pytest.raises(InvalidDateError):
        hr.book_room(1, "test", past_in, past_out)

def test_cancel_non_existent():
    hr = HotelReservationSystem()
    with pytest.raises(ReservationNotFoundError):
        hr.cancel_reservation("non-existent")

def test_get_occupancy_no_reservations():
    hr = HotelReservationSystem()
    hr.add_room(1, "test", 100)
    date = datetime.date(2024, 1, 1)
    result = hr.get_room_occupancy(date)
    assert result == []

def test_book_overlap_raises_room_unavailable():
    hr = HotelReservationSystem()
    hr.add_room(1, "test", 100)
    today = datetime.date.today()
    hr.book_room(1, "test", today, today + datetime.timedelta(days=3))
    with pytest.raises(RoomUnavailableError):
        hr.book_room(1, "test2", today + datetime.timedelta(days=1), today + datetime.timedelta(days=2))

def test_cancel_refund_policy_for_soon_checkin():
    hr = HotelReservationSystem()
    hr.add_room(1, "test", 100)
    today = datetime.date.today()
    check_in = today + datetime.timedelta(days=1)
    check_out = today + datetime.timedelta(days=3)
    res_id = hr.book_room(1, "test", check_in, check_out)
    refund = hr.cancel_reservation(res_id)
    assert refund == 0.0

import pytest
from data.input_code.d05_hotel import *
import datetime

def test_book_non_existent_room_raises():
    hr = HotelReservationSystem()
    today = datetime.date.today()
    with pytest.raises(RoomNotFoundError):
        hr.book_room(1, "test", today + datetime.timedelta(days=1), today + datetime.timedelta(days=2))

def test_book_invalid_dates_raises():
    hr = HotelReservationSystem()
    hr.add_room(1, "test", 100)
    today = datetime.date.today()
    check_in = today + datetime.timedelta(days=2)
    check_out = today + datetime.timedelta(days=1)
    with pytest.raises(InvalidDateError):
        hr.book_room(1, "test", check_in, check_out)

def test_cancel_refund_more_than_7_days():
    hr = HotelReservationSystem()
    hr.add_room(1, "test", 100)
    today = datetime.date.today()
    check_in = today + datetime.timedelta(days=8)
    check_out = today + datetime.timedelta(days=10)
    res_id = hr.book_room(1, "test", check_in, check_out)
    assert res_id == "RES-0001"
    refund = hr.cancel_reservation(res_id)
    assert refund == 200.0

def test_cancel_refund_between_2_and_7_days():
    hr = HotelReservationSystem()
    hr.add_room(1, "test", 100)
    today = datetime.date.today()
    check_in = today + datetime.timedelta(days=3)
    check_out = today + datetime.timedelta(days=5)
    res_id = hr.book_room(1, "test", check_in, check_out)
    assert res_id == "RES-0001"
    refund = hr.cancel_reservation(res_id)
    assert refund == 100.0

def test_get_room_occupancy_with_reservations():
    hr = HotelReservationSystem()
    hr.add_room(1, "test", 100)
    today = datetime.date.today()
    hr.book_room(1, "test", today, today + datetime.timedelta(days=3))
    occ = hr.get_room_occupancy(today + datetime.timedelta(days=1))
    assert occ == [1]

def test_book_room_success():
    hr = HotelReservationSystem()
    hr.add_room(1, "test", 100)
    today = datetime.date.today()
    res_id = hr.book_room(1, "test", today + datetime.timedelta(days=1), today + datetime.timedelta(days=2))
    assert res_id == "RES-0001"