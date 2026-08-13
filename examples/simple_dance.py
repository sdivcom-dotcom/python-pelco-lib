"""Interactive prompt that drives one camera, plus an "all" sweep.

Type one of the listed commands at the prompt. "all" walks the camera up,
down, left and right in turn, which is a quick way to check the wiring.
"""

import os
import sys

# Let the example run straight from a checkout, without installing the library.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import python_pelco_lib as pelco  # noqa: E402

PORT = "/dev/ttyUSB0"
BAUD = 2400
ADDRESS = "01"
PROTOCOL = "d"
DELAY_OPTICS = 0.05
DELAY_RUNS = 10
TIL_SPEED = 63
PAN_SPEED = 63

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
DANCE = ("up", "down", "left", "right")


def build(name, speed=None):
    """Look up ``pelco_<PROTOCOL>_<name>`` and call it."""
    builder = getattr(pelco, "pelco_%s_%s" % (PROTOCOL, name))
    if speed is None:
        return builder(ADDRESS)
    return builder(ADDRESS, speed)


def move(link, command):
    """Run one pan/tilt step and stop again."""
    speed = TIL_SPEED if command in TILT_COMMANDS else PAN_SPEED
    link.send_for(build(MOVE_COMMANDS[command], speed), build("stop"), DELAY_RUNS)


def main():
    print("Enter the command (%s, all):"
          % ", ".join(sorted(list(MOVE_COMMANDS) + list(OPTIC_COMMANDS) + ["stop"])))
    command = input().strip()

    # One open port for the whole session, so the "all" sweep does not
    # re-open the adapter between every step.
    with pelco.PelcoSerial(PORT, BAUD) as link:
        if command == "stop":
            link.send(build("stop"))
        elif command in MOVE_COMMANDS:
            move(link, command)
        elif command in OPTIC_COMMANDS:
            link.send_for(build(OPTIC_COMMANDS[command]), build("stop"), DELAY_OPTICS)
        elif command == "all":
            for step in DANCE:
                print(step)
                move(link, step)
        else:
            print("Not command")
            return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
