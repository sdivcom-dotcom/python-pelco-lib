# python-pelco-lib

*[Русская версия](README_ru.md)*

A small library for controlling PTZ cameras that speak **Pelco-D** or **Pelco-P**.

It does two things:

- **Command builders** turn a movement into a protocol message, returned as a hex string.
- **A transport** sends that string over an RS-485 serial port.

The two halves are independent — you can use the builders on their own if you send
the bytes some other way (network relay, another serial library, a test harness).

## Install

```bash
pip install .
```

The only runtime dependency is [pyserial](https://pypi.org/project/pyserial/), and it
is only needed for the transport.

## Quick start

```python
from python_pelco_lib import pelco_d_tilt_up, pelco_d_stop, write_com_command

port = "/dev/ttyUSB0"   # the virtual COM port of your USB-RS485 adapter
baud = 2400             # must match the rate set on the camera
address = "01"          # camera address on the bus

data = pelco_d_tilt_up(address, 32)
stop = pelco_d_stop(address)

# Tilt up for one second, then stop.
write_com_command(port, baud, data, stop, 1)
```

Every builder just returns a string, so you can inspect a command without any hardware:

```python
>>> from python_pelco_lib import pelco_d_pan_left, pelco_p_pan_left
>>> pelco_d_pan_left("01", 32)
'FF010004200025'
>>> pelco_p_pan_left("01", 32)
'A00100042000AF2A'
```

## Conventions

These apply to every builder.

**`address`** — the camera address on the bus. Accepts either the two-digit hex string
the library has always used (`"01"`, `"0A"`) or a plain `int`, which is read as the bus
number and formatted as hex, so `10` becomes `"0A"`. Invalid addresses raise `ValueError`.

> Pelco-P numbers cameras from zero, so the address byte is usually the camera number
> on the bus **minus one**. Pelco-D uses the number as-is.

**`pan_speed` / `til_speed`** — a decimal speed from `0` to `63` (`0x00`–`0x3F`).
Values outside the range are clamped rather than rejected, so a camera asked to move
faster than it can will still move. Numeric strings (`"32"`) work as well as ints.

The Pelco-P pan builders additionally accept the value `100` as a *turbo* pan
(`0x40`), exported as `TURBO_SPEED`. Pelco-D has no turbo sentinel.

## Commands

Both protocols expose the same set. Use the `pelco_d_` prefix for Pelco-D and the
`pelco_p_` prefix for Pelco-P — for example `pelco_d_zoom_in` and `pelco_p_zoom_in`.

| Function | Arguments | Description |
| --- | --- | --- |
| `..._stop` | `address` | Stop all camera movement |
| `..._tilt_up` | `address, til_speed` | Tilt up |
| `..._tilt_down` | `address, til_speed` | Tilt down |
| `..._tilt` | `address, up, down, til_speed` | Tilt up if `up` is set, down if `down` is set, otherwise stop |
| `..._pan_left` | `address, pan_speed` | Pan left |
| `..._pan_right` | `address, pan_speed` | Pan right |
| `..._pan` | `address, right, left, pan_speed` | Pan right if `right` is set, left if `left` is set, otherwise stop |
| `..._upleft` | `address, pan_speed, til_speed` | Move up and left |
| `..._upright` | `address, pan_speed, til_speed` | Move up and right |
| `..._down_left` | `address, pan_speed, til_speed` | Move down and left |
| `..._down_right` | `address, pan_speed, til_speed` | Move down and right |
| `..._zoom_in` | `address` | Zoom in (tele) |
| `..._zoom_out` | `address` | Zoom out (wide) |
| `..._focus_far` | `address` | Move focus far |
| `..._focus_near` | `address` | Move focus near |

In `..._tilt` and `..._pan`, the first flag wins if both are set.

## Transport

`port` is the device your USB-RS485 adapter appears as (`/dev/ttyUSB0`, `COM3`).
`baud` is the rate configured on the camera — usually 1200, 1800, 2400, 4800 or 9600.

### `write_com_action(port, baud, data)`

Opens the port, sends one command, and closes the port.

### `write_com_command(port, baud, data, data_stop, delay)`

Sends `data`, holds it for `delay` seconds, then sends `data_stop`. Useful for stepping
a camera a small, fixed amount. `data_stop` is sent even if the wait is interrupted, so
Ctrl-C in the middle of a movement does not leave the camera panning.

### `PelcoSerial(port, baud)`

Keeps the port open across commands. The two functions above re-open the port for every
message, which costs tens of milliseconds and resets the line — noticeable when commands
arrive in a stream, from a joystick, a GUI or a patrol loop.

```python
from python_pelco_lib import PelcoSerial, pelco_d_pan_left, pelco_d_stop

with PelcoSerial("/dev/ttyUSB0", 2400) as link:
    stop = pelco_d_stop("01")
    link.send_for(pelco_d_pan_left("01", 32), stop, 0.5)   # move, wait, stop
    link.send(stop)                                        # send one message
```

## Examples

The [examples/](examples/) directory holds four working programs. Each one puts the
repository root on `sys.path`, so they run straight from a checkout without installing
anything.

| File | What it does |
| --- | --- |
| [console.py](examples/console.py) | Send one command from the command line |
| [simple_dance.py](examples/simple_dance.py) | Interactive prompt, plus an `all` sweep that exercises every direction |
| [gamepad_pelco_p.py](examples/gamepad_pelco_p.py) | Drive a camera from a USB gamepad (needs `hid`) |
| [com_gui.py](examples/com_gui.py) | A PyQt5 remote control (needs `PyQt5`) |

```bash
python examples/console.py -p /dev/ttyUSB0 -b 2400 -a 01 -pr d -c right
```

## Message formats

Pelco-D, seven bytes. The checksum is the sum of the five bytes after the sync byte,
modulo 256:

```
FF | ADDRESS | DATA1 | DATA2 | PAN SPEED | TILT SPEED | CHECKSUM
```

Pelco-P, eight bytes. The checksum is the XOR of the seven preceding bytes, STX and
ETX included:

```
A0 | ADDRESS | DATA1 | DATA2 | PAN SPEED | TILT SPEED | AF | CHECKSUM
```

## Tests

```bash
pip install pytest
python -m pytest
```

The suite checks the built frames against the protocol specs and exercises the
transport against a fake serial port, so no hardware is required.

## Upgrading from 0.1

The modules used to sit in a directory named `python-pelco-lib`, which Python cannot
import, so programs imported the files directly. They now live in a proper package:

```python
# before
from commands_pelco_d import pelco_d_stop, pelco_d_tilt_up
from pelco_transport import write_com_action, write_com_command

# now
from python_pelco_lib import pelco_d_stop, pelco_d_tilt_up
from python_pelco_lib import write_com_action, write_com_command
```

The submodules are still there if you prefer them
(`from python_pelco_lib.commands_pelco_d import pelco_d_stop`).

Every builder returns the same bytes as before, with one exception: `pelco_d_tilt`,
`pelco_d_pan`, `pelco_p_tilt` and `pelco_p_pan` used to raise `TypeError` on every
call — they passed three arguments to two-argument builders — and now work.

## License

GPL-3.0. See [LICENSE](LICENSE).
