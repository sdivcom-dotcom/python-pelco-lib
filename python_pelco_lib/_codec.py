"""Encoding helpers shared by the Pelco-D and Pelco-P command builders.

Both protocols carry the same 16-bit command word (DATA1/DATA2) followed by a
pan-speed and a tilt-speed byte; only the framing and the checksum differ.
Everything that is common to the two lives here.
"""

import string

MIN_SPEED = 0x00
MAX_SPEED = 0x3F  # 63 - the fastest speed both protocols define
TURBO_SPEED = 100  # sentinel accepted by the Pelco-P pan builders

ZERO_BYTE = "00"

# DATA1/DATA2 command words. Identical in both protocols.
CMD_STOP = "0000"
CMD_TILT_UP = "0008"
CMD_TILT_DOWN = "0010"
CMD_PAN_LEFT = "0004"
CMD_PAN_RIGHT = "0002"
CMD_UP_LEFT = "000C"
CMD_UP_RIGHT = "000A"
CMD_DOWN_LEFT = "0014"
CMD_DOWN_RIGHT = "0012"
CMD_ZOOM_IN = "0020"
CMD_ZOOM_OUT = "0040"
CMD_FOCUS_FAR = "0080"
CMD_FOCUS_NEAR = "0100"


def hex_byte(value):
    """Format an integer in 0..255 as an upper-case two-digit hex string."""
    value = int(value)
    if not 0 <= value <= 0xFF:
        raise ValueError("byte value must be in 0..255, got %r" % (value,))
    return format(value, "02X")


def normalize_address(address):
    """Return the camera address as a two-digit hex string.

    Accepts either the hex string the library has always used ("01", "0A") or a
    plain int, which is formatted as hex - so 10 becomes "0A", not "10".
    """
    if isinstance(address, bool):
        raise TypeError("camera address must be an int or a hex string")
    if isinstance(address, int):
        return hex_byte(address)

    text = str(address).strip()
    if not text:
        raise ValueError("camera address must not be empty")
    if len(text) > 2 or not all(char in string.hexdigits for char in text):
        raise ValueError(
            "camera address must be one or two hex digits, got %r" % (address,)
        )
    return text.upper().zfill(2)


def clamp_speed(speed):
    """Clamp a pan/tilt speed to 0x00..0x3F and format it as a hex byte.

    Out-of-range values are clamped rather than rejected, which is what the
    library has always done: a camera that is asked to move faster than it can
    should still move.
    """
    speed = int(speed)
    return hex_byte(max(MIN_SPEED, min(MAX_SPEED, speed)))
