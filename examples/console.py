"""Send a single Pelco command from the command line.

    python console.py -p /dev/ttyUSB0 -b 2400 -a 01 -pr d -c right
"""

import argparse
import os
import sys

# Let the example run straight from a checkout, without installing the library.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import python_pelco_lib as pelco  # noqa: E402

# Command name on the command line -> builder suffix in the library.
MOVE_COMMANDS = {
    "up": "tilt_up",
    "down": "tilt_down",
    "left": "pan_left",
    "right": "pan_right",
}

OPTIC_COMMANDS = {
    "zoom_plus": "zoom_in",
    "zoom_minus": "zoom_out",
    "focus_plus": "focus_far",
    "focus_minus": "focus_near",
}

TILT_COMMANDS = ("up", "down")


def build(protocol, name, address, speed=None):
    """Look up ``pelco_<protocol>_<name>`` and call it."""
    builder = getattr(pelco, "pelco_%s_%s" % (protocol, name))
    if speed is None:
        return builder(address)
    return builder(address, speed)


def parse_args():
    parser = argparse.ArgumentParser(description="Simple console for PELCO")
    parser.add_argument('-p', '--port', dest='port', type=str,
                        default='/dev/ttyUSB0',
                        help='serial port of the USB-RS485 adapter')
    parser.add_argument('-b', '--baud', dest='baud', type=int,
                        default=pelco.DEFAULT_BAUDRATE,
                        help='baud rate configured on the camera')
    parser.add_argument('-a', '--address', dest='address', type=str,
                        default='01', help='camera address on the bus, in hex')
    parser.add_argument('-pr', '--protocol', dest='protocol', type=str,
                        default='d', choices=('d', 'p'),
                        help='pelco protocol variant')
    parser.add_argument('-c', '--command', dest='command', type=str,
                        default='right',
                        choices=sorted(list(MOVE_COMMANDS) + list(OPTIC_COMMANDS) + ['stop']),
                        help='command to send')
    parser.add_argument('-do', '--delay_optics', dest='delay_optics', type=float,
                        default=0.05, help='how long to hold a zoom/focus command')
    parser.add_argument('-dr', '--delay_runs', dest='delay_runs', type=float,
                        default=0.37, help='how long to hold a pan/tilt command')
    parser.add_argument('-ts', '--til_speed', dest='til_speed', type=int,
                        default=32, help='tilt speed, 0-63')
    parser.add_argument('-ps', '--pan_speed', dest='pan_speed', type=int,
                        default=32, help='pan speed, 0-63')
    return parser.parse_args()


def main():
    args = parse_args()
    stop = build(args.protocol, "stop", args.address)

    if args.command == "stop":
        pelco.write_com_action(args.port, args.baud, stop)
        return 0

    if args.command in MOVE_COMMANDS:
        speed = args.til_speed if args.command in TILT_COMMANDS else args.pan_speed
        data = build(args.protocol, MOVE_COMMANDS[args.command], args.address, speed)
        delay = args.delay_runs
    else:
        data = build(args.protocol, OPTIC_COMMANDS[args.command], args.address)
        delay = args.delay_optics

    pelco.write_com_command(args.port, args.baud, data, stop, delay)
    return 0


if __name__ == '__main__':
    sys.exit(main())
