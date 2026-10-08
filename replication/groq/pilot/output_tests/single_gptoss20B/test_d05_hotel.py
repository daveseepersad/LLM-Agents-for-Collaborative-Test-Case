import pytest
from datetime import date, timedelta
from data.input_code.d05_hotel import (
    HotelReservationSystem,
    RoomNotFoundError,
    RoomUnavailableError,
    InvalidDateError,
    ReservationNotFoundError,
)

# Helper to freeze today's date in the module under test
def freeze_today(monkeypatch, frozen_date: date):
    monkeypatch.setattr(
        "data.input_code.d05_hotel.datetime.date.today",
        lambda: frozen_date,
    )

@pytest.fixture
def system():
    return HotelReservationSystem()

def test_add_room_success(system):
    system.add_room(101, "Deluxe", 150.0)
    assert 101 in system.rooms
    assert system.rooms[101]["type"] == "Deluxe"
    assert system.rooms[101]["price_per_night"] == 150.0

def test_add_room_negative_price(system):
    with pytest.raises(ValueError):
        system.add_room(102, "Standard", -50.0)

def test_is_room_available_no_reservations(system):
    # No reservations yet, should be available
    assert system._is_room_available(201, date.today(), date.today() + timedelta(days=1))







def test_cancel_reservation_not_found(system):
    with pytest.raises(ReservationNotFoundError):
        system.cancel_reservation("NON-EXISTENT")





def test_add_room_overwrite(system):
    system.add_room(1201, "Standard", 60.0)
    assert system.rooms[1201]["price_per_night"] == 60.0
    system.add_room(1201, "Deluxe", 90.0)
    assert system.rooms[1201]["type"] == "Deluxe"
    assert system.rooms[1201]["price_per_night"] == 90.0

