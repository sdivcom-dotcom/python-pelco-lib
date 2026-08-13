"""Drive a Pelco-P camera from a USB gamepad.

The camera moves while the stick is held and stops when it returns to centre,
so there is no fixed step delay. The port is opened once for the whole session
instead of once per command.

Set VENDOR_ID/PRODUCT_ID to your own pad - the ids of every connected HID
device are printed at startup.
"""

import os
import sys
import time

import hid

# Let the example run straight from a checkout, without installing the library.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import python_pelco_lib as pelco  # noqa: E402

PORT = "/dev/ttyUSB0"
BAUD = 2400
ADDRESS = "01"
TIL_SPEED = 32
PAN_SPEED = 32

VENDOR_ID = 0x0079
PRODUCT_ID = 0x0011

# Byte offsets of the two stick axes in the HID report, and the values they
# report at each extreme. Centre is somewhere in between.
AXIS_X = 3
AXIS_Y = 4
AXIS_MIN = 0
AXIS_MAX = 255

POLL_INTERVAL = 0.01


def direction(report):
    """Return the direction the stick is pushed, or None when centred."""
    if report[AXIS_X] == AXIS_MIN:
        return "left"
    if report[AXIS_X] == AXIS_MAX:
        return "right"
    if report[AXIS_Y] == AXIS_MIN:
        return "up"
    if report[AXIS_Y] == AXIS_MAX:
        return "down"
    return None


def command_for(name):
    """Build the Pelco-P message for a direction."""
    if name == "left":
        return pelco.pelco_p_pan_left(ADDRESS, PAN_SPEED)
    if name == "right":
        return pelco.pelco_p_pan_right(ADDRESS, PAN_SPEED)
    if name == "up":
        return pelco.pelco_p_tilt_up(ADDRESS, TIL_SPEED)
    if name == "down":
        return pelco.pelco_p_tilt_down(ADDRESS, TIL_SPEED)
    return pelco.pelco_p_stop(ADDRESS)


def main():
    for device in hid.enumerate():
        print("0x%04x:0x%04x %s"
              % (device['vendor_id'], device['product_id'], device['product_string']))

    gamepad = hid.device()
    gamepad.open(VENDOR_ID, PRODUCT_ID)
    gamepad.set_nonblocking(True)

    stop = pelco.pelco_p_stop(ADDRESS)
    current = None

    try:
        with pelco.PelcoSerial(PORT, BAUD) as link:
            while True:
                report = gamepad.read(16)
                if not report:
                    time.sleep(POLL_INTERVAL)
                    continue

                wanted = direction(report)
                if wanted == current:
                    continue

                print(wanted or "stop")
                link.send(command_for(wanted) if wanted else stop)
                current = wanted
    except KeyboardInterrupt:
        pass
    finally:
        # Never leave the camera moving on the way out.
        pelco.write_com_action(PORT, BAUD, stop)
        gamepad.close()
    return 0


if __name__ == '__main__':
    sys.exit(main())
