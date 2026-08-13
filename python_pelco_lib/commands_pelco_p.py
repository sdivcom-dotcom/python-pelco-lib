"""Pelco-P command builders.

Every function returns the complete message as an upper-case hex string, ready
to be handed to :mod:`python_pelco_lib.pelco_transport`.

A Pelco-P message is eight bytes::

    A0 | ADDRESS | DATA1 | DATA2 | PAN SPEED | TILT SPEED | AF | CHECKSUM

The checksum is the XOR of the seven bytes that precede it, STX and ETX
included. Note that Pelco-P numbers cameras from zero, so the address byte is
usually the camera number on the bus minus one.
"""

from ._codec import (
    CMD_DOWN_LEFT,
    CMD_DOWN_RIGHT,
    CMD_FOCUS_FAR,
    CMD_FOCUS_NEAR,
    CMD_PAN_LEFT,
    CMD_PAN_RIGHT,
    CMD_STOP,
    CMD_TILT_DOWN,
    CMD_TILT_UP,
    CMD_UP_LEFT,
    CMD_UP_RIGHT,
    CMD_ZOOM_IN,
    CMD_ZOOM_OUT,
    TURBO_SPEED,
    ZERO_BYTE,
    clamp_speed,
    hex_byte,
    normalize_address,
)

__all__ = [
    "pelco_p_stop",
    "pelco_p_tilt_up",
    "pelco_p_tilt_down",
    "pelco_p_tilt",
    "pelco_p_pan_left",
    "pelco_p_pan_right",
    "pelco_p_pan",
    "pelco_p_upleft",
    "pelco_p_upright",
    "pelco_p_down_left",
    "pelco_p_down_right",
    "pelco_p_zoom_in",
    "pelco_p_zoom_out",
    "pelco_p_focus_far",
    "pelco_p_focus_near",
]

STX = "A0"
ETX = "AF"

TURBO_PAN_BYTE = "40"


def _checksum(frame):
    """XOR of every byte in the frame, as a hex byte."""
    checksum = 0
    for byte in bytearray.fromhex(frame):
        checksum ^= byte
    return hex_byte(checksum)


def _message(address, command, pan_speed=ZERO_BYTE, tilt_speed=ZERO_BYTE):
    """Frame one command word into a complete Pelco-P message."""
    frame = (
        STX + normalize_address(address) + command + pan_speed + tilt_speed + ETX
    )
    return frame + _checksum(frame)


def _pan_speed(speed):
    """Clamp a pan speed, mapping the magic value 100 to Pelco-P turbo pan."""
    if int(speed) == TURBO_SPEED:
        return TURBO_PAN_BYTE
    return clamp_speed(speed)


def pelco_p_stop(address):
    """Stop all camera movement."""
    return _message(address, CMD_STOP)


def pelco_p_tilt_up(address, til_speed):
    """Tilt the camera up at ``til_speed`` (0-63)."""
    return _message(address, CMD_TILT_UP, tilt_speed=clamp_speed(til_speed))


def pelco_p_tilt_down(address, til_speed):
    """Tilt the camera down at ``til_speed`` (0-63)."""
    return _message(address, CMD_TILT_DOWN, tilt_speed=clamp_speed(til_speed))


def pelco_p_tilt(address, up, down, til_speed):
    """Tilt up, down, or stop, depending on which flag is set.

    ``up`` wins if both flags are set; if neither is, the camera is stopped.
    """
    if up:
        return pelco_p_tilt_up(address, til_speed)
    if down:
        return pelco_p_tilt_down(address, til_speed)
    return pelco_p_stop(address)


def pelco_p_pan_left(address, pan_speed):
    """Pan the camera left at ``pan_speed`` (0-63, or 100 for turbo)."""
    return _message(address, CMD_PAN_LEFT, pan_speed=_pan_speed(pan_speed))


def pelco_p_pan_right(address, pan_speed):
    """Pan the camera right at ``pan_speed`` (0-63, or 100 for turbo)."""
    return _message(address, CMD_PAN_RIGHT, pan_speed=_pan_speed(pan_speed))


def pelco_p_pan(address, right, left, pan_speed):
    """Pan right, left, or stop, depending on which flag is set.

    ``right`` wins if both flags are set; if neither is, the camera is stopped.
    """
    if right:
        return pelco_p_pan_right(address, pan_speed)
    if left:
        return pelco_p_pan_left(address, pan_speed)
    return pelco_p_stop(address)


def pelco_p_upleft(address, pan_speed, til_speed):
    """Move the camera up and to the left."""
    return _message(
        address, CMD_UP_LEFT, _pan_speed(pan_speed), clamp_speed(til_speed)
    )


def pelco_p_upright(address, pan_speed, til_speed):
    """Move the camera up and to the right."""
    return _message(
        address, CMD_UP_RIGHT, _pan_speed(pan_speed), clamp_speed(til_speed)
    )


def pelco_p_down_left(address, pan_speed, til_speed):
    """Move the camera down and to the left."""
    return _message(
        address, CMD_DOWN_LEFT, _pan_speed(pan_speed), clamp_speed(til_speed)
    )


def pelco_p_down_right(address, pan_speed, til_speed):
    """Move the camera down and to the right."""
    return _message(
        address, CMD_DOWN_RIGHT, _pan_speed(pan_speed), clamp_speed(til_speed)
    )


def pelco_p_zoom_in(address):
    """Zoom the lens in (tele)."""
    return _message(address, CMD_ZOOM_IN)


def pelco_p_zoom_out(address):
    """Zoom the lens out (wide)."""
    return _message(address, CMD_ZOOM_OUT)


def pelco_p_focus_far(address):
    """Move the lens focus far."""
    return _message(address, CMD_FOCUS_FAR)


def pelco_p_focus_near(address):
    """Move the lens focus near."""
    return _message(address, CMD_FOCUS_NEAR)
