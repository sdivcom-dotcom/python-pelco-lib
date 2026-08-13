"""Serial (RS-485) transport for the hex command strings the builders return.

``port`` is the device the USB-RS485 adapter shows up as ("/dev/ttyUSB0",
"COM3"), ``baud`` is the rate configured on the camera - usually one of 1200,
1800, 2400, 4800 or 9600.
"""

import time

import serial

__all__ = ["DEFAULT_BAUDRATE", "PelcoSerial", "write_com_action", "write_com_command"]

DEFAULT_BAUDRATE = 2400


class PelcoSerial:
    """An open RS-485 port that stays open across commands.

    The module-level helpers below re-open the port for every message, which
    costs tens of milliseconds and resets the line. Use this class instead when
    commands come in a stream - from a joystick, a GUI or a patrol loop::

        with PelcoSerial("/dev/ttyUSB0", 2400) as link:
            link.send_for(pelco_d_pan_left("01", 32), pelco_d_stop("01"), 0.5)
    """

    def __init__(self, port, baud=DEFAULT_BAUDRATE, **kwargs):
        self.serial = serial.Serial(port=port, baudrate=int(baud), **kwargs)

    def send(self, data):
        """Write one hex command string to the port."""
        self.serial.write(bytes.fromhex(data))

    def send_for(self, data, data_stop, delay):
        """Send ``data``, hold it for ``delay`` seconds, then send ``data_stop``.

        ``data_stop`` is sent even if the wait is interrupted, so a Ctrl-C in
        the middle of a movement does not leave the camera panning.
        """
        self.send(data)
        try:
            time.sleep(float(delay))
        finally:
            self.send(data_stop)

    def close(self):
        self.serial.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()
        return False


def write_com_action(port, baud, data):
    """Open the port, send one command, and close the port again."""
    with PelcoSerial(port, baud) as link:
        link.send(data)


def write_com_command(port, baud, data, data_stop, delay):
    """Send a command, hold it for ``delay`` seconds, then send the stop command.

    Useful for stepping a camera a small, fixed amount.
    """
    with PelcoSerial(port, baud) as link:
        link.send_for(data, data_stop, delay)
