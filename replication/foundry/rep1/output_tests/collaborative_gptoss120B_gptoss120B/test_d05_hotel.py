import pytest
import datetime
from datetime import timedelta
from data.input_code.d05_hotel import *

# ----------------------------------------------------------------------
# Helper to build a system from a JSON‑style setup dict
# ----------------------------------------------------------------------
def build_system(setup: dict | None) -> HotelReservationSystem:
    hrs = HotelReservationSystem()
    if not setup:
        return hrs

    # add rooms
    for rn_str, info in setup.get("rooms", {}).items():
        rn = int(rn_str)
        hrs.add_room(rn, info["type"], info["price_per_night"])

    # add reservations
    for _, rinfo in setup.get("reservations", {}).items():
        reservation = Reservation(
            reservation_id=rinfo["reservation_id"],
            room_number=rinfo["room_number"],
            user_name=rinfo["user_name"],
            check_in=datetime.date.fromisoformat(rinfo["check_in"]),
            check_out=datetime.date.fromisoformat(rinfo["check_out"]),
            total_price=rinfo["total_price"],
        )
        hrs.reservations[reservation.reservation_id] = reservation

    return hrs

# ----------------------------------------------------------------------
# T1 – Add room (successful)
# ----------------------------------------------------------------------
def test_add_room_ok():
    hrs = HotelReservationSystem()
    hrs.add_room(101, "Deluxe", 150.0)
    assert 101 in hrs.rooms
    assert hrs.rooms[101]["type"] == "Deluxe"
    assert hrs.rooms[101]["price_per_night"] == 150.0

# ----------------------------------------------------------------------
# T2 – Add room (price <= 0 raises ValueError)
# ----------------------------------------------------------------------
def test_add_room_value_error():
    hrs = HotelReservationSystem()
    with pytest.raises(ValueError):
        hrs.add_room(102, "Standard", 0.0)

# ----------------------------------------------------------------------
# T3‑T6 – Book room error scenarios (parametrized)
# ----------------------------------------------------------------------
@pytest.mark.parametrize(
    "setup,input,expected_exc",
    [
        # T3 – room does not exist
        (
            None,
            {
                "room_number": 999,
                "user_name": "Alice",
                "check_in": (datetime.date.today() + timedelta(days=10)).isoformat(),
                "check_out": (datetime.date.today() + timedelta(days=12)).isoformat(),
            },
            RoomNotFoundError,
        ),
        # T4 – check‑in == check‑out (invalid order)
        (
            {"rooms": {"201": {"type": "Suite", "price_per_night": 200.0}}},
            {
                "room_number": 201,
                "user_name": "Bob",
                "check_in": (datetime.date.today() + timedelta(days=15)).isoformat(),
                "check_out": (datetime.date.today() + timedelta(days=15)).isoformat(),
            },
            InvalidDateError,
        ),
        # T5 – booking in the past
        (
            {"rooms": {"202": {"type": "Standard", "price_per_night": 120.0}}},
            {
                "room_number": 202,
                "user_name": "Carol",
                "check_in": (datetime.date.today() - timedelta(days=1)).isoformat(),
                "check_out": (datetime.date.today() + timedelta(days=1)).isoformat(),
            },
            InvalidDateError,
        ),
        # T6 – overlapping reservation (room unavailable)
        (
            {
                "rooms": {"301": {"type": "Deluxe", "price_per_night": 180.0}},
                "reservations": {
                    "RES-0001": {
                        "reservation_id": "RES-0001",
                        "room_number": 301,
                        "user_name": "Eve",
                        "check_in": (datetime.date.today() + timedelta(days=10)).isoformat(),
                        "check_out": (datetime.date.today() + timedelta(days=15)).isoformat(),
                        "total_price": 900.0,
                    }
                },
            },
            {
                "room_number": 301,
                "user_name": "Dave",
                "check_in": (datetime.date.today() + timedelta(days=12)).isoformat(),
                "check_out": (datetime.date.today() + timedelta(days=14)).isoformat(),
            },
            RoomUnavailableError,
        ),
    ],
    ids=["RoomNotFound", "InvalidDateOrder", "InvalidDatePast", "RoomUnavailable"],
)
def test_book_room_errors(setup, input, expected_exc):
    hrs = build_system(setup)

    check_in = datetime.date.fromisoformat(input["check_in"])
    check_out = datetime.date.fromisoformat(input["check_out"])

    with pytest.raises(expected_exc):
        hrs.book_room(
            input["room_number"], input["user_name"], check_in, check_out
        )

# ----------------------------------------------------------------------
# T7 – Successful booking returns RES-0001
# ----------------------------------------------------------------------
def test_book_room_success():
    hrs = HotelReservationSystem()
    hrs.add_room(401, "Standard", 100.0)

    res_id = hrs.book_room(
        401,
        "Frank",
        datetime.date.today() + timedelta(days=10),
        datetime.date.today() + timedelta(days=13),
    )
    assert res_id == "RES-0001"
    assert res_id in hrs.reservations

# ----------------------------------------------------------------------
# T8 – Cancel non‑existent reservation raises ReservationNotFoundError
# ----------------------------------------------------------------------
def test_cancel_reservation_not_found():
    hrs = HotelReservationSystem()
    with pytest.raises(ReservationNotFoundError):
        hrs.cancel_reservation("RES-9999")

# ----------------------------------------------------------------------
# T9‑T11 – Cancel reservation refund policy (parametrized)
# ----------------------------------------------------------------------
@pytest.mark.parametrize(
    "setup,res_id,expected_refund",
    [
        # T9 – >7 days before check‑in → full refund
        (
            {
                "rooms": {"501": {"type": "Suite", "price_per_night": 250.0}},
                "reservations": {
                    "RES-0100": {
                        "reservation_id": "RES-0100",
                        "room_number": 501,
                        "user_name": "Grace",
                        "check_in": (datetime.date.today() + timedelta(days=20)).isoformat(),
                        "check_out": (datetime.date.today() + timedelta(days=23)).isoformat(),
                        "total_price": 750.0,
                    }
                },
            },
            "RES-0100",
            750.0,
        ),
        # T10 – 2‑7 days before check‑in → 50% refund
        (
            {
                "rooms": {"502": {"type": "Deluxe", "price_per_night": 180.0}},
                "reservations": {
                    "RES-0101": {
                        "reservation_id": "RES-0101",
                        "room_number": 502,
                        "user_name": "Heidi",
                        "check_in": (datetime.date.today() + timedelta(days=5)).isoformat(),
                        "check_out": (datetime.date.today() + timedelta(days=8)).isoformat(),
                        "total_price": 540.0,
                    }
                },
            },
            "RES-0101",
            270.0,
        ),
        # T11 – <2 days before check‑in → no refund
        (
            {
                "rooms": {"503": {"type": "Standard", "price_per_night": 110.0}},
                "reservations": {
                    "RES-0102": {
                        "reservation_id": "RES-0102",
                        "room_number": 503,
                        "user_name": "Ivan",
                        "check_in": (datetime.date.today() + timedelta(days=1)).isoformat(),
                        "check_out": (datetime.date.today() + timedelta(days=3)).isoformat(),
                        "total_price": 220.0,
                    }
                },
            },
            "RES-0102",
            0.0,
        ),
    ],
    ids=["FullRefund", "HalfRefund", "NoRefund"],
)
def test_cancel_reservation_refunds(setup, res_id, expected_refund):
    hrs = build_system(setup)
    refund = hrs.cancel_reservation(res_id)
    assert refund == expected_refund
    # reservation must be removed after cancellation
    assert res_id not in hrs.reservations

# ----------------------------------------------------------------------
# T12‑T13 – Get room occupancy for a given date (parametrized)
# ----------------------------------------------------------------------
@pytest.mark.parametrize(
    "setup,date,expected_rooms",
    [
        # T12 – date within active reservation
        (
            {
                "rooms": {"601": {"type": "Suite", "price_per_night": 300.0}},
                "reservations": {
                    "RES-0200": {
                        "reservation_id": "RES-0200",
                        "room_number": 601,
                        "user_name": "Judy",
                        "check_in": (datetime.date.today() + timedelta(days=10)).isoformat(),
                        "check_out": (datetime.date.today() + timedelta(days=15)).isoformat(),
                        "total_price": 1500.0,
                    }
                },
            },
            datetime.date.today() + timedelta(days=12),
            [601],
        ),
        # T13 – date with no active reservations
        (
            {
                "rooms": {"602": {"type": "Standard", "price_per_night": 90.0}},
                "reservations": {
                    "RES-0201": {
                        "reservation_id": "RES-0201",
                        "room_number": 602,
                        "user_name": "Ken",
                        "check_in": (datetime.date.today() + timedelta(days=10)).isoformat(),
                        "check_out": (datetime.date.today() + timedelta(days=15)).isoformat(),
                        "total_price": 450.0,
                    }
                },
            },
            datetime.date.today() + timedelta(days=20),
            [],
        ),
    ],
    ids=["Occupied", "None"],
)
def test_get_room_occupancy(setup, date, expected_rooms):
    hrs = build_system(setup)
    occupied = hrs.get_room_occupancy(date)
    assert occupied == expected_rooms