"""Build and send Pelco-D and Pelco-P messages for PTZ cameras.

The command builders return a message as a hex string; the transport sends it
over an RS-485 serial port::

    from python_pelco_lib import pelco_d_tilt_up, pelco_d_stop, write_com_command

    write_com_command("/dev/ttyUSB0", 2400,
                      pelco_d_tilt_up("01", 32), pelco_d_stop("01"), 1)
"""

from ._codec import MAX_SPEED, MIN_SPEED, TURBO_SPEED
from .commands_pelco_d import (
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
from .commands_pelco_p import (
    pelco_p_down_left,
    pelco_p_down_right,
    pelco_p_focus_far,
    pelco_p_focus_near,
    pelco_p_pan,
    pelco_p_pan_left,
    pelco_p_pan_right,
    pelco_p_stop,
    pelco_p_tilt,
    pelco_p_tilt_down,
    pelco_p_tilt_up,
    pelco_p_upleft,
    pelco_p_upright,
    pelco_p_zoom_in,
    pelco_p_zoom_out,
)
from .pelco_transport import (
    DEFAULT_BAUDRATE,
    PelcoSerial,
    write_com_action,
    write_com_command,
)

__version__ = "0.2.0"

__all__ = [
    "MIN_SPEED",
    "MAX_SPEED",
    "TURBO_SPEED",
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
    "DEFAULT_BAUDRATE",
    "PelcoSerial",
    "write_com_action",
    "write_com_command",
    "__version__",
]
