"""Frame-level tests for the Pelco-D and Pelco-P builders.

The expected strings are checked against the protocol specs by hand, so they
also serve as a regression net for any future change to the encoders.
"""

import pytest

from python_pelco_lib import _codec
from python_pelco_lib.commands_pelco_d import (
    pelco_d_down_left,
    pelco_d_down_right,
    pelco_d_focus_far,
    pelco_d_focus_near,
    pelco_d_pan,
    pelco_d_pan_left,
    pelco_d_pan_right,
    pelco_d_stop,
    pelco_d_tilt,
    pelco_d_tilt_down,
    pelco_d_tilt_up,
    pelco_d_upleft,
    pelco_d_upright,
    pelco_d_zoom_in,
    pelco_d_zoom_out,
)
from python_pelco_lib.commands_pelco_p import (
    pelco_p_pan,
    pelco_p_pan_left,
    pelco_p_pan_right,
    pelco_p_stop,
    pelco_p_tilt,
    pelco_p_tilt_down,
    pelco_p_tilt_up,
    pelco_p_zoom_in,
)


def d_checksum(message):
    """Recompute a Pelco-D checksum straight from the spec."""
    return sum(bytearray.fromhex(message)[1:-1]) & 0xFF


def p_checksum(message):
    """Recompute a Pelco-P checksum straight from the spec."""
    checksum = 0
    for byte in bytearray.fromhex(message)[:-1]:
        checksum ^= byte
    return checksum


PELCO_D_CASES = [
    (pelco_d_stop("01"), "FF010000000001"),
    (pelco_d_pan_left("01", 32), "FF010004200025"),
    (pelco_d_pan_right("01", 32), "FF010002200023"),
    (pelco_d_tilt_up("01", 32), "FF010008002029"),
    (pelco_d_tilt_down("01", 32), "FF010010002031"),
    (pelco_d_upleft("01", 32, 10), "FF01000C200A37"),
    (pelco_d_upright("01", 32, 10), "FF01000A200A35"),
    (pelco_d_down_left("01", 32, 10), "FF010014200A3F"),
    (pelco_d_down_right("01", 32, 10), "FF010012200A3D"),
    (pelco_d_zoom_in("01"), "FF010020000021"),
    (pelco_d_zoom_out("01"), "FF010040000041"),
    (pelco_d_focus_far("01"), "FF010080000081"),
    (pelco_d_focus_near("01"), "FF010100000002"),
]

PELCO_P_CASES = [
    (pelco_p_stop("01"), "A00100000000AF0E"),
    (pelco_p_pan_left("01", 32), "A00100042000AF2A"),
    (pelco_p_tilt_up("01", 32), "A00100080020AF26"),
    (pelco_p_zoom_in("01"), "A00100200000AF2E"),
]


@pytest.mark.parametrize("actual,expected", PELCO_D_CASES)
def test_pelco_d_frames(actual, expected):
    assert actual == expected


@pytest.mark.parametrize("actual,expected", PELCO_P_CASES)
def test_pelco_p_frames(actual, expected):
    assert actual == expected


@pytest.mark.parametrize("message,_expected", PELCO_D_CASES)
def test_pelco_d_length_and_checksum(message, _expected):
    assert len(bytearray.fromhex(message)) == 7
    assert message.startswith("FF")
    assert bytearray.fromhex(message)[-1] == d_checksum(message)


@pytest.mark.parametrize("message,_expected", PELCO_P_CASES)
def test_pelco_p_length_and_checksum(message, _expected):
    frame = bytearray.fromhex(message)
    assert len(frame) == 8
    assert frame[0] == 0xA0
    assert frame[6] == 0xAF
    assert frame[-1] == p_checksum(message)


# These four used to raise TypeError on every call - they passed three
# arguments to two-argument builders.
def test_tilt_dispatches_to_up_and_down():
    assert pelco_d_tilt("01", 1, 0, 32) == pelco_d_tilt_up("01", 32)
    assert pelco_d_tilt("01", 0, 1, 32) == pelco_d_tilt_down("01", 32)
    assert pelco_d_tilt("01", 0, 0, 32) == pelco_d_stop("01")
    assert pelco_p_tilt("01", 1, 0, 32) == pelco_p_tilt_up("01", 32)
    assert pelco_p_tilt("01", 0, 1, 32) == pelco_p_tilt_down("01", 32)
    assert pelco_p_tilt("01", 0, 0, 32) == pelco_p_stop("01")


def test_pan_dispatches_to_right_and_left():
    assert pelco_d_pan("01", 1, 0, 32) == pelco_d_pan_right("01", 32)
    assert pelco_d_pan("01", 0, 1, 32) == pelco_d_pan_left("01", 32)
    assert pelco_d_pan("01", 0, 0, 32) == pelco_d_stop("01")
    assert pelco_p_pan("01", 1, 0, 32) == pelco_p_pan_right("01", 32)
    assert pelco_p_pan("01", 0, 1, 32) == pelco_p_pan_left("01", 32)
    assert pelco_p_pan("01", 0, 0, 32) == pelco_p_stop("01")


@pytest.mark.parametrize("speed", [-5, 0, 1, 63, 64, 255])
def test_speed_is_clamped_into_range(speed):
    message = bytearray.fromhex(pelco_d_pan_left("01", speed))
    assert _codec.MIN_SPEED <= message[4] <= _codec.MAX_SPEED


def test_speed_accepts_numeric_strings():
    assert pelco_d_pan_left("01", "32") == pelco_d_pan_left("01", 32)


def test_turbo_pan_speed_is_pelco_p_only():
    assert bytearray.fromhex(pelco_p_pan_left("01", _codec.TURBO_SPEED))[4] == 0x40
    # Pelco-D has no turbo sentinel, so 100 is just clamped to the maximum.
    assert bytearray.fromhex(pelco_d_pan_left("01", 100))[4] == _codec.MAX_SPEED


def test_address_accepts_hex_strings_and_ints():
    assert pelco_d_stop(1) == pelco_d_stop("01")
    assert pelco_d_stop("1") == pelco_d_stop("01")
    assert pelco_d_stop(10) == pelco_d_stop("0A")
    assert pelco_d_stop("0a") == pelco_d_stop("0A")


@pytest.mark.parametrize("address", ["", "   ", "xy", "123", "0g", -1, 256])
def test_invalid_address_is_rejected(address):
    with pytest.raises(ValueError):
        pelco_d_stop(address)
