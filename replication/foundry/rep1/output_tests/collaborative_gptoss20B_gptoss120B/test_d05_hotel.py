import pytest
import datetime
from data.input_code.d05_hotel import *

TODAY = datetime.date.today()

def in_days(days: int) -> str:
    return (TODAY + datetime.timedelta(days=days)).isoformat()

def date_pair(start_days: int, nights: int):
    cs = TODAY + datetime.timedelta(days=start_days)
    ce = cs + datetime.timedelta(days=nights)
    return cs.isoformat(), ce.isoformat()

# Build dynamic test plan to align with "today" reality of the system
test_plan = [
    {
        "id": "TC1_AddRoom_Success",
        "rationale": "CRITICAL: Adds a room with valid positive price, exercising normal path of add_room.",
        "target": "HotelReservationSystem.add_room",
        "input": {"room_number": 101, "room_type": "Deluxe", "price_per_night": 150.0},
        "expected": None,
        "setup": []
    },
    {
        "id": "TC2_AddRoom_InvalidPrice",
        "rationale": "CRITICAL: price_per_night <= 0 triggers ValueError branch.",
        "target": "HotelReservationSystem.add_room",
        "input": {"room_number": 102, "room_type": "Standard", "price_per_night": 0.0},
        "expected": "ValueError",
        "setup": []
    },
    {
        "id": "TC3_BookRoom_RoomNotFound",
        "rationale": "CRITICAL: Booking a non‑existent room raises RoomNotFoundError.",
        "target": "HotelReservationSystem.book_room",
        "input": {
          "room_number": 999,
          "user_name": "Alice",
          "check_in": in_days(10),
          "check_out": in_days(12)
        },
        "expected": "RoomNotFoundError",
        "setup": []
    },
    {
        "id": "TC4_BookRoom_InvalidDates_CheckInAfterOrEqualCheckOut",
        "rationale": "CRITICAL: check_in >= check_out triggers InvalidDateError.",
        "target": "HotelReservationSystem.book_room",
        "input": {
          "room_number": 101,
          "user_name": "Bob",
          "check_in": in_days(5),
          "check_out": in_days(5)
        },
        "expected": "InvalidDateError",
        "setup": [
          {
            "method": "add_room",
            "args": {"room_number": 101, "room_type": "Deluxe", "price_per_night": 100.0}
          }
        ]
    },
    {
        "id": "TC5_BookRoom_InvalidDates_PastCheckIn",
        "rationale": "CRITICAL: check_in in the past triggers InvalidDateError.",
        "target": "HotelReservationSystem.book_room",
        "input": {
          "room_number": 101,
          "user_name": "Carol",
          "check_in": (TODAY - datetime.timedelta(days=5)).isoformat(),
          "check_out": (TODAY - datetime.timedelta(days=3)).isoformat()
        },
        "expected": "InvalidDateError",
        "setup": [
          {
            "method": "add_room",
            "args": {"room_number": 101, "room_type": "Deluxe", "price_per_night": 100.0}
          }
        ]
    },
    {
        "id": "TC6_BookRoom_Unavailable",
        "rationale": "CRITICAL: Overlapping reservation causes _is_room_available to return False, raising RoomUnavailableError.",
        "target": "HotelReservationSystem.book_room",
        "input": {
          "room_number": 101,
          "user_name": "Dave",
          "check_in": in_days(20),
          "check_out": in_days(23)
        },
        "expected": "RoomUnavailableError",
        "setup": [
          {
            "method": "add_room",
            "args": {"room_number": 101, "room_type": "Deluxe", "price_per_night": 100.0}
          },
          {
            "method": "book_room",
            "args": {"room_number": 101, "user_name": "Eve", "check_in": in_days(20), "check_out": in_days(23)}
          }
        ]
    },
    {
        "id": "TC7_BookRoom_Success",
        "rationale": "CRITICAL: Successful booking path, verifies reservation ID format and total_price calculation.",
        "target": "HotelReservationSystem.book_room",
        "input": {
          "room_number": 101,
          "user_name": "Frank",
          "check_in": in_days(10),
          "check_out": in_days(13)
        },
        "expected": "RES-0001",
        "setup": [
          {
            "method": "add_room",
            "args": {"room_number": 101, "room_type": "Deluxe", "price_per_night": 100.0}
          }
        ]
    },
    {
        "id": "TC8_CancelReservation_NotFound",
        "rationale": "CRITICAL: Cancelling a non‑existent reservation raises ReservationNotFoundError.",
        "target": "HotelReservationSystem.cancel_reservation",
        "input": {"reservation_id": "RES-9999"},
        "expected": "ReservationNotFoundError",
        "setup": [
          {
            "method": "add_room",
            "args": {"room_number": 101, "room_type": "Deluxe", "price_per_night": 100.0}
          }
        ]
    },
    {
        "id": "TC9_CancelReservation_FullRefund",
        "rationale": "CRITICAL: days_until_checkin > 7 returns full total_price.",
        "target": "HotelReservationSystem.cancel_reservation",
        "input": {"reservation_id": "RES-0001"},
        "expected": 300.0,
        "setup": [
          {
            "method": "add_room",
            "args": {"room_number": 101, "room_type": "Deluxe", "price_per_night": 100.0}
          },
          {
            "method": "book_room",
            "args": {"room_number": 101, "user_name": "Grace", "check_in": in_days(20), "check_out": in_days(23)}
          }
        ]
    },
    {
        "id": "TC10_CancelReservation_HalfRefund",
        "rationale": "CRITICAL: 2 <= days_until_checkin <= 7 returns 50% of total_price.",
        "target": "HotelReservationSystem.cancel_reservation",
        "input": {"reservation_id": "RES-0001"},
        "expected": 150.0,
        "setup": [
          {
            "method": "add_room",
            "args": {"room_number": 101, "room_type": "Deluxe", "price_per_night": 100.0}
          },
          {
            "method": "book_room",
            "args": {"room_number": 101, "user_name": "Heidi", "check_in": in_days(6), "check_out": in_days(9)}
          }
        ]
    },
    {
        "id": "TC11_CancelReservation_NoRefund",
        "rationale": "CRITICAL: days_until_checkin < 2 returns 0.0 refund.",
        "target": "HotelReservationSystem.cancel_reservation",
        "input": {"reservation_id": "RES-0001"},
        "expected": 0.0,
        "setup": [
          {
            "method": "add_room",
            "args": {"room_number": 101, "room_type": "Deluxe", "price_per_night": 100.0}
          },
          {
            "method": "book_room",
            "args": {"room_number": 101, "user_name": "Ivan", "check_in": in_days(1), "check_out": in_days(3)}
          }
        ]
    },
    {
        "id": "TC12_GetRoomOccupancy_Occupied",
        "rationale": "CRITICAL: Date within reservation range returns occupied room number.",
        "target": "HotelReservationSystem.get_room_occupancy",
        "input": {"date": in_days(11)},
        "expected": [101],
        "setup": [
          {
            "method": "add_room",
            "args": {"room_number": 101, "room_type": "Deluxe", "price_per_night": 100.0}
          },
          {
            "method": "book_room",
            "args": {"room_number": 101, "user_name": "Judy", "check_in": in_days(10), "check_out": in_days(13)}
          }
        ]
    },
    {
        "id": "TC13_GetRoomOccupancy_Empty",
        "rationale": "CRITICAL: Date outside any reservation returns empty list.",
        "target": "HotelReservationSystem.get_room_occupancy",
        "input": {"date": in_days(14)},
        "expected": [],
        "setup": [
          {
            "method": "add_room",
            "args": {"room_number": 101, "room_type": "Deluxe", "price_per_night": 100.0}
          },
          {
            "method": "book_room",
            "args": {"room_number": 101, "user_name": "Ken", "check_in": in_days(10), "check_out": in_days(13)}
          }
        ]
    }
]

exception_map = {
    "ValueError": ValueError,
    "RoomNotFoundError": RoomNotFoundError,
    "InvalidDateError": InvalidDateError,
    "RoomUnavailableError": RoomUnavailableError,
    "ReservationNotFoundError": ReservationNotFoundError,
}

def coerce_call_args(method_name: str, input_args: dict) -> dict:
    """Convert input arguments to proper types for the called method."""
    args = dict(input_args)
    if method_name == "book_room":
        if "check_in" in args:
            args["check_in"] = datetime.date.fromisoformat(args["check_in"])
        if "check_out" in args:
            args["check_out"] = datetime.date.fromisoformat(args["check_out"])
    if method_name == "get_room_occupancy":
        if "date" in args:
            args["date"] = datetime.date.fromisoformat(args["date"])
    return args

@pytest.mark.parametrize("case", test_plan)
def test_hotel_reservation_system_plan(case):
    # Each test uses a fresh system to avoid cross-test state
    system = HotelReservationSystem()

    # Apply setup steps if any
    for step in case.get("setup", []):
        method_name = step["method"]
        method = getattr(system, method_name)
        args = dict(step["args"])
        if "check_in" in args:
            args["check_in"] = datetime.date.fromisoformat(args["check_in"])
        if "check_out" in args:
            args["check_out"] = datetime.date.fromisoformat(args["check_out"])
        method(**args)

    # Prepare actual call
    target_class, method_name = case["target"].split(".")
    assert target_class == "HotelReservationSystem"
    method = getattr(system, method_name)
    input_args = coerce_call_args(method_name, case["input"])

    expected = case.get("expected")

    if isinstance(expected, str) and expected in exception_map:
        with pytest.raises(exception_map[expected]):
            method(**input_args)
    else:
        result = method(**input_args)

        if method_name == "add_room":
            # post-condition: room should exist with given price
            room_number = case["input"]["room_number"]
            assert room_number in system.rooms
            assert system.rooms[room_number]["price_per_night"] == case["input"]["price_per_night"]
            assert system.rooms[room_number]["type"] == case["input"]["room_type"]
        elif method_name == "book_room":
            assert result == expected
        elif method_name == "cancel_reservation":
            assert result == expected
        elif method_name == "get_room_occupancy":
            assert result == expected