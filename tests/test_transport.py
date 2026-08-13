"""Transport tests, driven against a fake serial port.

``serial.Serial`` is patched out so the tests need no hardware.
"""

import pytest

from python_pelco_lib import pelco_transport
from python_pelco_lib.commands_pelco_d import pelco_d_pan_left, pelco_d_stop


class FakeSerial:
    """Records what was written and whether the port was closed."""

    instances = []

    def __init__(self, port, baudrate, **kwargs):
        self.port = port
        self.baudrate = baudrate
        self.writes = []
        self.closed = False
        FakeSerial.instances.append(self)

    def write(self, data):
        self.writes.append(data)

    def close(self):
        self.closed = True


@pytest.fixture
def fake_serial(monkeypatch):
    FakeSerial.instances = []
    monkeypatch.setattr(pelco_transport.serial, "Serial", FakeSerial)
    return FakeSerial


def test_write_com_action_sends_once_and_closes(fake_serial):
    pelco_transport.write_com_action("/dev/ttyUSB0", 2400, pelco_d_stop("01"))

    (port,) = fake_serial.instances
    assert port.writes == [bytes.fromhex("FF010000000001")]
    assert port.closed


def test_write_com_command_sends_data_then_stop(fake_serial):
    pelco_transport.write_com_command(
        "/dev/ttyUSB0", 2400, pelco_d_pan_left("01", 32), pelco_d_stop("01"), 0
    )

    (port,) = fake_serial.instances
    assert port.writes == [
        bytes.fromhex("FF010004200025"),
        bytes.fromhex("FF010000000001"),
    ]
    assert port.closed


def test_baudrate_accepts_a_string(fake_serial):
    pelco_transport.write_com_action("/dev/ttyUSB0", "2400", pelco_d_stop("01"))

    (port,) = fake_serial.instances
    assert port.baudrate == 2400


def test_stop_is_sent_even_if_the_wait_is_interrupted(fake_serial, monkeypatch):
    def interrupt(_seconds):
        raise KeyboardInterrupt

    monkeypatch.setattr(pelco_transport.time, "sleep", interrupt)

    with pytest.raises(KeyboardInterrupt):
        pelco_transport.write_com_command(
            "/dev/ttyUSB0", 2400, pelco_d_pan_left("01", 32), pelco_d_stop("01"), 10
        )

    (port,) = fake_serial.instances
    assert port.writes[-1] == bytes.fromhex("FF010000000001")
    assert port.closed


def test_pelco_serial_reuses_one_open_port(fake_serial):
    with pelco_transport.PelcoSerial("/dev/ttyUSB0", 2400) as link:
        link.send(pelco_d_pan_left("01", 32))
        link.send(pelco_d_stop("01"))
        assert not link.serial.closed

    (port,) = fake_serial.instances
    assert len(port.writes) == 2
    assert port.closed
