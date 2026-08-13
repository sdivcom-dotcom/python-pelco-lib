"""A small PyQt5 remote control for one Pelco camera.

Fill in the port, baud rate and camera address, pick the protocol, and use the
buttons. Every button routes through a single handler, so adding a command is
one line in the tables below.
"""

import os
import sys
from functools import partial

import serial
from PyQt5.QtWidgets import (
    QApplication,
    QButtonGroup,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QRadioButton,
    QVBoxLayout,
    QWidget,
)

# Let the example run straight from a checkout, without installing the library.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import python_pelco_lib as pelco  # noqa: E402

DELAY_OPTICS = 0.05
DELAY_RUNS = 0.5
TIL_SPEED = 63
PAN_SPEED = 63

# label, builder suffix, speed, delay, (row, column) in the movement grid
MOVE_BUTTONS = [
    ("UP", "tilt_up", TIL_SPEED, DELAY_RUNS, (0, 1)),
    ("Left", "pan_left", PAN_SPEED, DELAY_RUNS, (1, 0)),
    ("Right", "pan_right", PAN_SPEED, DELAY_RUNS, (1, 2)),
    ("Down", "tilt_down", TIL_SPEED, DELAY_RUNS, (2, 1)),
]

OPTIC_BUTTONS = [
    ("Zoom plus", "zoom_in", None, DELAY_OPTICS),
    ("Zoom minus", "zoom_out", None, DELAY_OPTICS),
    ("Focus plus", "focus_far", None, DELAY_OPTICS),
    ("Focus minus", "focus_near", None, DELAY_OPTICS),
]


class Remote(QWidget):

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.port_edit = QLineEdit("/dev/ttyUSB0")
        self.baud_edit = QLineEdit(str(pelco.DEFAULT_BAUDRATE))
        self.address_edit = QLineEdit("01")

        settings = QGridLayout()
        for row, (label, edit) in enumerate([
            ("Port:", self.port_edit),
            ("Baud rate:", self.baud_edit),
            ("Address:", self.address_edit),
        ]):
            settings.addWidget(QLabel(label), row, 0)
            settings.addWidget(edit, row, 1)

        settings_box = QGroupBox("Connection")
        settings_box.setLayout(settings)

        # Radio buttons, so the two protocols cannot both be selected at once.
        self.pelco_d = QRadioButton("Pelco-D")
        self.pelco_p = QRadioButton("Pelco-P")
        self.pelco_d.setChecked(True)
        protocols = QButtonGroup(self)
        protocols.addButton(self.pelco_d)
        protocols.addButton(self.pelco_p)

        protocol_layout = QVBoxLayout()
        protocol_layout.addWidget(self.pelco_d)
        protocol_layout.addWidget(self.pelco_p)
        protocol_box = QGroupBox("PELCO protocol")
        protocol_box.setLayout(protocol_layout)

        runner = QGridLayout()
        for label, name, speed, delay, (row, column) in MOVE_BUTTONS:
            runner.addWidget(self._button(label, name, speed, delay), row, column)
        runner_box = QGroupBox("Runner")
        runner_box.setLayout(runner)

        optics = QVBoxLayout()
        for label, name, speed, delay in OPTIC_BUTTONS:
            optics.addWidget(self._button(label, name, speed, delay))
        optics_box = QGroupBox("Optics")
        optics_box.setLayout(optics)

        self.status = QLabel("Ready")

        columns = QHBoxLayout()
        columns.addWidget(optics_box)
        columns.addWidget(runner_box)
        columns.addWidget(protocol_box)

        layout = QVBoxLayout()
        layout.addWidget(settings_box)
        layout.addLayout(columns)
        layout.addWidget(self.status)
        self.setLayout(layout)

        self.setWindowTitle('pelco-remote v.0.2')

    def _button(self, label, name, speed, delay):
        button = QPushButton(label, self)
        button.clicked.connect(partial(self.send, name, speed, delay))
        return button

    def connection(self):
        """Read and validate the connection fields."""
        port = self.port_edit.text().strip()
        if not port:
            raise ValueError("port is empty")
        baud = self.baud_edit.text().strip()
        if not baud.isdigit():
            raise ValueError("baud rate must be a number")
        address = self.address_edit.text().strip()
        return port, int(baud), address

    def send(self, name, speed, delay):
        """Build the message for the selected protocol and send it."""
        protocol = "d" if self.pelco_d.isChecked() else "p"
        try:
            port, baud, address = self.connection()
            builder = getattr(pelco, "pelco_%s_%s" % (protocol, name))
            data = builder(address) if speed is None else builder(address, speed)
            stop = getattr(pelco, "pelco_%s_stop" % protocol)(address)
        except (ValueError, TypeError) as error:
            self.status.setText("Invalid input: %s" % error)
            return

        try:
            pelco.write_com_command(port, baud, data, stop, delay)
        except (serial.SerialException, OSError) as error:
            self.status.setText("Serial error: %s" % error)
        else:
            self.status.setText("Sent %s" % data)


def main():
    app = QApplication(sys.argv)
    remote = Remote()
    remote.show()
    return app.exec_()


if __name__ == '__main__':
    sys.exit(main())
