"""Pelco-D command builders.

Every function returns the complete message as an upper-case hex string, ready
to be handed to :mod:`python_pelco_lib.pelco_transport`.

A Pelco-D message is seven bytes::

    FF | ADDRESS | DATA1 | DATA2 | PAN SPEED | TILT SPEED | CHECKSUM

The checksum is the sum of the five bytes after the sync byte, modulo 256.
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
    ZERO_BYTE,
    clamp_speed,
    hex_byte,
    normalize_address,
)

__all__ = [
    "pelco_d_stop",
    "pelco_d_tilt_up",
    "pelco_d_tilt_down",
    "pelco_d_tilt",
    "pelco_d_pan_left",
    "pelco_d_pan_right",
    "pelco_d_pan",
    "pelco_d_upleft",
    "pelco_d_upright",
    "pelco_d_down_left",
    "pelco_d_down_right",
    "pelco_d_zoom_in",
    "pelco_d_zoom_out",
    "pelco_d_focus_far",
    "pelco_d_focus_near",
]

SYNC_BYTE = "FF"


def _checksum(payload):
    """Sum of the payload bytes, modulo 256, as a hex byte."""
    return hex_byte(sum(bytearray.fromhex(payload)) & 0xFF)


def _message(address, command, pan_speed=ZERO_BYTE, tilt_speed=ZERO_BYTE):
    """Frame one command word into a complete Pelco-D message."""
    payload = normalize_address(address) + command + pan_speed + tilt_speed
    return SYNC_BYTE + payload + _checksum(payload)


def pelco_d_stop(address):
    """Stop all camera movement."""
    return _message(address, CMD_STOP)


def pelco_d_tilt_up(address, til_speed):
    """Tilt the camera up at ``til_speed`` (0-63)."""
    return _message(address, CMD_TILT_UP, tilt_speed=clamp_speed(til_speed))


def pelco_d_tilt_down(address, til_speed):
    """Tilt the camera down at ``til_speed`` (0-63)."""
    return _message(address, CMD_TILT_DOWN, tilt_speed=clamp_speed(til_speed))


def pelco_d_tilt(address, up, down, til_speed):
    """Tilt up, down, or stop, depending on which flag is set.

    ``up`` wins if both flags are set; if neither is, the camera is stopped.
    """
    if up:
        return pelco_d_tilt_up(address, til_speed)
    if down:
        return pelco_d_tilt_down(address, til_speed)
    return pelco_d_stop(address)


def pelco_d_pan_left(address, pan_speed):
    """Pan the camera left at ``pan_speed`` (0-63)."""
    return _message(address, CMD_PAN_LEFT, pan_speed=clamp_speed(pan_speed))


def pelco_d_pan_right(address, pan_speed):
    """Pan the camera right at ``pan_speed`` (0-63)."""
    return _message(address, CMD_PAN_RIGHT, pan_speed=clamp_speed(pan_speed))


def pelco_d_pan(address, right, left, pan_speed):
    """Pan right, left, or stop, depending on which flag is set.

    ``right`` wins if both flags are set; if neither is, the camera is stopped.
    """
    if right:
        return pelco_d_pan_right(address, pan_speed)
    if left:
        return pelco_d_pan_left(address, pan_speed)
    return pelco_d_stop(address)


def pelco_d_upleft(address, pan_speed, til_speed):
    """Move the camera up and to the left."""
    return _message(
        address, CMD_UP_LEFT, clamp_speed(pan_speed), clamp_speed(til_speed)
    )


def pelco_d_upright(address, pan_speed, til_speed):
    """Move the camera up and to the right."""
    return _message(
        address, CMD_UP_RIGHT, clamp_speed(pan_speed), clamp_speed(til_speed)
    )


def pelco_d_down_left(address, pan_speed, til_speed):
    """Move the camera down and to the left."""
    return _message(
        address, CMD_DOWN_LEFT, clamp_speed(pan_speed), clamp_speed(til_speed)
    )


def pelco_d_down_right(address, pan_speed, til_speed):
    """Move the camera down and to the right."""
    return _message(
        address, CMD_DOWN_RIGHT, clamp_speed(pan_speed), clamp_speed(til_speed)
    )


def pelco_d_zoom_in(address):
    """Zoom the lens in (tele)."""
    return _message(address, CMD_ZOOM_IN)


def pelco_d_zoom_out(address):
    """Zoom the lens out (wide)."""
    return _message(address, CMD_ZOOM_OUT)


def pelco_d_focus_far(address):
    """Move the lens focus far."""
    return _message(address, CMD_FOCUS_FAR)


def pelco_d_focus_near(address):
    """Move the lens focus near."""
    return _message(address, CMD_FOCUS_NEAR)
